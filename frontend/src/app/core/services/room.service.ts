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

@Injectable({
  providedIn: 'root'
})
export class RoomService {
  private apiUrl = 'http://localhost:5000/room';
  private socketUrl = 'http://localhost:5000';
  private socket?: Socket;

  // Subjects para o componente ouvir eventos específicos
  private roomUpdatedSource = new Subject<void>();
  roomUpdated$ = this.roomUpdatedSource.asObservable();

  private gameStartedSource = new Subject<string>();
  gameStarted$ = this.gameStartedSource.asObservable();

  private progressUpdateSource = new Subject<any>();
  progressUpdate$ = this.progressUpdateSource.asObservable();

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
    return this.http.post<Game_game>(`http://localhost:5000/room/${roomId}/start`,{ user_id: userId });
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
  }

  emitStartGame(roomId: string) {
    this.socket?.emit('start_game', { room_id: roomId });
  }

  disconnectSocket() {
    this.socket?.disconnect();
  }

  sendProgress(roomId: string, userId: string, progress: number) {
    console.log(" Enviando progress:", { roomId, userId, progress });

    this.socket?.emit('send_progress', { 
      room_id: roomId, 
      user_id: userId, 
      progress: progress 
    });
  }
}