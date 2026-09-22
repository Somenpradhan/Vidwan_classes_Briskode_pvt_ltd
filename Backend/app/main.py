import os
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes import (
    auth,
    courses,
    faculty,
    results,
    gallery,
    testimonials,
    contact,
    enquiries,
    vst,
    newsletter,
    admin,
    health
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("vidwan_api")

# Auto-create tables in dev environment (SQLite/PostgreSQL)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Vidwan Classes Production REST API Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
origins = settings.cors_origins
logger.info(f"Configuring CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploaded media directory
uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Mount API Routers under /api/v1
api_prefix = settings.API_V1_STR
app.include_router(auth.router, prefix=api_prefix)
app.include_router(courses.router, prefix=api_prefix)
app.include_router(faculty.router, prefix=api_prefix)
app.include_router(results.router, prefix=api_prefix)
app.include_router(gallery.router, prefix=api_prefix)
app.include_router(testimonials.router, prefix=api_prefix)
app.include_router(contact.router, prefix=api_prefix)
app.include_router(enquiries.router, prefix=api_prefix)
app.include_router(vst.router, prefix=api_prefix)
app.include_router(newsletter.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)
app.include_router(health.router, prefix=api_prefix)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An internal server error occurred. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )


@app.get("/")
def root():
    return {
        "message": "Welcome to Vidwan Classes REST API Service",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
