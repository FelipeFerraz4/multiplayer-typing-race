import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-room',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './room.html',
  styleUrl: './room.scss',
})
export class Room {

  avatars = [
    { id: 1, name: '🦊', url: '/assets/logo-water.webp' },
    { id: 2, name: '🐶', url: '/assets/logo-run.webp' },
    { id: 3, name: '🐱', url: '/assets/logo-ok.webp' },
    { id: 4, name: '🦄', url: '/assets/logo-sleep.webp' },
    { id: 5, name: '🐼', url: '/assets/logo-happy.webp' },
    { id: 6, name: '🐸', url: '/assets/logo-water.webp' },
    { id: 7, name: '🦉', url: '/assets/logo-water.webp' },
    { id: 8, name: '🐯', url: '/assets/logo-water.webp' }
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
    console.log('Corrida iniciada!');
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
