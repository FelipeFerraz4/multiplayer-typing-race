import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss',
})
export class Navbar {
  menuOpen = false;

  artigosOpen = false;
  ferramentasOpen = false;

  toggleMenu() {
    this.menuOpen = !this.menuOpen;

    // fecha accordions ao fechar o menu
    if (!this.menuOpen) {
      this.artigosOpen = false;
      this.ferramentasOpen = false;
    }
  }

}
