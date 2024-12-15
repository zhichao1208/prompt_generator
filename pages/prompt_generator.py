import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Prompt Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Left Sidebar: User Input Section
with st.sidebar:
    st.header("Task Configuration")
    
    # Task Description
    st.subheader("Task Description")
    task_description = st.text_area(
        "Task Description",
        placeholder="Enter task description, e.g., 'Extract date and buyer email from order PDF', or input your prompt for optimization.",
        help="Describe the specific task you need to complete"
    )
    
    # Task Type
    st.subheader("Task Type")
    task_type = st.radio(
        "Select Task Type",
        options=["Recommended", "Data Extraction", "Decision Support", "Content Generation", "Data Analysis"],
        help="Select task type, the system will optimize generation strategy accordingly"
    )
    
    # Language Model
    st.subheader("Language Model")
    model_options = {
        "Recommended": ["Recommended"],
        "Claude": ["claude-3-5-sonnet-202410", "claude-3-opus", "claude-3.5-haiku", "claude-3.5-sonnet"],
        "GPT": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-2024-04-09", "gpt-4o", "gpt-4o-mini"],
        "Other": ["cursor-small", "gemini-exp-1206", "o1-mini", "o1-preview"]
    }
    
    model_preference = []
    for model, versions in model_options.items():
        if st.checkbox(model, value=model=="Recommended"):
            if model == "Recommended":
                model_preference.extend(["Recommended"])
            else:
                selected_versions = st.multiselect(f"Select {model} versions", versions)
                model_preference.extend(selected_versions)
    
    # Tone and Context
    st.subheader("Tone and Context")
    tone = st.radio(
        "Communication Tone",
        options=["Professional", "Friendly", "Formal", "Casual"],
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
            placeholder='{\n  "order_date": "2024-12-15",\n  "buyer_name": "John Doe",\n  "buyer_email": "john.doe@example.com"\n}',
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
    col1, col2 = st.columns(2)
    with col1:
        generate_button = st.button("Generate Prompt", type="primary")
    with col2:
        optimize_button = st.button("Optimize Prompt")

# Main Content Area
st.title("Prompt Generator")

# Top Section: Prompt Comparison

# Function to render prompt card
def render_prompt_card(col, version, model_name="claude-3-opus"):
    with col:
        # Header section with title and buttons
        st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
                <h3 style='margin: 0;'>{version}</h3>
                <div style='display: flex; gap: 8px;'>
                    <div id='favorite_{version}' class='icon-button favorite'>⭐</div>
                    <div class='icon-button'>📥 Import</div>
                    <div class='icon-button'>🔍 Search</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Version info
        st.markdown("<div style='color: #666;'>Version 1.0 (2024-12-14)</div>", unsafe_allow_html=True)
        
        # Prompt Structure
        st.markdown("<h4 style='margin-top: 20px;'>Prompt Structure</h4>", unsafe_allow_html=True)
        
        # Role Section
        st.markdown("<div class='section-label'>Role</div>", unsafe_allow_html=True)
        default_role = """You are a highly skilled Data Extraction Specialist, adept at analyzing unstructured data like emails and attachments to extract accurate and relevant information. Your role involves ensuring all required fields are captured with precision, adhering to strict rules, and providing reasoning for any ambiguities encountered during extraction.""" if version == "Solution A" else ""
        st.text_area(
            "Define the role",
            value=default_role,
            key=f"{version}_role",
            height=100,
            label_visibility="collapsed"
        )
        
        # Task Section
        st.markdown("<div class='section-label'>Task</div>", unsafe_allow_html=True)
        default_task = """Your task is to extract order-related information from an email and its attachments. The email was sent by a customer to the seller. You will process this data for TechHeroes to fulfill the order accurately.

Data
Email Content:
{Email}
Attachments:
{Attachments}""" if version == "Solution A" else ""
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
- Log any unprocessable fields or ambiguities for manual review.""" if version == "Solution A" else ""
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
- Compliance with data protection regulations""" if version == "Solution A" else ""

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
        reasoning_method = st.selectbox(
            "Select Reasoning Method",
            options=[
                "Chain-of-Thought (CoT)",
                "Tree-of-Thought (ToT)",
                "Buffer of Thoughts (BoT)",
                "ReAct",
                "Program-of-Thought"
            ],
            key=f"{version}_reasoning_method",
            help="Select the reasoning method that best fits your task"
        )
        
        # Reasoning Details
        default_reasoning = """Implementation Details for Chain-of-Thought:

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
   - Document reasoning for choices made""" if version == "Solution A" else ""
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
        planning_method = st.selectbox(
            "Select Planning Method",
            options=[
                "Least-to-Most Decomposition",
                "Plan-and-Solve Strategy",
                "Progressive Task Refinement",
                "Dependency-Based Planning",
                "Hierarchical Task Planning"
            ],
            key=f"{version}_planning_method",
            help="Select the planning method that best fits your task complexity"
        )
        
        # Planning Details
        default_planning = """Implementation of Least-to-Most Decomposition:

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
   - Validate business rules""" if version == "Solution A" else ""
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
}""" if version == "Solution A" else ""
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
            
            # Model Selection
            models_to_evaluate = st.multiselect(
                "Select Models to Evaluate",
                options=[
                    "GPT-4 Turbo",
                    "GPT-4",
                    "Claude 3 Opus",
                    "Claude 3 Sonnet",
                    "Claude 3 Haiku",
                    "GPT-3.5 Turbo",
                    "Gemini Pro",
                    "Mixtral",
                    "LLaMA 2"
                ],
                default=["GPT-4 Turbo", "Claude 3 Opus"],
                key=f"{version}_model_selection",
                help="Select the models you want to evaluate for this prompt"
            )
            
            # Get user's model preferences from sidebar
            user_models = model_preference if 'model_preference' in locals() else []
            
            # Display model status labels
            st.markdown("##### Model Status")
            for model in models_to_evaluate:
                status_color = "#28a745" if model in user_models else "#dc3545"  # Green for match, Red for mismatch
                status_text = "✓ Matches User Preference" if model in user_models else "× Not in User Preference"
                st.markdown(f"""
                    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 4px;'>
                        <div style='color: {status_color};'>●</div>
                        <div style='font-weight: 500;'>{model}</div>
                        <div style='color: {status_color}; font-size: 0.9em;'>({status_text})</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Model Selection Rationale
            st.markdown("##### Selection Rationale")
            default_rationale = """This prompt configuration is optimized for data extraction tasks with the following considerations:

1. Model Capabilities:
   - GPT-4 Turbo: Excellent at handling complex data structures and validation rules
   - Claude 3 Opus: Strong in natural language understanding and format consistency

2. Task Requirements:
   - Structured data extraction from unstructured text
   - Multiple format handling (email, PDF, attachments)
   - Complex validation rules and error handling

3. Performance Factors:
   - Response accuracy and consistency
   - Processing speed for real-time requirements
   - Cost-effectiveness for production deployment""" if version == "Solution A" else ""
            
            st.text_area(
                "Model Selection Reasoning",
                value=default_rationale,
                height=200,
                help="Explanation of why these models were selected for this prompt"
            )
            
            # Model-specific settings
            if models_to_evaluate:
                st.markdown("##### Model Settings")
                for model in models_to_evaluate:
                    st.markdown(f"**{model}**")
                    cols = st.columns(2)
                    
                    with cols[0]:
                        # Temperature
                        st.slider(
                            "Temperature",
                            min_value=0.0,
                            max_value=1.0,
                            value=0.7,
                            step=0.1,
                            key=f"{version}_{model}_temp",
                            help="Controls randomness in the output"
                        )
                        
                        # Top P
                        st.slider(
                            "Top P",
                            min_value=0.0,
                            max_value=1.0,
                            value=0.9,
                            step=0.1,
                            key=f"{version}_{model}_top_p",
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
                            key=f"{version}_{model}_max_tokens",
                            help="Maximum number of tokens to generate"
                        )
                        
                        # Frequency Penalty
                        st.slider(
                            "Frequency Penalty",
                            min_value=-2.0,
                            max_value=2.0,
                            value=0.0,
                            step=0.1,
                            key=f"{version}_{model}_freq_penalty",
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
eval_tab1, eval_tab2, eval_tab3, eval_tab4 = st.tabs(["Test", "Evaluate", "Validate", "Suggestions"])

with eval_tab1:
    st.subheader("Test Results")
    if st.button("Run Test"):
        st.info("Running test...")
        # Add test results display here

with eval_tab2:
    st.subheader("Evaluation Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", "95%", "+2%")
    with col2:
        st.metric("Token Usage", "1,200", "-100")
    with col3:
        st.metric("Latency", "1.5s", "-0.3s")
    with col4:
        st.metric("Coherence", "High", "+1")
    
    # Visualization
    st.markdown("#### Performance Charts")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("Bar Chart placeholder")
    with chart_col2:
        st.markdown("Radar Chart placeholder")

with eval_tab3:
    st.subheader("Validation Report")
    if st.button("Run Validation"):
        st.info("Validating prompt...")
        st.markdown("#### Validation Results")
        st.markdown("- Rule Compliance Rate: 95%")
        st.markdown("- Error List:")
        st.markdown("  - No critical errors found")
        st.markdown("  - 2 minor warnings")

with eval_tab4:
    st.subheader("Training Data")
    st.file_uploader("Upload training data", type=["csv", "json"])
    if st.button("Start Training"):
        st.info("Training in progress...")
        with st.expander("Training Progress"):
            st.markdown("- Step 1: Data validation ✓")
            st.markdown("- Step 2: Model fine-tuning...")
            st.progress(0.45)