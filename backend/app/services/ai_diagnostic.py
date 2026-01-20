"""
AI Diagnostic Service

Analyzes repair requests using AI for diagnosis, severity, and price estimation.
"""
from typing import List
from app.models.request import Category, Severity
from app.schemas.request import AIAnalysisResponse, PriceRange


# Price ranges by category (min, max in cents)
CATEGORY_PRICES = {
    Category.PLUMBING: (8000, 25000),
    Category.ELECTRICAL: (10000, 30000),
    Category.LOCKSMITH: (6000, 15000),
    Category.HVAC: (15000, 50000),
    Category.APPLIANCES: (8000, 20000),
    Category.CARPENTRY: (10000, 25000),
    Category.GENERAL: (5000, 20000),
}

# Safety instructions by category
SAFETY_INSTRUCTIONS = {
    Category.PLUMBING: [
        "Chiudi immediatamente l'acqua se c'è una perdita",
        "Non usare apparecchi elettrici vicino all'acqua",
        "Metti degli asciugamani per limitare i danni",
    ],
    Category.ELECTRICAL: [
        "NON toccare fili scoperti o prese danneggiate",
        "Stacca l'interruttore generale se c'è odore di bruciato",
        "Non usare acqua per spegnere eventuali scintille",
        "Evacua se senti forte odore di bruciato",
    ],
    Category.LOCKSMITH: [
        "Resta in un luogo sicuro se sei fuori casa",
        "Non forzare la serratura, potresti danneggiarla",
    ],
    Category.HVAC: [
        "Spegni la caldaia se senti odore di gas",
        "Apri le finestre per ventilare",
        "NON accendere fiamme o interruttori se c'è odore di gas",
        "Esci di casa e chiama i Vigili del Fuoco se l'odore è forte",
    ],
}


async def analyze_request(
    request_id: str,
    category: Category,
    description: str,
    guided_answers: dict,
    media_urls: List[str],
) -> AIAnalysisResponse:
    """
    Analyze a repair request using AI.
    
    In production, this would:
    1. Send images to OpenAI Vision API
    2. Analyze description with NLP
    3. Cross-reference guided answers
    4. Return diagnosis with confidence
    """
    # Determine severity from guided answers
    severity = Severity.MEDIUM
    if guided_answers.get("sparks") or guided_answers.get("burning_smell"):
        severity = Severity.HIGH
    elif guided_answers.get("gas_smell"):
        severity = Severity.HIGH
    elif guided_answers.get("running_water") and category == Category.PLUMBING:
        severity = Severity.HIGH
    elif guided_answers.get("how_long", "").lower() in ["poco", "oggi", "hours"]:
        severity = Severity.MEDIUM
    else:
        severity = Severity.LOW
    
    # Get safety instructions
    safety = SAFETY_INSTRUCTIONS.get(category, ["Attendi il tecnico in sicurezza"])
    
    # Calculate price range
    base_min, base_max = CATEGORY_PRICES.get(category, (5000, 20000))
    if severity == Severity.HIGH:
        base_min = int(base_min * 1.3)
        base_max = int(base_max * 1.5)
    
    # Mock probable issue based on category
    issues = {
        Category.PLUMBING: "Possibile tubo rotto o perdita dal sifone",
        Category.ELECTRICAL: "Possibile cortocircuito o problema all'impianto",
        Category.LOCKSMITH: "Serratura bloccata o meccanismo danneggiato",
        Category.HVAC: "Problema alla caldaia o perdita nel circuito",
        Category.APPLIANCES: "Guasto all'elettrodomestico",
        Category.CARPENTRY: "Danneggiamento strutturale",
        Category.GENERAL: "Riparazione generica necessaria",
    }
    
    return AIAnalysisResponse(
        severity=severity,
        confidence=75 + (10 if media_urls else 0),
        probable_issue=issues.get(category, "Da valutare"),
        safety_instructions=safety,
        estimated_duration_hours=2.0 if severity == Severity.HIGH else 1.5,
        price_range=PriceRange(min_price=base_min, max_price=base_max),
    )
