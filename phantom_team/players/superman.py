import time

from smsoccer.localization.filter.particlefilter import ParticleFilter
from smsoccer.util.geometric import euclidean_distance, angle_between_points, cut_angle


class SuperMan(object):
    def __init__(self):
        self.old_distance = None
        self.fly = True

        self.old_message = None
        # Offline direction based on actions
        # self.local_direction = None

        self.new_sensed_msg = False

        self._old_ball_distance = None

        # Estimated values based on actions
        # self.local_ball_dir = None
        # self.local_ball_distance = None

        self.current_time = time.time()
        self.new_cycle = False

        # ### PF ##########
        self.pf = ParticleFilter()


    def update_super(self):
        self.new_sensed_msg = self.old_message != self.wm.last_message

        # if self.new_sensed_msg or self.local_direction is None:
        # self.local_direction = self.wm.abs_body_dir

        self.old_message = self.wm.last_message

        # new time
        new_time = time.time()
        self.new_cycle = new_time - self.current_time > 0.1

        if self.new_cycle:
            self.current_time = new_time
        # self.new_cycle = self.current_time < self.wm.sim_time
        # self.current_time = self.wm.sim_time

        # #### PF ###
        if self.new_sensed_msg and self.wm.abs_coords is not None and self.wm.abs_body_dir is not None and self.pf.started:
            self.pf.update_particles([self.wm.abs_coords[0], self.wm.abs_coords[1], self.wm.abs_body_dir])

    def dash_to_point(self, point, radio=10):
        """
        Run to a point.
        :param point: target point
        :param radio: tolerance to be in the point.
        :return:
        """
        # calculate absolute direction to point
        abs_point_dir = angle_between_points(self.pf.e_position, point)

        # subtract from absolute body direction to get relative angle
        relative_angle = abs_point_dir - self.pf.e_position[2]
        relative_angle = cut_angle(relative_angle)

        # if self.fly:
        P = 5
        D = 9
        distance = euclidean_distance(self.pf.e_position, point)

        if abs(distance) < radio:
            return True

        if self.old_distance is None:
            self.old_distance = distance

        control = P * distance + D * (self.old_distance - distance)

        if not -7 <= relative_angle <= 7:
            self.turn(relative_angle)

        else:
            print "cdash=", control
            self.dash(control)

        self.old_distance = distance


    # ##### actions with pff
    def turn(self, angle):
        self.wm.ah.turn(angle)
        self.pf.rotate_particles(angle)

    def dash(self, val):
        self.wm.ah.dash(val)
        self.pf.dash_particles(val)


    def dribbling_to(self, point, radio=10):
        target_d = euclidean_distance(self.pf.e_position, point)
        if target_d < radio:
            return True


        # find the ball
        if self.wm.ball is None or self.wm.ball.direction is None:
            self.turn(45)
            print "oh oh"
            return False

        # # BALL IDENTIFIED
        # if (
        #             self.new_sensed_msg or self.local_ball_dir is None) and self.wm.ball is not None and self.wm.ball.direction is not None:
        #     self.local_ball_dir = self.wm.ball.direction
        #     self.local_ball_distance = self.wm.ball.distance



        if self.is_ball_kickable():
            angle = cut_angle(angle_between_points(self.pf.e_position[:2], point)) - cut_angle(self.pf.e_position[2])
            self.wm.ah.kick(20, angle)
        else:
            if -7 <= self.wm.ball.direction <= 7:
                print "running"
                if self._old_ball_distance is None:
                    self._old_ball_distance = self.wm.ball.distance

                P = 15
                D = 3.5

                control = P * self.wm.ball.distance + D * (self._old_ball_distance - self.wm.ball.distance)
                print "c_dash=", control
                self.dash(control)
            else:
                self.turn(self.wm.ball.direction / 2.0)

        return False
