"""
User Service

Example microservice with full observability instrumentation.
"""

import sys
sys.path.append('../../sdk')

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

from observability_sdk import (
    TracingMiddleware,
    MetricsMiddleware,
    setup_logging,
    setup_tracing,
    get_logger,
    get_metrics,
    metrics_endpoint
)

# Service configuration
SERVICE_NAME = "user-service"
SERVICE_PORT = int(os.getenv("PORT", 8001))
JAEGER_HOST = os.getenv("JAEGER_HOST", "localhost")

# Initialize observability
setup_logging(SERVICE_NAME, level="INFO", json_format=True)
setup_tracing(SERVICE_NAME, jaeger_host=JAEGER_HOST)

logger = get_logger(__name__)
metrics = get_metrics()

# Create FastAPI app
app = FastAPI(
    title="User Service",
    description="User management microservice with full observability",
    version="1.0.0"
)

# Add observability middleware
app.add_middleware(TracingMiddleware)
app.add_middleware(MetricsMiddleware)


# Models
class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


# In-memory database (for demo purposes)
users_db: List[User] = [
    User(id=1, username="john_doe", email="john@example.com", full_name="John Doe"),
    User(id=2, username="jane_smith", email="jane@example.com", full_name="Jane Smith"),
]


# Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"service": SERVICE_NAME, "status": "healthy"}


@app.get("/metrics")
async def metrics_route():
    """Prometheus metrics endpoint"""
    return metrics_endpoint()


@app.get("/users", response_model=List[User])
async def list_users():
    """List all users"""
    logger.info("Listing all users", extra={"user_count": len(users_db)})
    
    with metrics.time_operation("list_users"):
        metrics.record_operation("list_users", "success")
        return users_db


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get user by ID"""
    logger.info(f"Fetching user", extra={"user_id": user_id})
    
    with metrics.time_operation("get_user"):
        user = next((u for u in users_db if u.id == user_id), None)
        
        if user is None:
            logger.warning(f"User not found", extra={"user_id": user_id})
            metrics.record_operation("get_user", "not_found")
            raise HTTPException(status_code=404, detail="User not found")
        
        metrics.record_operation("get_user", "success")
        return user


@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user"""
    logger.info(f"Creating user", extra={"username": user.username})
    
    with metrics.time_operation("create_user"):
        # Check if username already exists
        if any(u.username == user.username for u in users_db):
            logger.warning(f"Username already exists", extra={"username": user.username})
            metrics.record_operation("create_user", "conflict")
            raise HTTPException(status_code=409, detail="Username already exists")
        
        # Create new user
        new_id = max(u.id for u in users_db) + 1 if users_db else 1
        new_user = User(id=new_id, **user.dict())
        users_db.append(new_user)
        
        logger.info(f"User created successfully", extra={"user_id": new_id})
        metrics.record_operation("create_user", "success")
        
        return new_user


@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """Delete a user"""
    logger.info(f"Deleting user", extra={"user_id": user_id})
    
    with metrics.time_operation("delete_user"):
        user_index = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
        
        if user_index is None:
            logger.warning(f"User not found for deletion", extra={"user_id": user_id})
            metrics.record_operation("delete_user", "not_found")
            raise HTTPException(status_code=404, detail="User not found")
        
        users_db.pop(user_index)
        logger.info(f"User deleted successfully", extra={"user_id": user_id})
        metrics.record_operation("delete_user", "success")


if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} on port {SERVICE_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
