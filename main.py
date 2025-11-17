import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Lead, Post, CaseStudy, Testimonial

app = FastAPI(title="Marketing Agency API", description="Backend for marketing agency website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

# Lead capture endpoint
@app.post("/api/leads")
def create_lead(lead: Lead):
    try:
        lead_id = create_document("lead", lead)
        return {"status": "ok", "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Content endpoints
@app.get("/api/posts", response_model=List[Post])
def list_posts(limit: Optional[int] = None):
    try:
        docs = get_documents("post", {}, limit)
        # Convert ObjectId to str and filter fields according to model
        mapped = []
        for d in docs:
            mapped.append(Post(
                title=d.get("title", ""),
                slug=d.get("slug", ""),
                description=d.get("description"),
                content=d.get("content"),
                tags=d.get("tags")
            ))
        return mapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts/{slug}", response_model=Post)
def get_post(slug: str):
    try:
        docs = get_documents("post", {"slug": slug}, limit=1)
        if not docs:
            raise HTTPException(status_code=404, detail="Post not found")
        d = docs[0]
        return Post(
            title=d.get("title", ""),
            slug=d.get("slug", ""),
            description=d.get("description"),
            content=d.get("content"),
            tags=d.get("tags")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/case-studies", response_model=List[CaseStudy])
def list_case_studies(limit: Optional[int] = None):
    try:
        docs = get_documents("casestudy", {}, limit)
        mapped = []
        for d in docs:
            mapped.append(CaseStudy(
                title=d.get("title", ""),
                slug=d.get("slug", ""),
                client=d.get("client"),
                summary=d.get("summary"),
                results=d.get("results"),
                industries=d.get("industries")
            ))
        return mapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/case-studies/{slug}", response_model=CaseStudy)
def get_case_study(slug: str):
    try:
        docs = get_documents("casestudy", {"slug": slug}, limit=1)
        if not docs:
            raise HTTPException(status_code=404, detail="Case study not found")
        d = docs[0]
        return CaseStudy(
            title=d.get("title", ""),
            slug=d.get("slug", ""),
            client=d.get("client"),
            summary=d.get("summary"),
            results=d.get("results"),
            industries=d.get("industries")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials(limit: Optional[int] = None):
    try:
        docs = get_documents("testimonial", {}, limit)
        mapped = []
        for d in docs:
            mapped.append(Testimonial(
                name=d.get("name", ""),
                role=d.get("role"),
                company=d.get("company"),
                quote=d.get("quote", "")
            ))
        return mapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
