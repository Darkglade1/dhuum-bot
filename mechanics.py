

def from_json_data(json_data, time_limit):
    mechanic = Mechanic(json_data["interval"], json_data["playersInvolved"], json_data["mechanicNames"],
                        json_data["warnTime"], json_data["startTime"], time_limit)
    return mechanic


class Mechanic:

    def __init__(self, interval, players_involved, mechanic_names, warn_time=5000, start_time=0, end_time=9999):
        self.interval = interval
        self.players_involved = players_involved
        self.mechanic_names = mechanic_names
        self.warn_time = warn_time
        self.start_time = start_time
        self.end_time = end_time

    def get_time_to_message_dict(self, player_names):
        time_to_message = {}
        i = 0
        time = self.start_time
        while time < self.end_time:
            time_to_message[time - self.warn_time] = self.get_message(i, player_names)
            i += 1
            time += self.interval
        return time_to_message

    def get_message(self, index, player_names):
        mechanic_name = self.mechanic_names[index % len(self.mechanic_names)]
        if self.players_involved:
            player_name = player_names[index % len(player_names)]
            result = "{player} on {mechanic}."
            return result.format(player=player_name, mechanic=mechanic_name)
        else:
            return mechanic_name


    def printMechanics(self):
        print(self.interval)
        print(self.players_involved)
        print(self.mechanic_names)
        print(self.warn_time)
        print(self.start_time)
        print(self.end_time)
        return "I printed mechanics!"
