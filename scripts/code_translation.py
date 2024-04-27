import streamlit as st
from cg_utils import *


# Get text-to-text FMs
t2t_fms = get_t2t_fms(fm_vendors)
# Programming languages for code translation
pr_langs = ["C++", "Java", "JavaScript", "Python", "COBOL", "Go"]
# Construct promt template for code translation
prompt_template = """
You are an expert software developer in {tgt_lang}. 
You will translate the code below from to {tgt_lang} while following coding best practices and accurate syntax.
<code>
{code}
</code>

"""


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
            .stTextArea textarea {
                height: 700px !important;
            }
            #divshell {
                background-color: #f0f2f6;
                border-top-right-radius: 7px;
                border-top-left-radius: 7px;
                border-bottom-right-radius: 7px;
                border-bottom-left-radius: 7px;
            }
            button[kind="primary"] {
                background-color: #FF9900;
                border: none;
            }
        </style>
    '''
    st.write(css, unsafe_allow_html=True)
    st.header("Code Translation with Amazon Bedrock FMs")
    st.markdown("Select a **foundation model** and a target **programming language**, enter **code**,  and click **Translate**! Refer the [Demo Overview](Solutions%20Overview) for a description of the solution.")
    col1, col2, col3 = st.columns([0.8,2,2]) 
    with col1:    
        # st.markdown("<br /><br />", unsafe_allow_html=True)    
        fm = st.selectbox('Select Foundation Model',t2t_fms,key="fm_key")
        tgt_lang = st.selectbox("Select target programming language", pr_langs, key="tgt_lang_key")
        fm_prompt_validation = st.empty()
        if "src_lang_code_key" not in st.session_state:
            st.session_state.src_lang_code_key = ""
        if "tgt_code" not in st.session_state:
            tgt_code = ""          
        if st.button("Translate", type="primary"):
            if len(st.session_state.src_lang_code_key) < 50:
                with fm_prompt_validation.container():
                    st.error('Your question must contain at least 50 characters.', icon="🚨")
            else:
                prompt = prompt_template.format(code=st.session_state.src_lang_code_key, tgt_lang=st.session_state.tgt_lang_key)
                tgt_code = f"<div id='divshell'>{ask_fm(st.session_state.fm_key,prompt)}</div>"
    with col2:
        src_lang_code = st.text_area("Enter code to be translated in the text area below:",key="src_lang_code_key")
    with col3:
        # st.markdown("<br /><br />", unsafe_allow_html=True)
        st.markdown(tgt_code, unsafe_allow_html=True)


# Main  
if __name__ == "__main__":
    main()