import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Graph Generator Interface",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Layout Setup
st.title("Graph Generator Interface")
st.sidebar.header("User Settings")

# Sidebar: User Input
with st.sidebar:
    st.subheader("Task Input")
    task_description = st.text_area("Task Description", placeholder="Describe your task here (e.g., Extract data from webpage and generate emails)")

    st.subheader("Preferences")
    model_preference = st.selectbox("Language Model", ["Claude", "GPT-4", "PaLM", "Llama2"])
    cost_preference = st.select_slider("Cost Expectation", options=["Low", "Medium", "High"])
    prompt_type = st.multiselect("Preferred Prompt Types", ["Zero-Shot", "Few-Shot", "Chain-of-Thought (CoT)", "Tree-of-Thought (ToT)"])
    execution_flow = st.radio("Execution Flow", ["Sequential", "Hierarchical", "Consensual"])
    collaboration_features = st.checkbox("Enable Collaboration Features", value=True)

    st.subheader("Testing Goals")
    testing_goal = st.radio("Priority", ["Accuracy", "Speed", "Flexibility"])

# Main Layout
st.write("---")
st.header("Chat Module")

# Chat Module
with st.expander("Task Input and Dynamic Feedback", expanded=True):
    st.text_area("Chat History", value="System: Welcome! Please describe your task and preferences.", height=200)

    user_input = st.text_input("Your Input", placeholder="Enter additional requirements or adjustments...")
    if st.button("Submit Task"):
        st.success("Task submitted successfully! Generating options in the Composer Module...")

# Composer Module
st.write("---")
st.header("Composer Module")

# Layout Columns
col1, col2, col3 = st.columns([1, 1, 1])

# Option 1
with col1:
    st.subheader("Option 1")
    st.text_area("Summary", "Sequential flow, using Claude and Zero-Shot prompts. Accurate and cost-effective.", height=150)
    st.button("Select Option 1", key="option1")

# Option 2
with col2:
    st.subheader("Option 2")
    st.text_area("Summary", "Hierarchical flow with GPT-4 for dynamic task allocation and CoT prompts.", height=150)
    st.button("Select Option 2", key="option2")

# Option 3
with col3:
    st.subheader("Option 3")
    st.text_area("Summary", "Parallel flow leveraging Claude and PaLM with Few-Shot prompts.", height=150)
    st.button("Select Option 3", key="option3")

# Highlighted Changes Section
st.write("---")
st.header("Highlighted Changes")
with st.expander("Changes Based on Your Preferences"):
    st.markdown("- **Prompt Type:** Adjusted to include Chain-of-Thought (CoT) for logical reasoning tasks.")
    st.markdown("- **Language Model:** Replaced Claude with GPT-4 for better accuracy in hierarchical tasks.")
    st.markdown("- **Cost Impact:** Token usage increased by 20%.")
    st.markdown("Do you accept these changes?")
    if st.button("Accept Changes"):
        st.success("Changes accepted and applied to the selected option.")

# Version History Section
st.write("---")
st.header("Version History")
with st.expander("Review Previous Versions"):
    st.markdown("**Version 1** (Created: 2024-12-14 10:00 AM): Sequential flow with Claude.")
    st.markdown("**Version 2** (Created: 2024-12-14 10:15 AM): Hierarchical flow with GPT-4.")
    st.markdown("**Version 3** (Created: 2024-12-14 10:30 AM): Parallel flow with Few-Shot prompts.")
    version_select = st.selectbox("Select a Version to Review", ["Version 1", "Version 2", "Version 3"])
    if st.button("Restore Version"):
        st.success(f"{version_select} restored successfully!")
