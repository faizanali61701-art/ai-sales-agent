import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

class LeadDetails(BaseModel):
    name: Optional[str] = Field(description="Name of the lead")
    email: Optional[str] = Field(description="Email address of the lead")
    phone: Optional[str] = Field(description="Phone number of the lead")
    preferred_time: Optional[str] = Field(description="Preferred appointment date or time")
    ai_reply: str = Field(description="Natural response to continue conversation or confirm booking")

@router.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        system_instruction = (
            "You are an AI Sales Agent. Your job is to collect contact details (Name, Email, Phone, Preferred Booking Time) "
            "from the user to schedule a consultation call. Be helpful and natural."
        )

        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=f"{system_instruction}\n\nUser: {request.message}",
            config={
                'response_mime_type': 'application/json',
                'response_schema': LeadDetails,
            }
        )
        
        return {
            "status": "success",
            "data": response.parsed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))