import streamlit as st
import asyncio
import os
from src.models.state import SharedState
from src.utils.llm_client import LLMClient
from src.tools.search_client import SearchClient
from src.agents.orchestrator import Orchestrator
from src.agents.base import BaseAgent

# Set page configuration
st.set_page_config(
    page_title="Cosmetic Formulation AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Premium Design ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background & Text */
    .stApp {
        background-color: #0E1117; 
        color: #FAFAFA;
    }

    /* Gradient Headers */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #FF9A9E, #FECFEF, #E0C3FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stChatInput > div > div > textarea {
        background-color: #1c1f26;
        color: #fff;
        border: 1px solid #333;
        border-radius: 10px;
    }

    /* Cards/Expander Styling */
    .streamlit-expanderHeader {
        background-color: #1F2329;
        border-radius: 10px;
        color: #E0E0E0;
    }
    
    /* Table Styling */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #333;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #A3B9FF;
    }
    
    /* Chat Message Styling */
    div[data-testid="stChatMessage"] {
        background-color: transparent;
    }
    
    /* Report Container */
    .report-container {
        background-color: #151920;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #333;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .report-container h1, .report-container h2 {
        border-bottom: 1px solid #444;
        padding-bottom: 0.5rem;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0E1117; 
    }
    ::-webkit-scrollbar-thumb {
        background: #333; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #555; 
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🧪 Hydra AI")
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.info("Ready to formulate")

# --- Async Orchestrator Wrapper with Logging ---
async def run_formulation(request_text, status_box):
    # Setup Infrastructure
    llm_client = LLMClient()
    search_client = SearchClient()
    state = SharedState()
    
    # --- Monkey Patching for UI Transparency ---
    original_log = BaseAgent.log
    
    def custom_log(self, action: str, details: str):
        # Update UI: Markdown for styling
        msg = f"**[{self.name}]** {action}: {details}"
        status_box.markdown(msg)
        print(msg) 

    # Apply patch
    BaseAgent.log = custom_log
    
    try:
        orchestrator = Orchestrator(state, llm_client, search_client)
        # Run
        await orchestrator.run_workflow(request_text)
    finally:
        # Restore original log
        BaseAgent.log = original_log
        
    return state

# --- Main Content ---
st.title("Advanced Cosmetic Formulation Agent")
st.markdown("#### Design rich, stable, and effective cosmetic products driven by AI.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "content" in message:
             st.markdown(message["content"])

# Helper to render the rich result
def render_result(final_state):
    st.markdown("---")
    # Create tabs for results
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Brief & Research", "⚗️ Formulation", "⚖️ Stability", "📄 Final Report"])
    
    # --- Tab 1: Brief & Research ---
    with tab1:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown("### Parsed Brief")
            if final_state.brief:
                st.json(final_state.brief.model_dump())
            else:
                st.warning("Brief data unavailable")
        
        with col_b:
            st.markdown("### Research Pool")
            st.caption("Scientific evidence gathered from open web:")
            
            # Reduce visual footprint with a scrollable container
            with st.container(height=300, border=True):
                if final_state.evidence_pool:
                    for ev in final_state.evidence_pool:
                        # Compact view
                        with st.expander(f"📚 {ev.title[:50]}...", expanded=False):
                            st.markdown(f"**Relevance:** `{ev.relevance_score}`")
                            st.markdown(f"**Finding:** {ev.key_finding}")
                            st.markdown(f"[[Source]]({ev.source_url})")
                else:
                     st.info("No research data found.")
                    
            st.caption(f"Total Sources: {len(final_state.evidence_pool)}")

    # --- Tab 2: Formulation ---
    with tab2:
        if final_state.current_formula:
            f = final_state.current_formula
            col_header, col_metrics = st.columns([2, 1])
            with col_header:
                st.markdown(f"## {f.name}")
                st.markdown(f"_{f.description}_")
            with col_metrics:
                st.metric("pH Level", f.ph_target)
                st.metric("Viscosity", f.viscosity_target)
            
            st.markdown("#### Composition")
            # Prepare data for cleaner table
            ing_data = [
                {
                    "Phase": i.phase,
                    "Ingredient": i.name,
                    "%": f"{i.percentage}%",
                    "Function": i.function,
                    "Justification": i.justification
                }
                for i in f.ingredients
            ]
            st.dataframe(ing_data, width="stretch") # Updated based on deprecation warning
            st.info(f"**Total Composition:** {f.total_percentage}%")
        else:
            st.error("No composition generated.")

    # --- Tab 3: Stability ---
    with tab3:
        st.markdown("### Risk Analysis")
        if final_state.stability_risks:
            # Grid layout for risks
            cols = st.columns(2)
            for i, risk in enumerate(final_state.stability_risks):
                with cols[i % 2]:
                    risk_color = "red" if risk.risk_level in ["high", "critical"] else "orange" if risk.risk_level == "medium" else "green"
                    
                    if risk.risk_level in ["high", "critical"]:
                        container = st.error
                    elif risk.risk_level == "medium":
                        container = st.warning
                    else:
                        container = st.success
                        
                    # Fix: Pass the title as the body argument to the container
                    with container(body=f"[{risk.risk_level.upper()}] {risk.category.title()}"):
                        st.markdown(f"{risk.description}")
                        st.caption(f"🛡️ Mitigation: {risk.mitigation_strategy}")
        else:
            st.success("✅ No significant stability risks detected.")

    # --- Tab 4: Final Report ---
    with tab4:
        st.markdown("### Generated Documentation")
        report_content = final_state.meta_memory.get("final_report", "")
        
        if report_content:
            # Wrap in custom container for print-like look
            st.markdown('<div class="report-container">', unsafe_allow_html=True)
            st.markdown(report_content)
            
            # Explicitly append References if missing (though agent should handle it)
            # Just ensuring the container closes properly
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download PDF/Markdown",
                data=report_content,
                file_name="formulation_report.md",
                mime="text/markdown",
                # Fix: Replace use_container_width=True with width='stretch'
                help="Download the full report in Markdown format"
            )
        else:
            st.error("Report generation failed.")

# Accept user input
if prompt := st.chat_input("Describe your cosmetic product idea..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        # Status container for logs
        with st.status("🚀 **Agent Activity Log**", expanded=True) as status_box:
            try:
                # Run the function
                final_state = asyncio.run(run_formulation(prompt, status_box))
                status_box.update(label="✅ Workflow Complete!", state="complete", expanded=False)
            except Exception as e:
                status_box.update(label="❌ Workflow Failed", state="error")
                st.error(f"System Error: {str(e)}")
                st.stop()
        
        # Render the rich result
        render_result(final_state)
