import sqlite3
import google.generativeai as genai

# ✅ Configure Gemini
genai.configure(api_key="AIzaSyDUpZM4fz1A8Y3-0Rwqe59saKfxE9R0DUE")
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

print("🧠 Ecommerce AI Assistant (Terminal Mode)")
print("Type 'exit' to quit.\n")

while True:
    user_question = input("💬 Ask your question: ")
    if user_question.lower() == "exit":
        break

    prompt = f"""
You are a SQL assistant. Given the database schema:

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
- eligibility (INTEGER) -- 1 = eligible, 0 = not eligible
- message (TEXT)

Use ONLY these columns. Convert this question into SQL:
\"\"\"{user_question}\"\"\"
Only return the SQL query.
"""

    try:
        response = chat.send_message(prompt)

        # ✅ Clean up SQL from Gemini's markdown
        sql = response.text.strip().replace("```sql", "").replace("```", "").strip()

        print("\n📄 SQL Query:")
        print(sql)

        # Run the SQL
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()

        print("✅ Result:")
        print(result)
        print("\n" + "-" * 50 + "\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")
