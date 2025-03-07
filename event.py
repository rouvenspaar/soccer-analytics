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
class PlayerWithHeight(Player):
    height: int


@dataclass
class Goalkeeper:
    id: int
    name: str


@dataclass
class Pass:
    accurate: bool
    angle: float
    height: Optional[float]
    length: float
    recipient: Optional[Player]
    end_location: Location


@dataclass
class Attack:
    withShot: bool
    withShotOnGoal: bool
    withGoal: bool
    flank: str
    xg: float


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
    attack: Optional[Attack]


@dataclass
class Shot:
    bodyPart: str
    isGoal: bool
    onTarget: bool
    goalZone: str
    xg: float
    postShotXg: float
    goalkeeperActionId: int
    goalkeeper: Goalkeeper


@dataclass
class GroundDuel:
    opponent: Player
    duel_type: str
    kept_possession: bool
    progressed_with_ball: bool
    stopped_progress: Optional[bool]
    recovered_possession: Optional[bool]
    take_on: bool
    side: Optional[str]
    related_duel_id: int


@dataclass
class AerialDual:
    opponent: PlayerWithHeight
    first_touch: bool
    height: int
    relatedDuelId: int


@dataclass
class Infraction:
    yellow_card: bool
    red_card: bool
    type: str
    opponent: Player


@dataclass
class Carry:
    progression: float
    end_location: Location


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
    shot: Optional[Shot] = field(default=None)
    ground_duel: Optional[GroundDuel] = field(default=None)
    aerial_duel: Optional[AerialDual] = field(default=None)
    infraction: Optional[Infraction] = field(default=None)
    carry: Optional[Carry] = field(default=None)
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
        location=Location(**data["location"]) if data.get("location") else None,
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

        shot=Shot(
            bodyPart=data["shot"].get("bodyPart", ""),
            isGoal=data["shot"].get("isGoal", False),
            onTarget=data["shot"].get("onTarget", False),
            goalZone=data["shot"].get("goalZone", ""),
            xg=data["shot"].get("xg", 0.0),
            postShotXg=data["shot"].get("postShotXg", 0.0),
            goalkeeperActionId=data["shot"].get("goalkeeperActionId", 0),
            goalkeeper=Goalkeeper(**data["shot"]["goalkeeper"]) if data["shot"].get("goalkeeper") else None
        ) if data.get("shot") else None,

        ground_duel=GroundDuel(
            opponent=Player(**data["groundDuel"]["opponent"]),
            duel_type=data["groundDuel"].get("duel_type", ""),
            kept_possession=data["groundDuel"].get("kept_possession", False),
            progressed_with_ball=data["groundDuel"].get("progressed_with_ball", False),
            stopped_progress=data["groundDuel"].get("stopped_progress"),
            recovered_possession=data["groundDuel"].get("recovered_possession"),
            take_on=data["groundDuel"].get("take_on", False),
            side=data["groundDuel"].get("side"),
            related_duel_id=data["groundDuel"].get("related_duel_id", 0)
        ) if data.get("groundDuel") else None,

        aerial_duel=AerialDual(
            opponent=PlayerWithHeight(**data["aerialDuel"]["opponent"]),
            first_touch=data["aerialDuel"].get("first_touch", False),
            height=data["aerialDuel"]["height"],
            relatedDuelId=data["aerialDuel"]["relatedDuelId"]
        ) if data.get("aerialDuel") else None,

        infraction=Infraction(
            yellow_card=data["infraction"].get("yellow_card", False),
            red_card=data["infraction"].get("red_card", False),
            type=data["infraction"].get("type", ""),
            opponent=Player(**data["infraction"]["opponent"]) if data["infraction"].get("opponent") else None
        ) if data.get("infraction") else None,

        carry=Carry(
            progression=data["carry"]["progression"],
            end_location=Location(**data["carry"]["endLocation"])
        ) if data.get("carry") else None,

        possession=Possession(
            id=data["possession"]["id"],
            duration=data["possession"]["duration"],
            types=data["possession"]["types"],
            events_number=data["possession"]["eventsNumber"],
            event_index=data["possession"]["eventIndex"],
            start_location=Location(**data["possession"]["startLocation"]),
            end_location=Location(**data["possession"]["endLocation"]),
            team=Team(**data["possession"]["team"]),
            attack=Attack(
                withShot=data["possession"]["attack"]["withShot"],
                withShotOnGoal=data["possession"]["attack"]["withShotOnGoal"],
                withGoal=data["possession"]["attack"]["withGoal"],
                flank=data["possession"]["attack"]["flank"],
                xg=data["possession"]["attack"]["xg"]
            ) if data["possession"].get("attack") else None
        ) if data.get("possession") else None
    )

def load_events_from_json(filename: str) -> list[Event]:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [parse_event(event) for event in data["events"]]
