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

    cost_preference = st.selectbox("Cost Expectation", options=["Low", "Moderate", "Highest Quality"])

    # Advanced Settings in an expander
    with st.expander("Advanced Settings", expanded=False):
        planning_features = st.checkbox("Enable Planning Features", value=True)        
        collaboration_features = st.checkbox("Enable Collaboration Features", value=True)
        execution_flow = st.radio("Preferred Execution Flow", ["Recommended","Sequential", "Hierarchical", "Consensual"])
        testing_goal = st.radio("Priority Goals", ["Recommended", "Accuracy", "Speed", "Flexibility"])

    # Generate button
    if st.button("Generate", type="primary"):
        st.success("Generating prompts based on your preferences...")

# Main Layout
# Solutions
st.write("---")
st.header("Solutions")

# Modern Comparison Layout
col1, col2, col3 = st.columns(3)

# Style for icons and headers
icon_style = """
<style>
    .solution-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 24px;
        margin: 10px 0;
        text-align: center;
    }
    .solution-code {
        font-family: 'SF Mono', monospace;
        font-size: 14px;
        color: #1D6AE5;
        background: rgba(29, 106, 229, 0.1);
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 16px;
    }
    .solution-icon {
        font-size: 32px;
        color: #1D6AE5;
        margin: 20px 0;
        text-align: center;
    }
    .solution-header {
        font-size: 24px;
        font-weight: 600;
        margin: 16px 0;
        text-align: center;
        color: #1E1E1E;
    }
    .feature-row {
        padding: 24px 0;
        border-bottom: 1px solid #f0f0f0;
        text-align: center;
    }
    .feature-icon {
        font-size: 24px;
        color: #666;
        margin-bottom: 12px;
    }
    .feature-label {
        font-size: 16px;
        font-weight: 600;
        color: #1E1E1E;
        margin: 8px 0;
    }
    .feature-value {
        font-size: 15px;
        color: #666;
        margin: 4px 0;
    }
    .select-button {
        margin-top: 20px;
        width: 100%;
    }
</style>
"""
st.markdown(icon_style, unsafe_allow_html=True)

# Option 1
with col1:
    st.markdown('<div class="solution-card">', unsafe_allow_html=True)
    st.markdown('<div class="solution-code">ALPHA-S1</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Sequential Flow</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-icon">🔄</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Processing Speed</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">1.5s average response</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">🎯</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">claude-3.5-sonnet</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">💰</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Cost</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">Low - $0.01/1k tokens</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Accuracy</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">93% precision rate</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Option 2
with col2:
    st.markdown('<div class="solution-card">', unsafe_allow_html=True)
    st.markdown('<div class="solution-code">BETA-H2</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Hierarchical Flow</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-icon">📊</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Processing Speed</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">1.8s average response</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">🎯</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">gpt-4-turbo</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">💰</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Cost</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">High - $0.03/1k tokens</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Accuracy</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">97% precision rate</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Option 3
with col3:
    st.markdown('<div class="solution-card">', unsafe_allow_html=True)
    st.markdown('<div class="solution-code">GAMMA-P3</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Parallel Flow</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-icon">⚡</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Processing Speed</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">1.2s average response</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">🎯</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">claude-3.5-haiku</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">💰</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Cost</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">Moderate - $0.02/1k tokens</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-label">Accuracy</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-value">90% precision rate</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Selection buttons at the bottom
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Select ALPHA-S1", key="select_sequential", type="primary")
with col2:
    st.button("Select BETA-H2", key="select_hierarchical", type="primary")
with col3:
    st.button("Select GAMMA-P3", key="select_parallel", type="primary")

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
