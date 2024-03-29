import requests

class Weekly:
    """
    This class just makes the data a bit more orderly.
    """

    def __init__(self, athlete_id, first_name, last_name, distance,
                 activity_count, best_distance, best_moving_time, total_time,
                 velocity):
        self.athlete_id = athlete_id
        self.first_name = first_name
        self.last_name = last_name
        self.distance = distance
        self.activity_count = activity_count
        self.best_distance = best_distance
        self.best_moving_time = best_moving_time
        self.total_time = total_time
        self.velocity = velocity

    @staticmethod
    def from_dict(data: dict):
        return Weekly(
            data["athlete_id"],
            data["athlete_firstname"],
            data["athlete_lastname"],
            round(data["distance"]/1000,3),
            data["num_activities"],
            data["best_activities_distance"],
            data["best_activities_moving_time"],
            data["elapsed_time"],
            data["velocity"],
        )
    
    def get_runner(self):
        return (self.athlete_id, self.distance)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.distance} km"

headers = {
    "Referer": "Referer: https://www.strava.com/clubs/623637/leaderboard",
    "Accept": "text/javascript, application/javascript, "
    "application/ecmascript, application/x-ecmascript",
    "Host": "www.strava.com",
    "X-Requested-With": "XMLHttpRequest",
    "cookie": "_strava4_session=vdl5r7bn1h8q2h04eju3mlh0l5c3hoh0; _sp_ses.047d=*; _sp_id.047d=be26d328-b795-4cbf-88b2-0a4b8eb96343.1614779385.6.1618094430.1617907316.0b5f4533-89e4-402e-a0c4-a17cb95dc7ce"
}


def get_data(club_id: int, week_offset: int):
    url = "https://www.strava.com/clubs/{}/leaderboard?week_offset={}".format(club_id, week_offset)
    
    r = requests.get(url, headers=headers)

    return [Weekly.from_dict(d).get_runner() for d in r.json()["data"]]