import { Component } from '@angular/core';
import { NzInputModule } from 'ng-zorro-antd/input';

@Component({
  selector: 'app-prompt-dashboard',
  standalone: true,
  imports: [NzInputModule],
  templateUrl: './prompt-dashboard.component.html',
  styleUrls: ['./prompt-dashboard.component.scss']
})
export class PromptDashboardComponent {
  value: any = '';
}
