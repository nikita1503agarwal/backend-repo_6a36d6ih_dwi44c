"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (retain for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Marketing site schemas

class Lead(BaseModel):
    """
    Marketing leads from contact/booking forms
    Collection name: "lead"
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    service: Optional[str] = Field(None, description="Requested service")
    message: Optional[str] = Field(None, description="Message from user")
    schedule_iso: Optional[str] = Field(None, description="Preferred date/time in ISO 8601")
    source: Optional[str] = Field("website", description="Lead source")

class Post(BaseModel):
    """
    Blog posts
    Collection name: "post"
    """
    title: str
    slug: str
    description: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class CaseStudy(BaseModel):
    """
    Case studies / portfolio
    Collection name: "casestudy" (lowercase of class name)
    """
    title: str
    slug: str
    client: Optional[str] = None
    summary: Optional[str] = None
    results: Optional[str] = None
    industries: Optional[List[str]] = None

class Testimonial(BaseModel):
    """
    Client testimonials
    Collection name: "testimonial"
    """
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    quote: str
