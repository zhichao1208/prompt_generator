from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

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

@CrewBase
class ArchitectCrew():
	"""Architect crew for analyzing requirements"""

	def __init__(self):
		self.config_dir = Path(__file__).parent / "config"
		
		with open(self.config_dir / 'agents.yaml', 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open(self.config_dir / 'tasks.yaml', 'r') as f:
			self.tasks_config = yaml.safe_load(f)

	@agent
	def architect(self) -> Agent:
		"""Create an architect agent."""
		return Agent(
			role=self.agents_config['architect']['role'],
			goal=self.agents_config['architect']['goal'],
			backstory=self.agents_config['architect']['backstory'],
			verbose=True
		)

	def _format_task_description(self, task_name: str, inputs: dict) -> str:
		"""Format task description with all required variables."""
		description = self.tasks_config[task_name]['description']
		
		format_vars = inputs.copy() if inputs else {}
		
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

	@task
	def analyze_requirements_task(self, **inputs) -> Task:
		"""Create an analyze requirements task."""
		description = self._format_task_description('analyze_requirements_task', inputs)
		return Task(
			description=description,
			expected_output=self.tasks_config['analyze_requirements_task']['expected_output'],
			agent=self.architect(),
			output_json=ArchitectOutput
		)

	@crew
	def crew(self, inputs: dict = None) -> Crew:
		"""Creates the Architect crew"""
		if inputs is None:
			inputs = {}
		
		return Crew(
			agents=[self.architect()],
			tasks=[self.analyze_requirements_task(**inputs)],
			process=Process.sequential,
			verbose=True
		)

@CrewBase
class PromptEngineerCrew():
	"""Prompt Engineer crew for implementing optimization direction"""

	def __init__(self):
		self.config_dir = Path(__file__).parent / "config"
		
		with open(self.config_dir / 'agents.yaml', 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open(self.config_dir / 'tasks.yaml', 'r') as f:
			self.tasks_config = yaml.safe_load(f)

	@agent
	def prompt_engineer(self) -> Agent:
		"""Create a prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer']['role'],
			goal=self.agents_config['prompt_engineer']['goal'],
			backstory=self.agents_config['prompt_engineer']['backstory'],
			verbose=True
		)

	def _format_task_description(self, inputs: dict, direction: OptimizationDirection) -> str:
		"""Format task description with all required variables."""
		description = self.tasks_config['optimize_prompt_direction']['description']
		
		format_vars = inputs.copy() if inputs else {}
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

	@task
	def optimize_prompt_task(self, direction: OptimizationDirection, **inputs) -> Task:
		"""Create an optimize prompt task."""
		description = self._format_task_description(inputs, direction)
		return Task(
			description=description,
			expected_output=self.tasks_config['optimize_prompt_direction']['expected_output'],
			agent=self.prompt_engineer(),
			output_json=PromptStructure
		)

	@crew
	def crew(self, direction: OptimizationDirection, inputs: dict = None) -> Crew:
		"""Creates the Prompt Engineer crew"""
		if inputs is None:
			inputs = {}
		
		return Crew(
			agents=[self.prompt_engineer()],
			tasks=[self.optimize_prompt_task(direction, **inputs)],
			process=Process.sequential,
			verbose=True
		)

def run_optimization_process(inputs: dict = None) -> List[PromptStructure]:
	"""Run the complete optimization process with all crews."""
	if inputs is None:
		inputs = {}

	# 1. Run architect crew to get optimization directions
	architect_crew = ArchitectCrew()
	architect_result = architect_crew.crew(inputs).kickoff()
	
	# 2. Create prompt engineer crews for each direction
	prompt_engineer_crews = []
	results = []
	
	for direction in architect_result.optimization_directions:
		crew = PromptEngineerCrew()
		result = crew.crew(direction, inputs).kickoff()
		results.append(result)
	
	return results
