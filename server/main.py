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

        object_lists = ["TILES", "OBJECTS", "SENTIENTS"]
        for object_list in object_lists:
            self.map_data[object_list] = []
            for x in range(max_x + 1):
                self.map_data[object_list].append([])
                for y in range(max_y + 1):
                    self.map_data[object_list][x].append(None)
            for item in read_data[object_list]:
                self.map_data[object_list][item["X"]][item["Y"]] = item

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
            content_length = len(send_data_raw)
            try:
                connection.send(struct.pack(">I", content_length) + send_data_raw)
            except ConnectionResetError:
                print("Error - Connection from {0} was reset.".format(address[0]))
                break


if __name__ == "__main__":
    server = Server()
    server.start()
