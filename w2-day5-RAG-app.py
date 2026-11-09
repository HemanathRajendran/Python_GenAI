import streamlit as st

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import tempfile
import os


st.set_page_config(page_title="PDF RAG Chatbot")

st.title("📄 PDF RAG Chatbot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    st.success(f"{len(chunks)} chunks created")

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Vector Store
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    # LLM
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4.1-mini",
        temperature=0
    )

    question = st.text_input(
        "Ask a question about the PDF"
    )

    if question:

        with st.spinner("Searching..."):

            docs = retriever.invoke(question)

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

            prompt = ChatPromptTemplate.from_template(
                """
                Answer the question only from the context.

                Context:
                {context}

                Question:
                {question}

                If answer not found,
                say:
                'I could not find that in the PDF.'
                """
            )

            chain = (
                prompt
                | llm
                | StrOutputParser()
            )

            answer = chain.invoke(
                {
                    "context": context,
                    "question": question
                }
            )

            st.subheader("Answer")
            st.write(answer)

            with st.expander("Retrieved Chunks"):

                for i, doc in enumerate(docs, start=1):
                    st.write(f"### Chunk {i}")
                    st.write(doc.page_content)

    # Cleanup
    try:
        os.remove(pdf_path)
    except:
        pass
