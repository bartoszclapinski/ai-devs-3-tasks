from dataclasses import dataclass
from typing import Optional

@dataclass
class VerificationRequest:
    text: str
    msgID: str = "0"
    
@dataclass
class VerificationResponse:
    text: str
    msgID: str
    
@dataclass
class VerificationResult:
    success: bool
    flag: Optional[str] = None
    error: Optional[str] = None 