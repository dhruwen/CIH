import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# In-memory user store
users = {"jaya": "123"}  # This is just an example. Use a secure method for storing passwords in production.

# HTML and CSS templates
css = """
<style>
.chat-message {
    border-radius: 10px;
    padding: 10px;
    margin: 5px;
}
.user-message {
    background-color: #dcf8c6;
    text-align: right;
}
.bot-message {
    background-color: #ececec;
}
.card {
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    border-radius: 5px;
    text-align: center;
}
.card img {
    width: 100%;
    height: 200px; /* Ensuring all images have the same height */
    object-fit: cover; /* Covering the entire area without distortion */
    border-radius: 5px 5px 0 0;
}
.card-container {
    margin: 20px;
}
.card-title {
    padding: 10px 0;
}
.card-button {
    margin-top: 10px;
    width: 100%;
    display: block;
    text-align: center;
}
.centered-header {
    text-align: center;
}
</style>
"""

user_template = """
<div class="chat-message user-message">
    {{MSG}}
</div>
"""

bot_template = """
<div class="chat-message bot-message">
    {{MSG}}
</div>
"""

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def signup():
    st.header("Signup")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Signup"):
        if username in users:
            st.error("Username already exists")
        else:
            users[username] = password
            st.success("Signup successful. Please log in.")
            st.session_state.signup_page = False

def main():
    load_dotenv()
    st.set_page_config(page_title="COPBOT App", page_icon=":books:")

    if "page" not in st.session_state:
        st.session_state.page = "Main"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "signup_page" not in st.session_state:
        st.session_state.signup_page = False
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.write(css, unsafe_allow_html=True)

    if not st.session_state.logged_in:
        if st.session_state.signup_page:
            signup()
        else:
            login()
            if st.button("Go to Signup"):
                st.session_state.signup_page = True
                st.experimental_rerun()
    else:
        if st.session_state.page == "Main":
            st.markdown('<h1 class="centered-header">Welcome to Crime Investigation Helper</h1>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="card"><img src="https://cdn.getmidnight.com/bbe9047444895de971dcc65fe7f9504f/2020/09/AI-regulation-pic.png" alt="FIR Analytics"><div class="card-container"><h4 class="card-title">FIR Analytics</h4></div></div>', unsafe_allow_html=True)
                if st.button("Go to FIR Analytics Chatbot", key="fir_analytics"):
                    st.session_state.page = "Chatbot"
                    st.experimental_rerun()

            with col2:
                st.markdown('<div class="card"><img src="https://e3.365dm.com/23/08/1600x900/skynews-ai-artificial-intelligence_6246406.png?20230810134607" alt="Sketch Creation"><div class="card-container"><h4 class="card-title">Sketch Creation</h4></div></div>', unsafe_allow_html=True)
                if st.button("Go to Sketch Creation Chatbot", key="sketch_creation"):
                    st.session_state.page = "Chatbot"
                    st.experimental_rerun()

            with col3:
                st.markdown('<div class="card"><img src="https://img.pikbest.com/wp/202347/advanced-recognition-the-future-of-cyber-security-3d-scanning-for-facial-and-face-detection-systems_9757506.jpg!w700wp" alt="Face Detection"><div class="card-container"><h4 class="card-title">Face Detection</h4></div></div>', unsafe_allow_html=True)
                if st.button("Go to Face Detection Chatbot", key="face_detection"):
                    st.session_state.page = "Chatbot"
                    st.experimental_rerun()

        elif st.session_state.page == "Chatbot":
            st.header("Chat with COP Bot🤖")

            if st.button("Back to Main"):
                st.session_state.page = "Main"
                st.experimental_rerun()

            pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
            if st.button("Process"):
                with st.spinner("Processing"):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)

            user_question = st.text_input("Ask a question about your documents:")
            if user_question:
                handle_userinput(user_question)

            with st.sidebar:
                st.subheader("Chat History")
                for i, message in enumerate(st.session_state.chat_history):
                    if i % 2 == 0:
                        st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                    else:
                        st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

if __name__ == '__main__':
    main()

