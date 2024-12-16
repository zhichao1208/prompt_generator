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
      
    agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

    @agent
    def architect(self) -> Agent:
        return Agent(
            config=self.agents_config["architect"],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def prompt_engineer_1(self) -> Agent:
        return Agent(
            config=self.agents_config["prompt_engineer_1"],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def prompt_engineer_2(self) -> Agent:
        return Agent(
            config=self.agents_config["prompt_engineer_2"],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def prompt_engineer_3(self) -> Agent:
        return Agent(
            config=self.agents_config["prompt_engineer_3"],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def analyze_requirements_task(self) -> Task:
        """Create an analyze requirements task."""
        return Task(
            config=self.tasks_config["analyze_requirements_task"],
            agent=self.architect()
        )

    @task
    def optimize_prompt_direction_1(self) -> Task:
        """Create a develop strategies task."""
        return Task(
            config=self.tasks_config['optimize_prompt_direction_1'],
            agent=self.prompt_engineer_1()
        )

    @task
    def optimize_prompt_direction_2(self) -> Task:
        """Create a develop strategies task."""
        return Task(
            config=self.tasks_config['optimize_prompt_direction_2'],
            agent=self.prompt_engineer_2()
        )

    @task
    def optimize_prompt_direction_3(self) -> Task:
        """Create a develop strategies task."""
        return Task(
            config=self.tasks_config['optimize_prompt_direction_3'],
            agent=self.prompt_engineer_3()
        )


    @crew
    def architect_crew(self) -> Crew:
        """Creates the architect crew"""
        print("architect_crew method called")
        return Crew(
            agents=[self.architect()],
            tasks=[self.analyze_requirements_task()],
            process=Process.sequential,
            verbose=True,
            planning=True
        ) 
    @crew
    def prompt_engineer_crew(self) -> Crew:
        """Creates the prompt_engineer crew"""
        return Crew(
            agents=[self.prompt_engineer_1(),self.prompt_engineer_2(),self.prompt_engineer_3()],
            tasks=[self.optimize_prompt_direction_1(),self.optimize_prompt_direction_2(),self.optimize_prompt_direction_3()],
            process=Process.sequential,
            verbose=True,
            planning=True
        ) 

