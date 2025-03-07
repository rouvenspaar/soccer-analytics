from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Type:
    primary: str
    secondary: List[str]


@dataclass
class Location:
    x: int
    y: int


@dataclass
class Team:
    id: int
    name: str
    formation: str


@dataclass
class Player:
    id: int
    name: str
    position: str


@dataclass
class Pass:
    accurate: bool
    angle: float
    height: Optional[float]
    length: float
    recipient: Optional[Player]
    end_location: Location


@dataclass
class Possession:
    id: int
    duration: float
    types: List[str]
    events_number: int
    event_index: int
    start_location: Location
    end_location: Location
    team: Team
    attack: Optional[dict]


@dataclass
class Event:
    id: int
    match_id: int
    match_period: str
    minute: int
    second: int
    match_timestamp: str
    video_timestamp: float
    related_event_id: Optional[int]
    type: Type
    location: Location
    team: Team
    opponent_team: Team
    player: Player
    pass_: Optional[Pass] = field(default=None)
    shot: Optional[dict] = field(default=None)
    ground_duel: Optional[dict] = field(default=None)
    aerial_duel: Optional[dict] = field(default=None)
    infraction: Optional[dict] = field(default=None)
    carry: Optional[dict] = field(default=None)
    possession: Optional[Possession] = field(default=None)
