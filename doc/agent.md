# **Core Concepts**
# Agents
## Detailed guide on creating and managing agents within the CrewAI framework.
# [](https://docs.crewai.com/concepts/agents#overview-of-an-agent)Overview of an Agent
### In the CrewAI framework, anAgent is an autonomous unit that can:
* Perform specific tasks
* Make decisions based on its role and goal
* Use tools to accomplish objectives
* Communicate and collaborate with other agents
* Maintain memory of interactions
* Delegate tasks when allowed

⠀
Think of an agent as a specialized team member with specific skills, expertise, and responsibilities. For example, a Researcher agent might excel at gathering and analyzing information, while a Writer agent might be better at creating content.
# [](https://docs.crewai.com/concepts/agents#agent-attributes)Agent Attributes
| **Attribute** | **Parameter** | **Type** | **Description** |
|---|---|---|---|
| **Role** | role | str | Defines the agent’s function and expertise within the crew. |
| **Goal** | goal | str | The individual objective that guides the agent’s decision-making. |
| **Backstory** | backstory | str | Provides context and personality to the agent, enriching interactions. |
| **LLM** *(optional)* | llm | Union[str, LLM, Any] | Language model that powers the agent. Defaults to the model specified in OPENAI_MODEL_NAME or “gpt-4”. |
| **Tools** *(optional)* | tools | List[BaseTool] | Capabilities or functions available to the agent. Defaults to an empty list. |
| **Function Calling LLM** *(optional)* | function_calling_llm | Optional[Any] | Language model for tool calling, overrides crew’s LLM if specified. |
| **Max Iterations** *(optional)* | max_iter | int | Maximum iterations before the agent must provide its best answer. Default is 20. |
| **Max RPM** *(optional)* | max_rpm | Optional[int] | Maximum requests per minute to avoid rate limits. |
| **Max Execution Time** *(optional)* | max_execution_time | Optional[int] | Maximum time (in seconds) for task execution. |
| **Memory** *(optional)* | memory | bool | Whether the agent should maintain memory of interactions. Default is True. |
| **Verbose** *(optional)* | verbose | bool | Enable detailed execution logs for debugging. Default is False. |
| **Allow Delegation** *(optional)* | allow_delegation | bool | Allow the agent to delegate tasks to other agents. Default is False. |
| **Step Callback** *(optional)* | step_callback | Optional[Any] | Function called after each agent step, overrides crew callback. |
| **Cache** *(optional)* | cache | bool | Enable caching for tool usage. Default is True. |
| **System Template** *(optional)* | system_template | Optional[str] | Custom system prompt template for the agent. |
| **Prompt Template** *(optional)* | prompt_template | Optional[str] | Custom prompt template for the agent. |
| **Response Template** *(optional)* | response_template | Optional[str] | Custom response template for the agent. |
| **Allow Code Execution** *(optional)* | allow_code_execution | Optional[bool] | Enable code execution for the agent. Default is False. |
| **Max Retry Limit** *(optional)* | max_retry_limit | int | Maximum number of retries when an error occurs. Default is 2. |
| **Respect Context Window** *(optional)* | respect_context_window | bool | Keep messages under context window size by summarizing. Default is True. |
| **Code Execution Mode** *(optional)* | code_execution_mode | Literal["safe", "unsafe"] | Mode for code execution: ‘safe’ (using Docker) or ‘unsafe’ (direct). Default is ‘safe’. |
| **Embedder Config** *(optional)* | embedder_config | Optional[Dict[str, Any]] | Configuration for the embedder used by the agent. |
| **Knowledge Sources** *(optional)* | knowledge_sources | Optional[List[BaseKnowledgeSource]] | Knowledge sources available to the agent. |
| **Use System Prompt** *(optional)* | use_system_prompt | Optional[bool] | Whether to use system prompt (for o1 model support). Default is True. |
# [](https://docs.crewai.com/concepts/agents#creating-agents)Creating Agents
### There are two ways to create agents in CrewAI: usingYAML configuration (recommended) or defining them directly in code.
# [](https://docs.crewai.com/concepts/agents#yaml-configuration-recommended)YAML Configuration (Recommended)
### Using YAML configuration provides a cleaner, more maintainable way to define agents. We strongly recommend using this approach in your CrewAI projects.
### After creating your CrewAI project as outlined in the[Installation](https://docs.crewai.com/installation) section, navigate to the src/latest_ai_development/config/agents.yaml file and modify the template to match your requirements.

Variables in your YAML files (like {topic}) will be replaced with values from your inputs when running the crew:
Code


crew.kickoff(inputs={'topic': 'AI Agents'})
### Here’s an example of how to configure agents using YAML:
agents.yaml


# src/latest_ai_development/config/agents.yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.

reporting_analyst:
  role: >
    {topic} Reporting Analyst
  goal: >
    Create detailed reports based on {topic} data analysis and research findings
  backstory: >
    You're a meticulous analyst with a keen eye for detail. You're known for
    your ability to turn complex data into clear and concise reports, making
    it easy for others to understand and act on the information you provide.
### To use this YAML configuration in your code, create a crew class that inherits fromCrewBase:
Code


# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process
from crewai.project import CrewBase, agent, crew
from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'],
      verbose=True,
      tools=[SerperDevTool()]
    )

  @agent
  def reporting_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['reporting_analyst'],
      verbose=True
    )


The names you use in your YAML files (agents.yaml) should match the method names in your Python code.
# [](https://docs.crewai.com/concepts/agents#direct-code-definition)Direct Code Definition
### You can create agents directly in code by instantiating theAgent class. Here’s a comprehensive example showing all available parameters:
Code


from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent with all available parameters
agent = Agent(
    role="Senior Data Scientist",
    goal="Analyze and interpret complex datasets to provide actionable insights",
    backstory="With over 10 years of experience in data science and machine learning, "
              "you excel at finding patterns in complex datasets.",
    llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4"
    function_calling_llm=None,  # Optional: Separate LLM for tool calling
    memory=True,  # Default: True
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    max_iter=20,  # Default: 20 iterations
    max_rpm=None,  # Optional: Rate limit for API calls
    max_execution_time=None,  # Optional: Maximum execution time in seconds
    max_retry_limit=2,  # Default: 2 retries on error
    allow_code_execution=False,  # Default: False
    code_execution_mode="safe",  # Default: "safe" (options: "safe", "unsafe")
    respect_context_window=True,  # Default: True
    use_system_prompt=True,  # Default: True
    tools=[SerperDevTool()],  # Optional: List of tools
    knowledge_sources=None,  # Optional: List of knowledge sources
    embedder_config=None,  # Optional: Custom embedder configuration
    system_template=None,  # Optional: Custom system prompt template
    prompt_template=None,  # Optional: Custom prompt template
    response_template=None,  # Optional: Custom response template
    step_callback=None,  # Optional: Callback function for monitoring
)
### Let’s break down some key parameter combinations for common use cases:
## [](https://docs.crewai.com/concepts/agents#basic-research-agent)Basic Research Agent
Code


research_agent = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="You are an experienced researcher with attention to detail",
    tools=[SerperDevTool()],
    verbose=True  # Enable logging for debugging
)
## [](https://docs.crewai.com/concepts/agents#code-development-agent)Code Development Agent
Code


dev_agent = Agent(
    role="Senior Python Developer",
    goal="Write and debug Python code",
    backstory="Expert Python developer with 10 years of experience",
    allow_code_execution=True,
    code_execution_mode="safe",  # Uses Docker for safety
    max_execution_time=300,  # 5-minute timeout
    max_retry_limit=3  # More retries for complex code tasks
)
## [](https://docs.crewai.com/concepts/agents#long-running-analysis-agent)Long-Running Analysis Agent
Code


analysis_agent = Agent(
    role="Data Analyst",
    goal="Perform deep analysis of large datasets",
    backstory="Specialized in big data analysis and pattern recognition",
    memory=True,
    respect_context_window=True,
    max_rpm=10,  # Limit API calls
    function_calling_llm="gpt-4o-mini"  # Cheaper model for tool calls
)
## [](https://docs.crewai.com/concepts/agents#custom-template-agent)Custom Template Agent
Code


custom_agent = Agent(
    role="Customer Service Representative",
    goal="Assist customers with their inquiries",
    backstory="Experienced in customer support with a focus on satisfaction",
    system_template="""<|start_header_id|>system<|end_header_id|>
                        {{ .System }}<|eot_id|>""",
    prompt_template="""<|start_header_id|>user<|end_header_id|>
                        {{ .Prompt }}<|eot_id|>""",
    response_template="""<|start_header_id|>assistant<|end_header_id|>
                        {{ .Response }}<|eot_id|>""",
)
# [](https://docs.crewai.com/concepts/agents#parameter-details)Parameter Details
## [](https://docs.crewai.com/concepts/agents#critical-parameters)Critical Parameters
* role, goal, and backstory are required and shape the agent’s behavior
* llm determines the language model used (default: OpenAI’s GPT-4)

⠀[](https://docs.crewai.com/concepts/agents#memory-and-context)Memory and Context
* memory: Enable to maintain conversation history
* respect_context_window: Prevents token limit issues
* knowledge_sources: Add domain-specific knowledge bases

⠀[](https://docs.crewai.com/concepts/agents#execution-control)Execution Control
* max_iter: Maximum attempts before giving best answer
* max_execution_time: Timeout in seconds
* max_rpm: Rate limiting for API calls
* max_retry_limit: Retries on error

⠀[](https://docs.crewai.com/concepts/agents#code-execution)Code Execution
* allow_code_execution: Must be True to run code
* code_execution_mode:
  * "safe": Uses Docker (recommended for production)
  * "unsafe": Direct execution (use only in trusted environments)

⠀[](https://docs.crewai.com/concepts/agents#templates)Templates
* system_template: Defines agent’s core behavior
* prompt_template: Structures input format
* response_template: Formats agent responses

⠀
When using custom templates, you can use variables like {role}, {goal}, and {input} in your templates. These will be automatically populated during execution.
# [](https://docs.crewai.com/concepts/agents#agent-tools)Agent Tools
### Agents can be equipped with various tools to enhance their capabilities. CrewAI supports tools from:
* [CrewAI Toolkit](https://github.com/joaomdmoura/crewai-tools)
* [LangChain Tools](https://python.langchain.com/docs/integrations/tools)

⠀Here’s how to add tools to an agent:
Code


from crewai import Agent
from crewai_tools import SerperDevTool, WikipediaTools

# Create tools
search_tool = SerperDevTool()
wiki_tool = WikipediaTools()

# Add tools to agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[search_tool, wiki_tool],
    verbose=True
)
# [](https://docs.crewai.com/concepts/agents#agent-memory-and-context)Agent Memory and Context
### Agents can maintain memory of their interactions and use context from previous tasks. This is particularly useful for complex workflows where information needs to be retained across multiple tasks.
Code


from crewai import Agent

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and remember complex data patterns",
    memory=True,  # Enable memory
    verbose=True
)


When memory is enabled, the agent will maintain context across multiple interactions, improving its ability to handle complex, multi-step tasks.
# [](https://docs.crewai.com/concepts/agents#important-considerations-and-best-practices)Important Considerations and Best Practices
# [](https://docs.crewai.com/concepts/agents#security-and-code-execution)Security and Code Execution
* When using allow_code_execution, be cautious with user input and always validate it
* Use code_execution_mode: "safe" (Docker) in production environments
* Consider setting appropriate max_execution_time limits to prevent infinite loops

⠀[](https://docs.crewai.com/concepts/agents#performance-optimization)Performance Optimization
* Use respect_context_window: true to prevent token limit issues
* Set appropriate max_rpm to avoid rate limiting
* Enable cache: true to improve performance for repetitive tasks
* Adjust max_iter and max_retry_limit based on task complexity

⠀[](https://docs.crewai.com/concepts/agents#memory-and-context-management)Memory and Context Management
* Use memory: true for tasks requiring historical context
* Leverage knowledge_sources for domain-specific information
* Configure embedder_config when using custom embedding models
* Use custom templates (system_template, prompt_template, response_template) for fine-grained control over agent behavior

⠀[](https://docs.crewai.com/concepts/agents#agent-collaboration)Agent Collaboration
* Enable allow_delegation: true when agents need to work together
* Use step_callback to monitor and log agent interactions
* Consider using different LLMs for different purposes:
  * Main llm for complex reasoning
  * function_calling_llm for efficient tool usage

⠀[](https://docs.crewai.com/concepts/agents#model-compatibility)Model Compatibility
* Set use_system_prompt: false for older models that don’t support system messages
* Ensure your chosen llm supports the features you need (like function calling)

⠀[](https://docs.crewai.com/concepts/agents#troubleshooting-common-issues)Troubleshooting Common Issues
### 1 Rate Limiting: If you’re hitting API rate limits:
	* Implement appropriate max_rpm
	* Use caching for repetitive operations
	* Consider batching requests
### 2 Context Window Errors: If you’re exceeding context limits:
	* Enable respect_context_window
	* Use more efficient prompts
	* Clear agent memory periodically
### 3 Code Execution Issues: If code execution fails:
	* Verify Docker is installed for safe mode
	* Check execution permissions
	* Review code sandbox settings
### 4 Memory Issues: If agent responses seem inconsistent:
	* Verify memory is enabled
	* Check knowledge source configuration
	* Review conversation history management

⠀Remember that agents are most effective when configured according to their specific use case. Take time to understand your requirements and adjust these parameters accordingly.
