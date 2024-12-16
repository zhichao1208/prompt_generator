from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import json	


my_llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

class RequirementsAnalysis(BaseModel):
	summary: str
	constraints: List[str]
	success_factors: List[str]
	risks: List[Dict[str, str]]
	context: Dict[str, str]

class Direction(BaseModel):
    name: str 
    focus: str
    relevance: str
    benefits: List[str]
    implementation_considerations: Dict[str, Any]
    assigned_prompt_engineer: str

class DirectionsList(BaseModel):
    directions: List[Direction] = []

class PromptTemplate_1(BaseModel):
    role: str
    task: str
    rules_constraints: str
    reasoning_method: str
    planning_method: str
    output_format: str
    explanation_of_optimization_choices: str
    usage_guidelines: str


class PromptTemplate_2(BaseModel):
    role: str
    task: str
    rules_constraints: str
    reasoning_method: str
    planning_method: str
    output_format: str
    explanation_of_optimization_choices: str
    usage_guidelines: str

class PromptTemplate_3(BaseModel):
    role: str
    task: str
    rules_constraints: str
    reasoning_method: str
    planning_method: str
    output_format: str
    explanation_of_optimization_choices: str
    usage_guidelines: str

@CrewBase
class PromptSolutionCrew:
    """PromptSolutionCrew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    @agent
    def architect(self) -> Agent:
        return Agent(
            config=self.agents_config["architect"],
            allow_delegation=False,
            verbose=True,
            llm=my_llm
        )

    @agent
    def prompt_engineer_1(self) -> Agent:
        return Agent(
            config=self.agents_config["prompt_engineer_1"],
            allow_delegation=False,
            verbose=True,
            llm=my_llm
        )

    @agent
    def prompt_engineer_2(self) -> Agent:
        return Agent(
            config=self.agents_config["prompt_engineer_2"],
            allow_delegation=False,
            verbose=True,
            llm=my_llm
        )

    @agent
    def prompt_engineer_3(self) -> Agent:
        return Agent(
            config=self.agents_config["prompt_engineer_3"],
            allow_delegation=False,
            verbose=True,
            llm=my_llm
        )

    @task
    def analyze_requirements_task(self) -> Task:
        """Create an analyze requirements task."""
        return Task(
            config=self.tasks_config["analyze_requirements_task"],
            agent=self.architect(),
            output_json=DirectionsList
        )

    @task
    def optimize_prompt_direction_1(self) -> Task:
        """Create a develop strategies task."""
        return Task(
            config=self.tasks_config['optimize_prompt_direction_1'],
            agent=self.prompt_engineer_1(),
            output_json=PromptTemplate_1
        )

    @task
    def optimize_prompt_direction_2(self) -> Task:
        """Create a develop strategies task."""
        return Task(
            config=self.tasks_config['optimize_prompt_direction_2'],
            agent=self.prompt_engineer_2(),
            output_json=PromptTemplate_2
        )

    @task
    def optimize_prompt_direction_3(self) -> Task:
        """Create a develop strategies task."""
        return Task(
            config=self.tasks_config['optimize_prompt_direction_3'],
            agent=self.prompt_engineer_3(),
            output_json=PromptTemplate_3
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
    def prompt_engineer_crew_1(self) -> Crew:
        """Creates the prompt_engineer crew"""
        return Crew(
            agents=[self.prompt_engineer_1()],
            tasks=[self.optimize_prompt_direction_1()],
            process=Process.sequential,
            verbose=True,
            planning=True
        ) 

    @crew
    def prompt_engineer_crew_2(self) -> Crew:
        """Creates the prompt_engineer crew"""
        return Crew(
            agents=[self.prompt_engineer_2()],
            tasks=[self.optimize_prompt_direction_2()],
            process=Process.sequential,
            verbose=True,
            planning=True
        ) 

    @crew
    def prompt_engineer_crew_3(self) -> Crew:
        """Creates the prompt_engineer crew"""
        return Crew(
            agents=[self.prompt_engineer_3()],
            tasks=[self.optimize_prompt_direction_3()],
            process=Process.sequential,
            verbose=True,
            planning=True
        ) 
