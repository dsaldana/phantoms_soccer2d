from smsoccer.util.geometric import euclidean_distance, angle_between_points


class SuperMan(object):
    def __init__(self):
        self.old_distance = None
        self.fly = False


    def run_to_point(self, point):
        if self.fly:
            P = 5
            D = 9
            distance = euclidean_distance(self.wm.abs_coords, point)

            if self.old_distance is None:
                self.old_distance = distance

            control = P * distance + D * (self.old_distance - distance) + 40
            print "control dash=", control, distance
            self.wm.ah.dash(control)

            self.old_distance = distance


        else:
            self.turn_body_to_point(point)

        # self.fly = not self.fly
