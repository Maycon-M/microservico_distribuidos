from pydantic import BaseModel, Field, ConfigDict

class MedicineCreate(BaseModel):
    user_id: int
    name: str = Field(min_length=2, max_length=120)
    dose_amount: float = Field(gt=0)
    dose_unit: str = "mg"
    notes: str | None = None

class MedicineOut(BaseModel):
    id: int
    user_id: int
    name: str
    dose_amount: float
    dose_unit: str
    notes: str | None
    model_config = ConfigDict(from_attributes=True)
