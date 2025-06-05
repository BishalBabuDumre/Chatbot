from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from use_chatbot import NLPChatbot  # import your existing function
import os

app = FastAPI()

# Mount static files (for CSS/JS)
app.mount("/static", StaticFiles(directory="docs/static"), name="static")

# Templates for HTML responses
templates = Jinja2Templates(directory="docs")

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """Handle chat messages"""
    try:
        data = await request.json()
        user_input = data.get("message")
        if not user_input:
            raise HTTPException(status_code=400, detail="Message is required")
        
        response = NLPChatbot().respond(user_input)
        return JSONResponse({"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
