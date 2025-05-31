from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from generator import generate_code
from typing import Union
from models import User
from auth import pwd_context,get_current_user,create_access_token
from datetime import datetime,timezone,timedelta

#database import
from database import init_db,SessionLocal
#to use database in endpoint
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CodeGenerationRequest
from auth import add_to_blacklist,oauth2_scheme
#database initialization
init_db()

#to list past generations (db)
from typing import List

app = FastAPI(
    title = "CodeGen API",
    description="An API for generating code snippets",
    version = "1.0.1",
    openapi_tags=[
        {
            "name" : "Code Generation",
            "description" : "Endpoints for code generation"
        },
        {
            "name" : "System",
            "description" : "Health check and system status"
        }
    ]
)

# Allow Streamlit frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # or ["http://localhost:8501"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str = Field(...,example = "Reverse a string ",min_length=5,max_length=500)
    language: str = Field(...,example = "Python", enum = ["Python", "JavaScript", "C++", "Java", "Go"])

    class Config:
        schema_extra  = {
            "example" : {
                "prompt" : "Binary Search implementation",
                "language" : "Python"
            }  
        }

class GenerateSuccessResponse(BaseModel):
    code : str = Field(...,example = "def binary_search(arr, target):\n left,right=0,len(arr)-1",
                       description = "The generated code snippet")
    prompt : str = Field(..., example =  "Binary search implementation",
                         description = "The prompt was used to generate the code")
    language : str = Field(..., example = "Python",
                           description="Programming language of generated code")
    created_at : datetime = Field(..., example="2025-05-28T10:55:00",
                            description="Timestamp when the code was generated.")

class ErrorResponse(BaseModel):
    error : str = Field(..., example = "Invalid API key")
    details : Union[str, None] = Field(None, example="Authentication failed")


class UserCreate(BaseModel):
    username: str
    password: str

#database usage in endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#API routes
@app.get("/health", tags=["System"], summary="Service health check")
async def health_check():
    return {"status": "OK", "timestamp": datetime.now(timezone.utc)}

@app.post(
    "/generate",
    response_model=Union[GenerateSuccessResponse, ErrorResponse],
    tags=["Code Generation"],
    summary="Generate Code snippet",
    responses={
        status.HTTP_200_OK: {"model": GenerateSuccessResponse, "description": "Code generated successfully"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid Input"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse, "description": "LLM Service Unavailable"}
    }
)
async def generate(
    request: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    try:
        code = generate_code(request.prompt, request.language)
        db_obj = CodeGenerationRequest(
            prompt=request.prompt,
            language=request.language,
            generated_code=code,
            owner_id=current_user.id  # Link to the logged-in user
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return GenerateSuccessResponse(
            code=code,
            prompt=request.prompt,
            language=request.language,
            created_at=db_obj.created_at
        )
    except Exception as e:
        return ErrorResponse(error="Generation failed", details=str(e))
    
#for user auth
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Hash password and create user
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}

@app.post("/token")
def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    print(f"Login attempt for user: {form_data.username}")  # Debug
    if not user:
        print("User not found")  # Debug
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not pwd_context.verify(form_data.password, user.hashed_password):
        print("Password mismatch")  # Debug
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    print("Login successful")  # Debug
    access_token = create_access_token(data = {"sub" : user.username})
    return {"access_token" : access_token,"token_type" : "bearer"}

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    add_to_blacklist(token)
    return {"message": "Logged out successfully"}

#to get past generations
@app.get("/history", response_model=List[GenerateSuccessResponse])
def get_history(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    records = db.query(CodeGenerationRequest)\
               .filter(CodeGenerationRequest.owner_id == current_user.id)\
               .order_by(CodeGenerationRequest.created_at.desc())\
               .all()
    return [
        GenerateSuccessResponse(
            code=r.generated_code,
            prompt=r.prompt,
            language=r.language,
            created_at=r.created_at
        ) for r in records
    ]


