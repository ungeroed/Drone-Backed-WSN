from actor import DroneActor, NodeActor
import zmq, visual

drone_speed = 10 # cm per second
drone_rotation_speed = 20 # degrees per second

class World():

    def __init__(self, definition):
        self.context = zmq.Context()

        binding = "ipc:///tmp/drone_sim_world"
        self.socket = self.context.socket(zmq.PULL)
        self.socket.RCVTIMEO = 10
        self.socket.bind(binding)

        self.elements = {}

        for element in definition:
            element["gui"] = element["gui_constructor"](*(element["position"]))
            element["actor"] = element["actor_constructor"](element["name"])
            element["actor"].start()

            sock = self.context.socket(zmq.PUSH)
            sock.connect(element["actor"].binding)
            element["socket"] = sock

            self.elements[element["name"]] = element

        self.pending_movement = {}

    def get_message(self):
        return self.socket.recv_json()

    def send_message_to(self, actor_name, message):
        e = self.elements[actor_name]
        e["socket"].send_json(message)

    def start(self):
        while True:
            # Limit the loop rate for the sake of animation
            visual.rate(100)

            # Handle incoming messages
            try:
                message = self.get_message()

                if message["type"] == "move":
                    name = message["name"]
                    x, y, z = message["x"], message["y"], message["z"]

                    f_x = float(x)
                    f_y = float(y)
                    f_z = float(z)

                    number_of_steps = int(max(abs(x), abs(y), abs(z)) * 100 / drone_speed)
                    self.pending_movement[name] = {
                        "number_of_steps": number_of_steps,
                        "x_step": f_x / number_of_steps,
                        "y_step": f_y / number_of_steps,
                        "z_step": f_z / number_of_steps,
                    }
                else:
                    print "Unknown message type"
            except:
                pass

            # Handle pending movement
            movements_to_remove = []
            for name, movement in self.pending_movement.iteritems():
                for part in self.elements[name]["gui"].get_parts():
                    x_step, y_step, z_step = movement["x_step"], movement["y_step"], movement["z_step"]
                    part.pos += visual.vector(x_step, y_step, z_step)

                    self.elements[name]["position"][0] += x_step
                    self.elements[name]["position"][1] += y_step
                    self.elements[name]["position"][2] += z_step

                movement["number_of_steps"] -= 1
                
                if movement["number_of_steps"] == 0:
                    movements_to_remove.append(name)

            for name in movements_to_remove:
                del self.pending_movement[name]
