
from smsoccer.strategy.formation import player_position
from smsoccer.world.world_model import WorldModel, PlayModes
from smsoccer.players.abstractgoalie import AbstractGoalie
from smsoccer.util.fielddisplay import FieldDisplay
from smsoccer.util.geometric import euclidean_distance

from shapely.geometry import *

class GoalieAgent(AbstractGoalie):
    """
    Goalie Agent for Robocup Soccer Team
    """

    def __init__(self, visualization = False):
        super(GoalieAgent, self).__init__()

        self.visualization = visualization
        if visualization:
            self.display = FieldDisplay()

        self._my_goal_position = None

    def position_rules(self):

        if self._my_goal_position != None and self.wm.ball is not None:
            # euclidean_distance

            # Base Circle
            root_point = Point( self._my_goal_position )
            circle = root_point.buffer(13)

            circle_points = list(circle.exterior.coords)

            # Base Line
            ball_coords = self.wm.get_object_absolute_coords(self.wm.ball)
            line = LineString([ self._my_goal_position, ball_coords ])

            line_points = list( line.coords )

            return { "circle_points": circle_points, "line_points": line_points }

        return False

    def think(self):
        """
        Think method
        """

        # Draw Debug map
        if self.visualization:
            if self.wm.abs_coords is None:
                return

            self.display.clear()
            self.display.draw_robot(self.wm.abs_coords, self.wm.abs_body_dir)
            if self.wm.ball is not None:
                self.display.draw_circle(self.wm.get_object_absolute_coords(self.wm.ball), 4)

            rules = self.position_rules()
            if rules != False:
                self.display.draw_points( rules["circle_points"] );
                self.display.draw_line( rules["line_points"][0], rules["line_points"][1] )

            self.display.show()

        # END Draw Debug Map

        if not self.in_kick_off_formation:

            self._my_goal_position = player_position(self.wm.uniform_number, self.wm.side == WorldModel.SIDE_R)

            # Teleport to right position
            self.teleport_to_point(self._my_goal_position)
            # Player is ready in formation
            self.in_kick_off_formation = True
            return
