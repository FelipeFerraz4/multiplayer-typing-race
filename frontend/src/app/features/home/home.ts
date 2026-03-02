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

  constructor(
    private router: Router,
    private roomService: RoomService // Injeta o serviço que criamos
  ) {}

  // MÉTODO PARA CRIAR SALA (POST)
  createRoom() {
    if (!this.name.trim()) {
      alert('Por favor, digite seu nome antes de criar uma sala.');
      return;
    }

    this.isLoading = true;

    const userPayload: User = {
      id: btoa(this.name + Math.random()).substring(0, 8), // Gera um ID único simples
      name: this.name,
      is_host: true,
      avatar_id: 1 // Pode ser fixo por enquanto
    };

    this.roomService.createRoom(userPayload).subscribe({
      next: (room) => {
        this.isLoading = false;
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
    if (this.roomId.trim()) {
      // No futuro, aqui chamaremos o "joinRoom" no Service
      // Por enquanto, apenas navegamos com o ID digitado
      this.router.navigate(['/room', this.roomId.toUpperCase()]);
      this.closeModal();
    }
  }
}