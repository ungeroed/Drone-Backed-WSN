from visual import *
import math, numpy, numpy.linalg

# Variables
floor_length = 500
floor_width = 500
floor_height = 5

node_length = 10
node_width = 6
node_height = 5

drone_body_length = 15
drone_body_width = 10
drone_body_height = 8

drone_leg_length = 60
drone_leg_width = 3
drone_leg_height = 2

drone_foot_height = 15
drone_foot_radius = 1


def floor():
    return box(
        length=floor_length, width=floor_width, height=floor_height, 
        pos=vector(0, -17.5, 0), 
        material=materials.rough, color=color.green)

def node(x, y, z, degrees):
    cylinder(
        axis=vector(0, 200, 0), radius=0.5, 
        pos=vector(x, y - 17.5, z),
        color=color.red)
    return box(
        length=node_length, width=node_width, height=node_height, 
        pos=vector(x, y + (node_height - 17.5), z), 
        material=materials.wood, color=color.orange)

def body(x, y, z):
    return ellipsoid(
        length=15, width=10, height=8, 
        pos=vector(x, y, z), 
        material=materials.plastic, color=color.blue)

def leg(x, y, z):
    return box(
        length=drone_leg_length, width=drone_leg_width, height=drone_leg_height, 
        pos=vector(x, y, z), 
        material=materials.plastic, color=color.blue)

def foot(x, y, z):
    return cylinder(
        axis=vector(0, drone_foot_height, 0), radius=drone_foot_radius, 
        pos=vector(
            x - drone_leg_length / 2 + drone_foot_radius, 
            y - 15, 
            z), 
        material=materials.plastic, color=color.blue)

def pointer(x, y, z, c=color.red):
    return arrow(
        axis=vector(-10, 0, 0), radius=0.5, 
        pos=vector(x, y, z),
        color=c)
    
def rotate(obj, degrees, x, y, z):
    obj.rotate(
        angle=radians(degrees), 
        axis=vector(0, 1, 0), 
        origin=vector(x, y, z))


class GUI():

    def get_parts(self):
        raise Exception("Not implemented")


class DroneGUI(GUI):

    def __init__(self, x, y, z, degrees):
        self.body = body(x, y, z)

        self.leg_1 = leg(x, y, z)
        rotate(self.leg_1, 45, x, y, z)

        self.leg_2 = leg(x, y, z)
        rotate(self.leg_2, -45, x, y, z)

        self.foot_1 = foot(x, y, z)
        rotate(self.foot_1, 45, x, y, z)

        self.foot_2 = foot(x, y, z)
        rotate(self.foot_2, -45, x, y, z)

        self.foot_3 = foot(x, y, z)
        rotate(self.foot_3, 135, x, y, z)

        self.foot_4 = foot(x, y, z)
        rotate(self.foot_4, -135, x, y, z)

        self.pointer = pointer(x, y, z)

        self.parts = [
            self.body,
            self.leg_1,
            self.leg_2,
            self.foot_1,
            self.foot_2,
            self.foot_3,
            self.foot_4,
            self.pointer,
        ]

        self.orientation = 0
        if degrees != 0:
            self.rotate(degrees, instant=True)

    def get_parts(self):
        return self.parts

    #def _run(self):
    #    while True:
    #        self._move(*[random.randint(0, 20) for x in range(3)])
    #        time.sleep(2)
    
    #def _get_drone_position(self):
    #    return self.body.pos

    #def _get_node_position(self):
    #    return self.node.pos

    #def _get_forward_unit_vector(self):
    #    return vector(1, 0, 0).rotate( radians(self.orientation), vector(0, 1, 0) )

    #def _get_backward_unit_vector(self):
    #    return (-1) * self._get_forward_unit_vector()

    #def _get_right_unit_vector(self):
    #    return self._get_forward_unit_vector().rotate( radians(90), vector(0, 1, 0))

    #def _get_left_unit_vector(self):
    #    return self._get_forward_unit_vector().rotate( radians(-90), vector(0, 1, 0))

    #def _get_node_vector(self):
    #    return self.node.pos - self.body.pos

    #def move_forward(self, distance):
    #    v = self._get_forward_unit_vector() * (-distance)
    #    self._move(v[0], v[1], v[2])

    #def move_backward(self, distance):
    #    v = self._get_backward_unit_vector() * (-distance)
    #    self._move(v[0], v[1], v[2])

    #def move_left(self, distance):
    #    v = self._get_left_unit_vector() * distance
    #    self._move(v[0], v[1], v[2])

    #def move_right(self, distance):
    #    v = self._get_right_unit_vector() * distance
    #    self._move(v[0], v[1], v[2])

    #def land(self):
    #    self._move(0, -self.body.pos[1], 0)

    #def rotate_to_vector(self, v):
    #    vr = vector(v).rotate( radians(self.orientation), vector(0, 1, 0))

    #    a = self._get_backward_unit_vector()
    #    b = vr

    #    d = degrees(diff_angle(a, b))
    #    if numpy.cross(a, b)[1] < 0:
    #        d = -d
    #    self.rotate(d)

    #def rotate(self, degrees, instant=False):
    #    self.orientation = self.orientation + degrees

    #    number_of_steps = int(abs(degrees) * 100 / drone_rotation_speed)
    #    step = float(degrees) / float(number_of_steps)

    #    for i in range(number_of_steps):
    #        if not instant:
    #            rate(100)
    #        for part in self.parts:
    #            rotate(part, step, self.body.pos[0], self.body.pos[1], self.body.pos[2])

    #def _real_distance(self):
    #    return numpy.linalg.norm(self._get_node_vector())

    #def _real_direction(self):
    #    node_vector = self._get_node_vector()
    #    node_vector[1] = 0 # Don't consider the height
    #    return degrees(diff_angle(node_vector, self._get_forward_unit_vector()))

    #def get_sound_pressure_level(self):
    #    # TODO 
    #    # This is not based on actual data, but rather on physical
    #    # properties of audio and some reference values selected
    #    # without special reason
    #    reference_distance = 12.5
    #    reference_spl = 100
    #    return reference_spl + 20 * numpy.log10(reference_distance / self._real_distance())


class NodeGUI(GUI):
    def __init__(self,x,y,z,degrees):
        self.node = node(x,y,z,degrees)

    def get_parts(self):
        return [self.node]


class FloorGUI(GUI):
    def __init__(self,x,y,z,degrees):
        self.floor = floor()

    def get_parts(self):
        return [self.floor]
