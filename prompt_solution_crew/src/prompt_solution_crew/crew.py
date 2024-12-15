from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os

class OptimizationDirection(BaseModel):
	focus: str
	relevance: str
	benefits: List[str]
	implementation: Dict[str, Any]

class ArchitectOutput(BaseModel):
	optimization_directions: List[OptimizationDirection]

class PromptStructure(BaseModel):
	role: Dict[str, Any]
	task: Dict[str, Any]
	rules: Dict[str, Any]
	methods: Dict[str, str]
	explanation: str
	guidelines: List[str]

class BaseCrew():
	"""Base crew class with common functionality"""
	
	def __init__(self, config_path: str):
		self.config_dir = Path(__file__).parent / "config" / config_path
		
		with open(self.config_dir / 'agents.yaml', 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open(self.config_dir / 'tasks.yaml', 'r') as f:
			self.tasks_config = yaml.safe_load(f)
		
		# 初始化模型名称和配置
		model_name = os.environ.get("OPENAI_MODEL_NAME", "gpt-4")
		# 如果是 o1-preview，转换为 gpt-4-1106-preview
		if model_name == "gpt-o1-preview":
			model_name = "gpt-4-1106-preview"
			
		self.llm_config = {
			"temperature": 0.7,
			"model": model_name
		}

	def _format_task_description(self, task_name: str, inputs: dict, direction: OptimizationDirection = None) -> str:
		"""Format task description with all required variables."""
		description = self.tasks_config[task_name]['description']
		
		format_vars = inputs.copy() if inputs else {}
		
		if direction:
			format_vars['direction'] = json.dumps(direction.dict(), indent=2)
		
		required_fields = [
			'task_description', 'task_type', 'model_preference',
			'tone', 'context', 'data_input', 'examples'
		]
		for field in required_fields:
			if field not in format_vars:
				format_vars[field] = f"[No {field} provided]"
		
		try:
			return description.format(**format_vars)
		except KeyError as e:
			print(f"Missing required input: {e}")
			return description

class ArchitectCrew(BaseCrew):
	"""Architect crew for analyzing requirements"""

	def __init__(self):
		super().__init__('architect')

	def architect(self) -> Agent:
		"""Create an architect agent."""
		return Agent(
			role=self.agents_config['architect']['role'],
			goal=self.agents_config['architect']['goal'],
			backstory=self.agents_config['architect']['backstory'],
			verbose=True,
			llm_config=self.llm_config
		)

	def analyze_requirements_task(self, **inputs) -> Task:
		"""Create an analyze requirements task."""
		description = self._format_task_description('analyze_requirements_task', inputs)
		return Task(
			description=description,
			expected_output=self.tasks_config['analyze_requirements_task']['expected_output'],
			agent=self.architect(),
			output_json=ArchitectOutput
		)

	def run(self, inputs: dict = None) -> ArchitectOutput:
		"""Run the architect crew"""
		if inputs is None:
			inputs = {}
		
		crew = Crew(
			agents=[self.architect()],
			tasks=[self.analyze_requirements_task(**inputs)],
			process=Process.sequential,
			verbose=True
		)
		
		return crew.kickoff()

class PromptEngineerCrew(BaseCrew):
	"""Prompt Engineer crew for implementing optimization direction"""

	def __init__(self):
		super().__init__('engineer')

	def prompt_engineer(self) -> Agent:
		"""Create a prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer']['role'],
			goal=self.agents_config['prompt_engineer']['goal'],
			backstory=self.agents_config['prompt_engineer']['backstory'],
			verbose=True,
			llm_config=self.llm_config
		)

	def optimize_prompt_task(self, direction: OptimizationDirection, **inputs) -> Task:
		"""Create an optimize prompt task."""
		description = self._format_task_description('optimize_prompt_direction', inputs, direction)
		return Task(
			description=description,
			expected_output=self.tasks_config['optimize_prompt_direction']['expected_output'],
			agent=self.prompt_engineer(),
			output_json=PromptStructure
		)

	def run(self, direction: OptimizationDirection, inputs: dict = None) -> PromptStructure:
		"""Run the prompt engineer crew"""
		if inputs is None:
			inputs = {}
		
		crew = Crew(
			agents=[self.prompt_engineer()],
			tasks=[self.optimize_prompt_task(direction, **inputs)],
			process=Process.sequential,
			verbose=True
		)
		
		return crew.kickoff()

def run_optimization_process(inputs: dict = None) -> List[PromptStructure]:
	"""Run the complete optimization process."""
	if inputs is None:
		inputs = {}

	# 1. Run architect crew to get optimization directions
	architect_crew = ArchitectCrew()
	architect_result = architect_crew.run(inputs)
	
	# 2. Create prompt engineer crews for each direction
	results = []
	
	for direction in architect_result.optimization_directions:
		crew = PromptEngineerCrew()
		result = crew.run(direction, inputs)
		results.append(result)
	
	return results
