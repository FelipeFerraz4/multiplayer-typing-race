import eventlet
eventlet.monkey_patch() # OBRIGATÓRIO ser a primeira linha

from server import server
from controllers import room_ns, game_ns

def main():
    server.api.add_namespace(room_ns)
    server.api.add_namespace(game_ns)
    server.run()

if __name__=='__main__':
    main()