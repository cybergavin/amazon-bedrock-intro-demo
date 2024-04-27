import streamlit as st


st.set_page_config(page_title="Solutions Overview", layout="wide")
css = '''
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            # padding-left: 5rem;
            # padding-right: 5rem;
        }                
    </style>
'''
st.write(css, unsafe_allow_html=True)
st.header("Demo Overview")
st.write("This page provides an overview of the solutions used by the demos listed in the sidebar.")
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Question Answering", "Chatbot", "Text Search", "Code Translation", "RAG - Documents", "RAG - Bedrock Knowledge Base", "RAG - Web Search"])
with tab1:
    # FM QA using Amazon Bedrock
    st.subheader("Question Answering with Amazon Bedrock FMs")
    st.markdown("""
    This demo allows you to interact with an FM hosted by Amazon Bedrock, with questions or instructions. This demo uses:
    - Streamlit for the web interface
    - AWS SDK for python (Boto3) for access to FMs via API calls to Amazon Bedrock

    """)
    st.image('img/qa_fm.png', caption="Question Answering with FMs using Amazon Bedrock", width=650)
with tab2:
    # FM chat using Amazon Bedrock
    st.subheader("Chat with Amazon Bedrock FMs")
    st.markdown("""
    This demo allows you to chat with an FM, hosted by Amazon Bedrock. A chat stores your **conversation history** and provides it as context to the FM along with your question or instruction. This demo uses:
    - Streamlit for the web interface
    - LangChain library for using Amazon Bedrock FMs and conversational history

    """)
    st.image('img/chat_fm.png', caption="Chat with FMs using Amazon Bedrock", width=650)  
with tab3:  
    # Text Search
    st.subheader("Text Search")
    st.markdown("""
    This demo shows the results of searching for information from text with similarity search and a contextual query to an FM:  
    - **Similarity search:** Split text into sentences, convert sentences and query into embeddings, store embeddings in a vector datastore and find sentences whose embeddings are closest to that of the query (most similar).  A similarity search considers the semantics and context of the query based on closeness of vectors or embeddings. The top result of a similarity search is the sentence that most closely resembles the **context** and **meaning** of the query string.
    - **Contextual search:** Create a prompt with the query and the entire text (as context) to generate a response from an FM (hosted on Amazon Bedrock).
                
    """)
    st.markdown("""
    This demo solution uses:
    - Streamlit for the web interface
    - AWS SDK for python (Boto3) for API access to FMs via Amazon Bedrock
    - LangChain library for using FMs and the FAISS vector datastore
    - The Amazon Titan Embeddings G1 - Text FM for generating embeddings
    - The FAISS vector datastore for storing, indexing and searching embeddings
    - The Anthropic Claude v2 FM for genertating answers to natural language queries

    """)
    st.image('img/text_search.png', caption="Text Search - Similarity/Contextual", width=650)
with tab4:
    # Code Translation using Amazon Bedrock
    st.subheader("Code Translation with Amazon Bedrock FMs")
    st.markdown("""
    This demo allows you to translate code between programming languages using Amazon Bedrock FMs. Anthropic and Cohere FMs have been optimized for code and used for this demo. This demo uses:
    - Streamlit for the web interface
    - AWS SDK for python (Boto3) for API access to FMs via API calls to Amazon Bedrock
                
    """)
    st.image('img/code_translation.png', caption="Code Translation using Amazon Bedrock", width=650)
with tab5:
    # RAG - PDF Documents
    st.subheader("Retrieval Augmented Generation (RAG) - PDF Documents")
    st.markdown("This demo allows you to retrieve information from PDF documents using the RAG technique with FMs. When you upload a PDF document, it is split into chunks, the chunks are conveterd into embeddings and stored in a vector datastore. When you ask a question or send an instruction, your question/instruction is converted into embeddings and used for a similarity search to **retrieve** similar chunks of information from the vector datastore. The information retrieved is then used as context to **augment** a prompt to an FM to enable it **generate** an appropriate response.")
    st.markdown("""
    This demo uses:
    - Streamlit for the web interface
    - AWS SDK for python (Boto3) for API access to FMs via Amazon Bedrock
    - LangChain library for using FMs and vector datastores
    - The Amazon Titan Embeddings G1 - Text FM for generating embeddings
    - The FAISS vector datastore for storing, indexing and searching embeddings
    - Text-to-Text Bedrock FMs for generating answers to natural language queries

    """)
    st.image('img/rag_documents.png', caption="Retrieval Augmented Generation - Text Documents", width=650)
with tab6:
    # RAG - Bedrock Knowledge Base
    st.subheader("Retrieval Augmented Generation (RAG) - Amazon Bedrock Knowledge Base")
    st.markdown("""
    This demo allows you to retrieve information from documents using the Amazon Bedrock Knowledge Base feature.
    Amazon Bedrock Knowledge Base is a **fully managed RAG** workflow for your GenAI applications. 
    This demo solution uses:
    - Streamlit for the web interface
    - AWS SDK for python (Boto3) for API access to FMs via API calls to Amazon Bedrock
    - A provisioned Amazon Bedrock Knowledge Base
                
    """)
    st.image('img/rag_bedrock_kb.png', caption="Retrieval Augmented Generation - Amazon Bedrock Knowledge Base", width=650) 
with tab7:
    # RAG - WWW
    st.subheader("Retrieval Augmented Generation (RAG) - Web Search")
    st.markdown("""
    This demo allows you to retrieve information from the WWW using the RAG technique with FMs. FMs only have knowledge acquired based on their training prior to their release date. When you ask a question or send an instruction regarding a **recent event**, your question/instruction is used for a web search (using DuckDuckGo) to **retrieve** relevant information from the web. The information retrieved is then used as context to **augment** a prompt to an FM to enable it **generate** an appropriate response.
    This demo solution uses:
    - Streamlit for the web interface
    - AWS SDK for python (Boto3) for API access to FMs via API calls to Amazon Bedrock
    - LangChain library for DuckDuckGoSearch
                
    """)
    st.image('img/rag_www.png', caption="Retrieval Augmented Generation - WWW", width=650)
   