import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RoomService, User } from '../../core/services/room.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {
  name: string = '';
  roomId: string = ''; // Começa vazio para o modal
  showModal = false;
  isLoading = false; // Para dar feedback ao usuário
  selectedAvatarIndex: number = 0;

  constructor(
    private router: Router,
    private roomService: RoomService // Injeta o serviço que criamos
  ) {}

  avatars = [
    { id: 1, url: '/assets/characters/character_1.webp', name: 'bunny' },
    { id: 2, url: '/assets/characters/character_2.webp', name: 'kitty' },
    { id: 3, url: '/assets/characters/character_3.webp', name: 'puppy' },
    { id: 4, url: '/assets/characters/character_4.webp', name: 'fox' },
    { id: 5, url: '/assets/characters/character_5.webp', name: 'platypus' },
    { id: 6, url: '/assets/characters/character_6.webp', name: 'panda' },
    { id: 7, url: '/assets/characters/character_7.webp', name: 'little tiger' }
  ];

  ngOnInit() {
    // Define um avatar aleatório ao carregar a página
    this.selectedAvatarIndex = Math.floor(Math.random() * this.avatars.length);
  }

  get currentAvatar() {
    return this.avatars[this.selectedAvatarIndex];
  }

  nextAvatar() {
    this.selectedAvatarIndex = (this.selectedAvatarIndex + 1) % this.avatars.length;
  }

  // MÉTODO PARA CRIAR SALA (POST)
  createRoom() {
    if (!this.name.trim()) {
      alert('Por favor, digite seu nome antes de criar uma sala.');
      return;
    }

    this.isLoading = true;

    const userPayload: User = {
      id: "",
      name: this.name,
      is_host: true,
      avatar_id: this.currentAvatar.id
    };

    this.roomService.createRoom(userPayload).subscribe({
      next: (room) => {
        this.isLoading = false;
          userPayload.id = room.users.find(u => u.name === this.name)?.id || '';
          console.log('Sala criada com sucesso:', room);
          console.log('ID do usuário criado:', userPayload.id);
          localStorage.setItem('user_id', userPayload.id);

        // Navega para a sala com o ID REAL gerado pelo Python/Postgres
        this.router.navigate(['/room', room.id]);
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Erro ao criar sala:', err);
        alert('Erro ao conectar com o servidor RPC. Verifique se a API está rodando.');
      }
    });
  }

  // MÉTODOS DO MODAL
  openModal() {
    if (!this.name.trim()) {
      alert('Digite seu nome primeiro!');
      return;
    }
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.roomId = '';
  }

  confirmJoin() {

    if (!this.roomId.trim()) {
      alert('Digite o código da sala!');
      return;
    }

    if (!this.name.trim()) {
      alert('Digite seu nome primeiro!');
      return;
    }

    const payload = {
      id: "",
      name: this.name,
      is_host: false,
      avatar_id: this.currentAvatar.id,
      room_code: this.roomId.toUpperCase()
    };

    this.isLoading = true;

    this.roomService.joinRoom(payload).subscribe({
      next: (room) => {

        this.isLoading = false;
        localStorage.setItem('user_id', room.users.find(u => u.name === this.name)?.id || '');

        // 🚀 Agora você recebe a sala REAL do backend
        this.router.navigate(['/room', room.id]);

        this.closeModal();
      },
      error: (err) => {

        this.isLoading = false;

        console.error('Erro ao entrar na sala:', err);
        alert('Erro ao entrar na sala. Código inválido ou servidor offline.');
      }
    });
  }
}