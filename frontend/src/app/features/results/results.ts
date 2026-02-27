import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results.html',
  styleUrl: './results.scss',
})
export class Results implements OnInit {

  // Mock de dados dos 5 jogadores com diferentes progressos para testar o pódio
  players = [
    { name: 'Ryan', avatarId: 1, progress: 85 },
    { name: 'João', avatarId: 2, progress: 100 }, // 1º Lugar
    { name: 'Maria', avatarId: 3, progress: 92 }, // 2º Lugar
    { name: 'Pedro', avatarId: 4, progress: 70 },
    { name: 'Lobo', avatarId: 5, progress: 88 }, // 3º Lugar
  ];

  avatars = [
    { id: 1, url: '/assets/logo-water.webp' },
    { id: 2, url: '/assets/logo-run.webp' },
    { id: 3, url: '/assets/logo-ok.webp' },
    { id: 4, url: '/assets/logo-sleep.webp' },
    { id: 5, url: '/assets/logo-happy.webp' }
  ];

  avatarMap = new Map<number, { url: string }>();

  constructor(private router: Router) { }

  ngOnInit() {
    // Inicializa o mapa de avatares para que o HTML consiga buscar as imagens por ID
    this.avatars.forEach(avatar => {
      this.avatarMap.set(avatar.id, { url: avatar.url });
    });
  }

  get sortedPlayers() {
    // Ordena do maior progresso para o menor
    return [...this.players].sort((a, b) => b.progress - a.progress);
  }

  roomId = 'ABCD123';

  goToLobby() {
    // Navega de volta para a sala (room) ['/game', this.roomId]
    this.router.navigate(['/room', this.roomId]);
  }
}