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
st.write("# Amazon Bedrock - Introductory Demo 👋")

st.markdown(
    """
    Amazon Bedrock is a **fully managed** service that offers **API access** to a choice of high-performing **foundation models** (FMs) from leading AI companies
      including AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon, along with a broad set of capabilities 
      that you need to **build** generative AI (GenAI) applications, **simplifying** development while maintaining **privacy** and **security**. 

    This demo application provides a basic introduction to some GenAI use cases by allowing you to interact with FMs via Amazon Bedrock. 

    **👈 Select a demo from the sidebar** to explore some interactions with Amazon Bedrock!
  
    ### Want to learn more?
    - Check out [Amazon Bedrock](https://aws.amazon.com/bedrock/)
    - Explore [sample notebooks](https://github.com/aws-samples/amazon-bedrock-workshop)
    - Have fun with [PartyRock](PartyRock)

"""
)
