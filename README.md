# ecommerce_ai_agent
# 🧠 Ecommerce AI Assistant

This is a conversational AI assistant built using **FastAPI**, **Gemini 1.5 Flash (Google Generative AI)**, and **SQLite**, designed to help users query ecommerce-related data using natural language. It intelligently converts questions into SQL queries and fetches results from a local database.

## 💡 Features

- Conversational interface using **Gemini API**
- Converts natural language questions to SQL
- Executes SQL queries on an **ecommerce.db** SQLite database
- FastAPI web interface for interaction
- Optional: Streamlit terminal chat interface
- Bonus: Can be extended to visualize results (e.g., for total sales, CPC, RoAS)

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

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/RenukaAshok/ecommerce_ai_agent.git
cd ecommerce_ai_agent
