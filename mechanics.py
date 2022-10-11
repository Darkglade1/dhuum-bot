

def from_json_data(json_data):
    mechanic = Mechanic(json_data["interval"], json_data["playersInvolved"], json_data["mechanicNames"],
                        json_data["warnTime"], json_data["startTime"])
    return mechanic


class Mechanic:

    def __init__(self, interval, players_involved, mechanic_names, warn_time=5000, start_time=0):
        self.interval = interval
        self.players_involved = players_involved
        self.mechanic_names = mechanic_names
        self.warn_time = warn_time
        self.start_time = start_time

    def printMechanics(self):
        print(self.interval)
        print(self.players_involved)
        print(self.mechanic_names)
        print(self.warn_time)
        print(self.start_time)
        return "I printed mechanics!"
