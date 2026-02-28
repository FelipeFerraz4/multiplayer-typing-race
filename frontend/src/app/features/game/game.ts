import { Component, OnInit, ViewChild, ElementRef, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './game.html',
  styleUrls: ['./game.scss']
})
export class Game implements OnInit {

  constructor(private router: Router) { }

  private platformId = inject(PLATFORM_ID);
  private isBrowser = isPlatformBrowser(this.platformId);

  text: string = 'O rato roeu a roupa do rei de Roma e o rei de roma roeu a roupa do rei dos ratos.';
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
    return this.text.split('').map((char, i) => {
      const isCurrent = i === this.currentIndex;
      // Capturamos o que o usuário digitou nessa posição se houver erro
      const wrongChar = (isCurrent && this.isError) ? this.typedText[i] : null;

      return {
        char: char,
        isCorrect: i < this.currentIndex,
        isCurrent: isCurrent,
        isWrong: isCurrent && this.isError,
        wrongChar: wrongChar // Letra errada para mostrar na etiqueta
      };
    });
  }

  roomId = 'ABCD123';

  // Adicione esta variável para gerenciar o estado de erro visual (opcional)
  isError = false;

  onKeydown(event: KeyboardEvent) {
    // 1. Permite Backspace para o usuário poder apagar se você permitir erros (opcional)
    if (event.key === 'Backspace') {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.typedText = this.text.substring(0, this.currentIndex);
        this.isError = false;
        this.updateProgress();
      }
      event.preventDefault(); // Evitamos o comportamento padrão do input
      return;
    }

    // 2. Ignora teclas de controle (Shift, Alt, etc)
    if (event.key.length > 1) return;

    const charDigitado = event.key;
    const charEsperado = this.text[this.currentIndex];

    console.log(`Pressionou: [${charDigitado}] | Esperado: [${charEsperado}]`);

    // 3. Checagem em tempo real
    if (charDigitado === charEsperado) {
      this.currentIndex++;
      this.isError = false;

      // Atualizamos o texto que aparece no input/tela
      this.typedText = this.text.substring(0, this.currentIndex);

      this.updateProgress();
      this.scrollToCurrent();
      this.checkVictory();
    } else {
      // ERRO: Não avançamos o índice e ativamos o efeito de erro
      this.isError = true;
      this.triggerErrorEffect();
      console.log('Erro! Tecla bloqueada.');
    }

    // 4. BLOQUEIO: Impedimos que a tecla seja escrita no input automaticamente
    // Nós mesmos controlamos o valor da string via código
    event.preventDefault();
  }

  updateProgress() {
    this.players[4].progress = Math.min((this.currentIndex / this.text.length) * 100, 100);
  }

  checkVictory() {
    if (this.currentIndex >= this.text.length) {
      setTimeout(() => this.router.navigate(['/results', this.roomId]), 200);
    }
  }

  triggerErrorEffect() {
    // Exemplo de feedback: um pequeno "shake" na tela
    this.isError = true;
    setTimeout(() => this.isError = false, 200);
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