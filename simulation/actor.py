import multiprocessing, zmq, json, time, random

class Actor():
    
    def __init__(self, name):
        self.name = name

        self.binding = "ipc:///tmp/drone_sim_actor_%s" % self.name
        self.world_binding = "ipc:///tmp/drone_sim_world"

    def get_message(self):
        try:
            return self.pull_socket.recv_json()
        except:
            return None

    def send_message(self, message):
        message["name"] = self.name
        self.world_socket.send_json(message)

    def start(self):
        p = multiprocessing.Process(
            target=self.run,
            args=()
        )
        p.start()

    def run(self):
        context = zmq.Context()

        self.world_socket = context.socket(zmq.PUSH)
        self.world_socket.connect(self.world_binding)

        self.pull_socket = context.socket(zmq.PULL)
        self.pull_socket.RCVTIMEO = 1000
        self.pull_socket.bind(self.binding)

        self._run()

    def _run(self):
        raise Exception("Not implemented")

class DroneActor(Actor):
    def _run(self):
        while True:
            message = self.send_message({
                "type": "move",
                "x": random.randint(-20, 20),
                "y": random.randint(-20, 20),
                "z": random.randint(-20, 20),
            })
            time.sleep(3)

class NodeActor(Actor):
    def _run(self):
        print "Running node"
        while True:
            message = self.get_message()
            if message is not None:
                print "message", message

class FloorActor(Actor):
    def _run(self):
		pass

# vim: set et list number sts=4 ts=4 sw=4
