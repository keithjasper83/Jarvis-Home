from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

# Provide absolute resolution to packages/ui_shell/templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "packages" / "ui_shell" / "templates"

app = FastAPI(
    title="Jarvis Home",
    description="Local-first conversational automation platform",
    version="0.1.0"
)

# Shared Jinja2 template engine instance
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Register context processors if needed
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Renders the Dashboard / Home (Section 10).
    """
    # Later iterations will fetch DB context (Device count, health models, etc.)
    context = {
        "request": request,
        "health_status": "Online",
        "device_count": 0,
        "active_model": "Llama 3 8B (LM Studio)",
        "current_year": 2026
    }
    return templates.TemplateResponse(request=request, name="dashboard.html", context=context)

@app.get("/health")
async def health_check():
    """
    Basic JSON health check endpoint representing Section 32 foundation.
    """
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/devices", response_class=HTMLResponse)
async def devices_list(request: Request):
    """
    Placeholder for Devices List (Section 10).
    """
    context = {
        "request": request,
        "devices": []
    }
    # Currently reusing base but this would map to a devices_list.html
    return templates.TemplateResponse(request=request, name="base.html", context=context)
