import socket
import struct
import threading
import pickle
import json


class Server:
    force_thread_halt = False
    map_data = {}

    def start(self):
        self.load_map_data()
        client_listen_thread = threading.Thread(target=self.listen_for_clients)
        client_listen_thread.start()

    def load_map_data(self):
        with open("json/map.json", "r") as md:
            read_data = json.load(md)
            md.close()

        max_x = 0
        max_y = 0
        for tile in read_data["TILES"]:
            if tile["X"] > max_x:
                max_x = tile["X"]
            if tile["Y"] > max_y:
                max_y = tile["Y"]

        self.map_data["TILES"] = [[None] * (max_y + 1)] * (max_x + 1)
        self.map_data["OBJECTS"] = [[None] * (max_y + 1)] * (max_x + 1)
        self.map_data["SENTIENTS"] = [[None] * (max_y + 1)] * (max_x + 1)

        print(self.map_data["TILES"])
        for item in read_data["TILES"]:
            self.map_data["TILES"][item["X"]][item["Y"]] = item.copy()
        for item in read_data["OBJECTS"]:
            self.map_data["OBJECTS"][item["X"]][item["Y"]] = item.copy()
        for item in read_data["SENTIENTS"]:
            self.map_data["SENTIENTS"][item["X"]][item["Y"]] = item.copy()
        print(self.map_data["TILES"])

    def listen_for_clients(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 8000))
        s.listen(15)
        while not self.force_thread_halt:
            print("Waiting on client connections...")
            connection, address = s.accept()
            print("Connection established from {0}.".format(address[0]))
            client_thread = threading.Thread(target=self.handle_client_connection, args=(connection, address))
            client_thread.start()

    def handle_client_connection(self, connection, address):
        while not self.force_thread_halt:
            send_data = self.map_data.copy()
            send_data["PLAYER"] = {"X": 7, "Y": 5}
            send_data_raw = pickle.dumps(send_data)
            try:
                connection.send(struct.pack(">I", len(send_data_raw)))
                connection.send(send_data_raw)
            except ConnectionResetError:
                print("Error - Connection from {0} was reset.".format(address[0]))
                break


if __name__ == "__main__":
    server = Server()
    server.start()
