from pydantic import BaseModel, Field
from typing import List, Optional

class Dialogue(BaseModel):
    character: str
    text: str
    voice: str = "default"

class Character(BaseModel):
    name: str
    style: str = "3d_cinematic"
    asset: Optional[str] = None
    voice: str = "default"

class Scene(BaseModel):
    number: int
    background: str = ""
    characters: List[Character] = Field(default_factory=list)
    dialogue: List[Dialogue] = Field(default_factory=list)
    music: Optional[str] = None
    sfx: List[str] = Field(default_factory=list)
    duration: float = 6.0

class Project(BaseModel):
    title: str
    scenes: List[Scene]
