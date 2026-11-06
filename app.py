import streamlit as st

from zero_trust_agent import run_secure_query

st.set_page_config(page_title="Enterprise Zero-Trust GraphRAG", layout="wide")
st.title("Enterprise Zero-Trust GraphRAG")

with st.sidebar:
    st.header("Security Clearance")
    clearance = st.selectbox(
        "Simulated Security Clearance",
        options=["EXECUTIVE_ONLY", "STANDARD_EMPLOYEE", "CONTRACTOR"],
    )

query = st.chat_input("Ask a question about the secured data...")

if query:
    with st.spinner("Verifying clearances and querying the graph..."):
        response = run_secure_query(query, clearance)

    if "ACCESS DENIED" in response:
        st.error(response)
    else:
        st.success(response)

# To run this dashboard, use: .venv/bin/streamlit run app.py
