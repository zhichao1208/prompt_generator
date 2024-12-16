from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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
		
		# 存储分析���务的结果
		self.analysis_task = None

	@agent
	def architect(self) -> Agent:
		"""Create an architect agent."""
		return Agent(
			config=self.agents_config['architect'],
			verbose=True
		)

	@agent
	def prompt_engineer_1(self) -> Agent:
		"""Create the first prompt engineer agent."""
		return Agent(
			config=self.agents_config['prompt_engineer_1'],
			verbose=True
		)

	@agent
	def prompt_engineer_2(self) -> Agent:
		"""Create the second prompt engineer agent."""
		return Agent(
			config=self.agents_config['prompt_engineer_2'],
			verbose=True
		)

	@agent
	def prompt_engineer_3(self) -> Agent:
		"""Create the third prompt engineer agent."""
		return Agent(
			config=self.agents_config['prompt_engineer_3'],
			verbose=True
		)

	@task
	def analyze_requirements_task(self) -> Task:
		"""Create an analyze requirements task."""
		task = Task(
			config=self.tasks_config['analyze_requirements_task'],
			agent=self.architect()
		)
		self.analysis_task = task
		return task

	@task
	def optimize_prompt_direction_1(self) -> Task:
		"""Create the first prompt optimization task."""
		return Task(
			config=self.tasks_config['optimize_prompt_direction_1'],
			agent=self.prompt_engineer_1(),
			context=[self.analysis_task] if self.analysis_task else []
		)

	@task
	def optimize_prompt_direction_2(self) -> Task:
		"""Create the second prompt optimization task."""
		return Task(
			config=self.tasks_config['optimize_prompt_direction_2'],
			agent=self.prompt_engineer_2(),
			context=[self.analysis_task] if self.analysis_task else []
		)

	@task
	def optimize_prompt_direction_3(self) -> Task:
		"""Create the third prompt optimization task."""
		return Task(
			config=self.tasks_config['optimize_prompt_direction_3'],
			agent=self.prompt_engineer_3(),
			context=[self.analysis_task] if self.analysis_task else []
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PromptSolutionCrew crew"""
		return Crew(
			agents=[self.architect(), self.prompt_engineer_1(), 
					self.prompt_engineer_2(), self.prompt_engineer_3()],
			tasks=[
				self.analyze_requirements_task(),
				self.optimize_prompt_direction_1(),
				self.optimize_prompt_direction_2(),
				self.optimize_prompt_direction_3()
			],
			process=Process.sequential,
			verbose=True
		)

# Export the PromptSolutionCrew class
__all__ = ['PromptSolutionCrew']
