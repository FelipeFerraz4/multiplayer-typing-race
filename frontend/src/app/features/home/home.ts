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

  nickname: string = '';

  constructor(private router: Router) { }

  createRoom() {
    const roomId = Math.random().toString(36).substring(2, 8);
    this.router.navigate(['/room', roomId]);
  }

  joinRoom() {
    const roomId = prompt("Enter Room ID");
    if (roomId) {
      this.router.navigate(['/room', roomId]);
    }
  }
}