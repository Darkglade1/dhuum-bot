
def from_json_data(json_data, time_limit):
    mechanic = Mechanic(json_data["interval"], json_data["playersInvolved"], json_data["mechanicNames"],
                        json_data["warnTime"], json_data["startTime"], time_limit)
    if "playerList" in json_data:
        mechanic.player_list = json_data["playerList"]
    if "overrideFirstMechanicAssignment" in json_data:
        mechanic.override_first_mechanics_list = json_data["overrideFirstMechanicAssignment"]
    return mechanic


class Mechanic:
    def __init__(self, interval, players_involved, mechanic_names, warn_time=5, start_time=0, end_time=9999):
        self.interval = interval
        self.players_involved = players_involved
        self.mechanic_names = mechanic_names
        self.warn_time = warn_time
        self.start_time = start_time
        self.end_time = end_time
        self.player_list = None
        self.override_first_mechanics_list = None

    def get_time_to_message_list(self, player_names):
        time_to_message_list = []
        i = 0
        time = self.start_time
        while time < self.end_time:
            mechanic = (time - self.warn_time, self.get_message(i, player_names))
            time_to_message_list.append(mechanic)
            i += 1
            time += self.interval
        return time_to_message_list

    def get_message(self, index, player_names):
        mechanic_name = self.mechanic_names[index % len(self.mechanic_names)]
        if self.players_involved:
            if len(player_names) > 0:
                list_to_use = player_names
            else:
                list_to_use = self.player_list
            player_name = list_to_use[index % len(list_to_use)]
            if self.override_first_mechanics_list and len(self.override_first_mechanics_list) > 0:
                if mechanic_name in self.override_first_mechanics_list:
                    player_name = self.override_first_mechanics_list[mechanic_name]
                    del self.override_first_mechanics_list[mechanic_name]
            player_name = player_name.lower()
            player_name = player_name.strip()
            result = "{player} on {mechanic}"
            return result.format(player=player_name, mechanic=mechanic_name)
        else:
            return mechanic_name
