import { Routes } from '@angular/router';
import { MainFormComponent } from './main-form/main-form.component';
import { PromptDashboardComponent } from './prompt-dashboard/prompt-dashboard.component';
import { StatsDashboardComponent } from './stats-dashboard/stats-dashboard';

export const routes: Routes = [
  { path: 'main-form', component: MainFormComponent },
  { path: 'prompt-dashboard', component: PromptDashboardComponent },
  { path: 'stats', component: StatsDashboardComponent }
];
