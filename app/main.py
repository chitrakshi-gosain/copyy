"""
@purpose QuoteCheck Code Challenge
@author Chitrakshi Gosain
@date Last Edited - Sep 20, 2024
"""

from fastapi import FastAPI
from .routes import router

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    fast_api_app = FastAPI(
        title="Quotecheck Code Challenge",
        version="1.0.0",
    )

    # Include the API routes
    fast_api_app.include_router(router)

    return fast_api_app

# Create the FastAPI application instance
app = create_app()
