import { AfterViewInit, Component, OnInit, ViewChild, ElementRef, inject, PLATFORM_ID, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { RoomService } from '../../core/services/room.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './game.html',
  styleUrls: ['./game.scss']
})
export class Game implements OnInit, AfterViewInit, OnDestroy {

  roomId: string = '';
  userId: string = '';
  gameId: string = '';
  players: any[] = []; // Iniciar vazio, preencher do backend
  startTime: number = 0;
  avatarMap = new Map<number, { url: string }>();

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private roomService: RoomService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
    console.log('Componente Game destruído: Limpando listeners mas mantendo socket vivo.');
  }

  ngOnInit() {
    this.avatars.forEach(a => this.avatarMap.set(a.id, { url: a.url }));

    this.userId = localStorage.getItem('user_id') || '';
    
    this.route.paramMap.subscribe(params => {
      this.roomId = params.get('id') || '';
      if (this.roomId) {
        this.loadGameData();
        this.setupWebsocket();
      }
    });
  }

  avatars = [
    { id: 1, name: 'water', url: '/assets/logo-water.webp' },
    { id: 2, name: 'run', url: '/assets/logo-run.webp' },
    { id: 3, name: 'ok', url: '/assets/logo-ok.webp' },
    { id: 4, name: 'sleep', url: '/assets/logo-sleep.webp' },
    { id: 5, name: 'happy', url: '/assets/logo-happy.webp' }
  ];

  private subscriptions: Subscription = new Subscription();

  private platformId = inject(PLATFORM_ID);
  private isBrowser = isPlatformBrowser(this.platformId);

  text: string = 'O rato roeu a roupa do rei de Roma e o rei de roma roeu a roupa do rei dos ratos.';
  typedText = '';
  currentIndex = 0;

  loadGameData() {
    // Busca o texto e os jogadores iniciais da API Flask
    this.roomService.getRoomById(this.roomId).subscribe(room => {
      this.text = room.game?.text || '';

      this.players = room.users.map((u: any) => ({
        id: u.id,
        name: u.name,
        avatarId: u.avatar_id,
        progress: 0
      }));

      console.log('Dados do jogo carregados:', { text: this.text, players: this.players, room: room });

      this.startTime = Date.now();
      this.cdr.detectChanges();
    });
  }

  setupWebsocket() {
    const sub = this.roomService.progressUpdate$.subscribe((data: any) => {
      const player = this.players.find(p => p.id === data.user_id);
      if (player && data.user_id !== this.userId) {
        player.progress = data.progress;
        this.cdr.detectChanges();
      }
    });
    this.subscriptions.add(sub);
  }

  updateProgress() {
    if (!this.text.length) return;

    const progress = (this.currentIndex / this.text.length) * 100;

    // Atualiza localmente o seu avatar
    const me = this.players.find(p => p.id === this.userId);
    if (me) me.progress = progress;

    // Envia para o servidor via Socket (para atualizar os outros)
    this.roomService.sendProgress(this.roomId, this.userId, progress);
    
    // Opcional: Enviar para a API REST via POST para persistência/estatísticas
    // conforme o seu progress_update_model
  }

  checkVictory() {
    if (this.currentIndex >= this.text.length) {
      const elapsed = (Date.now() - this.startTime) / 1000;
      // Notifica o backend que você terminou
      this.router.navigate(['/results', this.roomId]);
    }
  }

  @ViewChild('textBox') textBox!: ElementRef;
  @ViewChild('hiddenInput') hiddenInput!: ElementRef;

  // 3. Adicione este método
  ngAfterViewInit() {
    // Verificamos se estamos no navegador para evitar erros de SSR
    if (this.isBrowser) {
      this.focusInput();
    }
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