import os
import json
from pydantic import BaseModel, Field
from typing import List, Literal
from google import genai
from google.genai import types

class ClauseAnalysis(BaseModel):
    clause_type: str = Field(description="The type of clause found (e.g., Deposit, Notice Period, Lock-in, Rent Increase, Maintenance, Painting Charges, Other).")
    clause_text: str = Field(description="The exact text or a close summary of the clause from the agreement.")
    risk_label: Literal["High", "Medium", "Low"] = Field(description="The risk level for the tenant.")
    explanation: str = Field(description="A plain-English explanation of why this clause is risky or what it means for the tenant.")

class AgreementAnalysis(BaseModel):
    overall_risk_score: Literal["High", "Medium", "Low"] = Field(description="The overall risk assessment of the rental agreement.")
    clauses: List[ClauseAnalysis] = Field(description="List of clauses analyzed from the agreement.")
    summary: str = Field(description="A brief overall summary of the agreement's terms.")

def analyze_agreement(text: str, api_key: str = None) -> AgreementAnalysis:
    """Analyzes the given rental agreement text using the Gemini API."""
    
    # Initialize the client with the provided API key (or let it fall back to environment)
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        client = genai.Client()
    
    prompt = """
    You are an expert real estate lawyer and tenant rights advocate. 
    Your task is to analyze the following rental agreement text and identify clauses that might be risky for the tenant.
    
    Specifically, look for clauses related to:
    - Security Deposit (e.g., unreasonable amounts, unfair deduction terms)
    - Notice Period (e.g., excessively long notice periods)
    - Rent Increase (e.g., frequent or uncapped increases)
    - Lock-in Period (e.g., long lock-in periods without exit clauses)
    - Painting Charges / Maintenance (e.g., tenant paying for routine painting or structural maintenance)
    
    Assign a risk label (High, Medium, Low) to each identified clause and provide a plain-English explanation of why it is flagged.
    Also, provide an overall risk score and a brief summary of the agreement.
    
    Agreement Text:
    {agreement_text}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt.format(agreement_text=text),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AgreementAnalysis,
            temperature=0.2,
        ),
    )
    
    # The response is a JSON string matching the schema. We parse it back into the Pydantic model.
    data = json.loads(response.text)
    return AgreementAnalysis(**data)
