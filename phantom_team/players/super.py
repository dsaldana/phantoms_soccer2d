from smsoccer.util.geometric import euclidean_distance, angle_between_points, cut_angle


class SuperMan(object):
    def __init__(self):
        self.old_distance = None
        self.fly = True

        self.old_message = None
        self.orientation = None

    def dash_to_point(self, point):
        if self.old_message != self.wm.last_message:
            self.orientation = self.wm.abs_body_dir

        self.old_message = self.wm.last_message

        # calculate absolute direction to point
        abs_point_dir = angle_between_points(self.wm.abs_coords, point)

        # subtract from absolute body direction to get relative angle
        relative_angle = abs_point_dir - self.orientation
        relative_angle = cut_angle(relative_angle)


        # if self.fly:
        P = 5
        D = 9
        distance = euclidean_distance(self.wm.abs_coords, point)

        if abs(distance) < 10:
            return True

        if self.old_distance is None:
            self.old_distance = distance

        control = P * distance + D * (self.old_distance - distance)

        if not -7 <= relative_angle <= 7:
            self.wm.ah.turn(relative_angle)

            self.orientation += relative_angle
            print "ang", relative_angle
        else:
            # print "run", relative_angle
            print "control dash=", control, distance
            self.wm.ah.dash(control)

        self.old_distance = distance



        # else:
        # self.turn_body_to_point(point)
        #     self.fly = not self.fly
