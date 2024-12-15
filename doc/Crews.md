# # Crews
## Understanding and utilizing crews in the crewAI framework with comprehensive attributes and functionalities.
# [](https://docs.crewai.com/concepts/crews#what-is-a-crew)What is a Crew?
### A crew in crewAI represents a collaborative group of agents working together to achieve a set of tasks. Each crew defines the strategy for task execution, agent collaboration, and the overall workflow.
# [](https://docs.crewai.com/concepts/crews#crew-attributes)Crew Attributes
| **Attribute** | **Parameters** | **Description** |
|---|---|---|---|
| **Tasks** | tasks | A list of tasks assigned to the crew. |
| **Agents** | agents | A list of agents that are part of the crew. |
| **Process** *(optional)* | process | The process flow (e.g., sequential, hierarchical) the crew follows. Default is sequential. |
| **Verbose** *(optional)* | verbose | The verbosity level for logging during execution. Defaults to False. |
| **Manager LLM** *(optional)* | manager_llm | The language model used by the manager agent in a hierarchical process. **Required when using a hierarchical process.** |
| **Function Calling LLM** *(optional)* | function_calling_llm | If passed, the crew will use this LLM to do function calling for tools for all agents in the crew. Each agent can have its own LLM, which overrides the crew’s LLM for function calling. |
| **Config** *(optional)* | config | Optional configuration settings for the crew, in Json or Dict[str, Any] format. |
| **Max RPM** *(optional)* | max_rpm | Maximum requests per minute the crew adheres to during execution. Defaults to None. |
| **Language** *(optional)* | language | Language used for the crew, defaults to English. |
| **Language File** *(optional)* | language_file | Path to the language file to be used for the crew. |
| **Memory** *(optional)* | memory | Utilized for storing execution memories (short-term, long-term, entity memory). |
| **Memory Config** *(optional)* | memory_config | Configuration for the memory provider to be used by the crew. |
| **Cache** *(optional)* | cache | Specifies whether to use a cache for storing the results of tools’ execution. Defaults to True. |
| **Embedder** *(optional)* | embedder | Configuration for the embedder to be used by the crew. Mostly used by memory for now. Default is {"provider": "openai"}. |
| **Full Output** *(optional)* | full_output | Whether the crew should return the full output with all tasks outputs or just the final output. Defaults to False. |
| **Step Callback** *(optional)* | step_callback | A function that is called after each step of every agent. This can be used to log the agent’s actions or to perform other operations; it won’t override the agent-specific step_callback. |
| **Task Callback** *(optional)* | task_callback | A function that is called after the completion of each task. Useful for monitoring or additional operations post-task execution. |
| **Share Crew** *(optional)* | share_crew | Whether you want to share the complete crew information and execution with the crewAI team to make the library better, and allow us to train models. |
| **Output Log File** *(optional)* | output_log_file | Whether you want to have a file with the complete crew output and execution. You can set it using True and it will default to the folder you are currently in and it will be called logs.txt or passing a string with the full path and name of the file. |
| **Manager Agent** *(optional)* | manager_agent | manager sets a custom agent that will be used as a manager. |
| **Prompt File** *(optional)* | prompt_file | Path to the prompt JSON file to be used for the crew. |
| **Planning** *(optional)* | planning | Adds planning ability to the Crew. When activated before each Crew iteration, all Crew data is sent to an AgentPlanner that will plan the tasks and this plan will be added to each task description. |
| **Planning LLM** *(optional)* | planning_llm | The language model used by the AgentPlanner in a planning process. |


**Crew Max RPM**: The max_rpm attribute sets the maximum number of requests per minute the crew can perform to avoid rate limits and will override individual agents’ max_rpm settings if you set it.
# [](https://docs.crewai.com/concepts/crews#creating-crews)Creating Crews
### There are two ways to create crews in CrewAI: usingYAML configuration (recommended) or defining them directly in code.
# [](https://docs.crewai.com/concepts/crews#yaml-configuration-recommended)YAML Configuration (Recommended)
### Using YAML configuration provides a cleaner, more maintainable way to define crews and is consistent with how agents and tasks are defined in CrewAI projects.
### After creating your CrewAI project as outlined in the[Installation](https://docs.crewai.com/installation) section, you can define your crew in a class that inherits from CrewBase and uses decorators to define agents, tasks, and the crew itself.
## [](https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators)Example Crew Class with Decorators
code


from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff


@CrewBase
class YourCrewName:
    """Description of your crew"""

    # Paths to your YAML configuration files
    # To see an example agent and task defined in YAML, checkout the following:
    # - Task: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    # - Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @before_kickoff
    def prepare_inputs(self, inputs):
        # Modify inputs before the crew starts
        inputs['additional_data'] = "Some extra information"
        return inputs

    @after_kickoff
    def process_output(self, output):
        # Modify output after the crew finishes
        output.raw += "\nProcessed after kickoff."
        return output

    @agent
    def agent_one(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_one'],
            verbose=True
        )

    @agent
    def agent_two(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_two'],
            verbose=True
        )

    @task
    def task_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_one']
        )

    @task
    def task_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_two']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator. 
            process=Process.sequential,
            verbose=True,
        )


Tasks will be executed in the order they are defined.
### TheCrewBase class, along with these decorators, automates the collection of agents and tasks, reducing the need for manual management.
## [](https://docs.crewai.com/concepts/crews#decorators-overview-from-annotations-py)Decorators overview fromannotations.py
### CrewAI provides several decorators in theannotations.py file that are used to mark methods within your crew class for special handling:
* @CrewBase: Marks the class as a crew base class.
* @agent: Denotes a method that returns an Agent object.
* @task: Denotes a method that returns a Task object.
* @crew: Denotes the method that returns the Crew object.
* @before_kickoff: (Optional) Marks a method to be executed before the crew starts.
* @after_kickoff: (Optional) Marks a method to be executed after the crew finishes.

⠀These decorators help in organizing your crew’s structure and automatically collecting agents and tasks without manually listing them.
# [](https://docs.crewai.com/concepts/crews#direct-code-definition-alternative)Direct Code Definition (Alternative)
### Alternatively, you can define the crew directly in code without using YAML configuration files.
code


from crewai import Agent, Crew, Task, Process
from crewai_tools import YourCustomTool

class YourCrewName:
    def agent_one(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data trends in the market",
            backstory="An experienced data analyst with a background in economics",
            verbose=True,
            tools=[YourCustomTool()]
        )

    def agent_two(self) -> Agent:
        return Agent(
            role="Market Researcher",
            goal="Gather information on market dynamics",
            backstory="A diligent researcher with a keen eye for detail",
            verbose=True
        )

    def task_one(self) -> Task:
        return Task(
            description="Collect recent market data and identify trends.",
            expected_output="A report summarizing key trends in the market.",
            agent=self.agent_one()
        )

    def task_two(self) -> Task:
        return Task(
            description="Research factors affecting market dynamics.",
            expected_output="An analysis of factors influencing the market.",
            agent=self.agent_two()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.agent_one(), self.agent_two()],
            tasks=[self.task_one(), self.task_two()],
            process=Process.sequential,
            verbose=True
        )
### In this example:
* Agents and tasks are defined directly within the class without decorators.
* We manually create and manage the list of agents and tasks.
* This approach provides more control but can be less maintainable for larger projects.

⠀[](https://docs.crewai.com/concepts/crews#crew-output)Crew Output
### The output of a crew in the CrewAI framework is encapsulated within theCrewOutput class. This class provides a structured way to access results of the crew’s execution, including various formats such as raw strings, JSON, and Pydantic models. The CrewOutput includes the results from the final task output, token usage, and individual task outputs.
# [](https://docs.crewai.com/concepts/crews#crew-output-attributes)Crew Output Attributes
| **Attribute** | **Parameters** | **Type** | **Description** |
| **Raw** | raw | str | The raw output of the crew. This is the default format for the output. |
| **Pydantic** | pydantic | Optional[BaseModel] | A Pydantic model object representing the structured output of the crew. |
| **JSON Dict** | json_dict | Optional[Dict[str, Any]] | A dictionary representing the JSON output of the crew. |
| **Tasks Output** | tasks_output | List[TaskOutput] | A list of TaskOutput objects, each representing the output of a task in the crew. |
| **Token Usage** | token_usage | Dict[str, Any] | A summary of token usage, providing insights into the language model’s performance during execution. |
# [](https://docs.crewai.com/concepts/crews#crew-output-methods-and-properties)Crew Output Methods and Properties
| **Method/Property** | **Description** |
| **json** | Returns the JSON string representation of the crew output if the output format is JSON. |
| **to_dict** | Converts the JSON and Pydantic outputs to a dictionary. |
| ****str**** | Returns the string representation of the crew output, prioritizing Pydantic, then JSON, then raw. |
# [](https://docs.crewai.com/concepts/crews#accessing-crew-outputs)Accessing Crew Outputs
### Once a crew has been executed, its output can be accessed through theoutput attribute of the Crew object. The CrewOutput class provides various ways to interact with and present this output.
## [](https://docs.crewai.com/concepts/crews#example)Example
Code


# Example crew execution
crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_task, write_article_task],
    verbose=True
)

crew_output = crew.kickoff()

# Accessing the crew output
print(f"Raw Output: {crew_output.raw}")
if crew_output.json_dict:
    print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
if crew_output.pydantic:
    print(f"Pydantic Output: {crew_output.pydantic}")
print(f"Tasks Output: {crew_output.tasks_output}")
print(f"Token Usage: {crew_output.token_usage}")
# [](https://docs.crewai.com/concepts/crews#memory-utilization)Memory Utilization
### Crews can utilize memory (short-term, long-term, and entity memory) to enhance their execution and learning over time. This feature allows crews to store and recall execution memories, aiding in decision-making and task execution strategies.
# [](https://docs.crewai.com/concepts/crews#cache-utilization)Cache Utilization
### Caches can be employed to store the results of tools’ execution, making the process more efficient by reducing the need to re-execute identical tasks.
# [](https://docs.crewai.com/concepts/crews#crew-usage-metrics)Crew Usage Metrics
### After the crew execution, you can access theusage_metrics attribute to view the language model (LLM) usage metrics for all tasks executed by the crew. This provides insights into operational efficiency and areas for improvement.
Code


# Access the crew's usage metrics
crew = Crew(agents=[agent1, agent2], tasks=[task1, task2])
crew.kickoff()
print(crew.usage_metrics)
# [](https://docs.crewai.com/concepts/crews#crew-execution-process)Crew Execution Process
* Sequential Process: Tasks are executed one after another, allowing for a linear flow of work.
* Hierarchical Process: A manager agent coordinates the crew, delegating tasks and validating outcomes before proceeding. Note: A manager_llm or manager_agent is required for this process and it’s essential for validating the process flow.

⠀[](https://docs.crewai.com/concepts/crews#kicking-off-a-crew)Kicking Off a Crew
### Once your crew is assembled, initiate the workflow with thekickoff() method. This starts the execution process according to the defined process flow.
Code


# Start the crew's task execution
result = my_crew.kickoff()
print(result)
# [](https://docs.crewai.com/concepts/crews#different-ways-to-kick-off-a-crew)Different Ways to Kick Off a Crew
### Once your crew is assembled, initiate the workflow with the appropriate kickoff method. CrewAI provides several methods for better control over the kickoff process:kickoff(), kickoff_for_each(), kickoff_async(), and kickoff_for_each_async().
* kickoff(): Starts the execution process according to the defined process flow.
* kickoff_for_each(): Executes tasks for each agent individually.
* kickoff_async(): Initiates the workflow asynchronously.
* kickoff_for_each_async(): Executes tasks for each agent individually in an asynchronous manner.

⠀Code


# Start the crew's task execution
result = my_crew.kickoff()
print(result)

# Example of using kickoff_for_each
inputs_array = [{'topic': 'AI in healthcare'}, {'topic': 'AI in finance'}]
results = my_crew.kickoff_for_each(inputs=inputs_array)
for result in results:
    print(result)

# Example of using kickoff_async
inputs = {'topic': 'AI in healthcare'}
async_result = my_crew.kickoff_async(inputs=inputs)
print(async_result)

# Example of using kickoff_for_each_async
inputs_array = [{'topic': 'AI in healthcare'}, {'topic': 'AI in finance'}]
async_results = my_crew.kickoff_for_each_async(inputs=inputs_array)
for async_result in async_results:
    print(async_result)
### These methods provide flexibility in how you manage and execute tasks within your crew, allowing for both synchronous and asynchronous workflows tailored to your needs.
# [](https://docs.crewai.com/concepts/crews#replaying-from-a-specific-task)Replaying from a Specific Task
### You can now replay from a specific task using our CLI commandreplay.
The replay feature in CrewAI allows you to replay from a specific task using the command-line interface (CLI). By running the command crewai replay -t <task_id>, you can specify the task_id for the replay process.
Kickoffs will now save the latest kickoffs returned task outputs locally for you to be able to replay from.
# [](https://docs.crewai.com/concepts/crews#replaying-from-a-specific-task-using-the-cli)Replaying from a Specific Task Using the CLI
### To use the replay feature, follow these steps:
### 1 Open your terminal or command prompt.
2 Navigate to the directory where your CrewAI project is located.
3 Run the following command:

⠀To view the latest kickoff task IDs, use:


crewai log-tasks-outputs
### Then, to replay from a specific task, use:


crewai replay -t <task_id>
### These commands let you replay from your latest kickoff tasks, still retaining context from previously executed tasks.
