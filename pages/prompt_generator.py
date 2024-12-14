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
st.header("Prompt Solutions")
tab1, tab2, tab3, tab4 = st.tabs(["Solution 1", "Solution 2", "Solution 3", "Search & Add"])

# Solution Tabs Content
for tab in [tab1, tab2, tab3]:
    with tab:
        # Version and Favorite Section
        col_version, col_favorite = st.columns([3, 1])
        with col_version:
            st.markdown("**Version:** 1.0 (2024-12-14)")
            with st.expander("Version History"):
                st.markdown("- v1.0 (2024-12-14): Initial version")
                st.markdown("- v0.9 (2024-12-13): Draft version")
        with col_favorite:
            st.button("⭐", key=f"{tab._key}_favorite")
        
        # Main Content
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Prompt Structure")
            
            # Role Section
            st.markdown("##### Role")
            st.text_area("Define the role", key=f"{tab._key}_role", height=100)
            
            # Task Section
            st.markdown("##### Task")
            st.text_area("Define the task", key=f"{tab._key}_task", height=100)
            
            # Context Section
            st.markdown("##### Context")
            st.text_area("In-prompt context", key=f"{tab._key}_context", height=100)
            
            # Rules Section
            st.markdown("##### Rules & Constraints")
            st.text_area("Define rules", key=f"{tab._key}_rules", height=100)
            
            # Output Format Section
            st.markdown("##### Output Format")
            st.text_area("Define output format", key=f"{tab._key}_output", height=100)

            # Enhancements Section
            with st.expander("Enhancements"):
                st.markdown("##### Rich Context Integration")
                st.text_area(
                    "Rich Context Integration",
                    placeholder="Example:\n- Tailor summaries based on user's industry background\n- Adapt to user's technical expertise level\n- Incorporate relevant domain terminology\n- Reference similar past cases",
                    help="Tips:\n- Customize content based on user profile\n- Adapt to user preferences\n- Include domain knowledge\n- Support multiple data formats",
                    key=f"{tab._key}_rich_context",
                    height=150
                )
                
                st.markdown("##### Reasoning Generation")
                st.text_area(
                    "Reasoning Generation",
                    placeholder="Example:\n- Break down complex tasks into steps\n- Explain decision points and trade-offs\n- Show alternative approaches considered\n- Highlight key assumptions made",
                    help="Tips:\n- Show step-by-step logic\n- Make decisions transparent\n- Allow manual adjustments\n- Explain key reasoning",
                    key=f"{tab._key}_reasoning",
                    height=150
                )
                
                st.markdown("##### Actionable Outputs")
                st.text_area(
                    "Actionable Outputs",
                    placeholder="Example:\n- Prioritized list of next steps\n- Clear success metrics for each action\n- Timeline recommendations\n- Required resources or dependencies",
                    help="Tips:\n- Provide clear recommendations\n- Include priority levels\n- Define success metrics\n- Suggest next steps",
                    key=f"{tab._key}_actionable",
                    height=150
                )
                
                st.markdown("##### Edge Case Handling")
                st.text_area(
                    "Edge Case Handling",
                    placeholder="Example:\n- Handle missing or invalid data gracefully\n- Provide fallback options for each step\n- Validate inputs against business rules\n- Monitor and log edge cases",
                    help="Tips:\n- Implement error detection\n- Create fallback strategies\n- Add validation checks\n- Handle unexpected inputs",
                    key=f"{tab._key}_edge_case",
                    height=150
                )
            
        with col2:
            # Evaluation Metrics
            st.subheader("Quick Metrics")
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Accuracy", "95%", "+2%")
                st.metric("Latency", "1.5s", "-0.3s")
            with metrics_col2:
                st.metric("Tokens", "1,200", "-100")
                st.metric("Logic", "High", "+1")

# Search Tab Content
with tab4:
    st.subheader("Search Templates")
    search_query = st.text_input("Search for templates", placeholder="e.g., Email Onboarding Prompt")
    
    col_search, col_filters = st.columns([2, 1])
    with col_search:
        st.markdown("#### Search Results")
        for i in range(3):
            with st.container():
                st.markdown(f"**Template {i+1}**")
                st.markdown("Compatibility: High")
                col_preview, col_apply = st.columns([1, 1])
                with col_preview:
                    st.button("Preview", key=f"preview_{i}")
                with col_apply:
                    st.button("Apply", key=f"apply_{i}")
                st.markdown("---")
    
    with col_filters:
        st.markdown("#### Filters")
        st.multiselect("Sources", ["PromptBase", "Internal", "Community"])
        st.slider("Minimum Compatibility", 0, 100, 80)

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