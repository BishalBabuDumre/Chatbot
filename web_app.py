from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2, os

from use_chatbot import NLPChatbot

app = FastAPI()

# Serve static + templates
app.mount("/static", StaticFiles(directory="docs/static"), name="static")
templates = Jinja2Templates(directory="docs")

# ---- Load chatbot once (not every request) ----
bot = NLPChatbot("chatbot_model.pkl")

def get_connection():
    return psycopg2.connect(
        host="chatbot-users.c9mci8a4irlr.us-west-1.rds.amazonaws.com",
        database="postgres",
        user="bdumrePostgres",
        password=os.getenv("DB_PASSWORD"),
        port="5432"
    )

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/save_user")
async def save_user(
    full_name: str = Form(...),
    address: str = Form(...),
    state: str = Form(...),
    zip_code: str = Form(...)
):
    try:
        print("📥 Received user info:", full_name, address, state, zip_code)  # DEBUG
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (full_name, address, state, zip_code) VALUES (%s, %s, %s, %s)",
            (full_name, address, state, zip_code)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("✅ User info inserted into DB")  # DEBUG
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        print("❌ Error saving user:", e)  # DEBUG
        return JSONResponse(content={"status": "error", "detail": str(e)})

# ---------------------------
# Chatbot endpoint with debug
# ---------------------------
@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        if not user_input:
            raise HTTPException(status_code=400, detail="Message is required")

        print(f"💬 User asked: {user_input}")  # DEBUG

        response = bot.respond(user_input)

        print(f"🤖 Bot replied: {response}")  # DEBUG

        return JSONResponse({"reply": response})
    except Exception as e:
        print("❌ Chat error:", e)  # DEBUG
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
