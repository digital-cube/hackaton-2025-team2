import os
from fastapi import HTTPException
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from services.points.models.models import UsersPoints, ActionTypeEnum
from services.points.schemas.schemas import TransportationFormSchema

# Load environment variables
load_dotenv()

# Mistral AI Configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL")


async def call_mistral_ai(prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:

    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY not found in environment variables")

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": MISTRAL_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                MISTRAL_API_URL,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except HTTPException as e:
        raise e

async def submit_transportation_form(user_id: str, form_data: TransportationFormSchema):

    user = await User.get(id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_address = user.addres

    prompt = await build_transportation_prompt(user_address=user_address, mode_of_transportation=form_data.mode_of_transportation)

    points, co2_emission = await call_mistral_ai(prompt=prompt)

    entry = await UsersPoints.create(action_type=ActionTypeEnum.TRANSPORTATION, points=points, user_id=user_id)

    point_difference = user.points + points
    user.points = point_difference
    await user.save()

    return {
        'message': 'Transportation form submitted successfully',
        'points_awarded': points,
    }

async def build_transportation_prompt(user_address: str, mode_of_transportation: str, tenant_address) -> str:
    prompt = f"""
    User Address: {user_address}
    Tenant Address: {tenant_address}
    Mode of transportation: {mode_of_transportation}
    
    
    """
    return prompt
