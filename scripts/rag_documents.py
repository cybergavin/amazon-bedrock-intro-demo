import streamlit as st
import os
import asyncio
from pathlib import Path, PurePath
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import FAISS
from utils import *


# Directories
UPLOAD_DIR = Path(__file__).resolve().parent.joinpath('', 'upload')
INPUT_DIR = Path(__file__).resolve().parent.joinpath('', 'input')
VECTOR_STORE_DIR = Path(__file__).resolve().parent.joinpath('', 'vector_store')
if not os.path.exists(UPLOAD_DIR):
   os.makedirs(UPLOAD_DIR)
if not os.path.exists(INPUT_DIR):
   os.makedirs(INPUT_DIR)   
if not os.path.exists(VECTOR_STORE_DIR):
   os.makedirs(VECTOR_STORE_DIR)


# Get text-to-text FMs
t2t_fms = list_bedrock_fm_ids(["TEXT"], ["TEXT"], ["ON_DEMAND"])


def process_docs(in_dir:str, out_dir:str):
    """Save uploaded files, process files for embeddings and move processed files"""
    with st.spinner('Splitting files, generating and storing embeddings...'):
        for doc in st.session_state.rag_docs_key:
            upload_path = Path(UPLOAD_DIR, doc.name)
            with open(upload_path, mode='wb') as w:
                w.write(doc.getvalue())
        pdf_chunks = split_pdfs(in_dir)
        st.session_state.faiss_vector_db = embeddings_faiss(pdf_chunks,VECTOR_STORE_DIR, bedrock_embeddings)                
        for f in os.listdir(in_dir):
            src_path = os.path.join(in_dir, f)
            dst_path = os.path.join(out_dir, f)
            os.rename(src_path, dst_path)
        
   
def list_files(dir:str):
    """Display file listing for a directory"""
    if len(os.listdir(dir)) > 0:
        for i,f in enumerate(os.listdir(dir)):
            st.markdown(f"-  {f}",unsafe_allow_html=True)


def split_pdfs(pdf_dir:str) -> list:
    """Load PDFs from a directory and split PDFs into tokens"""
    if os.listdir(pdf_dir):
        loader = DirectoryLoader(pdf_dir, loader_cls=PyPDFLoader)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
            separators=["\n", "\n\n", "(?<=\. )"]
            )
        document_chunks = text_splitter.split_documents(documents)
        return document_chunks


def embeddings_faiss(doc_list:list, db_dir:str, embeddings_fn):
    """Generate embeddings for document chunks and store in a FAISS vector datastore"""
    if doc_list:
        new_db = FAISS.from_documents(doc_list, embeddings_fn)
        if os.listdir(db_dir):
            local_db = FAISS.load_local(db_dir, embeddings_fn)
            local_db.merge_from(new_db)
            local_db.save_local(db_dir)
            return local_db
        else:
            new_db.save_local(db_dir)
            return new_db
    elif os.listdir(db_dir):
        local_db = FAISS.load_local(db_dir, embeddings_fn)
        return local_db
    else:
        return None


def empty_dir(data_dir:str):
    """Remove files from a dircetory"""
    for f in os.listdir(data_dir):
        os.remove(os.path.join(data_dir, f))
      

async def ask_fm_rag_off(prompt:str, modelid:str):
    """FM query - RAG disabled"""
    return ask_fm(modelid, prompt)


async def ask_fm_rag_on(prompt:str, modelid:str, vector_db):
    """FM contextual query - RAG enabled"""
    global augmented_prompt
    global top_k
    top_k = 3
    retriever = vector_db.as_retriever(search_kwargs={"k": top_k})
    results = retriever.invoke(prompt)
    result_text = []
    unique_sources = set()
    for document in results:
        # Extract text content from the document
        page_content = document.page_content.strip()
        result_text.append(page_content)
        # Extract source from the metadata
        source = document.metadata.get('source', 'Unknown')
        filename = source.split('/')[-1]
        unique_sources.add(filename)
    context = ' '.join(result_text)
    unique_sources_list = list(unique_sources)
    augmented_prompt = f"""
    Use only the following context to provide a concise answer to the question at the end. Skip the preamble. Avoid mentioning the context.
    If you cannot find the answer in the context, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    <question>
    {prompt}
    </question>
    """
    response, in_tokens, out_tokens = ask_fm(modelid,augmented_prompt)
    return response, in_tokens, out_tokens, unique_sources_list         


async def main():
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
    st.header("Retrieval Augmented Generation (RAG) - PDF Documents")
    st.markdown("**Select** a foundation model, **upload** and **submit** your document(s), **enter** a question or instruction to retrieve information from your document(s) and click **Ask**. " \
                 "You will see results with and without using RAG. " \
                 "Refer the [Demo Overview](Solutions%20Overview) for a description of the solution.")
    col1, col2, col3 = st.columns([0.75,2,0.25])
    with col1:
        rag_fm = st.selectbox('Select Foundation Model',t2t_fms, key="rag_fm_key")
        rag_docs = st.file_uploader(label="Upload Documents", type="pdf", accept_multiple_files=True, key="rag_docs_key")
        if st.session_state.rag_docs_key is not None:
            st.button("Submit Documents", type="primary", on_click=process_docs, args=(UPLOAD_DIR, INPUT_DIR))
        files = st.empty()
        with files.container():
            list_files(INPUT_DIR)
        if len(os.listdir(INPUT_DIR)) > 0:
            if st.button("Delete Documents", type="primary"):
                empty_dir(INPUT_DIR)
                empty_dir(VECTOR_STORE_DIR)
                with files.container():
                    list_files(INPUT_DIR)
                st.rerun()
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
                if 'faiss_vector_db' not in st.session_state:
                    st.session_state.faiss_vector_db = None
                with rag_fm_prompt_validation.container():
                    if len(rag_fm_prompt) < 10:
                        st.error('Your question or instruction must contain at least 10 characters.', icon="🚨")
                    elif len(os.listdir(INPUT_DIR)) == 0 and len(os.listdir(VECTOR_STORE_DIR)) == 0:
                        st.session_state.faiss_vector_db = None
                        st.error('There are no PDF documents for RAG. Please upload at least one document.', icon="🚨")
                    elif len(os.listdir(INPUT_DIR)) == 0 and len(os.listdir(VECTOR_STORE_DIR)) > 0:
                        empty_dir(VECTOR_STORE_DIR)
                        st.session_state.faiss_vector_db = None
                    elif len(os.listdir(INPUT_DIR)) > 0 and len(os.listdir(VECTOR_STORE_DIR)) == 0:
                        pdf_chunks = split_pdfs(INPUT_DIR)
                        st.session_state.faiss_vector_db = embeddings_faiss(pdf_chunks,VECTOR_STORE_DIR, bedrock_embeddings)
                    elif len(os.listdir(INPUT_DIR)) > 0 and len(os.listdir(VECTOR_STORE_DIR)) > 0:
                        st.session_state.faiss_vector_db = embeddings_faiss([],VECTOR_STORE_DIR, bedrock_embeddings)
                        tasks = []
                        task1 = asyncio.create_task(ask_fm_rag_off(rag_fm_prompt, rag_fm))
                        task2 = asyncio.create_task(ask_fm_rag_on(rag_fm_prompt, rag_fm, st.session_state.faiss_vector_db))
                        tasks.extend([task1, task2])
                        results = await asyncio.gather(*tasks)
                        with rag_disabled_response.container():
                            response_rag_off, _in_tokens, _out_tokens = results[0]
                            in_tokens = _in_tokens if _in_tokens is not None else "Not provided"
                            out_tokens = _out_tokens if _out_tokens is not None else "Not provided"
                            st.markdown(f"""<div id='divshell' style='background-color: #fdf1f2;'>
                            <p style='text-align: center;font-weight: bold;'>Without RAG ( {rag_fm} )</p>
                            {response_rag_off}</div>
                            <b>Input Tokens:</b> {in_tokens} | <b>Output Tokens:</b> {out_tokens}""", unsafe_allow_html=True)
                        with rag_enabled_response.container():
                            response, _in_tokens, _out_tokens, sources_list = results[1]
                            in_tokens = _in_tokens if _in_tokens is not None else "Not provided"
                            out_tokens = _out_tokens if _out_tokens is not None else "Not provided"
                            cs_sources = "\n".join([f"({i+1}) {item}" for i, item in enumerate(sources_list)])
                            st.markdown(f"""<div id='divshell' style='background-color: #f1fdf1;'><p style='text-align: center;font-weight: bold;'>With RAG ( {rag_fm} )</p>
                            {response}<br /><b>Source(s): </b>\n{cs_sources}</div>
                            <b>Input Tokens:</b> {in_tokens} | <b>Output Tokens:</b> {out_tokens}<br /><br />""", unsafe_allow_html=True)
                            expander = st.expander(f"See augmented prompt with top {top_k} search results from source(s) ({in_tokens} tokens)")
                            expander.write(augmented_prompt)


# Main  
if __name__ == "__main__":
    asyncio.run(main())