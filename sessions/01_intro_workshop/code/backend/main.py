from github import Github, Auth
from fastapi import FastAPI, HTTPException, Header
import os
from pydantic import BaseModel
import requests
from packaging import version
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from routes import api_routes

# Create FastAPI app
app = FastAPI()

# Register API routes
app.include_router(api_routes.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL, e.g., "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)







