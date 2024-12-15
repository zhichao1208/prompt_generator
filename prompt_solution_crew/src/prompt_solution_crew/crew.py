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
			llm=self.agents_config['architect']['llm'],
			verbose=True
		)

	@agent
	def prompt_engineer_1(self) -> Agent:
		"""Create first prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer_1']['role'],
			goal=self.agents_config['prompt_engineer_1']['goal'],
			backstory=self.agents_config['prompt_engineer_1']['backstory'],
			llm=self.agents_config['prompt_engineer_1']['llm'],
			verbose=True
		)

	@agent
	def prompt_engineer_2(self) -> Agent:
		"""Create second prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer_2']['role'],
			goal=self.agents_config['prompt_engineer_2']['goal'],
			backstory=self.agents_config['prompt_engineer_2']['backstory'],
			llm=self.agents_config['prompt_engineer_2']['llm'],
			verbose=True
		)

	@agent
	def prompt_engineer_3(self) -> Agent:
		"""Create third prompt engineer agent."""
		return Agent(
			role=self.agents_config['prompt_engineer_3']['role'],
			goal=self.agents_config['prompt_engineer_3']['goal'],
			backstory=self.agents_config['prompt_engineer_3']['backstory'],
			llm=self.agents_config['prompt_engineer_3']['llm'],
			verbose=True
		)

	@task
	def analyze_requirements_task(self) -> Task:
		"""Create an analyze requirements task."""
		return Task(
			description=self.tasks_config['analyze_requirements_task']['description'],
			expected_output=self.tasks_config['analyze_requirements_task']['expected_output'],
			agent=self.architect()
		)

	def _extract_directions(self, architect_output: str) -> Dict[str, str]:
		"""Extract the three directions from architect's JSON output."""
		try:
			output_dict = json.loads(architect_output)
			return {
				"direction_1": output_dict["optimization_directions"][0],
				"direction_2": output_dict["optimization_directions"][1],
				"direction_3": output_dict["optimization_directions"][2]
			}
		except (json.JSONDecodeError, KeyError, IndexError) as e:
			print(f"Error extracting directions: {e}")
			return {
				"direction_1": "Error extracting direction 1",
				"direction_2": "Error extracting direction 2", 
				"direction_3": "Error extracting direction 3"
			}

	@task
	def optimize_prompt_direction_1(self) -> Task:
		"""Create task for first optimization direction."""
		return Task(
			description=self.tasks_config['optimize_prompt_direction_1']['description'],
			expected_output=self.tasks_config['optimize_prompt_direction_1']['expected_output'],
			agent=self.prompt_engineer_1(),
			context=[self.analyze_requirements_task()]
		)

	@task
	def optimize_prompt_direction_2(self) -> Task:
		"""Create task for second optimization direction."""
		return Task(
			description=self.tasks_config['optimize_prompt_direction_2']['description'],
			expected_output=self.tasks_config['optimize_prompt_direction_2']['expected_output'],
			agent=self.prompt_engineer_2(),
			context=[self.analyze_requirements_task()]
		)

	@task
	def optimize_prompt_direction_3(self) -> Task:
		"""Create task for third optimization direction."""
		return Task(
			description=self.tasks_config['optimize_prompt_direction_3']['description'],
			expected_output=self.tasks_config['optimize_prompt_direction_3']['expected_output'],
			agent=self.prompt_engineer_3(),
			context=[self.analyze_requirements_task()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PromptSolutionCrew crew"""
		return Crew(
			agents=[
				self.architect(),
				self.prompt_engineer_1(),
				self.prompt_engineer_2(),
				self.prompt_engineer_3()
			],
			tasks=[
				self.analyze_requirements_task(),
				self.optimize_prompt_direction_1(),
				self.optimize_prompt_direction_2(),
				self.optimize_prompt_direction_3()
			],
			process=Process.sequential,
			verbose=True
		)
