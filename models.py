from typing import Optional

from pydantic import BaseModel


class EmergencyScenario(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_crisis_description: Optional[str] = None
