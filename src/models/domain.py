from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    name: str = Field(..., description="INCI name of the ingredient")
    percentage: float = Field(..., description="Target percentage in formula")
    function: str = Field(..., description="Primary function (e.g., Emulsifier, Humectant)")
    phase: str = Field(..., description="Processing phase (A, B, C)")
    justification: str = Field(..., description="Scientific reason for inclusion")
    supplier: Optional[str] = Field(None, description="Preferred supplier if any")

class Formula(BaseModel):
    name: str
    description: str
    form: str = Field(..., description="Physical form (e.g., O/W Emulsion, Gel)")
    ingredients: List[Ingredient]
    total_percentage: float = Field(..., description="Should check to equal 100%")
    ph_target: Optional[str]
    viscosity_target: Optional[str]

class Evidence(BaseModel):
    source_url: str
    source_type: Literal["paper", "textbook", "supplier_doc", "web", "patent"]
    title: str
    key_finding: str
    relevance_score: float = Field(..., ge=0, le=1)
    confidence_score: float = Field(..., ge=0, le=1)
    citation: str

class RiskAssessment(BaseModel):
    risk_level: Literal["low", "medium", "high", "critical"]
    category: Literal["stability", "compatibility", "safety", "regulatory"]
    description: str
    mitigation_strategy: str

class ProductBrief(BaseModel):
    product_type: str
    target_audience: str
    key_benefits: List[str]
    texture_preference: str
    packaging_type: str
    claims: List[str]
    constraints: List[str] = Field(default_factory=list, description="e.g. 'No silicones', 'Vegan'")
