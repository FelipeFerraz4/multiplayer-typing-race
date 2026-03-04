import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { io, Socket } from 'socket.io-client';

export interface User {
  id: string;
  name: string;
  is_host: boolean;
  avatar_id: number;
}

export interface Room_game {
  id: string;
  room_code: string;
  port: number | null;
  id_admin: string;
  state: string;
  users: User[];
  game: Game_game | null;
}

export interface UserProgress {
  user_id: string;
  progress: number;       
  progress_index: number;
}

export interface Game_game {
  id: string;
  room_id: string;
  text: string;
  text_size: number;
  state: 'CREATED' | 'RUNNING' | 'FINISHED';
  users_progress: UserProgress[];
}

export interface ProgressUpdateRequest {
  user_id: string;
  typed_characters: number;
  errors: number;
  elapsed_time: number;
}

export interface ProgressUpdateData {
  user_id: string;
  progress: number;
  progress_index: number;
}

export interface ProgressUpdateEvent {
  type: 'PROGRESS_UPDATED';
  data: ProgressUpdateData | any;
}

export interface GameResult {
  game_id: string;
  user_id: string;
  name: string;
  position: number;
  wpm: number;
  final_time: number;
}

export interface GameFinishedData {
  game_id: string;
  state: 'FINISHED';
  results: GameResult[];
}

export interface GameFinishedEvent {
  type: 'FINISHED';
  data: GameFinishedData;
}

const host = "192.168.31.26";

@Injectable({
  providedIn: 'root'
})
export class RoomService {
  private apiUrl = `http://${host}:5000/room`;
  private socketUrl = `http://${host}:5000`;
  private socket?: Socket;

  // Subjects para o componente ouvir eventos específicos
  private roomUpdatedSource = new Subject<void>();
  roomUpdated$ = this.roomUpdatedSource.asObservable();

  private gameStartedSource = new Subject<string>();
  gameStarted$ = this.gameStartedSource.asObservable();

  private progressUpdateSource = new Subject<UserProgress>();
  progressUpdate$ = this.progressUpdateSource.asObservable();

  private gameFinishedSource = new Subject<GameFinishedData>();
  gameFinished$ = this.gameFinishedSource.asObservable();

  constructor(private http: HttpClient) {}

  // --- Métodos HTTP ---
  createRoom(user: User): Observable<Room_game> {
    return this.http.post<Room_game>(`${this.apiUrl}/`, user);
  }

  joinRoom(payload: any): Observable<Room_game> {
    return this.http.put<Room_game>(`${this.apiUrl}/join`, payload);
  }

  getRoomById(roomId: string): Observable<Room_game> {
    return this.http.get<Room_game>(`${this.apiUrl}/${roomId}`);
  }

  startGame(roomId: string, userId: string): Observable<Game_game> {
    return this.http.post<Game_game>(`${this.apiUrl}/${roomId}/start`,{ user_id: userId });
  }

  // --- Métodos de WebSocket ---
  connectSocket(roomId: string) {
    if (this.socket?.connected) return;

    this.socket = io(this.socketUrl);

    this.socket.on('connect', () => {
      console.log('Conectado ao WebSocket');
      this.socket?.emit('join_room', { room_id: roomId });
    });

    // Quando alguém entra ou sai, o back emite esse evento
    this.socket.on('room_joined', () => {
      this.roomUpdatedSource.next();
    });

    // Quando o host inicia o jogo
    this.socket.on('game_started', (data: any) => {
      this.gameStartedSource.next(data.room_id);
    });

    this.socket.on('progress_update', (data: any) => {
      this.progressUpdateSource.next(data);
    });

    this.socket.on('game_finished', (data: GameFinishedData) => {
      console.log('Evento game_finished recebido do servidor:', data);
      this.gameFinishedSource.next(data);
    });
  }

  emitStartGame(roomId: string) {
    this.socket?.emit('start_game', { room_id: roomId });
  }

  disconnectSocket() {
    this.socket?.disconnect();
  }

  sendProgress(
    roomId: string,
    gameId: string,
    userId: string,
    typedCharacters: number,
    errors: number,
    elapsedTime: number
  ) {
    this.socket?.emit('send_progress', { 
      room_id: roomId,
      game_id: gameId,
      user_id: userId,
      typed_characters: typedCharacters,
      errors: errors,
      elapsed_time: elapsedTime
    });
  }
}