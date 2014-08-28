from smsoccer.util.geometric import euclidean_distance, angle_between_points, cut_angle


class SuperMan(object):
    def __init__(self):
        self.old_distance = None
        self.fly = True

        self.old_message = None
        # Offline direction based on actions
        self.local_direction = None

        self.new_sensed_msg = False

        self._old_ball_distance = None

        # Estimated values based on actions
        self.local_ball_dir = None
        self.local_ball_distance = None

    def update_super(self):
        self.new_sensed_msg = self.old_message != self.wm.last_message

        if self.new_sensed_msg or self.local_direction is None:
            self.local_direction = self.wm.abs_body_dir

        self.old_message = self.wm.last_message


    def dash_to_point(self, point, radio=10):
        """
        Run to a point.
        :param point: target point
        :param radio: tolerance to be in the point.
        :return:
        """
        # calculate absolute direction to point
        abs_point_dir = angle_between_points(self.wm.abs_coords, point)

        # subtract from absolute body direction to get relative angle
        relative_angle = abs_point_dir - self.local_direction
        relative_angle = cut_angle(relative_angle)

        # if self.fly:
        P = 5
        D = 9
        distance = euclidean_distance(self.wm.abs_coords, point)

        if abs(distance) < radio:
            return True

        if self.old_distance is None:
            self.old_distance = distance

        control = P * distance + D * (self.old_distance - distance)

        if not -7 <= relative_angle <= 7:
            self.wm.ah.turn(relative_angle)

            self.local_direction += relative_angle
        else:
            self.wm.ah.dash(control)

        self.old_distance = distance


    def dribbling_to(self, point, radio=10):
        if (
            self.new_sensed_msg or self.local_ball_dir is None) and self.wm.ball is not None and self.wm.ball.direction is not None:
            self.local_ball_dir = self.wm.ball.direction
            self.local_ball_distance = self.wm.ball.distance

        target_d = euclidean_distance(self.wm.abs_coords, point)

        if target_d < radio:
            return True

        if self.is_ball_kickable():
            angle = cut_angle(angle_between_points(self.wm.abs_coords, point)) - cut_angle(self.local_direction)
            self.wm.ah.kick(10, angle)
            self.local_ball_distance += 3 / 5
            self.local_ball_dir += angle

        else:
            if -7 <= self.local_ball_dir <= 7:
                print "running"
                if self._old_ball_distance is None:
                    self._old_ball_distance = self.local_ball_distance

                P = 1.3
                D = 0.5

                control = P * self.local_ball_distance + D * (self._old_ball_distance - self.local_ball_distance)
                print "cdash=", [control, self.local_ball_distance, self._old_ball_distance - self.local_ball_distance]
                self.wm.ah.dash(control)
            else:
                self.wm.ah.turn(self.local_ball_dir / 2)
                self.local_direction += self.local_ball_dir / 2

        return False