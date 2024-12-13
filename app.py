import tornado.ioloop
import tornado.web
import tornado.websocket
import redis
import threading
import json

try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("Connected to Redis successfully!")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
    exit(1)

CHANNEL = "chat_room"
connected_clients = set()

main_loop = tornado.ioloop.IOLoop.current()


def redis_listener():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(CHANNEL)
    print("Redis listener started...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received from Redis: {message['data']}")
            main_loop.add_callback(broadcast_message_to_clients, message['data'])


def broadcast_message_to_clients(data):
    if not connected_clients:
        print("No connected clients to broadcast message.")
        return

    print(f"Broadcasting message to {len(connected_clients)} clients: {data}")
    message = {"type": "message", "content": data}
    serialized_message = json.dumps(message)
    for client in connected_clients:
        try:
            client.write_message(serialized_message)
            print(f"Message sent to client {id(client)}: {serialized_message}")
        except Exception as e:
            print(f"Error broadcasting message to client {id(client)}: {e}")


def update_clients_list():
    client_list = [f"Client-{id(c)}" for c in connected_clients]
    update_message = {"type": "clients", "clients": client_list}
    serialized_update = json.dumps(update_message)
    for client in connected_clients:
        try:
            client.write_message(serialized_update)
            print(f"Updated client list sent to client {id(client)}")
        except Exception as e:
            print(f"Error updating client list for client {id(client)}: {e}")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print(f"Client {id(self)} connected")
        connected_clients.add(self)
        update_clients_list()

    def on_message(self, message):
        print(f"Received message from client {id(self)}: {message}")
        try:
            redis_client.publish(CHANNEL, message)
            print(f"Published to Redis: {message}")
        except Exception as e:
            print(f"Error publishing message to Redis: {e}")

    def on_close(self):
        print(f"Client {id(self)} disconnected")
        connected_clients.remove(self)
        update_clients_list()

    def check_origin(self, origin):
        return True


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", WebSocketHandler),
    ], static_path="static", template_path="templates")


if __name__ == "__main__":
    listener_thread = threading.Thread(target=redis_listener)
    listener_thread.daemon = True
    listener_thread.start()

    app = make_app()
    app.listen(8888)
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
