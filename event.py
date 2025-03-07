from dataclasses import dataclass, field
from typing import List, Optional, Dict
import json


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
    location: Optional[Location]
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


def parse_event(data: Dict) -> Event:
    return Event(
        id=data["id"],
        match_id=data["matchId"],
        match_period=data["matchPeriod"],
        minute=data["minute"],
        second=data["second"],
        match_timestamp=data["matchTimestamp"],
        video_timestamp=data["videoTimestamp"],
        related_event_id=data.get("relatedEventId"),
        type=Type(**data["type"]),
        location=Location(**data["location"]) if data.get("location") else None,  # No default value, uses Optional
        team=Team(**data["team"]),
        opponent_team=Team(**data["opponentTeam"]),
        player=Player(**data["player"]),
        pass_=Pass(
            accurate=data["pass"]["accurate"],
            angle=data["pass"]["angle"],
            height=data["pass"].get("height"),
            length=data["pass"]["length"],
            recipient=Player(**data["pass"]["recipient"]) if data["pass"].get("recipient") else None,
            end_location=Location(**data["pass"]["endLocation"])
        ) if data.get("pass") else None,
        possession=Possession(
            id=data["possession"]["id"],
            duration=data["possession"]["duration"],
            types=data["possession"]["types"],
            events_number=data["possession"]["eventsNumber"],
            event_index=data["possession"]["eventIndex"],
            start_location=Location(**data["possession"]["startLocation"]),
            end_location=Location(**data["possession"]["endLocation"]),
            team=Team(**data["possession"]["team"]),
            attack=data["possession"].get("attack")
        ) if data.get("possession") else None
    )

def load_events_from_json(filename: str) -> list[Event]:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [parse_event(event) for event in data["events"]]
