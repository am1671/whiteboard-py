from xmlrpc.client import ServerProxy
from threading import Thread
import uuid

class WhiteboardClient:
    def __init__(self, server_address):
        self.server = ServerProxy(server_address)
        self.name = None

    def choose_name(self):
        self.name = input("Enter your name: ")
        return self.name

    def put_shape(self, x, y, shape):
        return self.server.put_shape(x, y, shape, self.name)

    def delete_shape(self, x, y):
        return self.server.delete_shape(x, y, self.name)

    def get_whiteboard(self):
        whiteboard_state, state_id_str = self.server.get_whiteboard()
        state_id = uuid.UUID(state_id_str)  # Parse state_id string to UUID
        return whiteboard_state, state_id

    def notify(self, whiteboard_state, state_id, new_user_name):
        print(f"{new_user_name} joined the whiteboard.")
        print("\nUpdated Whiteboard:")
        print_whiteboard(whiteboard_state)
        print(f"Whiteboard State ID: {state_id}")

    def poll_request(self):
        return input("Type 'leave' to exit: ")

# Function to print the whiteboard with borders
def print_whiteboard(whiteboard_state):
    horizontal_border = "+---+---+---+---+---+"
    print(horizontal_border)
    for row in whiteboard_state:
        print("| {} | {} | {} | {} | {} |".format(*row))
        print(horizontal_border)

# Function to handle user input and perform operations
# Function to handle user input and perform operations
def main():
    client = WhiteboardClient('http://localhost:8000')
    while client.name is None:
        client.choose_name()
    print("Welcome to the whiteboard,", client.name)

    try:
        while True:
            print("\nMenu:")
            print("1. Put shape")
            print("2. Delete shape")
            print("3. View whiteboard")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                print("Choose a shape:")
                print("1. Square")
                print("2. Triangle")
                print("3. Rectangle")
                print("4. Custom Shape")
                shape_choice = input("Enter your choice: ")

                x = int(input("Enter X coordinate: "))
                y = int(input("Enter Y coordinate: "))

                if shape_choice == '1':
                    client.put_shape(x, y, "■")
                elif shape_choice == '2':
                    client.put_shape(x, y, "▲")
                elif shape_choice == '3':
                    client.put_shape(x, y, "□")
                elif shape_choice == '4':
                    custom_shape = input("Enter custom shape: ")
                    client.put_shape(x, y, custom_shape)
                else:
                    print("Invalid shape choice.")
                    
                print("Shape added successfully.")
            elif choice == '2':
                x = int(input("Enter X coordinate: "))
                y = int(input("Enter Y coordinate: "))
                client.delete_shape(x, y)
                print("Shape deleted successfully.")
            elif choice == '3':
                whiteboard_state, state_id = client.get_whiteboard()
                print("\nCurrent Whiteboard:")
                print_whiteboard(whiteboard_state)
                print(f"Whiteboard State ID: {state_id}")
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
