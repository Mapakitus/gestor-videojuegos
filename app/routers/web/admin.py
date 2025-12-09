
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Configura la carpeta de plantillas
templates = Jinja2Templates(directory="app/templates")

# Crea el router con el prefijo /admin
router = APIRouter(prefix="/admin", tags=["admin"])

# Endpoint para la página principal del panel de administración
@router.get("", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    """
    Renderiza la página del panel de administración.
    """
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "title": "Panel de Administración"}
    )