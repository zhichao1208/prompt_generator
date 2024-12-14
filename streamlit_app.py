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

# Main Layout
st.header("Solutions")

# Style for icons and headers
icon_style = """
<style>
    .feature-row {
        display: flex;
        align-items: center;
        padding: 32px 0;
        text-align: left;
        margin: 0 auto;
        gap: 24px;
    }
    .feature-content {
        flex: 1;
    }
    .feature-icon-left {
        font-size: 32px;
        color: #666;
        width: 40px;
        text-align: center;
        flex-shrink: 0;
    }
    .metric-large {
        font-size: 56px;
        font-weight: 700;
        color: #1E1E1E;
        line-height: 1.1;
        margin: 0;
    }
    .metric-best {
        color: #22C55E;
    }
    .metric-unit {
        font-size: 40px;
        font-weight: 600;
        margin-left: 4px;
    }
    .solution-header {
        font-size: 28px;
        font-weight: 600;
        margin: 16px 0;
        color: #1E1E1E;
    }
    .feature-label {
        font-size: 20px;
        font-weight: 600;
        color: #1E1E1E;
        margin: 0 0 4px 0;
    }
    .feature-highlight {
        font-size: 28px;
        font-weight: 600;
        color: #1E1E1E;
        margin: 0;
    }
    .feature-subtext {
        font-size: 16px;
        color: #666;
        margin: 4px 0 0 0;
    }
    .highlight-green {
        color: #22C55E;
    }
    .highlight-red {
        color: #EF4444;
    }
</style>
"""
st.markdown(icon_style, unsafe_allow_html=True)

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

# Add after the sidebar input section and before the Solutions section
def get_solution_codenames(task_description):
    # Check keywords in task description to determine theme and codenames
    task_lower = task_description.lower()
    
    # Data processing/analysis related tasks
    if any(word in task_lower for word in ['data', 'analyze', 'process', 'extract']):
        return {
            'sequential': 'ATLAS-PRIME',  # Atlas - Titan who carries data
            'hierarchical': 'ORACLE-NEXUS',  # Oracle - Symbol of wisdom
            'parallel': 'HYDRA-CORE'  # Hydra - Symbol of parallel processing
        }
    
    # Creative/generative tasks
    elif any(word in task_lower for word in ['create', 'generate', 'design', 'write']):
        return {
            'sequential': 'MUSE-FLOW',  # Art muse
            'hierarchical': 'GENESIS-PRIME',  # Creation myth
            'parallel': 'AURORA-SYNC'  # Aurora's creative diversity
        }
    
    # AI/Machine Learning tasks
    elif any(word in task_lower for word in ['ai', 'predict', 'learn', 'model']):
        return {
            'sequential': 'CORTEX-ONE',  # Brain cortex
            'hierarchical': 'NEXUS-MIND',  # Mind nexus
            'parallel': 'NEURAL-STORM'  # Neural storm
        }
    
    # Communication/Collaboration tasks
    elif any(word in task_lower for word in ['communicate', 'chat', 'message', 'email']):
        return {
            'sequential': 'HERMES-LINK',  # Hermes - Messenger of gods
            'hierarchical': 'HIVE-MIND',  # Hive mind
            'parallel': 'ECHO-NET'  # Echo goddess
        }
    
    # Default sci-fi style codenames
    return {
        'sequential': 'QUANTUM-FLOW',
        'hierarchical': 'MATRIX-CORE',
        'parallel': 'NOVA-SYNC'
    }

# Get codenames before Solutions section
codenames = get_solution_codenames(task_description)

# Create columns with specific ratios for better spacing
col1, col2, col3 = st.columns([1, 1, 1])

# Option 1
with col1:
    st.markdown('<div class="solution-card">', unsafe_allow_html=True)
    st.markdown('<div class="solution-code">QUANTUM-FLOW</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Sequential Flow</div>', unsafe_allow_html=True)
    
    # Speed Metric
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon-left">⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-content">', unsafe_allow_html=True)
    st.markdown('<div class="metric-large">1.5<span class="metric-unit">s</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Average Response Time</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    # Model
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon-left">🎯</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-content">', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">claude-3.5-sonnet</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Base Model</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    # Cost
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon-left">💰</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-content">', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight highlight-green">$0.01</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">per 1k tokens</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    # Accuracy
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon-left">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-content">', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">93%</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Precision Rate</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# Option 2
with col2:
    st.markdown('<div class="solution-card">', unsafe_allow_html=True)
    st.markdown('<div class="solution-code">MATRIX-CORE</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="header-icon">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Hierarchical Flow</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-large">1.8<span class="metric-unit">s</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Average Response Time</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="metric-icon">🎯</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">gpt-4-turbo</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Base Model</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="metric-icon">💰</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">$0.03</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">per 1k tokens</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="metric-icon">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">97%</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Precision Rate</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Option 3
with col3:
    st.markdown('<div class="solution-card">', unsafe_allow_html=True)
    st.markdown('<div class="solution-code">NOVA-SYNC</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="header-icon">⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Parallel Flow</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-large">1.2<span class="metric-unit">s</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Average Response Time</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="metric-icon">🎯</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">claude-3.5-haiku</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Base Model</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="metric-icon">💰</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">$0.02</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">per 1k tokens</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-row">', unsafe_allow_html=True)
    st.markdown('<div class="metric-icon">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-highlight">90%</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-subtext">Precision Rate</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Selection buttons at the bottom
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.button(f"Select {codenames['sequential']}", key="select_sequential", type="primary")
with col2:
    st.button(f"Select {codenames['hierarchical']}", key="select_hierarchical", type="primary")
with col3:
    st.button(f"Select {codenames['parallel']}", key="select_parallel", type="primary")

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
