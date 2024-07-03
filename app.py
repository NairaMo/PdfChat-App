import streamlit as st
from src.utils.env_loader import load_env_variables
from src.utils.streamlit_helper import add_vertical_space
from src.pdf.pdf_processor import PDFProcessor
from src.embeddings.openai_embeddings import OpenAIEmbeddingsManager
from src.chat.chat_service import ChatService
from src.chat.vector_store import VectorStore

# Load environment variables from .env file
load_env_variables()

def main():
    st.header("Chat with PDF 💬")

    # Sidebar information
    with st.sidebar:
        st.title('Pdf-Chat App')
        st.markdown('''
        ## About
        This app is an LLM-powered chatbot built using:
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        - [OpenAI](https://platform.openai.com/docs/models) LLM model
        ''')
        add_vertical_space(5)
        st.write('Made by Nour Maged & Naira Mohammed')

    # Uploading PDF file 
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    if pdf is not None:
        try:
            pdf_processor = PDFProcessor(pdf)
            text_chunks = pdf_processor.process_pdf()

            embeddings_manager = OpenAIEmbeddingsManager()
            vector_store = embeddings_manager.create_vector_store(text_chunks)

            st.write('Embeddings Computation Completed.')

            # Accept user's questions/query
            query = st.text_input('Ask questions about your PDF:')
            if query:
                chat_service = ChatService(vector_store)
                response = chat_service.answer_query(query)
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if _name_ == '_main_':
    main()
