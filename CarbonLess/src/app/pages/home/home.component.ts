import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzStatisticModule } from 'ng-zorro-antd/statistic';
import { NzGridModule } from 'ng-zorro-antd/grid';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzProgressModule } from 'ng-zorro-antd/progress';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    NzCardModule,
    NzStatisticModule,
    NzGridModule,
    NzButtonModule,
    NzIconModule,
    NzProgressModule
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  // Mock data
  userName = 'User';
  monthlyProgress = 45;
  currentRank = 12;
  totalPoints = 1250;
  treeHealth = 'Growing';

  recentActivities = [
    { icon: 'car', text: 'Used public transport 3 times this week', points: '+30' },
    { icon: 'bulb', text: 'Saved energy by turning off lights', points: '+15' },
    { icon: 'smile', text: 'Recycled waste properly', points: '+20' }
  ];
}
