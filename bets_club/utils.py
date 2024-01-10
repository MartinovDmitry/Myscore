from bets_club.schemas import SchStandingsResponse


class Schedule:
    @staticmethod
    def points_definition(record: str):
        lst = [int(i) for i in record.split('-')]
        points = lst[0] * 3 + lst[1] * 1
        return points

    @staticmethod
    def total_matches_definition(record: str):
        total_matches = sum([int(i) for i in record.split('-')])
        return total_matches

    @classmethod
    def update_schedule(cls, schema: SchStandingsResponse):
        schema.points = cls.points_definition(schema.record)
        schema.total_matches = cls.total_matches_definition(schema.record)
        return schema
