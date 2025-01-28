import logging

import dspy
import streamlit as st

from lighthearted.dspy_utils import generate_follow_up_questions
from lighthearted.utils import stream_text


# Setup
logger = logging.getLogger(__name__)
lm = dspy.LM('vertex_ai/meta/llama-3.1-405b-instruct-maas')
dspy.configure(lm=lm)


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
    st.session_state["messages"] = [{"role": "ai", "content": welcome_message, "init": True}]
if "hardcoded_questions" not in st.session_state:
    st.session_state["hardcoded_questions"] = questions.copy()
if "follow_up_questions" not in st.session_state:
    st.session_state["follow_up_questions"] = []
if "welcome_streamed" not in st.session_state:
    st.session_state["welcome_streamed"] = False
  

for msg in st.session_state.messages:
    if not st.session_state["welcome_streamed"]:
        st.chat_message(msg["role"]).write(stream_text(msg["content"]))
        st.session_state["welcome_streamed"] = True
    else:
        st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    # Identify the last AI message
    last_ai_message = next(
        (msg for msg in reversed(st.session_state["messages"]) if msg["role"] == "ai"),
        None,
    )

    if last_ai_message and last_ai_message.get("init"):
        # Last question was hardcoded, generate follow-up questions
        new_questions = generate_follow_up_questions(
            init_question=last_ai_message["content"], human_answer=prompt
        )
        logger.info(f"Generated follow-up questions: {new_questions}")

        # Store follow-up questions and ask the first one
        st.session_state["follow_up_questions"] = new_questions.follow_up_question
        if st.session_state["follow_up_questions"]:
            next_question = st.session_state["follow_up_questions"].pop(0)
            st.session_state.messages.append({"role": "ai", "content": next_question})
            st.chat_message("ai").write(stream_text(next_question))

    elif st.session_state["follow_up_questions"]:
        # Last question was generated, ask the next follow-up question
        next_question = st.session_state["follow_up_questions"].pop(0)
        st.session_state.messages.append({"role": "ai", "content": next_question})
        st.chat_message("ai").write(stream_text(next_question))
    else:
        # No more follow-up questions, move to the next hardcoded question
        if st.session_state["hardcoded_questions"]:
            next_question = st.session_state["hardcoded_questions"].pop(0)
            st.session_state.messages.append({"role": "ai", "content": next_question, "init": True})
            st.chat_message("ai").write(stream_text(next_question))
