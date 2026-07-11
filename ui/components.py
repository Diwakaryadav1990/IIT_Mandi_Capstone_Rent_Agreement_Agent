import streamlit as st
import os

def render_header():
    """Renders the main title and description of the application."""
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right bottom, #f8fafc, #eff6ff);
        }
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #1E3A8A, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            letter-spacing: -1px;
        }
        .sub-header {
            font-size: 1.25rem;
            color: #64748B;
            margin-bottom: 25px;
            font-weight: 500;
        }
        .guardrail {
            background: rgba(254, 242, 242, 0.7);
            backdrop-filter: blur(10px);
            border-left: 4px solid #EF4444;
            padding: 1.2rem;
            border-radius: 8px;
            color: #991B1B;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        div.stButton > button:first-child {
            background: linear-gradient(to right, #2563EB, #1D4ED8);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">Rental Agreement Red Flag Agent 📝</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload your rental agreement (PDF or Text) or paste the text directly. The AI agent will review it and highlight any potentially risky clauses for tenants.</div>', unsafe_allow_html=True)
    st.markdown('<div class="guardrail"><strong>Disclaimer:</strong> This tool provides informational analysis based on AI and is <strong>NOT legal advice</strong>. Always consult a qualified lawyer for legal decisions.</div>', unsafe_allow_html=True)


def render_upload_section():
    """Renders the file upload and text paste inputs."""
    input_method = st.radio("Choose Input Method", ("Upload File", "Paste Text"), horizontal=True)
    
    agreement_text = ""
    filename = "Pasted Text"
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload Rental Agreement (PDF or TXT)", type=["pdf", "txt"])
        if uploaded_file is not None:
            filename = uploaded_file.name
            if uploaded_file.type == "application/pdf":
                from utils.pdf_helper import extract_text_from_pdf
                try:
                    agreement_text = extract_text_from_pdf(uploaded_file)
                    st.success("PDF loaded successfully.")
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
            elif uploaded_file.type == "text/plain":
                try:
                    agreement_text = uploaded_file.read().decode("utf-8")
                    st.success("Text file loaded successfully.")
                except Exception as e:
                    st.error(f"Error reading Text file: {e}")

    elif input_method == "Paste Text":
        agreement_text = st.text_area("Paste Agreement Text Here", height=300)

    return agreement_text, filename


def render_results(analysis_result):
    """Beautifully renders the analysis results."""
    st.markdown("---")
    st.subheader("Analysis Results")
    
    # Overall Risk Score
    risk_color_map = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}
    bg_color_map = {"High": "#FEF2F2", "Medium": "#FFFBEB", "Low": "#ECFDF5"}
    
    risk_score = analysis_result.overall_risk_score
    text_color = risk_color_map.get(risk_score, "#3B82F6")
    bg_color = bg_color_map.get(risk_score, "#EFF6FF")
    
    st.markdown(f"""
    <div style="background-color: {bg_color}; border: 1px solid {text_color}; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
        <h3 style="color: {text_color}; margin-top: 0;">Overall Risk Score: {risk_score}</h3>
        <p style="margin-bottom: 0;"><strong>Summary:</strong> {analysis_result.summary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Highlighted Clauses")
    
    if not analysis_result.clauses:
        st.success("No significant risky clauses found!")
    else:
        for clause in analysis_result.clauses:
            clause_color = risk_color_map.get(clause.risk_label, "#3B82F6")
            with st.expander(f"{clause.clause_type} (Risk: {clause.risk_label})"):
                st.markdown(f"**Risk Level:** <span style='color:{clause_color}; font-weight:bold;'>{clause.risk_label}</span>", unsafe_allow_html=True)
                st.markdown(f"**Clause Text from Agreement:**\n> {clause.clause_text}")
                st.markdown(f"**Agent Explanation:**\n{clause.explanation}")
