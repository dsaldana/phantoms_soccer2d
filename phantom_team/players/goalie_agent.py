
from smsoccer.strategy.formation import player_position
from smsoccer.world.world_model import WorldModel, PlayModes
from smsoccer.players.abstractgoalie import AbstractGoalie
from smsoccer.util.fielddisplay import FieldDisplay
from smsoccer.util.geometric import euclidean_distance

from superman import SuperMan

from shapely.geometry import *

class GoalieAgent(AbstractGoalie, SuperMan):
    """
    Goalie Agent for Robocup Soccer Team
    """

    def __init__(self, visualization = False):
        AbstractGoalie.__init__(self)
        SuperMan.__init__(self)

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

            # Destination Point

            inter = circle.intersection( line )
            point = list( inter.coords )[1]

            return { "circle_points": circle_points, "line_points": line_points, "destination_point": point }

        return False

    def think(self):
        """
        Think method
        """

        self.update_super()

        rules = self.position_rules()

        # Draw Debug map
        if self.visualization:
            if self.wm.abs_coords is None:
                return

            self.display.clear()
            self.display.draw_robot(self.wm.abs_coords, self.wm.abs_body_dir)
            if self.wm.ball is not None:
                self.display.draw_circle(self.wm.get_object_absolute_coords(self.wm.ball), 4)

            if rules != False:
                self.display.draw_points( rules["circle_points"] );
                self.display.draw_line( rules["line_points"][0], rules["line_points"][1] )

            self.display.show()

        # END Draw Debug Map

        # DEBUG

        # print self.wm.abs_body_dir

        # END DEBUG

        if not self.in_kick_off_formation:

            self._my_goal_position = player_position(self.wm.uniform_number, self.wm.side == WorldModel.SIDE_R)

            # Teleport to right position
            self.teleport_to_point(self._my_goal_position)
            # Player is ready in formation
            self.in_kick_off_formation = True
        else:
            # Act
            if self.wm.play_mode != PlayModes.BEFORE_KICK_OFF:

                if rules == False:
                    # self.turn_body_to_point( self._my_goal_position )
                    # self.wm.ah.turn(10)

                    if self.dash_to_point( self._my_goal_position, radio = 1 ) == True:
                        # turn to field
                        print "reach !"
                    return

                self.dash_to_point( rules["destination_point"], radio = 1 );
