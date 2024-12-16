# Kickoff Crew Asynchronously
## Kickoff a Crew Asynchronously
# [](https://docs.crewai.com/how-to/kickoff-async#introduction)Introduction
### CrewAI provides the ability to kickoff a crew asynchronously, allowing you to start the crew execution in a non-blocking manner. This feature is particularly useful when you want to run multiple crews concurrently or when you need to perform other tasks while the crew is executing.
# [](https://docs.crewai.com/how-to/kickoff-async#asynchronous-crew-execution)Asynchronous Crew Execution
### To kickoff a crew asynchronously, use thekickoff_async() method. This method initiates the crew execution in a separate thread, allowing the main thread to continue executing other tasks.
# [](https://docs.crewai.com/how-to/kickoff-async#method-signature)Method Signature
Code


def kickoff_async(self, inputs: dict) -> CrewOutput:
# [](https://docs.crewai.com/how-to/kickoff-async#parameters)Parameters
* inputs (dict): A dictionary containing the input data required for the tasks.

⠀[](https://docs.crewai.com/how-to/kickoff-async#returns)Returns
* CrewOutput: An object representing the result of the crew execution.

⠀[](https://docs.crewai.com/how-to/kickoff-async#potential-use-cases)Potential Use Cases
* Parallel Content Generation: Kickoff multiple independent crews asynchronously, each responsible for generating content on different topics. For example, one crew might research and draft an article on AI trends, while another crew generates social media posts about a new product launch. Each crew operates independently, allowing content production to scale efficiently.
* Concurrent Market Research Tasks: Launch multiple crews asynchronously to conduct market research in parallel. One crew might analyze industry trends, while another examines competitor strategies, and yet another evaluates consumer sentiment. Each crew independently completes its task, enabling faster and more comprehensive insights.
* Independent Travel Planning Modules: Execute separate crews to independently plan different aspects of a trip. One crew might handle flight options, another handles accommodation, and a third plans activities. Each crew works asynchronously, allowing various components of the trip to be planned simultaneously and independently for faster results.

⠀[](https://docs.crewai.com/how-to/kickoff-async#example-single-asynchronous-crew-execution)Example: Single Asynchronous Crew Execution
### Here’s an example of how to kickoff a crew asynchronously using asyncio and awaiting the result:
Code


import asyncio
from crewai import Crew, Agent, Task

# Create an agent with code execution enabled
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

# Create a task that requires code execution
data_analysis_task = Task(
    description="Analyze the given dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent
)

# Create a crew and add the task
analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

# Async function to kickoff the crew asynchronously
async def async_crew_execution():
    result = await analysis_crew.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Crew Result:", result)

# Run the async function
asyncio.run(async_crew_execution())
# [](https://docs.crewai.com/how-to/kickoff-async#example-multiple-asynchronous-crew-executions)Example: Multiple Asynchronous Crew Executions
### In this example, we’ll show how to kickoff multiple crews asynchronously and wait for all of them to complete usingasyncio.gather():
Code


import asyncio
from crewai import Crew, Agent, Task

# Create an agent with code execution enabled
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

# Create tasks that require code execution
task_1 = Task(
    description="Analyze the first dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent
)

task_2 = Task(
    description="Analyze the second dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent
)

# Create two crews and add tasks
crew_1 = Crew(agents=[coding_agent], tasks=[task_1])
crew_2 = Crew(agents=[coding_agent], tasks=[task_2])

# Async function to kickoff multiple crews asynchronously and wait for all to finish
async def async_multiple_crews():
    result_1 = crew_1.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    result_2 = crew_2.kickoff_async(inputs={"ages": [20, 22, 24, 28, 30]})

    # Wait for both crews to finish
    results = await asyncio.gather(result_1, result_2)

    for i, result in enumerate(results, 1):
        print(f"Crew {i} Result:", result)

# Run the async function
asyncio.run(async_multiple_crews())

# Kickoff Crew for Each
## Kickoff Crew for Each Item in a List
# [](https://docs.crewai.com/how-to/kickoff-for-each#introduction)Introduction
### CrewAI provides the ability to kickoff a crew for each item in a list, allowing you to execute the crew for each item in the list. This feature is particularly useful when you need to perform the same set of tasks for multiple items.
# [](https://docs.crewai.com/how-to/kickoff-for-each#kicking-off-a-crew-for-each-item)Kicking Off a Crew for Each Item
### To kickoff a crew for each item in a list, use thekickoff_for_each() method. This method executes the crew for each item in the list, allowing you to process multiple items efficiently.
Here’s an example of how to kickoff a crew for each item in a list:
Code


from crewai import Crew, Agent, Task

# Create an agent with code execution enabled
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

# Create a task that requires code execution
data_analysis_task = Task(
    description="Analyze the given dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age calculated from the dataset"
)

# Create a crew and add the task
analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task],
    verbose=True,
    memory=False,
    respect_context_window=True  # enable by default
)

datasets = [
  { "ages": [25, 30, 35, 40, 45] },
  { "ages": [20, 25, 30, 35, 40] },
  { "ages": [30, 35, 40, 45, 50] }
]

# Execute the crew
result = analysis_crew.kickoff_for_each(inputs=datasets)
Was this page helpful?


Yes


No
**[Kickoff Crew Asynchronously](https://docs.crewai.com/how-to/kickoff-async)[Replay Tasks from Latest Crew Kickoff](https://docs.crewai.com/how-to/replay-tasks-from-latest-crew-kickoff)**[website](https://crewai.com/)[x](https://x.com/crewAIInc)[github](https://github.com/crewAIInc/crewAI)[linkedin](https://www.linkedin.com/company/crewai-inc)[youtube](https://youtube.com/@crewAIInc)[Powered by Mintlify](https://mintlify.com/preview-request?utm_campaign=poweredBy&utm_medium=docs&utm_source=docs.crewai.com)
# Replay Tasks from Latest Crew Kickoff
### Replay tasks from the latest crew.kickoff(…)
# [](https://docs.crewai.com/how-to/replay-tasks-from-latest-crew-kickoff#introduction)Introduction
CrewAI provides the ability to replay from a task specified from the latest crew kickoff. This feature is particularly useful when you’ve finished a kickoff and may want to retry certain tasks or don’t need to refetch data over and your agents already have the context saved from the kickoff execution so you just need to replay the tasks you want to.

You must run crew.kickoff() before you can replay a task. Currently, only the latest kickoff is supported, so if you use kickoff_for_each, it will only allow you to replay from the most recent crew run.
Here’s an example of how to replay from a task:
## [](https://docs.crewai.com/how-to/replay-tasks-from-latest-crew-kickoff#replaying-from-specific-task-using-the-cli)Replaying from Specific Task Using the CLI
To use the replay feature, follow these steps:

**1**
**Open your terminal or command prompt.**


**2**
**Navigate to the directory where your CrewAI project is located.**


**3**
**Run the following commands:**
To view the latest kickoff task_ids use:


crewai log-tasks-outputs
Once you have your task_id to replay, use:


crewai replay -t <task_id>

Ensure crewai is installed and configured correctly in your development environment.
## [](https://docs.crewai.com/how-to/replay-tasks-from-latest-crew-kickoff#replaying-from-a-task-programmatically)Replaying from a Task Programmatically
To replay from a task programmatically, use the following steps:

**1**
**Specify the `task_id` and input parameters for the replay process.**
Specify the task_id and input parameters for the replay process.

**2**
**Execute the replay command within a try-except block to handle potential errors.**
Execute the replay command within a try-except block to handle potential errors.
Code



  def replay():
  """
  Replay the crew execution from a specific task.
  """
  task_id = '<task_id>'
  inputs = {"topic": "CrewAI Training"}  # This is optional; you can pass in the inputs you want to replay; otherwise, it uses the previous kickoff's inputs.
  try:
      YourCrewName_Crew().crew().replay(task_id=task_id, inputs=inputs)

  except subprocess.CalledProcessError as e:
      raise Exception(f"An error occurred while replaying the crew: {e}")

  except Exception as e:
      raise Exception(f"An unexpected error occurred: {e}")
# [](https://docs.crewai.com/how-to/replay-tasks-from-latest-crew-kickoff#conclusion)Conclusion
With the above enhancements and detailed functionality, replaying specific tasks in CrewAI has been made more efficient and robust. Ensure you follow the commands and steps precisely to make the most of these features.
