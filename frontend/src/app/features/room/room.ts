import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RoomService, Room_game, User } from '../../core/services/room.service';

@Component({
  selector: 'app-room',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './room.html',
  styleUrl: './room.scss',
})
export class Room {

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private roomService: RoomService,
    private cdr: ChangeDetectorRef
  ) {}

  roomId: string = '';
  room_code: string = '';
  room?: Room_game;
  players: User[] = [];
  is_host = false;
  loading = true;
  currentUserId: string | null = '';

  avatars = [
    { id: 1, name: 'water', url: '/assets/logo-water.webp' },
    { id: 2, name: 'run', url: '/assets/logo-run.webp' },
    { id: 3, name: 'ok', url: '/assets/logo-ok.webp' },
    { id: 4, name: 'sleep', url: '/assets/logo-sleep.webp' },
    { id: 5, name: 'happy', url: '/assets/logo-happy.webp' }
  ];

  avatarMap = new Map<number, { name: string; url: string }>();

  ngOnInit() {
    this.currentUserId = localStorage.getItem('user_id');

    // Criar mapa de avatars (isso está ok)
    this.avatars.forEach(avatar => {
      this.avatarMap.set(avatar.id, { name: avatar.name, url: avatar.url });
    });

    this.route.paramMap.subscribe(params => {
      this.roomId = params.get('id') || '';
      if (this.roomId) {
        this.loadRoom();
        
        // Inicia o socket através do serviço
        this.roomService.connectSocket(this.roomId);
      }
    });

    // Ouve se a sala foi atualizada (alguém entrou)
    this.roomService.roomUpdated$.subscribe(() => {
      this.loadRoom(); 
    });

    // Ouve se o jogo começou
    this.roomService.gameStarted$.subscribe((id) => {
      this.router.navigate(['/game', id]);
    });
  }

  loadRoom() {

    this.loading = true;

    this.roomService.getRoomById(this.roomId).subscribe({
      next: (room) => {

        console.log("ROOM RECEBIDA:", room);

        this.room = room;
        this.players = room.users;

        if (room.id_admin && this.currentUserId) {
          this.is_host = room.id_admin?.toLowerCase() === this.currentUserId?.toLowerCase();
        } else {
          this.is_host = false;
        }

        this.loading = false;
        this.cdr.detectChanges();

        console.log("Loading agora:", this.loading);
        console.log("É host?", this.is_host);
      },
      error: (err) => {
        console.error('Erro ao carregar sala:', err);
        this.loading = false;
      }
    });
  }

  copyRoomId() {
    if (this.room?.room_code) {
      navigator.clipboard.writeText(this.room.room_code);
    }
  }

  startGame() {
    if (!this.roomId) {
      console.error("Room ID não encontrado");
      return;
    }

    this.roomService.startGame(this.roomId, this.currentUserId!).subscribe({
      next: (game) => {
        console.log("Jogo iniciado:", game);

        // Só depois que o backend confirmou
        this.roomService.emitStartGame(this.roomId);
      },
      error: (err) => {
        console.error("Erro ao iniciar jogo:", err);
      }
    });
  }

  ngOnDestroy() {
    this.roomService.disconnectSocket();
  }

}