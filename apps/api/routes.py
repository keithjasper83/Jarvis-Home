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
    Devices List view (Section 10).
    """
    mock_devices = [
        {"id": "d1", "friendly_name": "Kitchen Sink Light", "host": "192.168.1.10", "room": "Kitchen", "device_type": "light", "health_state": "Online", "protocol": "http"},
        {"id": "d2", "friendly_name": "Living Room TV", "host": "192.168.1.11", "room": "Living Room", "device_type": "tv", "health_state": "Online", "protocol": "ssh"},
        {"id": "d3", "friendly_name": "Front Door Lock", "host": "192.168.1.12", "room": "Entry", "device_type": "switch", "health_state": "Offline", "protocol": "tapo"},
    ]
    context = {
        "request": request,
        "devices": mock_devices,
        "current_year": 2026
    }
    return templates.TemplateResponse(request=request, name="devices.html", context=context)
