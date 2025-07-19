import streamlit as st
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Load environment variables
load_dotenv()

# Load modules
from utils.rag_chain_faiss import load_pdf_chunks, build_faiss_index, retrieve_context, ask_with_context
from utils.ghl_webhook import send_to_ghl

# Set Streamlit page config
st.set_page_config(page_title="AI Recruiting Assistant", layout="wide")

# Title
st.title("🏈 AI Recruiting Assistant")
st.markdown("Use this tool to ask recruiting questions and receive intelligent, personalized answers based on expert data.")

# Load and embed recruiting FAQ
st.info("Loading recruiting data...")
chunks = load_pdf_chunks("data/recruiting_faqs.pdf")
index, _ = build_faiss_index(chunks)
st.success("Ready for questions!")

# Ask the AI agent
with st.expander("🧠 Ask a Recruiting Question"):
    question = st.text_input("Type your question here:")

    if question:
        with st.spinner("Thinking..."):
            context = retrieve_context(index, question, chunks)
            answer = ask_with_context(question, " ".join(context))
            st.markdown("### 🤖 Answer")
            st.write(answer)

            # Send interaction to GHL
            send_to_ghl({
                "question": question,
                "answer": answer,
                "tag": "RAG_Response"
            })
