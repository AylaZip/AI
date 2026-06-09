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


class Agent:
    def __init__(self, environment: EnvironmentClass):
        self.environment = environment

    def sensor(self) -> LocationState:
        location = self.environment.current_location
        return location, self.environment.states[location] # returns a tuple

    def actuator(self, action: Action) -> None:
        location = self.environment.current_location
        if action == Action.SUCK:
            self.environment.states[location] = States.CLEAN
        elif action == Action.RIGHT and action in location.allowed_moves():
            idx = locations.index(location)
            self.environment.current_location = locations[idx + 1]
        elif action == Action.LEFT and action in location.allowed_moves():
            idx = locations.index(location)
            self.environment.current_location = locations[idx - 1]

    def evaluate(self) -> Action:
        """:return: The action that the agent has chosen to take. For printing purposes"""
        state = self.sensor()

        action = self.choose_action(state)

        self.actuator(action)

        return action

    @staticmethod
    def choose_action(state: LocationState) -> Action:
        if state[1] == States.DIRTY:
            return Action.SUCK
        if state[0] == Location.A:
            return Action.RIGHT
        if state[0] == Location.B:
            return Action.RIGHT
        if state[0] == Location.C:
            return Action.RIGHT
        if state[0] == Location.D:
            return Action.LEFT
        return Action.NO_OP


def run(n: int) -> None:
    loc_w = 10
    stat_w = 8
    act_w = 7
    icon = "-> "

    print(f"{'Current':{loc_w + stat_w + act_w}s}{icon}{'New':8s}")
    print(f"{'location':{loc_w}s}{'status':{stat_w}s}{'action':{act_w}s}{icon}{'location':{loc_w}s}{'status':{stat_w}s}")

    agent = Agent(base_environment)
    for i in range(1, n):
        (location, status) = agent.sensor()
        print(f"{location.name:{loc_w}s}{status.name:{stat_w}s}", end='')
        action = agent.evaluate()
        (location, status) = agent.sensor()
        print(f"{action.name:{act_w}s}{icon}{location.name:{loc_w}s}{status.name:{stat_w}s}")


if __name__ == '__main__':
    run(10)
