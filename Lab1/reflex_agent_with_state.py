from Enums import States, Location, Action, LocationState

type LocationMap = dict[Location, States]
locations = [Location.A, Location.B, Location.C, Location.D]

class EnvironmentClass:
    def __init__(self, current_location: Location, states: LocationMap):
        self.current_location = current_location
        self.states = states


base_environment = EnvironmentClass(
    current_location=Location.A,
    states={
        Location.A: States.DIRTY,
        Location.B: States.DIRTY,
        Location.C: States.DIRTY,
        Location.D: States.DIRTY
    }
)


class StatefulReflexAgent:
    def __init__(self):
        self.model: LocationMap = {
            Location.A: States.UNKNOWN,
            Location.B: States.UNKNOWN,
            Location.C: States.UNKNOWN,
            Location.D: States.UNKNOWN,
        }

        self.state: LocationState = (Location.UNKNOWN, States.UNKNOWN)
        self.last_action: Action = Action.NO_OP

    def match_rule(self) -> Action:
        percept = self.state
        if percept[1] == States.DIRTY:
            return Action.SUCK
        if self.model[Location.A] == self.model[Location.B] == self.model[Location.C] == self.model[Location.D] == States.CLEAN:
            return Action.NO_OP
        if percept[0] == Location.A:
            return Action.RIGHT
        if percept[0] == Location.B:
            if self.model[Location.A] == States.UNKNOWN:
                return Action.LEFT
            else:
                return Action.RIGHT
        if percept[0] == Location.C:
            if self.model[Location.B] == States.UNKNOWN:
                return Action.LEFT
            else:
                return Action.RIGHT
        if percept[0] == Location.D:
            return Action.LEFT
        return Action.NO_OP

    def update_state(self, percept: LocationState) -> None:
        location, status = percept
        self.model[location] = status

    def sensors(self, environment: EnvironmentClass) -> tuple[Location, States]:
        location = environment.current_location
        return location, environment.states[location]

    def actuators(self, requested_action: Action, environment: EnvironmentClass) -> None:
        location = environment.current_location

        if requested_action not in location.allowed_moves():
            return

        if requested_action == Action.SUCK:
            environment.states[location] = States.CLEAN
        elif requested_action == Action.RIGHT:
            idx = locations.index(location)
            environment.current_location = locations[idx + 1]
        elif requested_action == Action.LEFT:
            idx = locations.index(location)
            environment.current_location = locations[idx - 1]

    def act(self, environment: EnvironmentClass) -> Action:
        percept = self.sensors(environment)
        self.state = percept
        self.update_state(percept)
        action = self.match_rule()
        self.actuators(action, environment)
        return action


def run(n):
    loc_w = 10
    stat_w = 8
    act_w = 7
    icon = "-> "

    print(f"{'Current':{loc_w + stat_w + act_w}s}{icon}{'New':8s}")
    print(f"{'location':{loc_w}s}{'status':{stat_w}s}{'action':{act_w}s}{icon}{'location':{loc_w}s}{'status':{stat_w}s}")

    agent = StatefulReflexAgent()
    for i in range(1, n):
        (location, status) = agent.sensors(base_environment)
        print(f"{location.name:{loc_w}s}{status.name:{stat_w}s}", end='')
        action = agent.act(base_environment)
        (location, status) = agent.sensors(base_environment)
        print(f"{action.name:{act_w}s}{icon}{location.name:{loc_w}s}{status.name:{stat_w}s}")


if __name__ == '__main__':
    run(20)
