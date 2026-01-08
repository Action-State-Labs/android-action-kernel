from typing import Literal, Union, List
from pydantic import BaseModel, Field, field_validator

class TapAction(BaseModel):
    action: Literal["tap"] = "tap"
    coordinates: List[int] = Field(..., description="[x, y] coordinates to tap")
    reason: str = Field(..., description="Why this tap is needed")

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, v):
        if len(v) != 2:
            raise ValueError("coordinates must be [x, y]")
        if not all(isinstance(coord, int) and coord >= 0 for coord in v):
            raise ValueError("coordinates must be positive integers")
        return v

class TypeAction(BaseModel):
    action: Literal["type"] = "type"
    text: str = Field(..., description="Text to type")
    reason: str = Field(..., description="Why this text is needed")

class NavigationAction(BaseModel):
    action: Literal["home", "back"] = Field(..., description="Navigation action")
    reason: str = Field(..., description="Why this navigation is needed")

class ControlAction(BaseModel):
    action: Literal["wait", "done"] = Field(..., description="Control action")
    reason: str = Field(..., description="Why this action is needed")

# Union type for all possible actions
AndroidAction = Union[TapAction, TypeAction, NavigationAction, ControlAction]
