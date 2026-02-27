import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {

  name: string = '';

  constructor(private router: Router) { }

  roomId = 'ABCD123';

  createRoom() {
    this.router.navigate(['/room', this.roomId]);
  }

  showModal = false;

  openModal() {
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.roomId = '';
  }

  confirmJoin() {
    if (this.roomId.trim()) {
      this.router.navigate(['/room', this.roomId]);
      this.closeModal();
    }
  }
}