import streamlit as st
from st_pages import show_pages_from_config

st.set_page_config(
    page_title="Amazon Bedrock - Introductory Demo",
    page_icon="👋",
    layout="wide"
)
show_pages_from_config(".streamlit/pages_sections.toml")
css = '''
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
    </style>
'''
st.write(css, unsafe_allow_html=True)
st.write("# PartyRock 💽")

st.markdown(
"""
**[PartyRock](https://partyrock.aws/)** is an Amazon Bedrock playground for building and sharing generative AI apps as part of an *educational* and *fun* experience! PartyRock provides an easy, **no-code**, interactive UI for getting introduced to the power of foundation models with Amazon Bedrock. **Anyone** (no AWS account required) can access PartyRock with free trial use for a limited time, by creating a profile using a social login from amazon.com, Apple, or Google. 
    
Check out these videos below of some PartyRock apps.

-  [Code Translator](https://www.youtube.com/watch?v=U8njepI6Sj0)
-  [School Quiz Generator](https://www.youtube.com/watch?v=iEsxdsET7nI)
""")
