from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2, os
from datetime import datetime

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="docs/static"), name="static")
templates = Jinja2Templates(directory="docs")

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="bdumrePostgres",
        password=os.getenv("DB_PASSWORD"),
        host="chatbot-users.c9mci8a4irlr.us-west-1.rds.amazonaws.com",
        port="5432",
    )

@app.post("/submit_user")
async def submit_user(request: Request):
    data = await request.json()
    full_name = data.get("full_name")
    address = data.get("address")
    state = data.get("state")
    zip_code = data.get("zip_code")

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (full_name, address, state, zip_code, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, address, state, zip_code, datetime.utcnow()))
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse({"message": "User info saved successfully"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
