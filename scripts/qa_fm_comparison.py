import streamlit as st
from cg_utils import *

# Get text-to-text FMs
t2t_fms = get_t2t_fms(fm_vendors)


def main():
    """Main function for app"""
    st.set_page_config(page_title="fm QA Comparison", layout="wide")
    css = '''
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                # padding-left: 5rem;
                # padding-right: 5rem;
            } 
            #divshell {
                background-color: #f0f2f6;
                border-top-right-radius: 7px;
                border-top-left-radius: 7px;
                border-bottom-right-radius: 7px;
                border-bottom-left-radius: 7px;
            }         
        </style>
    '''
    st.write(css, unsafe_allow_html=True)
    st.header("Question Answering comparison with Amazon Bedrock FMs")
    st.markdown("Select two FMs, ask a question or give an instruction and press Enter! Refer the [Demo Overview](Solutions%20Overview) for a description of the solution.")
    fm_compare_prompt = st.text_input('Enter question or instruction',key="fm_compare_prompt_key")
    fm_prompt_validation = st.empty()
    col1, col2, col3 = st.columns([2,2,0.25])
    with col1:
        fm_1 = st.selectbox('Select Foundation Model 1',t2t_fms,key="fm_1_key")
        fm_1_output = st.empty()
    with col2:
        fm_2 = st.selectbox('Select Foundation Model 2',t2t_fms,key="fm_2_key")
        fm_2_output = st.empty()
    with col3:
        st.markdown("<br />", unsafe_allow_html=True)
        if fm_compare_prompt:
            if len(st.session_state.fm_compare_prompt_key) < 10:
                with fm_prompt_validation.container():
                    st.error('Your question must contain at least 10 characters.', icon="🚨")
            else:
                with fm_1_output.container():
                    st.markdown(f"<div id='divshell'>{ask_fm(st.session_state.fm_1_key,st.session_state.fm_compare_prompt_key)}</div>", unsafe_allow_html=True)
                with fm_2_output.container():
                    st.markdown(f"<div id='divshell'>{ask_fm(st.session_state.fm_2_key,st.session_state.fm_compare_prompt_key)}</div>", unsafe_allow_html=True)

# Main  
if __name__ == "__main__":
    main()