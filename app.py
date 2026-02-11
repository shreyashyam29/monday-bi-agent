import streamlit as st
import json
from monday import run_monday_query
from llm import call_llm


# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Monday AI Agent", layout="wide")
st.title("🧠 Monday.com AI Business Agent")

st.markdown("Ask business questions about your Monday boards.")


# ---------------------------------
# USER INPUT
# ---------------------------------
monday_token = st.text_input("Enter Monday API Token", type="password")
user_question = st.text_area("Ask your question")

submit = st.button("Ask")


# ---------------------------------
# LLM → GRAPHQL GENERATOR
# ---------------------------------
def generate_graphql_query(user_question):
    prompt = f"""
You are a monday.com GraphQL expert.

IMPORTANT RULES:
- Use EXACT field names.
- Use snake_case (items_page NOT itemsPage).
- Only use valid monday.com fields.
- Do NOT invent fields.

Valid structure example:

query {{
  boards(limit: 5) {{
    id
    name
    items_page(limit: 10) {{
      items {{
        id
        name
      }}
    }}
  }}
}}

User question:
\"\"\"{user_question}\"\"\"

Return ONLY a valid GraphQL query.
No explanation.
"""

    response = call_llm(prompt)

    # Clean possible extra formatting from LLM
    response = response.strip()
    if response.startswith("```"):
        response = response.split("```")[1]

    return response


# ---------------------------------
# LLM → BUSINESS ANALYSIS
# ---------------------------------
def analyze_data(user_question, data):
    prompt = f"""
You are a business intelligence analyst.

User question:
\"\"\"{user_question}\"\"\"

Data from Monday (JSON):
{json.dumps(data, indent=2)}

Instructions:
- Answer clearly
- Provide insights, not raw JSON
- Mention if data is incomplete
- Be concise and business-focused
"""

    return call_llm(prompt)


# ---------------------------------
# MAIN AGENT FLOW
# ---------------------------------
if submit:

    if not monday_token:
        st.error("Please enter your Monday API token.")
        st.stop()

    if not user_question.strip():
        st.error("Please enter a question.")
        st.stop()

    with st.spinner("AI Agent thinking..."):

        # Step 1: Generate GraphQL Query
        graphql_query = generate_graphql_query(user_question)

        st.subheader("Generated GraphQL Query")
        st.code(graphql_query, language="graphql")

        # Step 2: Fetch Data from Monday
        monday_response = run_monday_query(monday_token, graphql_query)

        if "errors" in monday_response:
            st.error("Monday API Error")
            st.json(monday_response)
            st.stop()

        st.subheader("Raw Data from Monday")
        st.json(monday_response)

        # Step 3: Business Intelligence Analysis
        insight = analyze_data(user_question, monday_response)

        st.subheader("AI Business Insight")
        st.write(insight)
