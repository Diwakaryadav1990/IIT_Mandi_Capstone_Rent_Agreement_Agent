import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables (like GEMINI_API_KEY)
load_dotenv()

from core.agent import analyze_agreement
from core.logger import log_analysis
from ui.components import render_header, render_upload_section, render_results

st.set_page_config(page_title="Rental Agreement Red Flag Agent", page_icon="📝", layout="wide")

@st.dialog("API Key Required")
def api_key_popup():
    st.write("Please provide your Gemini API Key to use this application.")
    api_key_input = st.text_input("Gemini API Key", type="password")
    if st.button("Submit"):
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.rerun()
        else:
            st.error("Please enter a valid API key.")

def get_api_key_from_file():
    """Tries to read the API key from a local api_key.txt file."""
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            key = f.read().strip()
            if key:
                return key
    return None

def main():
    # Render the attractive header
    render_header()
    
    # Check for API Key in session state, api_key.txt, or environment
    active_api_key = st.session_state.get("api_key") or get_api_key_from_file() or os.environ.get("GEMINI_API_KEY")
    
    if not active_api_key:
        api_key_popup()
        st.stop() # Stop execution until the key is provided

    # Render upload section
    agreement_text, filename = render_upload_section()

    # Analysis Button
    if st.button("Analyze Agreement", type="primary"):
        if not agreement_text.strip():
            st.error("Please provide agreement text to analyze.")
        else:
            with st.spinner("Agent is analyzing the agreement..."):
                try:
                    # Call the Gemini Agent
                    analysis_result = analyze_agreement(agreement_text, api_key=active_api_key)
                    
                    # Log the result
                    details_json = analysis_result.model_dump_json()
                    log_analysis(filename=filename, overall_risk_score=analysis_result.overall_risk_score, details=details_json)
                    
                    # Display Results
                    render_results(analysis_result)
                    
                    st.success("Analysis complete and logged.")
                    
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
