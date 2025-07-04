import streamlit as st
from streamlit_calendar import calendar
from backend import process_user_input
from agents.show_tasks_agent import ShowTasksAgent

calendar_options = {
        "initialView": "dayGridWeek",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek"
        }
    }

st.set_page_config(layout="wide")
st.title("AI Task Manager")

st.markdown("""
    <style>
    .stColumn {
        height: 70vh;
        overflow-y: auto;
        padding: 1rem;
    }
            
    .stColumn > * > :nth-child(2) {
        height: 50vh;
        overflow-y: auto;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([2, 3], gap="medium")

with left_col:
    st.markdown("### 💬 Chat with Assistant")

    scroll_area = st.container(border=True)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi there! I'm your task assistant. How can I help?"}
        ]

    with scroll_area.container():

        for msg in st.session_state.messages:
            with scroll_area.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "🧑"):
                st.markdown(msg["content"])

    user_input = st.chat_input("Speak to the agent...", key="user_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with scroll_area.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        with scroll_area.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                assistant_reply,output_title, output_data = process_user_input(user_input)
                st.markdown(assistant_reply)
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                st.session_state.output_title = output_title
                st.session_state.last_output = output_data

with right_col:
    st.subheader("📅 Calendar View")
    with st.container(border=True):
        st.markdown("_(Google Calendar integration coming soon...)_")
        calendar_component = calendar(
            events=[],
            options=calendar_options,
            key="unique_calendar_key"
        )
    st.divider()

    output_title = st.session_state.get("output_title")
    if not output_title:
        output_title = "Today's Tasks"

    title = "📋 " + output_title
    st.write(f"### {title}")

    if "last_output" in st.session_state and st.session_state.last_output is not None:
        output_data = st.session_state.last_output
        
    else:
        show_task_agent = ShowTasksAgent()
        output_data = show_task_agent._get_today_tasks()
    if len(output_data)>0:
        st.dataframe(output_data, use_container_width=True, hide_index=True)
    else:
        st.info("Ask me something like 'What are my tasks for today?' or 'Show me my work-related tasks'.")
