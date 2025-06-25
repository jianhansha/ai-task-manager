import streamlit as st
from agents.task_SQL_agent import load_sql_agent
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

st.set_page_config(page_title="SQL Agent", layout="centered")

st.title("Henry: Your AI Agent Personal Asistant")

query = st.text_area("How can I help you? :")

if 'agent' not in st.session_state:
    st.session_state.agent = load_sql_agent()

if st.button("Run Query"):
    if query.strip():
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.run(query)
                st.success("✅ Done")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a question.")