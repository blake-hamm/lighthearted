import streamlit as st

from lighthearted.utils import stream_text

st.title("❤️️ Lighthearted ❤️️")
st.caption("A mental health app powered by AI.")

welcome_message = """
Welcome to lighthearted! This app is meant to improve mental health through positive affirmations, habits, goal setting and vision boards.
First, lighthearted needs to get to know you better in order to personalize your goals. We will walk through a few questions and build your profile.
First, why have you chosen to use this app today?
"""
questions = [
  "What are some of your most important values?",
  "What motivates you to wake up in the morning?",
  "What are some goals you have?",
]

# Setup chat state
if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role": "ai", "content": welcome_message}]
if "questions" not in st.session_state:
  st.session_state["questions"] = questions.copy()

for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
  st.session_state.messages.append({"role": "user", "content": prompt})
  st.chat_message("human").write(prompt)

  if st.session_state["questions"]:
    next_question = st.session_state["questions"].pop(0)
    st.session_state.messages.append({"role": "ai", "content": next_question})
    st.chat_message("ai").write(next_question)
