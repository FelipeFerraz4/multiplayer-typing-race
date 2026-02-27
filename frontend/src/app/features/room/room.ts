import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-room',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './room.html',
  styleUrl: './room.scss',
})
export class Room {
  constructor(private router: Router) { }

  avatars = [
    { id: 1, name: 'water', url: '/assets/logo-water.webp' },
    { id: 2, name: 'run', url: '/assets/logo-run.webp' },
    { id: 3, name: 'ok', url: '/assets/logo-ok.webp' },
    { id: 4, name: 'sleep', url: '/assets/logo-sleep.webp' },
    { id: 5, name: 'happy', url: '/assets/logo-happy.webp' }
  ];
  roomId = 'ABCD123';
  isHost = true;

  players = [
    { name: 'Ryan', isHost: true, avatarId: 1 },
    { name: 'João', isHost: false, avatarId: 2 },
    { name: 'Maria', isHost: false, avatarId: 3 },
    { name: 'Pedro', isHost: false, avatarId: 4 },
    { name: 'Lobo', isHost: false, avatarId: 5 },
  ];

  copyRoomId() {
    navigator.clipboard.writeText(this.roomId);
  }

  startGame() {
    this.router.navigate(['/game', this.roomId]);
  }

  avatarMap = new Map<number, { name: string; url: string }>();

  ngOnInit() {
    this.avatars.forEach(avatar => {
      this.avatarMap.set(avatar.id, {
        name: avatar.name,
        url: avatar.url
      });
    });
  }
}
