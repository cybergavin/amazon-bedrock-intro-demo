import streamlit as st
from cg_utils import *
import time


# Create boto3 clients
bedrock_agent = boto3.client(service_name='bedrock-agent')
bedrock_agent_runtime = boto3.client(service_name='bedrock-agent-runtime')
s3 = boto3.client(service_name='s3')


# Get text-to-text FMs
t2t_fms = get_t2t_fms(fm_vendors)


def sync_kb(kb_id:str, ds_id:str):
    """Synchronize the Bedrock knowledge base with its data source"""
    job_done = False
    with st.spinner('Syncing Bedrock knowledge base with data source...'):
        response = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=ds_id )
        sync_job_id = response["ingestionJob"]["ingestionJobId"]
        while not job_done:
            time.sleep(1)
            get_kb_job = bedrock_agent.get_ingestion_job(
                knowledgeBaseId=kb_id,
                dataSourceId=ds_id,
                ingestionJobId=sync_job_id )
            if get_kb_job["ingestionJob"]["status"] != "STARTING" and get_kb_job["ingestionJob"]["status"] != "IN_PROGRESS":
                job_done = True


def upload_docs(docs:list, bucket:str):
    """Upload the file(s) to the S3 bucket (data source)"""
    for doc in docs:
        s3.upload_fileobj(doc, bucket, doc.name)
  

def ask_fm_rag_off(prompt:str, modelid:str):
    """FM query - RAG disabled"""
    return ask_fm(modelid, prompt)


def ask_fm_rag_on(prompt:str, modelid:str, kb_id:str):
    """FM contextual query - RAG enabled, powered by Bedrock's knowledge base"""
    kb_response = bedrock_agent_runtime.retrieve(
        knowledgeBaseId=kb_id,
        retrievalQuery={
            'text': prompt
        },
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 1
        }}
    )
    context = kb_response["retrievalResults"][0]["content"]["text"]
    source = kb_response["retrievalResults"][0]["location"]["s3Location"]["uri"]
    augmented_prompt = f"""Use the following context to provide a concise answer to the question below. If you cannot find the answer, just say that you don't know.
    Do not provide your reasoning for the answer.

     Context: {context}

     Question: {prompt}
    
    """
    response = ask_fm(modelid, augmented_prompt)
    return f"""{response}<br /><br /> <b>Source:</b> {source.split('/')[-1]}"""


def main():
    """Main function for RAG"""
    st.set_page_config(page_title="Retrieval Augmented Generation - Similarity Search", layout="wide")
    css = '''
        <style>   
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                # padding-left: 5rem;
                # padding-right: 5rem;
            }
            button[kind="primary"] {
                background-color: #FF9900;
                border: none;
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
    st.header("Retrieval Augmented Generation (RAG) - powered by Bedrock's knowledge base")
    st.markdown("**Select** a foundation model, **enter** your knowledge base ID and data source ID, **upload** and **submit** your document(s), **enter** a question or instruction to retrieve information from your document(s) and click **Ask**. " \
                 "You will see results with and without using RAG. " \
                 "Refer the [Demo Overview](Solutions%20Overview) for a description of the solution.")
    col1, col2, col3 = st.columns([0.75,2,0.25])
    with col1:
        rag_fm = st.selectbox('Select Foundation Model',t2t_fms, key="rag_fm_key")
        rag_s3 = st.text_input('Enter S3 bucket name',key="rag_s3_key")
        rag_kb = st.text_input('Enter Knowledge Base ID',key="rag_kb_key")
        rag_ds = st.text_input('Enter Knowledge Base Data Source ID',key="rag_ds_key")
        rag_kb_docs = st.file_uploader(label="Upload Documents", type="pdf", accept_multiple_files=True, key="rag_kb_docs_key")
        col1_col1, col1_col2 = st.columns([1, 0.5])
        if st.session_state.rag_kb_docs_key is not None:
            with col1_col1:
                st.button("Submit Documents", type="primary", on_click=upload_docs, args=(st.session_state.rag_kb_docs_key, st.session_state.rag_s3_key))
        with col1_col2:
            st.button("Sync KB", type="primary", on_click=sync_kb, args=(st.session_state.rag_kb_key, st.session_state.rag_ds_key))
    with col2:
        rag_fm_prompt = st.text_input('Enter your question or instruction for information from the uploaded document(s)', key="rag_fm_prompt_key",label_visibility="visible")
        rag_fm_prompt_validation = st.empty()
        col2_col1, col2_col2 = st.columns([1, 1])
        with col2_col1:
            rag_disabled_response = st.empty()               
        with col2_col2:
            rag_enabled_response = st.empty()
    with col3:
        st.markdown("<br />", unsafe_allow_html=True)
        if st.button("Ask!", type="primary"):
            if rag_fm_prompt is not None:
                with rag_fm_prompt_validation.container():
                    if len(rag_fm_prompt) < 10:
                        st.error('Your question or instruction must contain at least 10 characters.', icon="🚨")
                with rag_disabled_response.container():
                    st.markdown(f"<div id='divshell' style='background-color: #fdf1f2;'><p style='text-align: center;font-weight: bold;'>Without RAG ( {rag_fm} )</p>{ask_fm_rag_off(rag_fm_prompt, rag_fm)}</div>", unsafe_allow_html=True)
                with rag_enabled_response.container():
                    st.markdown(f"<div id='divshell' style='background-color: #f1fdf1;'><p style='text-align: center;font-weight: bold;'>With RAG ( {rag_fm} )</p>{ask_fm_rag_on(rag_fm_prompt, rag_fm, st.session_state.rag_kb_key)}</div>", unsafe_allow_html=True)


# Main  
if __name__ == "__main__":
    main()