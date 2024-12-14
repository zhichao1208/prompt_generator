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
st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Prompt Solutions</h1>", unsafe_allow_html=True)

# Create three columns with equal width
col1, col2, col3 = st.columns(3)

# Function to render prompt card
def render_prompt_card(col, version, model_name="claude-3-opus"):
    with col:
        # Version selector (centered)
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><h3>{version}</h3></div>", unsafe_allow_html=True)
        
        # Model image/icon placeholder (centered)
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'>🤖</div>", unsafe_allow_html=True)
        
        # Model name and color options (centered)
        st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{model_name}</div>", unsafe_allow_html=True)
        
        # Price and rate (centered)
        st.markdown("""
            <div style='text-align: center; margin-bottom: 20px;'>
                <div style='font-size: 1.2em; font-weight: bold;'>$0.01/1k tokens</div>
                <div style='color: #666;'>Rate: 25 tokens/second</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Buy button (centered)
        st.markdown("<div style='text-align: center; margin-bottom: 30px;'>", unsafe_allow_html=True)
        st.button("Select", key=f"select_{version}", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Specifications section
        st.markdown("<div style='margin-bottom: 30px;'>", unsafe_allow_html=True)
        
        # Summary section with larger numbers
        st.markdown("""
            <div style='text-align: center; margin-bottom: 30px;'>
                <h2 style='font-size: 2.5em; margin-bottom: 5px;'>98%</h2>
                <div>Accuracy Rate</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Features with icons
        st.markdown("""
            <div style='margin-bottom: 20px;'>
                <div style='margin-bottom: 15px;'>
                    🎯 High Precision Output
                </div>
                <div style='margin-bottom: 15px;'>
                    ⚡ Fast Response Time
                </div>
                <div style='margin-bottom: 15px;'>
                    🔄 Context Awareness
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Detailed specifications
        st.markdown("<h4>Specifications</h4>", unsafe_allow_html=True)
        
        specs = {
            "Context Length": "100k tokens",
            "Response Time": "< 1s",
            "Memory Usage": "8GB",
            "API Rate Limit": "100 req/min"
        }
        
        for key, value in specs.items():
            st.markdown(f"""
                <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                    <div style='color: #666;'>{key}</div>
                    <div style='font-weight: 500;'>{value}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Divider
        st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
        
        # Capabilities section
        st.markdown("<h4>Capabilities</h4>", unsafe_allow_html=True)
        capabilities = [
            "✓ Multi-language Support",
            "✓ Code Generation",
            "✓ Data Analysis",
            "✓ Content Creation"
        ]
        
        for cap in capabilities:
            st.markdown(f"<div style='margin-bottom: 10px;'>{cap}</div>", unsafe_allow_html=True)

# Render three prompt cards
render_prompt_card(col1, "Solution A", "GPT-4 Turbo")
render_prompt_card(col2, "Solution B", "Claude 3 Opus")
render_prompt_card(col3, "Solution C", "Claude 3 Sonnet")

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