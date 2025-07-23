from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlite3
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDUpZM4fz1A8Y3-0Rwqe59saKfxE9R0DUE")
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

# FastAPI app
app = FastAPI()

# Request schema
class QuestionRequest(BaseModel):
    question: str

# Route: POST /ask-question
@app.post("/ask-question")
async def ask_ai(request: QuestionRequest):
    user_question = request.question

    # STRICT Prompt to force Gemini to return only SQL
    prompt = f"""
You are an SQL assistant.

🛑 RULES:
- Return ONLY the SQL query.
- Do NOT include comments, explanations, markdown, or formatting.
- The query must be valid SQLite and based on the schema below.

📦 SCHEMA:

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
- eligibility (INTEGER)  -- 1 = eligible, 0 = not eligible
- message (TEXT)

Use item_id to join across tables if needed.

User question: {user_question}

SQL:
"""

    # Get SQL from Gemini
    try:
        response = chat.send_message(prompt)
        sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
    except Exception as e:
        return {"error": f"Gemini Error: {str(e)}"}

    # Execute SQL on the SQLite DB
    try:
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
    except Exception as e:
        return {
            "question": user_question,
            "sql": sql_query,
            "error": f"Database Error: {str(e)}"
        }

    return {
        "question": user_question,
        "sql": sql_query,
        "result": result
    }
