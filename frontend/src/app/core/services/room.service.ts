import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Interface baseada no que sua API retorna
export interface User {
  id: string;
  name: string;
  is_host: boolean;
  avatar_id: number;
}

export interface Room {
  id: string;
  port: number | null;
  id_admin: string;
  state: string;
  users: User[];
  game: any | null;
}

@Injectable({
  providedIn: 'root'
})
export class RoomService {

  private apiUrl = 'http://localhost:5000/room';

  constructor(private http: HttpClient) {}

  createRoom(user: User): Observable<Room> {
    return this.http.post<Room>(`${this.apiUrl}/`, user);
  }

  joinRoom(payload: { id: string; name: string; is_host: boolean; avatar_id: number; room_code: string }): Observable<Room> {
    console.log("RoomService: joinRoom called with payload:", payload);
    return this.http.put<Room>(`${this.apiUrl}/join`, payload);
  }
}