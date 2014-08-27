from super import SuperMan
from smsoccer.players.abstractplayer import AbstractPlayer
from smsoccer.strategy.formation import player_position
from smsoccer.world.world_model import WorldModel, PlayModes


class AtackAgent(AbstractPlayer, SuperMan):
    """
    This is a DEMO about how to extend the AbstractAgent and implement the
    think method. For a new development is recommended to do the same.
    """


    def __init__(self, visualization=False):

        AbstractPlayer.__init__(self)
        SuperMan.__init__(self)

        self.visualization = visualization
        if visualization:
            from smsoccer.util.fielddisplay import FieldDisplay

            self.display = FieldDisplay()

        self.current_time = 0

    def think(self):
        """
        Performs a single step of thinking for our agent.  Gets called on every
        iteration of our think loop.
        """
        if self.visualization:
            if self.wm.abs_coords[0] is None:
                return

            self.display.clear()
            self.display.draw_robot(self.wm.abs_coords, self.wm.abs_body_dir)
            if self.wm.ball is not None:
                self.display.draw_circle(self.wm.get_object_absolute_coords(self.wm.ball), 4)
                # print self.wm.ball.direction, self.wm.ball.distance
            self.display.show()

        # take places on the field by uniform number
        if not self.in_kick_off_formation:
            position_point = player_position(self.wm.uniform_number)
            # Teleport to right position
            self.teleport_to_point(position_point)

            # turns to attack field
            if self.wm.side == WorldModel.SIDE_R:
                self.wm.ah.turn(180)

            # Player is ready in formation
            self.in_kick_off_formation = True
            return

        # kick off!
        if self.wm.play_mode == PlayModes.BEFORE_KICK_OFF:
            # player 9 takes the kick off
            if self.wm.uniform_number == 9:
                if self.is_ball_kickable():
                    # kick with 100% extra effort at enemy goal
                    self.kick_to(self.goal_pos, 1.0)
                    # print self.goal_pos
                else:
                    # move towards ball
                    if self.wm.ball is not None:
                        if self.wm.ball.direction is not None \
                                and -7 <= self.wm.ball.direction <= 7:
                            self.wm.ah.dash(50)
                        else:
                            self.wm.turn_body_to_point((0, 0))

                # turn to ball if we can see it, else face the enemy goal
                if self.wm.ball is not None:
                    self.turn_neck_to_object(self.wm.ball)

                return

        # attack!
        else:
            # If not new cicle
            # if self.current_time == self.wm.sim_time:
            #     return

            # self.current_time = self.wm.sim_time
            # print self.wm.sim_time

            if self.wm.abs_coords is not None:

                self.dash_to_point((50,25))
                return

            # find the ball
            if self.wm.ball is None or self.wm.ball.direction is None:
                self.wm.ah.turn(35)
                return

            # kick it at the enemy goal
            if self.is_ball_kickable():

                # angle = cut_angle(angle_between_points(self.wm.abs_coords, self.goal_pos)) - cut_angle(self.wm.abs_body_dir)
                # self.wm.ah.kick(20, angle)
                self.kick_to((0, 20))
                return
            else:
                # move towards ball
                if -7 <= self.wm.ball.direction <= 7:
                    self.wm.ah.dash(5 * self.wm.ball.distance + 20)
                else:
                    # face ball
                    self.wm.ah.turn(self.wm.ball.direction / 2)

                return

