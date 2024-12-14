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
    task_type = st.selectbox(
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
    tone = st.selectbox(
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
        few_shot = st.text_area(
            "Input-Output Examples",
            placeholder='Input: PDF contains "Order Date: 2024-12-15"\nOutput: {"order_date": "2024-12-15"}',
            help="Provide input-output examples to help system understand task requirements"
        )
    
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
            
        with col2:
            st.subheader("Version Info")
            st.markdown("**Version:** 1.0")
            st.markdown("**Created:** 2024-12-14")
            
            # Version History
            with st.expander("Version History"):
                st.markdown("- v1.0 (2024-12-14): Initial version")
                st.markdown("- v0.9 (2024-12-13): Draft version")

# Search Tab Content
with tab4:
    st.subheader("Search Templates")
    search_query = st.text_input("Search for templates", placeholder="e.g., Email Onboarding Prompt")
    
    st.subheader("Saved Templates")
    with st.expander("My Templates"):
        st.markdown("- Template 1: Email Generation")
        st.markdown("- Template 2: Data Extraction")
        st.markdown("- Template 3: Decision Support")

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

with eval_tab3:
    st.subheader("Validation Report")
    if st.button("Run Validation"):
        st.info("Validating prompt...")
        # Add validation results display here

with eval_tab4:
    st.subheader("Training Data")
    st.file_uploader("Upload training data", type=["csv", "json"])
    if st.button("Start Training"):
        st.info("Training in progress...")
        # Add training progress display here 