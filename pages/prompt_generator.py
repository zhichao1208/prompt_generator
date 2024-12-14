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
                    <div class='icon-button'>📥</div>
                    <div class='icon-button'>🔍</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Version info
        st.markdown("<div style='color: #666;'>Version 1.0 (2024-12-14)</div>", unsafe_allow_html=True)
        
        # Prompt Structure
        st.markdown("<h4 style='margin-top: 20px;'>Prompt Structure</h4>", unsafe_allow_html=True)
        
        # Role Section
        st.markdown("<div class='section-label'>Role</div>", unsafe_allow_html=True)
        st.text_area(
            "Define the role",
            key=f"{version}_role",
            height=100,
            label_visibility="collapsed"
        )
        
        # Task Section
        st.markdown("<div class='section-label'>Task</div>", unsafe_allow_html=True)
        st.text_area(
            "Define the task",
            key=f"{version}_task",
            height=100,
            label_visibility="collapsed"
        )
        
        # Context Section
        st.markdown("<div class='section-label'>Context</div>", unsafe_allow_html=True)
        st.text_area(
            "In-prompt context",
            key=f"{version}_context",
            height=100,
            label_visibility="collapsed"
        )
        
        # Rules Section
        st.markdown("<div class='section-label'>Rules & Constraints</div>", unsafe_allow_html=True)
        st.text_area(
            "Define rules",
            key=f"{version}_rules",
            height=100,
            label_visibility="collapsed"
        )
        
        # Output Format Section
        st.markdown("<div class='section-label'>Output Format</div>", unsafe_allow_html=True)
        st.text_area(
            "Define output format",
            key=f"{version}_output",
            height=100,
            label_visibility="collapsed"
        )
        
        # Enhancements Section
        with st.expander("Enhancements"):
            # Reasoning
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
            st.text_area(
                "Reasoning Details",
                placeholder="Describe how to implement the selected reasoning method...\n\nExample:\nIf using CoT:\n- Break down the problem into steps\n- Show intermediate reasoning\n- Validate each step\n- Connect conclusions",
                help="Tips:\n- Explain implementation details\n- Include specific steps\n- Consider edge cases\n- Add validation points",
                key=f"{version}_reasoning_details",
                height=150
            )
            
            # Planning and Task Decomposition
            st.markdown("<div class='section-label'>Planning and Task Decomposition</div>", unsafe_allow_html=True)
            
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
            st.text_area(
                "Planning Details",
                placeholder="Describe how to implement the selected planning method...\n\nExample:\nIf using Least-to-Most:\n- Identify smallest solvable subtasks\n- Define task dependencies\n- Create execution sequence\n- Add validation checkpoints",
                help="Tips:\n- Break down complex tasks\n- Define clear dependencies\n- Include progress tracking\n- Add error handling",
                key=f"{version}_planning_details",
                height=150
            )
            
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
                    "input": 'PDF contains "Order Date: 2024-12-15" and "Customer: John Doe"',
                    "output": '{"order_date": "2024-12-15", "customer_name": "John Doe"}'
                },
                {
                    "input": 'Email body: "Shipment #12345 will arrive on March 1st, 2024"',
                    "output": '{"shipment_id": "12345", "delivery_date": "2024-03-01"}'
                },
                {
                    "input": 'Invoice shows: Total Amount: $299.99, Due Date: 2024-04-30',
                    "output": '{"amount": 299.99, "due_date": "2024-04-30"}'
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
                    "case": "Missing or Invalid Date",
                    "input": 'PDF contains "Order Date: Invalid" or date field is empty',
                    "handling": "Return error message: {'error': 'Invalid or missing date format', 'field': 'order_date'}"
                },
                {
                    "case": "Multiple Dates in Document",
                    "input": 'Document contains multiple dates: "Order: 2024-01-01, Delivery: 2024-02-01"',
                    "handling": "Extract context-specific date based on field labels, return all dates with labels"
                },
                {
                    "case": "Inconsistent Data Format",
                    "input": 'Mixed date formats: "01/15/2024" and "2024-01-16"',
                    "handling": "Normalize all dates to ISO format (YYYY-MM-DD) before processing"
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
eval_tab1, eval_tab2, eval_tab3, eval_tab4 = st.tabs(["Test", "Evaluate", "Validate", "Train"])

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