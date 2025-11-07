import { Routes } from '@angular/router';
import { MainFormComponent } from './main-form/main-form.component';
import { PromptDashboardComponent } from './prompt-dashboard/prompt-dashboard.component';
import { LeafletMapComponent } from './leaflet-map/leaflet-map';
import { LoginComponent } from './auth/login/login.component';
import { authGuard } from './auth/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'main-form', component: MainFormComponent, canActivate: [authGuard] },
  { path: 'prompt-dashboard', component: PromptDashboardComponent, canActivate: [authGuard] },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'leaflet', component: LeafletMapComponent, canActivate: [authGuard] }
];
