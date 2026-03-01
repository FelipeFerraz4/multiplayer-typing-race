import { Routes } from '@angular/router';
import { Home } from './features/home/home';
import { Room } from './features/room/room';
import { Game } from './features/game/game';
import { Results } from './features/results/results';

import { Rules } from './features/rules/rules'
import { About } from './features/about/about'

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'room/:id', component: Room },
    { path: 'game/:id', component: Game },
    { path: 'results/:id', component: Results },
    { path: 'rules', component: Rules},
    { path: 'about', component: About}
];