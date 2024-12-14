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

# Add after the sidebar input section and before the Solutions section
def get_solution_codenames(task_description):
    # 根据任务描述中的关键词来选择主题和代号
    task_lower = task_description.lower()
    
    # 数据处理/分析相关任务
    if any(word in task_lower for word in ['data', 'analyze', 'process', 'extract']):
        return {
            'sequential': 'ATLAS-PRIME',  # Atlas - 承担数据重任的泰坦神
            'hierarchical': 'ORACLE-NEXUS',  # Oracle - 智慧与预见的象征
            'parallel': 'HYDRA-CORE'  # Hydra - 多头并行处理的象征
        }
    
    # 创意/生成相关任务
    elif any(word in task_lower for word in ['create', 'generate', 'design', 'write']):
        return {
            'sequential': 'MUSE-FLOW',  # 艺术缪斯
            'hierarchical': 'GENESIS-PRIME',  # 创世神话
            'parallel': 'AURORA-SYNC'  # 极光的多彩创意
        }
    
    # AI/机器学习相关任务
    elif any(word in task_lower for word in ['ai', 'predict', 'learn', 'model']):
        return {
            'sequential': 'CORTEX-ONE',  # 大脑皮层
            'hierarchical': 'NEXUS-MIND',  # 思维枢纽
            'parallel': 'NEURAL-STORM'  # 神经风暴
        }
    
    # 通信/协作相关任务
    elif any(word in task_lower for word in ['communicate', 'chat', 'message', 'email']):
        return {
            'sequential': 'HERMES-LINK',  # 传讯使者赫尔墨斯
            'hierarchical': 'HIVE-MIND',  # 蜂巢思维
            'parallel': 'ECHO-NET'  # 回声女神
        }
    
    # 默认科幻风格代号
    return {
        'sequential': 'QUANTUM-FLOW',
        'hierarchical': 'MATRIX-CORE',
        'parallel': 'NOVA-SYNC'
    }

# 在 Solutions 部分之前添加代号获取
codenames = get_solution_codenames(task_description)

# Style for icons and headers
icon_style = """
<style>
    .solution-card {
        background: #f8f9fa;
        border-radius: 20px;
        padding: 32px;
        margin: 24px 16px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        min-height: 600px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        position: relative;
    }
    .solution-code {
        font-family: 'SF Mono', monospace;
        font-size: 16px;
        font-weight: 600;
        color: #1D6AE5;
        background: rgba(29, 106, 229, 0.1);
        padding: 8px 20px;
        border-radius: 24px;
        display: inline-block;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .solution-icon {
        font-size: 56px;
        color: #1D6AE5;
        margin: 24px auto;
        text-align: center;
        line-height: 1;
        display: block;
    }
    .solution-header {
        font-size: 28px;
        font-weight: 600;
        margin: 16px 0 32px 0;
        text-align: center;
        color: #1E1E1E;
        line-height: 1.3;
    }
    .feature-container {
        width: 100%;
        max-width: 320px;
    }
    .feature-row {
        padding: 24px 0;
        border-bottom: 1px solid #eaeaea;
        text-align: center;
        margin: 0 auto;
    }
    .feature-row:last-child {
        border-bottom: none;
    }
    .feature-icon {
        font-size: 28px;
        color: #666;
        margin-bottom: 16px;
        display: block;
    }
    .feature-label {
        font-size: 18px;
        font-weight: 600;
        color: #1E1E1E;
        margin: 0 0 8px 0;
        line-height: 1.4;
    }
    .feature-value {
        font-size: 16px;
        color: #666;
        margin: 0;
        line-height: 1.5;
    }
    .select-button {
        margin-top: 24px;
        width: 100%;
        max-width: 320px;
        position: absolute;
        bottom: 32px;
        left: 50%;
        transform: translateX(-50%);
    }
    .stButton>button {
        width: 100%;
        max-width: 320px;
        margin: 0 auto;
        display: block;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        border-radius: 8px;
    }
</style>
"""
st.markdown(icon_style, unsafe_allow_html=True)

# Main Layout
st.header("Solutions")

# Create columns with specific ratios for better spacing
col1, col2, col3 = st.columns([1, 1, 1])

# Option 1
with col1:
    st.markdown('<div class="solution-card">', unsafe_allow_html=True)
    st.markdown('<div class="solution-code">QUANTUM-FLOW</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Sequential Flow</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-icon">🔄</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-container">', unsafe_allow_html=True)
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
    st.markdown('<div class="solution-code">MATRIX-CORE</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Hierarchical Flow</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-icon">📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-container">', unsafe_allow_html=True)
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
    st.markdown('<div class="solution-code">NOVA-SYNC</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-header">Parallel Flow</div>', unsafe_allow_html=True)
    st.markdown('<div class="solution-icon">⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-container">', unsafe_allow_html=True)
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
