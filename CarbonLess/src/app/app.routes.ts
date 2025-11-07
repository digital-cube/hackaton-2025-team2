import { Routes } from '@angular/router';
import { MainFormComponent } from './main-form/main-form.component';
import { PromptDashboardComponent } from './prompt-dashboard/prompt-dashboard.component';
import { LoginComponent } from './auth/login/login.component';
import { authGuard } from './auth/auth.guard';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';
import { HomeComponent } from './pages/home/home.component';
import { TreeComponent } from './pages/tree/tree.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: 'home', component: HomeComponent },
      { path: 'categories', component: MainFormComponent },
      { path: 'tree', component: TreeComponent },
      { path: 'leaderboard', component: PromptDashboardComponent }, // Placeholder for now
      { path: 'statistics', component: PromptDashboardComponent }, // Placeholder for now
      { path: '', redirectTo: '/home', pathMatch: 'full' }
    ]
  }
];
