from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="AIzaSyDUpZM4fz1A8Y3-0Rwqe59saKfxE9R0DUE")
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

# Create FastAPI app
app = FastAPI()

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Your Ecommerce AI Assistant</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f8f8f8;
        }}
        h1 {{
            color: #2c3e50;
        }}
        form {{
            margin-top: 20px;
        }}
        input[type="text"] {{
            width: 600px;
            padding: 10px;
            font-size: 16px;
        }}
        input[type="submit"] {{
            padding: 10px 20px;
            font-size: 16px;
            background-color: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }}
        .output {{
            margin-top: 30px;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px #ccc;
        }}
        pre {{
            background: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>🧠 Your Ecommerce AI Assistant</h1>
    <form method="post">
        <label for="question">💬 Ask your question:</label><br><br>
        <input type="text" id="question" name="question" required>
        <input type="submit" value="Ask">
    </form>
    {output}
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def form_get():
    return html_template.format(output="")

@app.post("/", response_class=HTMLResponse)
async def form_post(question: str = Form(...)):
    prompt = f"""
You are a professional SQL assistant. The database has the following schema:

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
- eligibility (INTEGER) -- 1=eligible, 0=not eligible
- message (TEXT)

Generate a clean SQLite query using only these columns and table names for the following question:
\"\"\"{question}\"\"\"
Only give the SQL query.
    """

    try:
        response = chat.send_message(prompt)
        sql_query_raw = response.text.strip()

        # Clean the SQL from markdown/code blocks
        sql_query = sql_query_raw.replace("```sql", "").replace("```", "").strip()

        if not sql_query.lower().startswith("select"):
            raise ValueError("Gemini didn't return a valid SQL query.")

        # Execute SQL query
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()

        output = f"""
        <div class="output">
            <h3>📄 SQL Query:</h3>
            <pre>{sql_query}</pre>
            <h3>✅ Result:</h3>
            <pre>{result}</pre>
        </div>
        """

    except Exception as e:
        output = f"""
        <div class="output">
            <h3>❌ Error:</h3>
            <pre>{str(e)}</pre>
        </div>
        """

    return html_template.format(output=output)
