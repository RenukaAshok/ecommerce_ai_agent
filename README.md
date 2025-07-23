# ecommerce_ai_agent
# 🧠 Ecommerce AI Assistant

This is a conversational AI assistant built using **FastAPI**, **Gemini 1.5 Flash (Google Generative AI)**, and **SQLite**, designed to help users query ecommerce-related data using natural language. It intelligently converts questions into SQL queries and fetches results from a local database.

## 💡 Features

## 📂 Project Structure

- `db.py` → Converts CSV files into a SQLite database (`ecommerce.db`)
- `ask_with_gemini.py` → FastAPI-based chatbot using Gemini + SQL
- `terminal_chat.py` → Terminal interface for asking questions
- `ecommerce_ui.py` → Streamlit chatbot with better UI
- `ask_with_gemini.py`→ FastAPI web interface for asking questions
- `ecommerce.db` → Auto-generated SQLite database
- CSV files → Your input data files for ad_sales, total_sales, and eligibility

---

## 🗃️ Dataset Overview

This project uses an SQLite database (`ecommerce.db`) with three tables:

### 📦 Tables:

1. `ad_sales`
   - `date`
   - `item_id`
   - `ad_sales`
   - `impressions`
   - `ad_spend`
   - `clicks`
   - `units_sold`

2. `total_sales`
   - `date`
   - `item_id`
   - `total_sales`
   - `total_units_ordered`

3. `eligibility`
   - `eligibility_datetime_utc`
   - `item_id`
   - `eligibility` (1 = eligible, 0 = not eligible)
   - `message`

---

