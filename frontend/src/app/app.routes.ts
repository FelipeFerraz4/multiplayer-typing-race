import { Routes } from '@angular/router';
import { Home } from './features/home/home';
import { Room } from './features/room/room';
import { Game } from './features/game/game';
import { Results } from './features/results/results';

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'room/:id', component: Room },
    { path: 'game/:id', component: Game },
    { path: 'results/:id', component: Results }
];