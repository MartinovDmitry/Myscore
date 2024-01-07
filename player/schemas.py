from pydantic import BaseModel


class SchPlayerCreate(BaseModel):
    first_name: str
    second_name: str
    age: int
    club_id: int
    matches: int
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    trophies_num: int
    rating: int


class SchPlayerResponse(SchPlayerCreate):
    pass
