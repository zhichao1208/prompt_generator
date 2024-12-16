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
		
		# 初始化agents和tasks列表
		self.agents = []
		self.tasks = []
		
		# 存储分析任务的结果
		self.analysis_task = None
		
		# 存储用户输入
		self.user_inputs = {
			'task_description': '',
			'task_type': '',
			'model_preference': '',
			'tone': '',
			'context': '',
			'data_input': '',
			'examples': ''
		}

	def set_user_inputs(self, task_description: str, task_type: str, model_preference: str,
					 tone: str, context: str, data_input: str, examples: str):
		"""设置用户输入参数"""
		self.user_inputs = {
			'task_description': task_description,
			'task_type': task_type,
			'model_preference': model_preference,
			'tone': tone,
			'context': context,
			'data_input': data_input,
			'examples': examples
		}

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
			config=self.agents_config['prompt_engineer'],
			verbose=True
		)

	@agent
	def prompt_engineer_2(self) -> Agent:
		"""Create the second prompt engineer agent."""
		return Agent(
			config=self.agents_config['prompt_engineer'],
			verbose=True
		)

	@agent
	def prompt_engineer_3(self) -> Agent:
		"""Create the third prompt engineer agent."""
		return Agent(
			config=self.agents_config['prompt_engineer'],
			verbose=True
		)

	@task
	def analyze_requirements_task(self, task_description: str = None, task_type: str = None, 
							  model_preference: str = None, tone: str = None, 
							  context: str = None, data_input: str = None, 
							  examples: str = None) -> Task:
		"""Create an analyze requirements task."""
		# 如果没有提供参数，使用存储的用户输入
		inputs = {
			'task_description': task_description or self.user_inputs['task_description'],
			'task_type': task_type or self.user_inputs['task_type'],
			'model_preference': model_preference or self.user_inputs['model_preference'],
			'tone': tone or self.user_inputs['tone'],
			'context': context or self.user_inputs['context'],
			'data_input': data_input or self.user_inputs['data_input'],
			'examples': examples or self.user_inputs['examples']
		}
		
		task = Task(
			description=self.tasks_config['analyze_requirements_task']['description'].format(**inputs),
			expected_output=self.tasks_config['analyze_requirements_task']['expected_output'],
			agent=self.architect()
		)
		self.analysis_task = task
		return task

	@task
	def optimize_prompt_direction_1(self, task_description: str = None, task_type: str = None,
								model_preference: str = None, tone: str = None,
								context: str = None, data_input: str = None,
								examples: str = None) -> Task:
		"""Create the first prompt optimization task."""
		# 如果没有提供参数，使用存储的用户输入
		inputs = {
			'task_description': task_description or self.user_inputs['task_description'],
			'task_type': task_type or self.user_inputs['task_type'],
			'model_preference': model_preference or self.user_inputs['model_preference'],
			'tone': tone or self.user_inputs['tone'],
			'context': context or self.user_inputs['context'],
			'data_input': data_input or self.user_inputs['data_input'],
			'examples': examples or self.user_inputs['examples']
		}
		
		return Task(
			description=self.tasks_config['optimize_prompt_direction_1']['description'].format(**inputs),
			expected_output=self.tasks_config['optimize_prompt_direction_1']['expected_output'],
			agent=self.prompt_engineer_1(),
			context=[self.analysis_task] if self.analysis_task else []
		)

	@task
	def optimize_prompt_direction_2(self, task_description: str = None, task_type: str = None,
								model_preference: str = None, tone: str = None,
								context: str = None, data_input: str = None,
								examples: str = None) -> Task:
		"""Create the second prompt optimization task."""
		# 如果没有提供参数，使用存储的用户输入
		inputs = {
			'task_description': task_description or self.user_inputs['task_description'],
			'task_type': task_type or self.user_inputs['task_type'],
			'model_preference': model_preference or self.user_inputs['model_preference'],
			'tone': tone or self.user_inputs['tone'],
			'context': context or self.user_inputs['context'],
			'data_input': data_input or self.user_inputs['data_input'],
			'examples': examples or self.user_inputs['examples']
		}
		
		return Task(
			description=self.tasks_config['optimize_prompt_direction_2']['description'].format(**inputs),
			expected_output=self.tasks_config['optimize_prompt_direction_2']['expected_output'],
			agent=self.prompt_engineer_2(),
			context=[self.analysis_task] if self.analysis_task else []
		)

	@task
	def optimize_prompt_direction_3(self, task_description: str = None, task_type: str = None,
								model_preference: str = None, tone: str = None,
								context: str = None, data_input: str = None,
								examples: str = None) -> Task:
		"""Create the third prompt optimization task."""
		# 如果没有提供参数，使用存储的用户输入
		inputs = {
			'task_description': task_description or self.user_inputs['task_description'],
			'task_type': task_type or self.user_inputs['task_type'],
			'model_preference': model_preference or self.user_inputs['model_preference'],
			'tone': tone or self.user_inputs['tone'],
			'context': context or self.user_inputs['context'],
			'data_input': data_input or self.user_inputs['data_input'],
			'examples': examples or self.user_inputs['examples']
		}
		
		return Task(
			description=self.tasks_config['optimize_prompt_direction_3']['description'].format(**inputs),
			expected_output=self.tasks_config['optimize_prompt_direction_3']['expected_output'],
			agent=self.prompt_engineer_3(),
			context=[self.analysis_task] if self.analysis_task else []
		)

	def create_crew(self, task_description: str, task_type: str, model_preference: str,
				 tone: str, context: str, data_input: str, examples: str) -> Crew:
		"""Creates and returns a new crew instance with the given parameters"""
		# 设置用户输入
		self.set_user_inputs(task_description, task_type, model_preference,
						  tone, context, data_input, examples)
		
		# 创建任务
		analysis_task = self.analyze_requirements_task()
		tasks = [
			analysis_task,
			self.optimize_prompt_direction_1(),
			self.optimize_prompt_direction_2(),
			self.optimize_prompt_direction_3()
		]
		
		return Crew(
			agents=[self.architect(), self.prompt_engineer_1(), 
					self.prompt_engineer_2(), self.prompt_engineer_3()],
			tasks=tasks,
			process=Process.sequential,
			verbose=True
		)

# Export the PromptSolutionCrew class
__all__ = ['PromptSolutionCrew']
