from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

def create_app():
    app = FastAPI(
        title="Quotecheck Code Challenge",
        version="1.0.0",
    )
    
    # Include the API routes
    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8080",
            "http://localhost:8000",
            "http://localhost:3000",
            "http://localhost:3001",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

# Create the FastAPI application instance
app = create_app()
