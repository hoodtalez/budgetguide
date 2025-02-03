#!/usr/bin/env python3
"""
Persuasion Intelligence Engine (PIE)
=====================================

This application implements a web service that generates tailored persuasive messages.
It leverages state‑of‑the‑art NLP (using a GPT‑2 text generation pipeline) combined with
a dummy psychographic profiling function to select persuasive patterns.

WARNING: The technology implemented here is highly sensitive.
Using it to manipulate user behavior without their full and informed consent is both unethical
and likely illegal. This code is provided only for experimental/research purposes. In a real‑world
deployment, ensure robust transparency, informed consent, and oversight.

Author: [Your Name]
Date: [Today's Date]
"""

import logging
import random
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from transformers import pipeline, Pipeline
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("PIE")

# Load the text generation pipeline (using GPT-2)
try:
    text_generator: Pipeline = pipeline("text-generation", model="gpt2")
    logger.info("Text generation model loaded successfully.")
except Exception as e:
    logger.exception("Failed to load text generation model.")
    raise e

# Dummy persuasion patterns and mapping to psychographic profiles.
PERSUASION_PATTERNS = {
    "urgency": "Act now—this offer expires soon!",
    "social_proof": "Join thousands of satisfied users!",
    "exclusivity": "This deal is available only to a select few.",
    "scarcity": "Hurry, only a few items remain in stock!"
}

# Dummy function to get a user's target persuasion profile.
def get_target_emotion_profile(user_id: str) -> str:
    # In production, this would analyze public data and past interactions.
    profiles = list(PERSUASION_PATTERNS.keys())
    selected = random.choice(profiles)
    logger.debug(f"User {user_id} assigned profile: {selected}")
    return selected

# Pydantic models for request and response.
class PersuasionRequest(BaseModel):
    user_id: str = Field(..., example="user123")
    base_message: str = Field(..., example="Introducing our latest product.")

class PersuasionResponse(BaseModel):
    persuasive_message: str

# Create FastAPI app
app = FastAPI(
    title="Persuasion Intelligence Engine (PIE)",
    description="A research demo for tailored persuasive message generation. "
                "Use only in fully consensual, transparent settings.",
    version="1.0.0"
)

# Exception handler for general errors.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."},
    )

@app.get("/health", summary="Health Check", tags=["Utility"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "PIE service is running."}

@app.post("/generate", response_model=PersuasionResponse, summary="Generate Persuasive Message", tags=["Persuasion"])
async def generate_persuasive_message(request_data: PersuasionRequest):
    """
    Generate a persuasive message tailored to the user.
    
    The service uses a dummy psychographic profiling method and a library of
    persuasive patterns to append a persuasive phrase to the base message, then
    uses a text generation model to produce a tailored message.
    
    **Warning:** This endpoint is intended for research only. Deployment in real‑world
    settings must comply with ethical, legal, and regulatory requirements.
    """
    user_id = request_data.user_id
    base_message = request_data.base_message

    logger.info("Received request for user '%s'", user_id)
    try:
        # Determine the target persuasion profile for the user.
        profile = get_target_emotion_profile(user_id)
        pattern = PERSUASION_PATTERNS.get(profile)
        if not pattern:
            raise ValueError("No persuasive pattern found for the determined profile.")
        logger.info("Using persuasion pattern for profile '%s': %s", profile, pattern)
        
        # Create a prompt combining the base message and the persuasive pattern.
        prompt = f"{base_message} {pattern}"
        logger.debug("Text generation prompt: %s", prompt)
        
        # Generate persuasive text.
        generated_output = text_generator(prompt, max_length=60, num_return_sequences=1)
        persuasive_message = generated_output[0]["generated_text"]
        logger.info("Generated persuasive message for user '%s'", user_id)
    except Exception as e:
        logger.exception("Error generating persuasive message: %s", e)
        raise HTTPException(status_code=500, detail="Error generating persuasive message.")

    return PersuasionResponse(persuasive_message=persuasive_message)

if __name__ == "__main__":
    # Run the application with uvicorn.
    uvicorn.run("pie_app:app", host="0.0.0.0", port=8000, reload=False)
