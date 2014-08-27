
from smsoccer.strategy.formation import player_position
from smsoccer.world.world_model import WorldModel, PlayModes
from smsoccer.players.abstractgoalie import AbstractGoalie

class GoalieAgent(AbstractGoalie):
    """
    Goalie Agent for Robocup Soccer Team
    """

    def __init__(self):
        super(GoalieAgent, self).__init__()

        self._back_to_goal = False
        self._my_goal_position = None

        self.__control_turn = True

    def think(self):
        """
        Think method
        """
        if not self.in_kick_off_formation:

            self._my_goal_position = player_position(self.wm.uniform_number, self.wm.side == WorldModel.SIDE_R)
            # Teleport to right position
            self.wm.teleport_to_point(self._my_goal_position)
            # Player is ready in formation
            self.in_kick_off_formation = True
            return

