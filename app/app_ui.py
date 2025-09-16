import streamlit as st
from app.crew_sales import run_sales_clone  # Changed import to relative

st.title("Sales Leader & Technical Advisor Chat")
st.write("Ask about BPO positioning, consulting coaching, accounting strategies, or technical objections.")

if "history" not in st.session_state:
    st.session_state["history"] = []

question = st.text_input("Enter your sales question:")

if st.button("Ask") and question:
    answer = run_sales_clone(question)
    st.session_state["history"].append((question, answer))

for q, a in reversed(st.session_state["history"]):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**AI:** {a}")