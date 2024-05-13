import streamlit as st
import re
import asyncio
from langchain.vectorstores import FAISS
from utils import *


async def similarity_search(query:str, text:str) -> str:
    """Similarity search using LangChain, Bedrock's Titan embeddings and FAISS"""
    bedrock_embeddings = BedrockEmbeddings(client=bedrock_runtime)
    sentences_list = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    faiss = FAISS.from_texts(sentences_list, bedrock_embeddings)
    results = faiss.similarity_search(query,1)
    result = ""
    for r in range(len(results)):
        result = result + "\n" + results[r].page_content
    if result:
        return result
    else:
        return "No matches for similarity search!"
    

async def get_fm_response(model_id, prompt):
    """Async wrapper to get response from a foundation model"""
    return ask_fm(model_id, prompt)


async def main():
    """Main function for text querying"""
    st.set_page_config(page_title="Text Query", layout="wide")
    css = '''
        <style>
            .stTextArea textarea {
                height: 190px;
                # color: #de8d0b;
            }
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                # padding-left: 5rem;
                # padding-right: 5rem;
            } 
            #divshell {
                border-top-right-radius: 7px;
                border-top-left-radius: 7px;
                border-bottom-right-radius: 7px;
                border-bottom-left-radius: 7px;
            }                         
        </style>
    '''
    st.write(css, unsafe_allow_html=True)
    st.header("Similarity Search Vs FM Contextual Query")
    st.write("Enter your query regarding the text and press Enter to see the results of a similarity search and a contextual query against an FM. You may modify the text or use your own text.")
    st.markdown("Refer the [Demo Overview](Solutions%20Overview) for a description of the solution.")
    default_text =  """New York City, often referred to as the "Big Apple," is a bustling metropolis known for its iconic skyline, Broadway theaters, and vibrant cultural scene. Paris, the capital of France, is celebrated for its romantic ambiance, exquisite cuisine, and world-renowned landmarks such as the Eiffel Tower and Louvre Museum. Tokyo, the capital of Japan, is a dynamic city where modern skyscrapers blend seamlessly with historic temples, bustling street markets, and cutting-edge technology. Rio de Janeiro, located in Brazil, captivates visitors with its stunning beaches, lively samba music, and iconic Christ the Redeemer statue atop Corcovado mountain. Istanbul, straddling Europe and Asia, boasts a rich history as the former capital of the Byzantine and Ottoman Empires, characterized by its majestic mosques, bustling bazaars, and scenic Bosphorus Strait."""
    text = st.text_area('sentences',default_text, key="sentences_key",label_visibility="hidden",)
    search_string = st.text_input("Enter query:",key="search_string_key",label_visibility="visible")
    search_string_validation = st.empty()
    col1, col2 = st.columns([1,1])
    if search_string:
        tasks = []
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        prompt = f"""Use the following context to provide a concise answer to the question at the end. Skip the preamble.
        If you don't know the answer, just say that you don't know, don't try to make up an answer. Avoid mentioning the context.
        <context>{text}</context>
        <question>{st.session_state.search_string_key}</question>
        """
        task1 = asyncio.create_task(similarity_search(st.session_state.search_string_key, text))
        task2 = asyncio.create_task(get_fm_response(model_id, prompt))
        tasks.extend([task1, task2])
        results = await asyncio.gather(*tasks)
        with col1:
            st.markdown(f"""<div id='divshell' style='background-color: #fbf1dc;'>
            <p style='text-align: center;font-weight: bold;'>Similarity Search</p>{results[0]}<br /></div>
            <br /><br />
            <b>NOTE:</b> A similarity search uses vector representations (embeddings) of the text
            and so the response comprises part of the <u>original text</u> that is most semantically similar to the query.""", unsafe_allow_html=True)
        with col2:
            fm_response, in_tokens, out_tokens = results[1]
            st.markdown(f"""<div id='divshell' style='background-color: #f1fdf1;'>
            <p style='text-align: center;font-weight: bold;'>FM Contextual Query ({model_id})</p>{fm_response}<br /></div>
            <b>Input Tokens:</b> {in_tokens} | <b>Output Tokens:</b> {out_tokens}
            <br /><br />
            <b>NOTE:</b> By simply passing the entire original text to an FM, the FM will attempt to provide a meaningful response
            based on its understanding of the text and query.""", unsafe_allow_html=True)
        st.markdown("""<br /><br />Due to context window limitations with FMs, the retrieval augmented generation (RAG) prompt engineering technique
        uses a combination of semantic search and augmented FM prompts (context) to obtain desired responses.""", unsafe_allow_html=True)
# Main   
if __name__ == "__main__":
    asyncio.run(main())