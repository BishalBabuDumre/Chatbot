from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2, os

app = FastAPI()

# Serve static files (CSS/JS)
app.mount("/static", StaticFiles(directory="docs/static"), name="static")
templates = Jinja2Templates(directory="docs")

# Database connection
def get_connection():
    return psycopg2.connect(
        host="chatbot-users.c9mci8a4irlr.us-west-1.rds.amazonaws.com",  # e.g. mydb.xxxxx.rds.amazonaws.com
        database="postgres",
        user="bdumrePostgres",
        password=os.getenv("DB_PASSWORD"),
        port="5432"
    )

# Home page
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Save user info
@app.post("/save_user")
async def save_user(
    full_name: str = Form(...),
    address: str = Form(...),
    state: str = Form(...),
    zip_code: str = Form(...)
):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (full_name, address, state, zip_code) VALUES (%s, %s, %s, %s)",
            (full_name, address, state, zip_code)
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)})
