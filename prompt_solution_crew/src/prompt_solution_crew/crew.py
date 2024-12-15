from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from crewai.parsers import JsonOutputParser

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

	@task
	def analyze_requirements_task(self) -> Task:
		"""Create an analyze requirements task."""
		return Task(
			description=self.tasks_config['analyze_requirements_task']['description'],
			expected_output=self.tasks_config['analyze_requirements_task']['expected_output'],
			agent=self.architect(),
			output_parser=JsonOutputParser(pydantic_model=RequirementsAnalysis)
		)

	@task
	def develop_strategies_task(self) -> Task:
		"""Create a develop strategies task."""
		return Task(
			description=self.tasks_config['develop_strategies_task']['description'],
			expected_output=self.tasks_config['develop_strategies_task']['expected_output'],
			agent=self.architect(),
			output_parser=JsonOutputParser(pydantic_model=StrategicApproaches),
			context=[self.analyze_requirements_task()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PromptSolutionCrew crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True
		)
