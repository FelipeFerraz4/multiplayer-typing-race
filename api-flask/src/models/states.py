from enum import Enum

class RoomState(str, Enum):
    WAITING = 'WAITING'
    PLAYING = 'PLAYING'
    FINISHED = 'FINISHED'

class GameState(str, Enum):
    CREATED = 'CREATED'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    
    
ROOM_STATES = [state.value for state in RoomState]
GAME_STATES = [state.value for state in GameState]
