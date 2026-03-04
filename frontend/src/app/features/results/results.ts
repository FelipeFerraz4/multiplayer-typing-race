import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GameResult, RoomService } from '../../core/services/room.service';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results.html',
  styleUrl: './results.scss',
})
export class Results implements OnInit {

  players: GameResult[] = [];
  roomId: string = '';
  loading: boolean = true;

  avatars = [
    { id: 1, url: '/assets/characters/character_1.webp', name: 'bunny' },
    { id: 2, url: '/assets/characters/character_2.webp', name: 'kitty' },
    { id: 3, url: '/assets/characters/character_3.webp', name: 'puppy' },
    { id: 4, url: '/assets/characters/character_4.webp', name: 'fox' },
    { id: 5, url: '/assets/characters/character_5.webp', name: 'platypus' },
    { id: 6, url: '/assets/characters/character_6.webp', name: 'panda' },
    { id: 7, url: '/assets/characters/character_7.webp', name: 'little tiger' }
  ];

  avatarMap = new Map<number, { url: string, name: string }>();

  constructor(
    private router: Router,
    private route: ActivatedRoute, // Injetado para pegar o ID da URL
    private roomService: RoomService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.avatars.forEach(avatar => {
      this.avatarMap.set(avatar.id, { url: avatar.url, name: avatar.name });
    });

    // 1. Pega o ID da sala pela URL (ex: /results/ID-DA-SALA)
    this.route.paramMap.subscribe(params => {
      this.roomId = params.get('id') || '';
      if (this.roomId) {
        this.loadFinalResults();
      }
    });
  }

  loadFinalResults() {
    this.loading = true;

    // 1. Buscamos a sala para ter a lista de usuários e seus avatares
    this.roomService.getRoomById(this.roomId).subscribe({
      next: (room) => {
        const roomUsers = room.users;
        const gameId = room.game?.id;

        // 2. Buscamos os resultados finais
        if (!gameId) {
          console.error('Game ID not found');
          this.loading = false;
          return;
        }
        this.roomService.getResults(gameId).subscribe({
          next: (results) => {

            console.log('Resultados brutos:', results);
            // 3. Cruzamos os dados: adicionamos o avatar_id da sala nos resultados
            this.players = results.map(res => {
              const userInRoom = roomUsers.find(u => u.id === res.user_id);
              return {
                ...res,
                avatar_id: userInRoom ? userInRoom.avatar_id : 1 // fallback para avatar 1
              };
            });
            
            console.log('Resultados processados:', this.players);
            this.loading = false;
            this.cdr.detectChanges();
          },
          error: (err) => {
            console.error('Erro nos resultados:', err);
            this.loading = false;
          }
        });
      },
      error: (err) => {
        console.error('Erro ao buscar sala:', err);
        this.loading = false;
      }
    });
  }

  get sortedPlayers() {
    return [...this.players].sort((a, b) => a.position - b.position);
  }

  goToLobby() {
    this.router.navigate(['/room', this.roomId]);
  }
}