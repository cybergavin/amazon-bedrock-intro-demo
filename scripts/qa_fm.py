import streamlit as st
from utils import *

# Get text-to-text FMs
t2t_fms = list_bedrock_fm_ids(["TEXT"], ["TEXT"], ["ON_DEMAND"])


def main():
    """Main function for app"""
    st.set_page_config(page_title="Amazon Bedrock Playpen", layout="wide")
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
    st.header("Question Answering with Amazon Bedrock FMs")
    st.markdown("Select a foundation model, ask a question or give an instruction and press Enter! Refer the [Demo Overview](Solutions%20Overview) for a description of the solution.")
    col1, col2 = st.columns([0.4,1])
    with col1:          
        fm = st.selectbox('Select Foundation Model',t2t_fms,key="fm_key")
    with col2:
        fm_prompt = st.text_input("Enter question or instruction", key="fm_prompt_key")
        fm_prompt_validation = st.empty()
        fm_output = st.empty()
        st.markdown("<br />", unsafe_allow_html=True)
        if fm_prompt:
            if len(st.session_state.fm_prompt_key) < 10:
                with fm_prompt_validation.container():
                    st.error('Your question must contain at least 10 characters.', icon="🚨")
            else:
                with fm_output.container():
                    response, _in_tokens, _out_tokens = ask_fm(st.session_state.fm_key,st.session_state.fm_prompt_key)
                    in_tokens = _in_tokens if _in_tokens is not None else "Not provided"
                    out_tokens = _out_tokens if _out_tokens is not None else "Not provided"
                    st.markdown(f"""<div id='divshell'>{response}</div>
                    <b>Input Tokens:</b> {in_tokens} | <b>Output Tokens:</b> {out_tokens}""", unsafe_allow_html=True)

# Main  
if __name__ == "__main__":
    main()