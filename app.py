import streamlit as st
import random

st.set_page_config(page_title="AI Snake Game", layout="centered")

st.title("🐍 AI Snake Game (Web Demo)")
st.write("This is a browser-based demo of the AI Snake Bot.")

if "score" not in st.session_state:
    st.session_state.score = 0

if st.button("▶️ AI Move"):
    move = random.choice(["Left", "Right", "Up", "Down"])
    st.session_state.score += random.randint(1, 10)

    st.success(f"AI moved: {move}")
    st.write(f"Current Score: **{st.session_state.score}**")

if st.button("🔄 Reset Game"):
    st.session_state.score = 0
    st.info("Game Reset!")

st.markdown("---")
st.write("👨‍💻 GitHub Repository:")
st.write("https://github.com/suranjan2006/AI_Snake_Bot")
