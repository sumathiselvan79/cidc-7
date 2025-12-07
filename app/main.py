from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import templates, forms

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PDF Template Service",
    description="Intelligent PDF form management with GraphDB integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(templates.router)
app.include_router(forms.router)

@app.get("/")
def read_root():
    return {
        "message": "PDF Template Service API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "templates": "/templates",
            "forms": "/forms"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
