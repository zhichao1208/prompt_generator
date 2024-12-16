import streamlit as st
import sys
import os
from pathlib import Path

# 添加 prompt_solution_crew 到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "prompt_solution_crew" / "src"))

from prompt_solution_crew.crew import PromptSolutionCrew,RequirementsAnalysis,Strategy,StrategicApproaches

# 存储和处理 crew 结果
def process_crew_results(results):
    try:
        # 直接返回完整的分析结果
        if isinstance(results, dict):
            return results
        return {}
    except Exception as e:
        st.error(f"处理结果时出错: {str(e)}")
        return {}

# 创建 session state 变量来存储架构师分析
if "architect_analysis" not in st.session_state:
    st.session_state.architect_analysis = None

# 处理结果并存储到 session state
def store_analysis(results):
    analysis = process_crew_results(results)
    if analysis:
        st.session_state.architect_analysis = analysis

# Page Configuration
st.set_page_config(
    page_title="Prompt Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Left Sidebar: User Input Section


with st.sidebar:
    st.header("Task Configuration")
    # API 状态检查
    st.subheader("API 状态")
    
    # 安全地检查配置（同时检查 secrets 和环境变量）
    def check_config(key):
        try:
            return bool(st.secrets.get(key)) or bool(os.getenv(key))
        except Exception:
            return bool(os.getenv(key))

    api_status = {
        "OpenAI KEY": check_config("OPENAI_API_KEY"),
        "OpenAI Model": check_config("OPENAI_MODEL_NAME")
    }
    
    for api, status in api_status.items():
        if status:
            st.success(f"{api} ✓")
        else:
            st.error(f"{api} ✗")

    # Task Description
    st.subheader("Task Description")
    task_description = st.text_area(
        "Task Description",
        value="Extract order date, buyer name and email address from my order pdf",
        placeholder="Enter task description, e.g., 'Extract date and buyer email from order PDF', or input your prompt for optimization.",
        help="Describe the specific task you need to complete"
    )
    
    # Task Type
    st.subheader("Task Type")
    task_type = st.radio(
        "Select Task Type",
        options=["Recommended", "Data Extraction", "Decision Support", "Content Generation", "Data Analysis"],
        index=1,  # 选择 "Data Extraction"
        help="Select task type, the system will optimize generation strategy accordingly"
    )
    
    # Language Model
    st.subheader("Language Model")
    model_options = {
        "Recommended": ["Recommended"],
        "Claude": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        "GPT": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        "Other": ["gemini-pro", "mixtral", "llama-2"]
    }
    
    model_preference = []
    for model, versions in model_options.items():
        if model == "Recommended":
            if st.checkbox(model, value=True):
                model_preference.extend(["Recommended"])
        elif model == "GPT":
            if st.checkbox(model, value=True):
                selected_versions = st.multiselect(f"Select {model} versions", versions, default=["gpt-4-turbo"])
                model_preference.extend(selected_versions)
        else:
            if st.checkbox(model):
                selected_versions = st.multiselect(f"Select {model} versions", versions)
                model_preference.extend(selected_versions)
    
    # Tone and Context
    st.subheader("Tone and Context")
    tone = st.radio(
        "Communication Tone",
        options=["Professional", "Friendly", "Formal", "Casual"],
        index=0,  # 选择 "Professional"
        help="Choose the tone style for output content"
    )
    
    context = st.text_area(
        "Context Information",
        placeholder="Describe background context to help optimize generation...",
        help="Provide task-related background information"
    )
    
    # Data Input (Optional)
    with st.expander("Data Input (Optional)"):
        data_input = st.text_area(
            "Sample Data",
            value='''Order Details
Date: 2024-03-20
Customer Information:
Name: John Smith
Email: john.smith@example.com
Order Number: ORD-2024-001''',
            help="Paste or upload related data (supports JSON or CSV)"
        )
    
    # Few-Shot Examples (Optional)
    with st.expander("Few-Shot Examples (Optional)"):
        st.markdown("Add examples to help the system understand your requirements better")
        
        # Container for all examples
        examples_container = st.container()
        
        # State for tracking number of examples
        if 'num_examples' not in st.session_state:
            st.session_state.num_examples = 1
        
        # Function to add new example
        def add_example():
            st.session_state.num_examples += 1
        
        # Function to remove last example
        def remove_example():
            if st.session_state.num_examples > 1:
                st.session_state.num_examples -= 1
        
        # Display existing examples
        for i in range(st.session_state.num_examples):
            with examples_container:
                st.markdown(f"**Example {i+1}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.text_area(
                        "Input",
                        placeholder='PDF contains "Order Date: 2024-12-15"',
                        key=f"example_input_{i}",
                        height=100
                    )
                with col2:
                    st.text_area(
                        "Output",
                        placeholder='{"order_date": "2024-12-15"}',
                        key=f"example_output_{i}",
                        height=100
                    )
                st.markdown("---")
        
        # Add/Remove example buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button("➕ Add Example", on_click=add_example)
        with col2:
            if st.session_state.num_examples > 1:
                st.button("➖ Remove Example", on_click=remove_example)

    # Action Buttons
    if st.button("Generate Prompt", type="primary"):
        try:
            # 创建状态容器
            status_container = st.empty()
            result_container = st.empty()
            
            # 显示初始状态
            status_container.info("正在初始化 PromptSolutionCrew...")
            
            # 从Task Configuration收集用户设置
            
            # 收集Few-Shot Examples
            examples = []
            for i in range(st.session_state.num_examples):
                example_input = st.session_state.get(f"example_input_{i}")
                example_output = st.session_state.get(f"example_output_{i}")
                if example_input and example_output:
                    examples.append({
                        "input": example_input,
                        "output": example_output
                    })

            # 准备输入参数
            inputs = {
                'task_description': task_description,
                'task_type': task_type,
                'model_preference': str(model_preference),
                'tone': tone,
                'context': context or 'not defined',
                'sample_data': data_input or 'not defined',
                'examples': str(examples) if examples else 'not defined'
            }
            
            # 更新状态
            status_container.info("开始生成架构...")
            
            # 显示用户输入的配置信息
            st.subheader("用户配置信息")
            st.code(inputs, language="text")
            
            # 使用 spinner 显示生成过程
            with st.spinner('正在生成...'):
                try:
                    # 创建 PromptSolutionCrew 实例并运行
                    architect_crew = PromptSolutionCrew().architect_crew()
                    architect_results = architect_crew.kickoff(inputs=inputs)
                    
                    # 更新状态
                    status_container.success("✅ 架构分析完成!")
                    
                    # 显示架构分析结果
                    if architect_results:
                        result_container.json(architect_results)
                        
                        # 存储架构分析结果
                        store_analysis(architect_results)
                        
                        # 准备 prompt engineer 的输入
                        prompt_inputs = {
                            'task_description': task_description,
                            'task_type': task_type,
                            'model_preference': str(model_preference),
                            'tone': tone,
                            'context': context or 'not defined',
                            'sample_data': data_input or 'not defined',
                            'examples': str(examples) if examples else 'not defined',  # 包含原始输入
                            "architect_results": architect_results  # 传递完整的架构分析
                        }
                        
                        # 运行 prompt engineer crew
                        status_container.info("开始生成优化提示词...")
                        st.code(prompt_inputs, language="text")

                        with st.spinner('正在生成优化提示词...'):
                            prompt_engineer_crew = PromptSolutionCrew().prompt_engineer_crew()
                            engineer_results = prompt_engineer_crew.kickoff(inputs=prompt_inputs)
                            
                            # 更新状态
                            status_container.success("✅ 提示词生成成功!")
                            
                            # 存储结果
                            st.session_state.prompt_result_1 = engineer_results
                            print(engineer_results)
                            
                            # 显示优化后的提示词
                            st.subheader("🎯 优化后的提示词结构")
                            st.json(engineer_results)
                    else:
                        result_container.info("生成完成，但未返回结果。")
                        
                except Exception as e:
                    st.error(f"生成过程中出现错误: {str(e)}")
                    st.error("详细错误信息:")
                    st.exception(e)
                    
        except Exception as e:
            st.error(f"初始化过程中出现错误: {str(e)}")
            st.error("详细错误信息:")
            st.exception(e)
            st.error("请检查配置并重试")
    
# Main Content Area
st.title("Prompt Generator")


# Top Section: Prompt Comparison

# Function to render prompt card
def render_prompt_card(col, version, model_name="claude-3-opus"):
    with col:
        # Header section with title and buttons
        st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
                <h3 style='margin: 0;'>{
                    "JARVIS" if version == "Solution A" else 
                    "SHERLOCK" if version == "Solution B" else 
                    "FLASH"}</h3>
                <div style='display: flex; gap: 8px;'>
                    <div id='favorite_{version}' class='icon-button favorite'>⭐</div>
                    <div class='icon-button'>📥 </div>
                    <div class='icon-button'>🔍 </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Version info
        st.markdown("<div style='color: #666; margin-bottom: 10px;'>Version 1.0 (2024-12-14)</div>", unsafe_allow_html=True)
        
        # Solution Introduction
        st.markdown("<h4 style='margin-top: 20px;'>Overview</h4>", unsafe_allow_html=True)

        intro_text = """•Comprehensive Approach
•Complete data validation and error handling
•Resource Consumption: high""" if version == "Solution A" else (
            """•Validation Focus
•Strong error detection and correction
•Resource Consumption: medium""" if version == "Solution B" else 
            """•Lightweight Design
•Fast processing speed
•Resource Consumption: low""")
        
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 12px; border-radius: 4px; margin-top: 8px; margin-bottom: 12px; border: 1px solid #e9ecef;'>
                <div style='font-size: 0.9em; color: #444; line-height: 1.5; white-space: pre-line;'>
                    {intro_text}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Prompt Structure
        st.markdown("<h4 style='margin-top: 20px;'>Prompt Structure</h4>", unsafe_allow_html=True)
        
        # Role Section
        st.markdown("<div class='section-label'>Role</div>", unsafe_allow_html=True)
        default_role = """You are a highly skilled Data Extraction Specialist, adept at analyzing unstructured data like emails and attachments to extract accurate and relevant information. Your role involves ensuring all required fields are captured with precision, adhering to strict rules, and providing reasoning for any ambiguities encountered during extraction.""" if version == "Solution A" else ("""You are a Data Validation Expert specializing in PDF document analysis and structured information extraction. Your focus is on maintaining data accuracy, implementing robust validation rules, and ensuring data consistency across different document formats. You excel at pattern recognition and data standardization.""" if version == "Solution B" else """You are a Focused Data Parser with expertise in minimal, targeted information extraction. Your specialty lies in quickly identifying and extracting specific data points from documents while maintaining high accuracy. You excel at efficient processing and streamlined output generation.""")
        st.text_area(
            "Define the role",
            value=default_role,
            key=f"{version}_role",
            height=100,
            label_visibility="collapsed"
        )
        
        # Task Section
        st.markdown("<div class='section-label'>Task</div>", unsafe_allow_html=True)
        default_task = """Your task is to extract order-related information from an email and its attachments. The email was sent by a customer to the seller. You will process this data for TechHeroes to fulfill the order accurately.""" if version == "Solution A" else ("""Your primary task is to extract and validate three key pieces of information from PDF documents:
1. Order date - Must be in a valid date format
2. Buyer name - Full name of the customer
3. Email address - Must be a valid individual email address

You will:
- Scan the PDF for these specific data points
- Apply validation rules to each field
- Standardize the format of extracted information
- Report any validation issues or missing data""" if version == "Solution B" else """Your task is to perform targeted extraction of three essential fields from PDF documents:
1. Order date
2. Buyer name
3. Email address

Focus Areas:
- Direct field extraction without additional validation
- Quick identification of target information
- Simple format standardization
- Minimal processing overhead""")
        st.text_area(
            "Define the task",
            value=default_task,
            key=f"{version}_task",
            height=150,
            label_visibility="collapsed"
        )
        
        # Rules Section
        st.markdown("<div class='section-label'>Rules & Constraints</div>", unsafe_allow_html=True)
        default_rules = """General Rules
Accuracy First:
- Extract only explicitly stated information.
- Do not infer or generate information that is not directly present in the email or attachments.

Missing Data Handling:
- For missing fields, use "unknown" as the value.

Email Address Validation:
- The buyer_email_address must belong to an individual (e.g., john.doe@example.com) and not a generic address (e.g., info@ or order@).

Article Code Processing:
- Extract only the seller's (TechHeroes) product_n_article_code.
- Remove any special characters (., -, ) and output as a continuous alphanumeric string.
- If multiple product codes exist, ensure they are presented as a comma-separated list.

Output Format Consistency:
- Follow the predefined JSON structure for outputs without deviation.

Advanced Constraints
Reasoning for Ambiguities:
- If multiple possible values exist for a field, justify the selected value in the Reasoning section.

Contextual Priority:
- Prioritize data found in the email body over data in attachments.
- If duplicate information exists, retain the most recent and complete entry.

Time Zone Standardization:
- Normalize all dates to the YYYY-MM-DD format.

Error Logging:
- Log any unprocessable fields or ambiguities for manual review.""" if version == "Solution A" else ("""Data Quality Rules:
1. Field Validation
   - Order Date: Must be a valid date within the last 30 days
   - Buyer Name: Must contain both first and last name
   - Email: Must be individual email (not generic/group address)

2. Format Requirements
   - Dates: Convert all formats to YYYY-MM-DD
   - Names: Capitalize first letter of each word
   - Email: Convert to lowercase, verify format

3. Data Completeness
   - All three fields are mandatory
   - No partial extractions allowed
   - Missing data must be flagged

4. Validation Process
   - Apply regex patterns for email validation
   - Check date format and validity
   - Verify name format and completeness

5. Error Handling
   - Log all validation failures
   - Provide specific error messages
   - Suggest possible corrections""" if version == "Solution B" else """Essential Rules:
1. Extraction Focus
   - Extract only the three required fields
   - Skip all other information
   - No complex validation required

2. Basic Formatting
   - Date: Convert to YYYY-MM-DD
   - Name: Keep original format
   - Email: Convert to lowercase

3. Processing Rules
   - Single-pass extraction only
   - No cross-validation required
   - Skip ambiguous data

4. Output Requirements
   - Minimal JSON structure
   - No additional metadata
   - Empty string for missing fields""")
        st.text_area(
            "Define rules",
            value=default_rules,
            key=f"{version}_rules",
            height=300,
            label_visibility="collapsed"
        )
        
        # Context Section
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 8px;'>
                <div class='section-label'>Context</div>
                <div class='icon-button show-original' title='Show Original Context'>📄</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Get user input from sidebar
        user_context = context if 'context' in locals() else ""
        
        # Default context when no user input
        default_context = """Background:
- TechHeroes is an e-commerce company specializing in tech products
- They receive orders through email and various document formats
- The system needs to process both direct customer emails and forwarded messages

Current Process:
- Customer service receives order emails
- Manual data extraction is time-consuming and error-prone
- Need automated solution for accurate data extraction

Technical Environment:
- Email server supports IMAP/POP3 protocols
- Document processing system handles PDF, DOC, and image formats
- Integration with order management system required

Business Requirements:
- 24/7 order processing capability
- Real-time data extraction and validation
- Compliance with data protection regulations""" if version == "Solution A" else ("""Processing Environment:
- PDF processing system with OCR capabilities
- Regular document structure updates
- High volume of daily orders

Current Workflow:
- Documents received through multiple channels
- Automated initial scanning
- Manual verification for exceptions

Technical Setup:
- OCR engine for text extraction
- Pattern matching algorithms
- Validation rule engine

Quality Requirements:
- 99.9% accuracy target
- Real-time validation
- Automated error reporting""" if version == "Solution B" else """Processing Setup:
- Basic PDF text extraction
- Single-thread processing
- Minimal memory usage

Current Workflow:
- Direct field extraction
- No preprocessing required
- Simple output generation

Technical Environment:
- Basic text parser
- Minimal dependencies
- Lightweight processing

Performance Focus:
- Speed over complexity
- Resource efficiency
- Minimal overhead""")

        # Display context with user input override
        display_context = user_context if user_context else default_context
        st.text_area(
            "Define context",
            value=display_context,
            key=f"{version}_context",
            height=200,
            label_visibility="collapsed"
        )
        
        # Add JavaScript for showing original context
        st.markdown("""
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const showOriginalButtons = document.querySelectorAll('.show-original');
                showOriginalButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        // Show original context in a modal or tooltip
                        alert(`Original Context:\n\n${default_context}`);
                    });
                });
            });
        </script>
        """, unsafe_allow_html=True)
        
        # Update CSS for context icon
        st.markdown("""
        <style>
        .show-original {
            cursor: pointer;
            padding: 2px 8px;
            font-size: 0.9em;
        }
        .show-original:hover {
            background: #e9ecef;
            border-radius: 4px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Reasoning Section
        st.markdown("<div class='section-label'>Reasoning</div>", unsafe_allow_html=True)
        
        # Reasoning Method Selection
        default_reasoning_method = "Chain-of-Thought (CoT)" if version == "Solution A" else ("ReAct" if version == "Solution B" else "Tree-of-Thought (ToT)")
        reasoning_method = st.selectbox(
            "Select Reasoning Method",
            options=[
                "Chain-of-Thought (CoT)",
                "Tree-of-Thought (ToT)",
                "Buffer of Thoughts (BoT)",
                "ReAct",
                "Program-of-Thought"
            ],
            index=["Chain-of-Thought (CoT)", "Tree-of-Thought (ToT)", "Buffer of Thoughts (BoT)", "ReAct", "Program-of-Thought"].index(default_reasoning_method),
            key=f"{version}_reasoning_method",
            help="Select the reasoning method that best fits your task"
        )
        
        # Reasoning Details based on selected method
        reasoning_templates = {
            "Chain-of-Thought (CoT)": """Implementation Details for Chain-of-Thought:

1. Initial Data Scan
   - Identify all potential data fields in email and attachments
   - Mark ambiguous or duplicate information
   
2. Field Extraction
   - Apply validation rules for each field type
   - Handle special cases (dates, email addresses, product codes)
   
3. Data Normalization
   - Convert dates to YYYY-MM-DD format
   - Clean product codes by removing special characters
   - Validate email format
   
4. Cross-validation
   - Compare data between email body and attachments
   - Resolve conflicts using priority rules
   - Document reasoning for choices made""",
            "ReAct": """Implementation Details for ReAct:

1. Observation Phase
   - Scan document for target fields
   - Identify potential data locations
   - Note any irregularities or patterns

2. Thought Process
   - Analyze document structure
   - Consider possible data formats
   - Plan extraction strategy

3. Action Steps
   - Extract target fields
   - Apply validation rules
   - Standardize formats

4. Verification
   - Check extraction results
   - Validate against rules
   - Document any issues""",
            "Tree-of-Thought (ToT)": """Implementation Details for Tree-of-Thought:

1. Root Analysis
   - Identify document structure
   - Map key information locations
   - Define extraction paths

2. Branch Development
   - Create parallel extraction strategies
   - Consider alternative data formats
   - Establish validation branches

3. Path Evaluation
   - Compare extraction results
   - Score path effectiveness
   - Select optimal route

4. Result Synthesis
   - Combine successful paths
   - Apply final validation
   - Generate output"""
        }
        
        default_reasoning = reasoning_templates.get(reasoning_method, "")
        st.text_area(
            "Define reasoning",
            value=default_reasoning,
            key=f"{version}_reasoning",
            height=250,
            label_visibility="collapsed"
        )
        
        # Planning Section
        st.markdown("<div class='section-label'>Planning</div>", unsafe_allow_html=True)
        
        # Planning Method Selection
        default_planning_method = "Least-to-Most Decomposition" if version == "Solution A" else ("Plan-and-Solve Strategy" if version == "Solution B" else "Progressive Task Refinement")
        planning_method = st.selectbox(
            "Select Planning Method",
            options=[
                "Least-to-Most Decomposition",
                "Plan-and-Solve Strategy",
                "Progressive Task Refinement",
                "Dependency-Based Planning",
                "Hierarchical Task Planning"
            ],
            index=["Least-to-Most Decomposition", "Plan-and-Solve Strategy", "Progressive Task Refinement", "Dependency-Based Planning", "Hierarchical Task Planning"].index(default_planning_method),
            key=f"{version}_planning_method",
            help="Select the planning method that best fits your task complexity"
        )
        
        # Planning Details based on selected method
        planning_templates = {
            "Least-to-Most Decomposition": """Implementation of Least-to-Most Decomposition:

1. Field-level Tasks
   - Identify required fields (order_number, dates, emails, etc.)
   - Define validation rules for each field
   - Create field-specific extraction functions

2. Document-level Tasks
   - Parse email body structure
   - Extract attachment content
   - Create document traversal strategy

3. Integration Tasks
   - Combine data from multiple sources
   - Apply business rules and constraints
   - Generate final output structure

4. Validation Tasks
   - Verify data completeness
   - Check format compliance
   - Validate business rules""",
            "Plan-and-Solve Strategy": """Implementation of Plan-and-Solve Strategy:

1. Analysis Phase
   - Identify document type and structure
   - Locate potential data regions
   - Map validation requirements

2. Extraction Strategy
   - Define field extraction sequence
   - Set up validation checkpoints
   - Prepare error handlers

3. Processing Steps
   - Extract each target field
   - Apply immediate validation
   - Format standardization

4. Quality Control
   - Run validation suite
   - Check completeness
   - Generate quality report""",
            "Progressive Task Refinement": """Implementation of Progressive Task Refinement:

1. Initial Scan
   - Quick document overview
   - Identify key sections
   - Mark target fields

2. Refinement Steps
   - Focus on each target field
   - Apply specific extraction rules
   - Validate as you go

3. Optimization
   - Refine extraction patterns
   - Improve accuracy
   - Minimize processing time

4. Final Check
   - Verify all fields
   - Format consistency
   - Output preparation"""
        }
        
        default_planning = planning_templates.get(planning_method, "")
        st.text_area(
            "Define planning",
            value=default_planning,
            key=f"{version}_planning",
            height=200,
            label_visibility="collapsed"
        )
        
        # Output Format Section
        st.markdown("<div class='section-label'>Output Format</div>", unsafe_allow_html=True)
        
        # Add format selection
        output_format = st.selectbox(
            "Select Output Format",
            options=["JSON", "Email", "Markdown", "Text", "Other"],
            key=f"{version}_output_format",
            help="Select the desired output format for the response"
        )
        
        default_output = """{
  "Reasoning": [
    "Reasoning statements documenting decision-making processes and resolving ambiguities."
  ],
  "Buyer": {
    "buyer_company_name": "string",
    "buyer_person_name": "string",
    "buyer_email_address": "string"
  },
  "Order": {
    "order_number": "string",
    "order_date": "YYYY-MM-DD",
    "delivery_address_street": "string",
    "delivery_address_city": "string",
    "delivery_address_postal_code": "string",
    "delivery_address_country": "string",
    "delivery_additional_details": "string"
  },
  "Product": [
    {
      "product_1_position": 1,
      "product_1_article_code": "string",
      "product_1_quantity": "integer"
    },
    {
      "product_n_position": "integer",
      "product_n_article_code": "string",
      "product_n_quantity": "integer"
    }
  ]
}""" if version == "Solution A" else ("""{
  "status": "success|error",
  "extracted_data": {
    "order_date": "YYYY-MM-DD",
    "buyer_name": "First Last",
    "email": "user@domain.com"
  },
  "validation_results": {
    "date_valid": true|false,
    "name_valid": true|false,
    "email_valid": true|false
  },
  "errors": [
    {
      "field": "field_name",
      "error": "error_description",
      "suggestion": "correction_suggestion"
    }
  ]
}""" if version == "Solution B" else """{
  "extracted_data": {
    "date": "YYYY-MM-DD",
    "name": "string",
    "email": "string"
  }
}""")
        st.text_area(
            "Define output format",
            value=default_output,
            key=f"{version}_output",
            height=300,
            label_visibility="collapsed"
        )
        
        # Enhancements Section
        with st.expander("Enhancements"):
            # Multi-Model Evaluation
            st.markdown("<div class='section-label'>Multi-Model Evaluation</div>", unsafe_allow_html=True)
            
            # Get user's model preference (use the first selected GPT model)
            selected_model = None
            for model, versions in model_options.items():
                if model == "GPT" and st.session_state.get(f"checkbox_{model}", False):
                    selected_versions = st.session_state.get(f"multiselect_{model}", [])
                    if selected_versions:
                        selected_model = selected_versions[0]
                        break
            
            if not selected_model:
                selected_model = "gpt-4-turbo"  # 默认模型
            
            # Display selected model status
            st.markdown("##### Model Status")
            st.markdown(f"""
                <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 4px;'>
                    <div style='color: #28a745;'>●</div>
                    <div style='font-weight: 500;'>{selected_model}</div>
                    <div style='color: #28a745; font-size: 0.9em;'>(User Preferred Model)</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Model Selection Rationale
            st.markdown("##### Selection Rationale")
            default_rationale = """This prompt configuration is optimized for data extraction tasks with the following considerations:

1. Model Selection:
   - Using GPT-4 Turbo as the primary model for its superior performance in structured data extraction
   - Optimized for accuracy and consistency in field identification

2. Task Alignment:
   - Perfect match for PDF parsing and data normalization
   - Strong capability in handling multiple date formats
   - Excellent at email validation and formatting

3. Performance Benefits:
   - High accuracy in field extraction
   - Fast processing speed
   - Cost-effective for production use""" if version == "Solution A" else ("""This prompt configuration is optimized for validation tasks with the following considerations:

1. Model Selection:
   - Using GPT-4 Turbo for its robust validation capabilities
   - Excellent at pattern recognition and error detection

2. Task Alignment:
   - Specialized in data validation and standardization
   - Strong in identifying format inconsistencies
   - Built-in error correction suggestions

3. Performance Benefits:
   - High validation accuracy
   - Real-time processing
   - Efficient error handling""" if version == "Solution B" else """This prompt configuration is optimized for minimal extraction with the following considerations:

1. Model Selection:
   - Using GPT-4 Turbo for its precise extraction capabilities
   - Focused on efficiency and accuracy

2. Task Alignment:
   - Specialized in key field extraction
   - Minimal but essential validation
   - Streamlined processing

3. Performance Benefits:
   - Quick response time
   - Resource efficient
   - Cost optimized""")
            
            st.text_area(
                "Model Selection Reasoning",
                value=default_rationale,
                height=200,
                key=f"{version}_model_rationale",
                help="Explanation of why this model was selected for this prompt"
            )
            
            # Model Settings
            st.markdown("##### Model Settings")
            cols = st.columns(2)
            
            with cols[0]:
                # Temperature
                st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.7,
                    step=0.1,
                    key=f"{version}_temp",
                    help="Controls randomness in the output"
                )
                
                # Top P
                st.slider(
                    "Top P",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.9,
                    step=0.1,
                    key=f"{version}_top_p",
                    help="Controls diversity via nucleus sampling"
                )
            
            with cols[1]:
                # Max tokens
                st.number_input(
                    "Max Tokens",
                    min_value=1,
                    max_value=4096,
                    value=2048,
                    step=1,
                    key=f"{version}_max_tokens",
                    help="Maximum number of tokens to generate"
                )
                
                # Frequency Penalty
                st.slider(
                    "Frequency Penalty",
                    min_value=-2.0,
                    max_value=2.0,
                    value=0.0,
                    step=0.1,
                    key=f"{version}_freq_penalty",
                    help="Adjusts likelihood based on frequency"
                )
            
            st.markdown("---")
            
            # Dynamic Prompt Optimization
            st.markdown("<div class='section-label'>Dynamic Prompt Optimization</div>", unsafe_allow_html=True)
            
            # Examples Section
            st.markdown("##### Examples")
            
            # Container for examples
            examples_container = st.container()
            
            # State for tracking number of examples
            if f'{version}_num_examples' not in st.session_state:
                st.session_state[f'{version}_num_examples'] = 3  # Default 3 examples
            
            # Default examples data
            default_examples = [
                {
                    "input": """Email Content:
Subject: Order Confirmation #12345
From: john.smith@company.com
Date: 2024-03-15

Dear TechHeroes,
Please process my order #TH-2024-12345.
Shipping Address: 123 Main St, Boston, MA 02108""",
                    "output": """{
  "order_number": "TH202412345",
  "buyer_email": "john.smith@company.com",
  "order_date": "2024-03-15",
  "shipping_address": {
    "street": "123 Main St",
    "city": "Boston",
    "state": "MA",
    "zip": "02108"
  }
}"""
                },
                {
                    "input": """Attachment: invoice.pdf
Order: #TH-2024-56789
Customer: Jane Doe (jane.doe@email.com)
Products:
- 2x TH-PRD-001 ($99.99 each)
- 1x TH-PRD-002 ($149.99)""",
                    "output": """{
  "order_number": "TH202456789",
  "buyer_email": "jane.doe@email.com",
  "products": [
    {
      "code": "THPRD001",
      "quantity": 2,
      "price": 99.99
    },
    {
      "code": "THPRD002",
      "quantity": 1,
      "price": 149.99
    }
  ]
}"""
                },
                {
                    "input": """Email Content:
From: support@vendor.com
Subject: Updated Order Details

Updated delivery for order #TH-2024-78901
New delivery date: April 1st, 2024
Contact: Mark Wilson (mark.w@customer.com)""",
                    "output": """{
  "error": "Invalid sender email",
  "details": "Email must be from individual address, not support@vendor.com",
  "order_data": {
    "order_number": "TH202478901",
    "delivery_date": "2024-04-01",
    "contact_email": "mark.w@customer.com"
  }
}"""
                }
            ]
            
            # Function to add new example
            def add_example(version):
                st.session_state[f'{version}_num_examples'] += 1
            
            # Function to remove last example
            def remove_example(version):
                if st.session_state[f'{version}_num_examples'] > 1:
                    st.session_state[f'{version}_num_examples'] -= 1
            
            # Display examples
            for i in range(st.session_state[f'{version}_num_examples']):
                with examples_container:
                    st.markdown(f"**Example {i+1}**")
                    col1, col2 = st.columns(2)
                    with col1:
                        default_input = default_examples[i]["input"] if i < len(default_examples) else ""
                        st.text_area(
                            "Input",
                            value=default_input,
                            key=f"{version}_example_input_{i}",
                            height=100
                        )
                    with col2:
                        default_output = default_examples[i]["output"] if i < len(default_examples) else ""
                        st.text_area(
                            "Output",
                            value=default_output,
                            key=f"{version}_example_output_{i}",
                            height=100
                        )
                    st.markdown("---")
            
            # Add/Remove example buttons
            col1, col2 = st.columns(2)
            with col1:
                st.button("➕ Add Example", key=f"{version}_add_example", 
                         on_click=add_example, args=(version,))
            with col2:
                if st.session_state[f'{version}_num_examples'] > 1:
                    st.button("➖ Remove Example", key=f"{version}_remove_example",
                             on_click=remove_example, args=(version,))
            
            # Edge Cases Section
            st.markdown("##### Edge Cases")
            
            # State for tracking number of edge cases
            if f'{version}_num_edge_cases' not in st.session_state:
                st.session_state[f'{version}_num_edge_cases'] = 3  # Default 3 edge cases
            
            # Default edge cases
            default_edge_cases = [
                {
                    "case": "Invalid Email Format",
                    "input": """From: sales@company.com
Order: #TH-2024-99999
Customer: Alice Johnson""",
                    "handling": """Return error:
{
  "error": "Invalid email format",
  "details": "Generic email address not allowed (sales@company.com)",
  "required": "Individual email address (e.g., firstname.lastname@company.com)"
}"""
                },
                {
                    "case": "Multiple Order Numbers",
                    "input": """Reference: #TH-2024-11111
Original Order: #TH-2024-22222
Updated Order: #TH-2024-33333""",
                    "handling": """Extract all order numbers and prioritize:
{
  "current_order": "TH202433333",
  "original_order": "TH202422222",
  "reference_order": "TH202411111",
  "note": "Using most recent order number as primary reference"
}"""
                },
                {
                    "case": "Inconsistent Date Formats",
                    "input": """Order Date: 03/15/2024
Delivery: 2024-04-01
Expected: 1st May 2024""",
                    "handling": """Normalize all dates to ISO format:
{
  "order_date": "2024-03-15",
  "delivery_date": "2024-04-01",
  "expected_date": "2024-05-01",
  "note": "All dates normalized to YYYY-MM-DD format"
}"""
                }
            ]
            
            # Function to add new edge case
            def add_edge_case(version):
                st.session_state[f'{version}_num_edge_cases'] += 1
            
            # Function to remove last edge case
            def remove_edge_case(version):
                if st.session_state[f'{version}_num_edge_cases'] > 1:
                    st.session_state[f'{version}_num_edge_cases'] -= 1
            
            # Display edge cases
            for i in range(st.session_state[f'{version}_num_edge_cases']):
                with st.container():
                    st.markdown(f"**Edge Case {i+1}**")
                    default_case = default_edge_cases[i] if i < len(default_edge_cases) else {"case": "", "input": "", "handling": ""}
                    
                    # Case Description
                    st.text_input("Case Description", 
                                value=default_case["case"],
                                key=f"{version}_edge_case_desc_{i}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_area(
                            "Example Input",
                            value=default_case["input"],
                            key=f"{version}_edge_case_input_{i}",
                            height=80
                        )
                    with col2:
                        st.text_area(
                            "Handling Strategy",
                            value=default_case["handling"],
                            key=f"{version}_edge_case_handling_{i}",
                            height=80
                        )
                    st.markdown("---")
            
            # Add/Remove edge case buttons
            col1, col2 = st.columns(2)
            with col1:
                st.button("➕ Add Edge Case", key=f"{version}_add_edge_case",
                         on_click=add_edge_case, args=(version,))
            with col2:
                if st.session_state[f'{version}_num_edge_cases'] > 1:
                    st.button("➖ Remove Edge Case", key=f"{version}_remove_edge_case",
                             on_click=remove_edge_case, args=(version,))

# Add custom CSS
st.markdown("""
<style>
    .section-label {
        color: #666;
        font-size: 0.9em;
        font-weight: 500;
        margin-bottom: 5px;
        margin-top: 15px;
    }
    .stTextArea textarea {
        font-size: 0.9em;
        border-radius: 4px;
    }
    .stExpander {
        border: none;
        box-shadow: none;
        background-color: transparent;
    }
    .icon-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 4px 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        cursor: pointer;
        background: #f8f9fa;
        font-size: 0.9em;
        transition: all 0.2s;
    }
    
    .icon-button:hover {
        background: #e9ecef;
    }
    
    .favorite {
        color: #666;
    }
    
    .favorite.active {
        color: #ffd700;
        background: #fff4e6;
    }
    
    /* Add JavaScript for favorite button toggle */
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.favorite').forEach(button => {
                button.addEventListener('click', function() {
                    this.classList.toggle('active');
                });
            });
        });
    </script>
</style>
""", unsafe_allow_html=True)

# Create three columns with equal width
col1, col2, col3 = st.columns(3)

# Render three prompt cards
render_prompt_card(col1, "Solution A")
render_prompt_card(col2, "Solution B")
render_prompt_card(col3, "Solution C")

# Bottom Section: Evaluation & Analysis
st.header("Evaluation & Analysis")
eval_tab1, eval_tab2 = st.tabs(["Test & Results", "Evaluation Metrics"])

with eval_tab1:
    st.subheader("Test Input")
    
    # 显示用户输入的任务
    st.markdown("**Task Description:**")
    st.info("Extract order date, buyer name and email address from my order pdf")
    
    # 文件上传
    uploaded_file = st.file_uploader("Upload PDF file for testing", type=['pdf'])
    
    # Run Test 按钮
    if st.button("Run Test", type="primary"):
        st.info("Running test with all three solutions...")
        
        # 创建三列显示测试结果
        test_col1, test_col2, test_col3 = st.columns(3)
        
        with test_col1:
            st.markdown("#### JARVIS Results")
            
            # Planning 部分
            st.markdown("**Planning:**")
            st.code("""1. Document Analysis
- Parse PDF structure
- Identify key sections
- Map target fields

2. Field Extraction
- Date patterns
- Name formats
- Email validation

3. Data Validation
- Format check
- Completeness verify
- Error handling""")
            
            # Reasoning 部分
            st.markdown("**Reasoning:**")
            st.code("""Using Chain-of-Thought:
1. Located order section
2. Found date: 2024-03-20
3. Identified customer info block
4. Extracted name: John Smith
5. Validated email format
6. Confirmed: john.smith@example.com""")
            
            # Output 部分
            st.markdown("**Output:**")
            st.json({
                "order_date": "2024-03-20",
                "buyer_name": "John Smith",
                "email": "john.smith@example.com",
                "confidence_score": 0.95
            })
            
        with test_col2:
            st.markdown("#### SHERLOCK Results")
            
            # Planning 部分
            st.markdown("**Planning:**")
            st.code("""1. Initial Scan
- Document structure check
- Field location mapping
- Validation rules setup

2. Data Processing
- Pattern matching
- Format validation
- Error detection

3. Quality Control
- Data verification
- Format standardization
- Completeness check""")
            
            # Reasoning 部分
            st.markdown("**Reasoning:**")
            st.code("""Using ReAct:
1. PDF scan complete
2. Date found: 2024-03-20
3. Name section identified
4. Name extracted: John Smith
5. Email located and validated
6. Email confirmed: john.smith@example.com""")
            
            # Output 部分
            st.markdown("**Output:**")
            st.json({
                "extracted_data": {
                    "date": "2024-03-20",
                    "name": "John Smith",
                    "email": "john.smith@example.com"
                },
                "validation": {
                    "all_fields_found": True,
                    "formats_valid": True
                }
            })
            
        with test_col3:
            st.markdown("#### FLASH Results")
            
            # Planning 部分
            st.markdown("**Planning:**")
            st.code("""1. Quick Scan
- Target field search
- Direct extraction
- Basic validation

2. Processing
- Simple pattern match
- Format check
- Data extraction""")
            
            # Reasoning 部分
            st.markdown("**Reasoning:**")
            st.code("""Using Tree-of-Thought:
1. Scanned document
2. Found date: 2024-03-20
3. Extracted name: John Smith
4. Found email: john.smith@example.com
5. Basic validation passed""")
            
            # Output 部分
            st.markdown("**Output:**")
            st.json({
                "date": "2024-03-20",
                "name": "John Smith",
                "email": "john.smith@example.com"
            })

with eval_tab2:
    
    # 首先显示评估结果
    st.markdown("### Evaluation Results")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    # 创建核心指标对比可化
    st.markdown("### Core Metrics Comparison")
    
    # 准备数据
    metrics_data = {
        "JARVIS": {
            "Accuracy": 98,
            "Goal Achievement": 100,
            "Efficiency": 95,
            "Logic Score": 97
        },
        "SHERLOCK": {
            "Accuracy": 95,
            "Goal Achievement": 95,
            "Efficiency": 93,
            "Logic Score": 93
        },
        "FLASH": {
            "Accuracy": 92,
            "Goal Achievement": 90,
            "Efficiency": 98,
            "Logic Score": 90
        }
    }
    
    # 使用Plotly建雷达图
    import plotly.graph_objects as go
    
    categories = list(metrics_data["JARVIS"].keys())
    
    fig = go.Figure()
    
    colors = {"JARVIS": "#1f77b4", "SHERLOCK": "#ff7f0e", "FLASH": "#2ca02c"}
    
    for solution in metrics_data:
        values = list(metrics_data[solution].values())
        # 添��首个值到末尾以闭合图形
        values.append(values[0])
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            name=solution,
            line=dict(color=colors[solution]),
            fill='toself',
            opacity=0.4
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        height=400,
        margin=dict(l=80, r=80, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    
    # JARVIS Results
    with metric_col1:
        st.markdown("#### JARVIS Analysis")
        
        # 核心维度
        st.markdown("**Core Metrics**")
        
        # 第一行：准确性和目标达成度
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", "98%", help="Match rate between expected and actual outputs")
        with col2:
            st.metric("Goal Achievement", "100%", help="Completion rate of required tasks")
        
        # 第二行：效率和逻辑性
        col3, col4 = st.columns(2)
        with col3:
            st.metric("Efficiency", "95%", help="Overall efficiency score")
            # Efficiency Breakdown Box
            st.markdown("""
                <div style='background-color: #f1f8ff; padding: 10px; border-radius: 4px; margin-top: 5px; margin-bottom: 20px; border: 1px solid #cce5ff;'>
                    <div style='font-size: 0.9em; color: #004085; margin-bottom: 5px;'>
                        <strong>Efficiency Breakdown</strong>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085; margin-bottom: 3px;'>
                        <span>Token Usage:</span>
                        <span>2,500</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085; margin-bottom: 3px;'>
                        <span>Response Time:</span>
                        <span>2.5s</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085;'>
                        <span>Cost per Run:</span>
                        <span>$0.05</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.metric("Logic Score", "97%", help="Quality of reasoning process")
        
        # 高级维度（展���区）
        with st.expander("Advanced Dimensions"):
            # 稳定性分析
            st.markdown("**Stability Analysis**")
            stab_col1, stab_col2 = st.columns(2)
            with stab_col1:
                st.metric("Format Compatibility", "96%", help="Ability to handle different document formats")
                st.metric("Error Handling", "98%", help="Effectiveness in handling exceptions")
            with stab_col2:
                st.metric("Cross-platform", "95%", help="Consistency across different platforms")
                st.metric("System Stability", "97%", help="Overall system stability")
            
            # 可解释性
            st.markdown("**Explainability**")
            exp_col1, exp_col2 = st.columns(2)
            with exp_col1:
                st.metric("Process Transparency", "98%", help="Clarity of the extraction process")
                st.metric("Decision Clarity", "97%", help="Clarity of decision making")
            with exp_col2:
                st.metric("Documentation", "96%", help="Quality of reasoning documentation")
                st.metric("Reasoning Path", "95%", help="Clarity of reasoning steps")
            
            # 创造力
            st.markdown("**Creativity & Adaptability**")
            cre_col1, cre_col2 = st.columns(2)
            with cre_col1:
                st.metric("Pattern Recognition", "94%", help="Ability to identify data patterns")
                st.metric("Format Flexibility", "93%", help="Adaptability to format changes")
            with cre_col2:
                st.metric("Edge Case Handling", "92%", help="Handling of unusual scenarios")
                st.metric("Learning Ability", "91%", help="Capability to learn from new cases")
            
            # 安全性
            st.markdown("**Safety & Compliance**")
            saf_col1, saf_col2 = st.columns(2)
            with saf_col1:
                st.metric("Data Protection", "99%", help="Security of data handling")
                st.metric("Bias Prevention", "98%", help="Prevention of biased results")
            with saf_col2:
                st.metric("Compliance", "97%", help="Adherence to standards")
                st.metric("Risk Control", "96%", help="Effectiveness of risk management")
    
    # SHERLOCK Results
    with metric_col2:
        st.markdown("#### SHERLOCK Analysis")
        
        # 核心维度
        st.markdown("**Core Metrics**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", "95%", help="Match rate between expected and actual outputs")
        with col2:
            st.metric("Goal Achievement", "98%", help="Completion rate of required tasks")
        
        col3, col4 = st.columns(2)
        with col3:
            st.metric("Efficiency", "97%", help="Overall efficiency score")
            # Efficiency Breakdown Box
            st.markdown("""
                <div style='background-color: #f1f8ff; padding: 10px; border-radius: 4px; margin-top: 5px; margin-bottom: 20px; border: 1px solid #cce5ff;'>
                    <div style='font-size: 0.9em; color: #004085; margin-bottom: 5px;'>
                        <strong>Efficiency Breakdown</strong>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085; margin-bottom: 3px;'>
                        <span>Token Usage:</span>
                        <span>1,800</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085; margin-bottom: 3px;'>
                        <span>Response Time:</span>
                        <span>1.8s</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085;'>
                        <span>Cost per Run:</span>
                        <span>$0.035</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.metric("Logic Score", "96%", help="Quality of reasoning process")
        
        # SHERLOCK Advanced Dimensions
        with st.expander("Advanced Dimensions"):
            # 稳定性分析
            st.markdown("**Stability Analysis**")
            stab_col1, stab_col2 = st.columns(2)
            with stab_col1:
                st.metric("Format Compatibility", "97%", help="Ability to handle different document formats")
                st.metric("Error Handling", "96%", help="Effectiveness in handling exceptions")
            with stab_col2:
                st.metric("Cross-platform", "97%", help="Consistency across different platforms")
                st.metric("System Stability", "97%", help="Overall system stability")
            
            # 可解释性
            st.markdown("**Explainability**")
            exp_col1, exp_col2 = st.columns(2)
            with exp_col1:
                st.metric("Process Transparency", "96%", help="Clarity of the extraction process")
                st.metric("Decision Clarity", "95%", help="Clarity of decision making")
            with exp_col2:
                st.metric("Documentation", "97%", help="Quality of reasoning documentation")
                st.metric("Reasoning Path", "95%", help="Clarity of reasoning steps")
            
            # 创造力
            st.markdown("**Creativity & Adaptability**")
            cre_col1, cre_col2 = st.columns(2)
            with cre_col1:
                st.metric("Pattern Recognition", "92%", help="Ability to identify data patterns")
                st.metric("Format Flexibility", "91%", help="Adaptability to format changes")
            with cre_col2:
                st.metric("Edge Case Handling", "93%", help="Handling of unusual scenarios")
                st.metric("Learning Ability", "91%", help="Capability to learn from new cases")
            
            # 安全性
            st.markdown("**Safety & Compliance**")
            saf_col1, saf_col2 = st.columns(2)
            with saf_col1:
                st.metric("Data Protection", "98%", help="Security of data handling")
                st.metric("Bias Prevention", "97%", help="Prevention of biased results")
            with saf_col2:
                st.metric("Compliance", "98%", help="Adherence to standards")
                st.metric("Risk Control", "96%", help="Effectiveness of risk management")
    
    # FLASH Results
    with metric_col3:
        st.markdown("#### FLASH Analysis")
        
        # 核心维度
        st.markdown("**Core Metrics**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", "92%", help="Match rate between expected and actual outputs")
        with col2:
            st.metric("Goal Achievement", "95%", help="Completion rate of required tasks")
        
        col3, col4 = st.columns(2)
        with col3:
            st.metric("Efficiency", "99%", help="Overall efficiency score")
            # Efficiency Breakdown Box
            st.markdown("""
                <div style='background-color: #f1f8ff; padding: 10px; border-radius: 4px; margin-top: 5px; margin-bottom: 20px; border: 1px solid #cce5ff;'>
                    <div style='font-size: 0.9em; color: #004085; margin-bottom: 5px;'>
                        <strong>Efficiency Breakdown</strong>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085; margin-bottom: 3px;'>
                        <span>Token Usage:</span>
                        <span>1,200</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085; margin-bottom: 3px;'>
                        <span>Response Time:</span>
                        <span>1.2s</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; font-size: 0.85em; color: #004085;'>
                        <span>Cost per Run:</span>
                        <span>$0.025</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.metric("Logic Score", "93%", help="Quality of reasoning process")
        
        # FLASH Advanced Dimensions
        with st.expander("Advanced Dimensions"):
            # 稳定性分析
            st.markdown("**Stability Analysis**")
            stab_col1, stab_col2 = st.columns(2)
            with stab_col1:
                st.metric("Format Compatibility", "94%", help="Ability to handle different document formats")
                st.metric("Error Handling", "93%", help="Effectiveness in handling exceptions")
            with stab_col2:
                st.metric("Cross-platform", "92%", help="Consistency across different platforms")
                st.metric("System Stability", "90%", help="Overall system stability")
            
            # 可解释性
            st.markdown("**Explainability**")
            exp_col1, exp_col2 = st.columns(2)
            with exp_col1:
                st.metric("Process Transparency", "91%", help="Clarity of the extraction process")
                st.metric("Decision Clarity", "92%", help="Clarity of decision making")
            with exp_col2:
                st.metric("Documentation", "90%", help="Quality of reasoning documentation")
                st.metric("Reasoning Path", "89%", help="Clarity of reasoning steps")
            
            # 创造力
            st.markdown("**Creativity & Adaptability**")
            cre_col1, cre_col2 = st.columns(2)
            with cre_col1:
                st.metric("Pattern Recognition", "88%", help="Ability to identify data patterns")
                st.metric("Format Flexibility", "87%", help="Adaptability to format changes")
            with cre_col2:
                st.metric("Edge Case Handling", "87%", help="Handling of unusual scenarios")
                st.metric("Learning Ability", "86%", help="Capability to learn from new cases")
            
            # 安全性
            st.markdown("**Safety & Compliance**")
            saf_col1, saf_col2 = st.columns(2)
            with saf_col1:
                st.metric("Data Protection", "96%", help="Security of data handling")
                st.metric("Bias Prevention", "95%", help="Prevention of biased results")
            with saf_col2:
                st.metric("Compliance", "94%", help="Adherence to standards")
                st.metric("Risk Control", "93%", help="Effectiveness of risk management")
    
    # 维度权重调整
    st.markdown("### Dimension Weights")
    
    # 创建选项卡用于不同方案的权重调整
    weight_tabs = st.tabs(["JARVIS Weights", "SHERLOCK Weights", "FLASH Weights"])
    
    for idx, tab in enumerate(weight_tabs):
        with tab:
            solution_name = ["JARVIS", "SHERLOCK", "FLASH"][idx]
            st.markdown(f"#### {solution_name} Dimension Weights")
            
            # 核心维度
            st.markdown("**Core Dimensions**")
            core_col1, core_col2 = st.columns(2)
            with core_col1:
                accuracy_weight = st.slider(
                    "Accuracy Weight", 0.0, 1.0, 0.3, 0.1,
                    help="Measures the match between expected and actual outputs",
                    key=f"{solution_name}_accuracy"
                )
                efficiency_weight = st.slider(
                    "Efficiency Weight", 0.0, 1.0, 0.2, 0.1,
                    help="Evaluates token usage, response time, and cost",
                    key=f"{solution_name}_efficiency"
                )
            with core_col2:
                logic_weight = st.slider(
                    "Logic Weight", 0.0, 1.0, 0.3, 0.1,
                    help="Assesses reasoning path and process clarity",
                    key=f"{solution_name}_logic"
                )
                goal_weight = st.slider(
                    "Goal Achievement Weight", 0.0, 1.0, 0.2, 0.1,
                    help="Checks if all required tasks are completed",
                    key=f"{solution_name}_goal"
                )
            
            # 高级维度
            st.markdown("**Advanced Dimensions**")
            adv_col1, adv_col2 = st.columns(2)
            with adv_col1:
                stability_weight = st.slider(
                    "Stability Weight", 0.0, 1.0, 0.1, 0.1,
                    help="Tests robustness across different inputs",
                    key=f"{solution_name}_stability"
                )
                explain_weight = st.slider(
                    "Explainability Weight", 0.0, 1.0, 0.1, 0.1,
                    help="Evaluates clarity of reasoning process",
                    key=f"{solution_name}_explain"
                )
            with adv_col2:
                creative_weight = st.slider(
                    "Creativity Weight", 0.0, 1.0, 0.1, 0.1,
                    help="Assesses flexibility and adaptability",
                    key=f"{solution_name}_creative"
                )
                safety_weight = st.slider(
                    "Safety Weight", 0.0, 1.0, 0.1, 0.1,
                    help="Checks for bias and harmful content",
                    key=f"{solution_name}_safety"
                )
            
            # 新生成按钮
            if st.button(f"Regenerate {solution_name} Prompt", type="primary", key=f"regenerate_{solution_name}"):
                # 版本号管理
                if f'{solution_name}_version' not in st.session_state:
                    st.session_state[f'{solution_name}_version'] = 1.0
                else:
                    st.session_state[f'{solution_name}_version'] += 0.1
                
                st.success(f"""
                Prompt regenerated successfully!
                New version: {st.session_state[f'{solution_name}_version']:.1f}
                
                Weight Configuration:
                - Accuracy: {accuracy_weight}
                - Efficiency: {efficiency_weight}
                - Logic: {logic_weight}
                - Goal Achievement: {goal_weight}
                - Stability: {stability_weight}
                - Explainability: {explain_weight}
                - Creativity: {creative_weight}
                - Safety: {safety_weight}
                """)
    
    # 权重调整建议
    with st.expander("Weight Adjustment Tips"):
        st.markdown("""
        **How to Adjust Weights:**
        
        1. **Task-Specific Focus:**
           - Data Extraction: Prioritize accuracy and efficiency
           - Creative Tasks: Increase creativity and stability weights
           - Critical Applications: Emphasize safety and explainability
        
        2. **Use Case Considerations:**
           - Production Environment: Higher weights for stability and efficiency
           - Development Phase: Focus on accuracy and explainability
           - User-Facing Applications: Balance all dimensions
        
        3. **Performance Optimization:**
           - Identify bottlenecks in current results
           - Adjust weights to focus on improvement areas
           - Monitor impact on overall performance
        """)

# 添加自定义CSS样式
st.markdown("""
<style>
    /* 调整指标标题的样式 */
    .metric-label {
        white-space: normal !important;
        height: auto !important;
        min-height: 25px;
        line-height: 1.2;
        font-size: 14px !important;
    }
    
    /* 调整指标��的样式 */
    .metric-value {
        font-size: 24px !important;
        line-height: 1.2;
        margin: 5px 0;
    }
    
    /* 调整列间距 */
    .row-widget.stHorizontal > div {
        padding: 10px 5px;
    }
</style>
""", unsafe_allow_html=True)