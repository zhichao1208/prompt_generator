from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

class RequirementsAnalysis(BaseModel):
	summary: str
	constraints: List[str]
	success_factors: List[str]
	risks: List[Dict[str, str]]
	context: Dict[str, str]

class Strategy(BaseModel):
	name: str
	core_focus: str
	priorities: List[str]
	implementation: Dict[str, Any]
	benefits: List[str]
	trade_offs: List[str]
	resources: Dict[str, Any]
	risk_mitigation: List[str]
	success_metrics: List[str]

class StrategicApproaches(BaseModel):
	strategies: List[Strategy]

@CrewBase
class PromptSolutionCrew():
	"""PromptSolutionCrew crew"""

	def __init__(self):
		# 使用绝对路径
		self.config_dir = Path(__file__).parent / "config"
		
		# 读取配置文件
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

	@agent
	def prompt_engineer_1(self) -> Agent:
		"""Create first prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer_1']['role'],
			goal=self.agents_config['prompt_engineer_1']['goal'],
			backstory=self.agents_config['prompt_engineer_1']['backstory'],
			verbose=True
		)

	@agent
	def prompt_engineer_2(self) -> Agent:
		"""Create second prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer_2']['role'],
			goal=self.agents_config['prompt_engineer_2']['goal'],
			backstory=self.agents_config['prompt_engineer_2']['backstory'],
			verbose=True
		)

	@agent
	def prompt_engineer_3(self) -> Agent:
		"""Create third prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer_3']['role'],
			goal=self.agents_config['prompt_engineer_3']['goal'],
			backstory=self.agents_config['prompt_engineer_3']['backstory'],
			verbose=True
		)

	@task
	def analyze_requirements_task(self, **inputs) -> Task:
		"""Create an analyze requirements task."""
		description = self._format_task_description('analyze_requirements_task', inputs)
		return Task(
			description=description,
			expected_output=self.tasks_config['analyze_requirements_task']['expected_output'],
			agent=self.architect()
		)

	def _get_direction_from_output(self, output: str, index: int) -> str:
		"""Extract a specific direction from the architect's output."""
		try:
			output_dict = json.loads(output)
			return output_dict["optimization_directions"][index]
		except (json.JSONDecodeError, KeyError, IndexError) as e:
			print(f"Error extracting direction {index + 1}: {e}")
			return f"Error extracting direction {index + 1}"

	def _format_task_description(self, task_name: str, inputs: dict, direction: str = None) -> str:
		"""Format task description with all required variables."""
		description = self.tasks_config[task_name]['description']
		
		# Create a copy of inputs to avoid modifying the original
		format_vars = inputs.copy() if inputs else {}
		
		# Add direction if provided
		if direction is not None:
			if "direction_1" in description:
				format_vars["direction_1"] = direction
			elif "direction_2" in description:
				format_vars["direction_2"] = direction
			elif "direction_3" in description:
				format_vars["direction_3"] = direction
		
		# Add default values for missing required fields
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
	def optimize_prompt_direction_1(self, architect_output: str = "", **inputs) -> Task:
		"""Create task for first optimization direction."""
		direction = self._get_direction_from_output(architect_output, 0) if architect_output else None
		description = self._format_task_description('optimize_prompt_direction_1', inputs, direction)
		return Task(
			description=description,
			expected_output=self.tasks_config['optimize_prompt_direction_1']['expected_output'],
			agent=self.prompt_engineer_1(),
			context=[self.analyze_requirements_task(**inputs)]
		)

	@task
	def optimize_prompt_direction_2(self, architect_output: str = "", **inputs) -> Task:
		"""Create task for second optimization direction."""
		direction = self._get_direction_from_output(architect_output, 1) if architect_output else None
		description = self._format_task_description('optimize_prompt_direction_2', inputs, direction)
		return Task(
			description=description,
			expected_output=self.tasks_config['optimize_prompt_direction_2']['expected_output'],
			agent=self.prompt_engineer_2(),
			context=[self.analyze_requirements_task(**inputs)]
		)

	@task
	def optimize_prompt_direction_3(self, architect_output: str = "", **inputs) -> Task:
		"""Create task for third optimization direction."""
		direction = self._get_direction_from_output(architect_output, 2) if architect_output else None
		description = self._format_task_description('optimize_prompt_direction_3', inputs, direction)
		return Task(
			description=description,
			expected_output=self.tasks_config['optimize_prompt_direction_3']['expected_output'],
			agent=self.prompt_engineer_3(),
			context=[self.analyze_requirements_task(**inputs)]
		)

	@crew
	def crew(self, inputs: dict = None) -> Crew:
		"""Creates the PromptSolutionCrew crew"""
		if inputs is None:
			inputs = {}

		analyze_task = self.analyze_requirements_task(**inputs)
		
		return Crew(
			agents=[
				self.architect(),
				self.prompt_engineer_1(),
				self.prompt_engineer_2(),
				self.prompt_engineer_3()
			],
			tasks=[
				analyze_task,
				self.optimize_prompt_direction_1(architect_output=analyze_task.output, **inputs),
				self.optimize_prompt_direction_2(architect_output=analyze_task.output, **inputs),
				self.optimize_prompt_direction_3(architect_output=analyze_task.output, **inputs)
			],
			process=Process.sequential,
			verbose=True,
			planning=True
		)
