"""
@author Chitrakshi Gosain
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

def create_app() -> FastAPI:
    """_summary_

    Returns:
        FastAPI: _description_
    """
    fast_api_app = FastAPI(
        title="Quotecheck Code Challenge",
        version="1.0.0",
    )

    # Include the API routes
    fast_api_app.include_router(router)

    fast_api_app.add_middleware(
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

    return fast_api_app

# Create the FastAPI application instance
app = create_app()
