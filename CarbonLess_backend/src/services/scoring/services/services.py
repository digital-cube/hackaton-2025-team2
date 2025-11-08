import os
from fastapi import HTTPException
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from src.services.tenants.models.models import Users, Tenants

from src.services.scoring.models.models import UsersPoints, ActionTypeEnum
from src.services.scoring.schemas.schemas import TransportationFormSchema

load_dotenv()

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

async def submit_transportation_form(current_user: dict, form_data: TransportationFormSchema):

    user_id = current_user['user_id']

    user = await Users.get_or_none(id=user_id)

    if not user:
        HTTPException(status_code=404, detail="User not found")

    tenant = await Tenants.get_or_none(id=user.id_tenant)

    if not tenant:
        HTTPException(status_code=404, detail="Tenant not found")

    prompt = await build_transportation_prompt(
        user_id=user_id,
        mode_of_transportation=form_data.mode_of_transportation,
        tenant_address=tenant.address
    )

    system_prompt = "You are a precise environmental calculator. Always respond with valid JSON only, no additional text."

    points, co2_emission = await call_mistral_ai(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=1000
    )

    entry = await UsersPoints.create(
        action_type=ActionTypeEnum.TRANSPORTATION,
        points=points,
        user_id=user_id,
        co2_emission=co2_emission
    )

    # Update user's total points
    user = await Users.get(id=user_id)
    user.points = user.points + points
    await user.save()

    return {
        'message': 'Transportation form submitted successfully',
        'points_awarded': points,
        'co2_emission': co2_emission,
        'total_points': user.points
    }

async def build_transportation_prompt(user_id: str, mode_of_transportation: str, tenant_address) -> str:
    user = await Users.get(id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prompt = f"""
    You are an environmental impact calculator. Calculate CO2 emissions and award points using a FAIR DISTANCE-BASED SYSTEM.
    Goal: A person walking 500m and a person driving 50km should get similar (but not identical) points - walking should be slightly better.

    **User Information:**
    - User Address: {user.address}
    - Tenant Address: {tenant_address}
    - Current Trip Transportation Method: {mode_of_transportation}

    **Your Task:**
    1. Calculate the approximate distance between addresses in kilometers
    2. Calculate actual CO2 emissions for this trip
    3. Apply the DYNAMIC MULTIPLIER SYSTEM below

    **Transportation CO2 Emissions Reference:**
    - Walking: 0 kg CO2/km
    - Bicycle: 0.03 kg CO2/km
    - Train: 0.040 kg CO2/km
    - Electric vehicle: 0.047 kg CO2/km
    - Bus: 0.093 kg CO2/km
    - Carpool (3+ passengers): 0.057 kg CO2/km
    - Hybrid car: 0.100 kg CO2/km
    - Motorcycle: 0.103 kg CO2/km
    - Regular car: 0.170 kg CO2/km ← BASELINE (worst option)

    **NEW DYNAMIC SCORING SYSTEM:**

    **Step 1: Calculate Base Points**
    Base Points = (0.170 - actual_emission) × distance × 10
    - If using car: Base = 0 (it's the baseline)
    - actual_emission = CO2 per km for chosen method

    **Step 2: Calculate Distance-Based Multiplier**
    Each transport method has an EXPONENTIAL multiplier that grows with distance:

    - **Walking**: Multiplier = distance^1.3
      (Fastest growth - walking 20km is heroic)

    - **Bicycle**: Multiplier = distance^1.25
      (Very high growth - cycling far is a big commitment)

    - **Train**: Multiplier = distance^1.15
      (Good growth - efficient for longer distances)

    - **Electric vehicle**: Multiplier = distance^1.1
      (Moderate growth - cleaner than gas)

    - **Bus**: Multiplier = distance^1.1
      (Moderate growth - public transport)

    - **Carpool**: Multiplier = distance^1.05
      (Slight growth - better than solo car)

    - **Hybrid car**: Multiplier = distance^0.9
      (Slight decrease - not much better than regular car)

    - **Motorcycle**: Multiplier = distance^0.8
      (Decreasing - not eco-friendly)

    Intermediate Points = Base Points × Multiplier

    **Step 3: Apply Car Penalty/Reward**
    ONLY for regular car usage:
    - 0-3 km: -10 points per km (serious penalty - you should walk/bike!)
    - 3-8 km: -3 points per km (moderate penalty - still could bike/bus)
    - 8-20 km: +1 point total (acceptable distance)
    - 20-40 km: +2 points total (reasonable distance)
    - 40+ km: +3 points total (acceptable for very long distance)

    Final Points = Intermediate Points + Car Adjustment

    **Important Rules:**
    1. Car on short distances (0-8km) gets NEGATIVE points
    2. Car on medium-long distances (8km+) gets small POSITIVE points (1-3 range)
    3. Walking/cycling grows exponentially - 20km walking >> 2km walking
    4. All eco-friendly options benefit more from longer distances
    5. System is fair: effort and sacrifice are rewarded proportionally

    **Expected Results:**
    - Walking 0.5 km: ~4 points
    - Walking 20 km: ~800 points
    - Car 0.5 km: -5 points (bad choice)
    - Car 50 km: +3 points (acceptable)
    - Bicycle 5 km: ~70 points
    - Train 30 km: ~400 points

    **CRITICAL:** Respond with ONLY valid JSON, no additional text:
    {{"points": <integer>, "co2_emission": <float>}}

    **Calculation Examples:**

    Example 1: 0.5 km by walking
    - Base: (0.170 - 0) × 0.5 × 10 = 8.5
    - Multiplier: 0.5^1.3 = 0.435
    - Final: 8.5 × 0.435 = 3.7 ≈ 4 points
    Response: {{"points": 4, "co2_emission": 0.0}}

    Example 2: 20 km by walking
    - Base: (0.170 - 0) × 20 × 10 = 340
    - Multiplier: 20^1.3 = 50.4
    - Final: 340 × 50.4 / 20 ≈ 857 points
    (Note: divide by distance to normalize, or adjust formula as needed)
    Response: {{"points": 857, "co2_emission": 0.0}}

    Example 3: 0.5 km by car
    - Base: 0
    - Car penalty: -10 × 0.5 = -5 points
    - Final: -5 points
    Response: {{"points": -5, "co2_emission": 0.085}}

    Example 4: 50 km by car
    - Base: 0
    - Car reward: +3 points (40+ km range)
    - Final: +3 points
    Response: {{"points": 3, "co2_emission": 8.5}}

    Example 5: 5 km by bicycle
    - Base: (0.170 - 0.03) × 5 × 10 = 70
    - Multiplier: 5^1.25 = 8.95
    - Final: 70 × 8.95 / 5 ≈ 125 points
    Response: {{"points": 125, "co2_emission": 0.15}}

    Example 6: 30 km by train
    - Base: (0.170 - 0.040) × 30 × 10 = 390
    - Multiplier: 30^1.15 = 57.4
    - Final: 390 × 57.4 / 30 ≈ 746 points
    Response: {{"points": 746, "co2_emission": 1.2}}

    Note: Adjust the multiplier application as mathematically appropriate to achieve the target point ranges.
    """
    return prompt
