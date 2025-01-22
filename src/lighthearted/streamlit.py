import streamlit as st

st.title("❤️️ Lighthearted ❤️️")
st.caption("A mental health app powered by AI.")

with st.form(key='profile'):
  st.text_input(
    "What is your preferred name?",
    value="Blake",
    key="name"
  )
  st.text_input(
    "Why are you using this app?",
    value="Improve my mental health.",
    key="reason"
  )
  st.text_area(
    "What are some of your goals?",
    value="""- Become an independent freelancer
- Build a local community
- Spend more time outdoors""",
    key="goals"
  )
  st.form_submit_button()
