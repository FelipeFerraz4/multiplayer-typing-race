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
  game: unknown | null;
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

  // --- Métodos de WebSocket ---
  connectSocket(roomId: string) {
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
  }

  emitStartGame(roomId: string) {
    this.socket?.emit('start_game', { room_id: roomId });
  }

  disconnectSocket() {
    this.socket?.disconnect();
  }
}