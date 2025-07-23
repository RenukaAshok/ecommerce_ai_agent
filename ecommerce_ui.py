import streamlit as st
import sqlite3
import google.generativeai as genai

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyDUpZM4fz1A8Y3-0Rwqe59saKfxE9R0DUE")
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

# ✅ Streamlit Page Config
st.set_page_config(page_title="Ecommerce AI Assistant")
st.title("🛒 Ecommerce AI Assistant")
st.write("Ask questions about your ecommerce sales and ad performance data!")

# ✅ Sample Question Buttons
st.markdown("### 🔍 Example Questions:")
example_questions = [
    "What is my total sales?",
    "Which product had the highest CPC?",
    "Calculate the RoAS",
    "How many units were sold in total?",
    "Which item had the most impressions?",
    "What is the average ad spend per item?",
    "Total sales for eligible products only"
]

selected_example = st.selectbox("Choose a sample question or ask your own below:", [""] + example_questions)

# ✅ User input
user_input = st.text_input("💬 Ask your question:", value=selected_example if selected_example else "")

if st.button("Ask AI") and user_input:
    with st.spinner("🤖 Thinking..."):

        # Strict prompt: only return raw SQL
        prompt = f"""
You are a strict SQL assistant. Convert the user's question into a valid **SQLite SQL query** using ONLY this schema:

Table: ad_sales
- date (TEXT)
- item_id (INTEGER)
- ad_sales (REAL)
- impressions (INTEGER)
- ad_spend (REAL)
- clicks (INTEGER)
- units_sold (INTEGER)

Table: total_sales
- date (TEXT)
- item_id (INTEGER)
- total_sales (REAL)
- total_units_ordered (INTEGER)

Table: eligibility
- eligibility_datetime_utc (TEXT)
- item_id (INTEGER)
- eligibility (INTEGER)
- message (TEXT)

⚠️ IMPORTANT:
- DO NOT explain anything.
- DO NOT return markdown like ```sql.
- Just return the SQL query as plain text.

User's Question: {user_input}
"""

        try:
            response = chat.send_message(prompt)
            sql_query = response.text.strip()
        except Exception as e:
            st.error(f"❌ Gemini Error: {str(e)}")
            st.stop()

        # Show the generated query
        st.markdown("### 🧠 Gemini SQL Output:")
        st.code(sql_query, language="sql")

        # Execute the query on SQLite
        try:
            conn = sqlite3.connect("ecommerce.db")
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            conn.close()

            st.markdown("### 📊 Query Result:")

            # Show simple number if single value
            if rows and len(rows[0]) == 1:
                st.metric("Result", f"{rows[0][0]:,.2f}")
            else:
                st.dataframe(rows)

        except Exception as e:
            st.error(f"❌ Database Error: {str(e)}")
