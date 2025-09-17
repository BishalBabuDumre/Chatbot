from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2
from pydantic import BaseModel
import os

# -------------------------------
# FastAPI setup
# -------------------------------
app = FastAPI()

# Mount static files (style.css, script.js) from docs/static/
app.mount("/static", StaticFiles(directory=os.path.join("docs", "static")), name="static")

# Setup Jinja2 templates (index.html in docs/)
templates = Jinja2Templates(directory="docs")

# -------------------------------
# PostgreSQL connection (AWS RDS)
# -------------------------------
conn = psycopg2.connect(
    host="chatbot-users.c9mci8a4irlr.us-west-1.rds.amazonaws.com",  # e.g. mydb.xxxxx.rds.amazonaws.com
    database="chatbot-users",
    user="bdumrePostgres",
    password=os.getenv("DB_PASSWORD"),
    port="5432"
)

# -------------------------------
# Request Models
# -------------------------------
class UserInfo(BaseModel):
    full_name: str
    address: str
    state: str
    zip_code: str

class ChatMessage(BaseModel):
    message: str

# -------------------------------
# Routes
# -------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main page with form + chatbox"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/save_user")
async def save_user(user: UserInfo):
    """Save user info to PostgreSQL"""
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (full_name, address, state, zip_code)
            VALUES (%s, %s, %s, %s)
            """,
            (user.full_name, user.address, user.state, user.zip_code),
        )
        conn.commit()
        cur.close()
        return {"message": "User saved successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/chat")
async def chat(msg: ChatMessage):
    """Simple chatbot logic"""
    user_message = msg.message.strip()

    # 🔹 Replace with real chatbot logic later
    if "hello" in user_message.lower():
        bot_response = "Hi there! How can I help you today?"
    else:
        bot_response = f"You said: {user_message}"

    return {"response": bot_response}


# -------------------------------
# Run the app (with uvicorn)
# -------------------------------
# Run using: uvicorn web_app:app --reload --host 0.0.0.0 --port 8000
