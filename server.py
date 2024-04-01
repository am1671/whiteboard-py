from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from threading import Lock
import uuid

class WhiteboardServer:
    def __init__(self):
        self.whiteboard = [[' ']*5 for _ in range(5)]  # Initialize whiteboard as a 5x5 2D list
        self.lock = Lock()  # Lock for thread safety
        self.clients = {}  # Dictionary to store client names and addresses
        self.state_id = uuid.uuid4()  # Initial state ID

    def put_shape(self, x, y, shape, client_name):
        with self.lock:
            if 0 <= x < 5 and 0 <= y < 5:
                self.whiteboard[y][x] = shape
                self.state_id = uuid.uuid4()  # Update state ID
                return True
            return False

    def delete_shape(self, x, y, client_name):
        with self.lock:
            if 0 <= x < 5 and 0 <= y < 5:
                self.whiteboard[y][x] = ' '
                self.state_id = uuid.uuid4()  # Update state ID
                return True
            return False

    def get_whiteboard(self):
        with self.lock:
            return self.whiteboard, str(self.state_id)  # Convert state_id to string

    def join_whiteboard(self, client_name, client_address):
        with self.lock:
            self.clients[client_address] = client_name
            return True

    def leave_whiteboard(self, client_address):
        with self.lock:
            if client_address in self.clients:
                del self.clients[client_address]
                return True
            return False

    def get_clients(self):
        with self.lock:
            return self.clients

# Function to update whiteboard for all clients
def update_whiteboard():
    whiteboard_state, state_id = whiteboard_server.get_whiteboard()
    clients = whiteboard_server.get_clients()
    for client_address, client_name in clients.items():
        client = ServerProxy(f"http://{client_address[0]}:{client_address[1]}")
        client.notify(whiteboard_state, state_id, client_name)

# Function to handle client connections
def handle_client(client_address):
    print(f"Client connected: {client_address}")
    client = ServerProxy(f"http://{client_address[0]}:{client_address[1]}")
    client_name = client.choose_name()
    whiteboard_server.join_whiteboard(client_name, client_address)
    update_whiteboard()

    while True:
        client_request = client.poll_request()
        if client_request == "leave":
            whiteboard_server.leave_whiteboard(client_address)
            print(f"Client {client_name} left the whiteboard")
            update_whiteboard()
            break

# Start XML-RPC server
whiteboard_server = WhiteboardServer()
server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)  # Set allow_none=True to handle NoneType values
server.register_instance(whiteboard_server)

print("Whiteboard server is running...")

# Serve requests indefinitely
server.serve_forever()
