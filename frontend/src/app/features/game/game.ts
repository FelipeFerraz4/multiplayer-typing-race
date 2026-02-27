import { Component, OnInit, ViewChild, ElementRef, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './game.html',
  styleUrls: ['./game.scss']
})
export class Game implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private isBrowser = isPlatformBrowser(this.platformId);

  text: string = 'O rato roeu a roupa do rei de Roma enquanto corria pela floresta encantada.';
  typedText = '';
  currentIndex = 0;

  avatars = [
    { id: 1, name: 'water', url: '/assets/logo-water.webp' },
    { id: 2, name: 'run', url: '/assets/logo-run.webp' },
    { id: 3, name: 'ok', url: '/assets/logo-ok.webp' },
    { id: 4, name: 'sleep', url: '/assets/logo-sleep.webp' },
    { id: 5, name: 'happy', url: '/assets/logo-happy.webp' }
  ];

  avatarMap = new Map<number, { url: string }>();

  players = [
    { name: 'Ryan', avatarId: 1, progress: 0 },
    { name: 'João', avatarId: 5, progress: 0 },
    { name: 'Maria', avatarId: 3, progress: 0 },
    { name: 'Pedro', avatarId: 4, progress: 0 },
    { name: 'Lobo', avatarId: 2, progress: 0 }
  ];

  @ViewChild('textBox') textBox!: ElementRef;
  @ViewChild('hiddenInput') hiddenInput!: ElementRef;

  ngOnInit() {
    this.avatars.forEach(a => this.avatarMap.set(a.id, { url: a.url }));
  }

  get formattedText() {
    return this.text.split('').map((char, i) => ({
      char: char,
      isCorrect: i < this.currentIndex,
      isCurrent: i === this.currentIndex
    }));
  }

  onTyping() {
    this.currentIndex = this.typedText.length;
    this.players[4].progress = Math.min((this.currentIndex / this.text.length) * 100, 100);
    this.scrollToCurrent();

    if (this.currentIndex >= this.text.length) {
      setTimeout(() => alert('🏆 Você venceu!'), 200);
    }
  }

  scrollToCurrent() {
    if (!this.isBrowser) return;

    setTimeout(() => {
      const currentLetter = document.querySelector('.current') as HTMLElement;
      const textBox = this.textBox.nativeElement;

      if (currentLetter && textBox) {
        const offset = currentLetter.offsetLeft - (textBox.clientWidth / 2);
        textBox.scrollLeft = offset > 0 ? offset : 0;
      }
    }, 0);
  }

  focusInput() {
    this.hiddenInput.nativeElement.focus();
  }
}