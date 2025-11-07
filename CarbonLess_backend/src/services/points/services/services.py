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


async def extract_mistral_json_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and parse JSON response from Mistral AI.

    Args:
        response: The full response dictionary from Mistral AI

    Returns:
        Parsed JSON object with points and co2_emission
    """
    import json
    import re

    try:
        content = response["choices"][0]["message"]["content"]

        # Try to extract JSON from the response
        # Sometimes AI might add extra text, so we look for JSON pattern
        json_match = re.search(r'\{[^}]*"points"[^}]*"co2_emission"[^}]*\}', content)

        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)

        # If no match, try to parse the whole content as JSON
        return json.loads(content)

    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to extract JSON response from Mistral AI: {e}. Response: {content}")


async def submit_transportation_form(user_id: str, form_data: TransportationFormSchema, tenant_address: str):

    # Build the prompt with user information
    prompt = await build_transportation_prompt(
        user_id=user_id,
        mode_of_transportation=form_data.mode_of_transportation,
        tenant_address=tenant_address
    )

    # Call Mistral AI with specific system prompt for JSON response
    system_prompt = "You are a precise environmental calculator. Always respond with valid JSON only, no additional text."

    mistral_response = await call_mistral_ai(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.3,  # Lower temperature for more consistent JSON output
        max_tokens=500
    )

    # Extract JSON data from Mistral AI response
    calculation_result = await extract_mistral_json_response(mistral_response)

    points = calculation_result["points"]
    co2_emission = calculation_result["co2_emission"]

    # Create points record in database
    entry = await UsersPoints.create(
        action_type=ActionTypeEnum.TRANSPORTATION,
        points=points,
        user_id=user_id,
        co2_emission=co2_emission
    )

    # Update user's total points
    user = await User.get(id=user_id)
    user.points = user.points + points
    await user.save()

    return {
        'message': 'Transportation form submitted successfully',
        'points_awarded': points,
        'co2_emission': co2_emission,
        'total_points': user.points
    }

async def build_transportation_prompt(user_id: str, mode_of_transportation: str, tenant_address) -> str:
    user = await User.get(id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prompt = f"""
You are an environmental impact calculator. Based on the following information, calculate the CO2 emissions and award/deduct points for
this user's transportation choice. IMPORTANT: Apply distance-based harshness - reward greater sacrifices more generously.

**User Information:**
- User Address: {user.address}
- Tenant Address: {tenant_address}
- User's Primary Transportation Method: {user.mode_of_transportation}
- Current Trip Transportation Method: {mode_of_transportation}

**Your Task:**
1. Calculate the approximate distance between User Address and Tenant Address in kilometers
2. Estimate CO2 emissions (in kg) for this trip using the specified mode of transportation
3. Apply DISTANCE-AWARE SCORING with harshness multipliers based on distance and sacrifice level

**Transportation CO2 Emissions (based on Our World in Data & European Environment Agency 2024):**
1. Walking - 0 g CO2/km (cleanest option)
2. Bicycle - 0.016-0.05 kg CO2/km (minimal emissions from food energy)
3. Electric vehicle - 0.047 kg CO2/km (including electricity generation)
4. Train - 0.040 kg CO2/km
5. Carpool (shared car, 3+ passengers) - 0.057 kg CO2/km (car emissions divided by passengers)
6. Bus - 0.093 kg CO2/km
7. Motorcycle - 0.103 kg CO2/km
8. Regular car (petrol/diesel) - 0.170 kg CO2/km
9. Hybrid car - 0.100 kg CO2/km

**DISTANCE-AWARE POINT CALCULATION SYSTEM:**

**Base Points:**
- Calculate CO2 saved: (primary_method_emission - current_method_emission) × distance
- Base points = CO2_saved × 10

**Distance Harshness Multipliers (apply to eco-friendly choices):**
- 0-2 km: 1.0× (short distance, minimal sacrifice)
- 2-5 km: 1.3× (reasonable distance, moderate effort)
- 5-10 km: 1.8× (significant distance, notable sacrifice)
- 10-15 km: 2.5× (long distance, major commitment)
- 15+ km: 3.5× (extreme distance, exceptional dedication)

**Sacrifice Bonus (additional multipliers):**
- Walking/Bicycle on 10+ km trip: +100 bonus points (extraordinary effort)
- Walking/Bicycle on 5-10 km trip: +50 bonus points (significant effort)
- Switching from car to bike/walking: +20% extra
- Using carpool instead of solo car: +15% extra
- Using public transport (train/bus) on 15+ km: +30% extra

**Penalty System (for worse choices than primary method):**
- Deduct: (CO2_excess × distance × 5) points
- Apply distance penalty: worse choices on longer distances = harsher penalties
- Example: Using car when primary is bike on 10km trip = heavy penalty

**Practicality Consideration:**
- Walking 15+ km: Award maximum points but note this is impractical
- Cycling 20+ km: Award very high points for exceptional commitment
- Don't penalize reasonable car use on 30+ km trips if no alternatives exist

**Point Boundaries:**
- Minimum: -200 points (very harmful choices on long distances)
- Maximum: +800 points (exceptional eco-friendly sacrifices on long distances)

**IMPORTANT:** You must respond with ONLY a valid JSON object in this exact format, with no additional text:
{{"points": <integer>, "co2_emission": <float>}}

Example responses:
- Short trip (2km), bike instead of car: {{"points": 35, "co2_emission": 0.04}}
- Long trip (12km), bike instead of car: {{"points": 380, "co2_emission": 0.30}}
- Very long trip (20km), car instead of primary bike: {{"points": -150, "co2_emission": 3.40}}
    """
    return prompt
