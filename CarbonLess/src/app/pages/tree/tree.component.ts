import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzProgressModule } from 'ng-zorro-antd/progress';
import { NzTagModule } from 'ng-zorro-antd/tag';
import { NzGridModule } from 'ng-zorro-antd/grid';

@Component({
  selector: 'app-tree',
  standalone: true,
  imports: [
    CommonModule,
    NzCardModule,
    NzProgressModule,
    NzTagModule,
    NzGridModule
  ],
  templateUrl: './tree.component.html',
  styleUrls: ['./tree.component.scss']
})
export class TreeComponent {
  // Mock data
  monthlyProgress = 45;
  monthlyGoal = 100;

  milestones = [
    { percent: 25, label: 'Seedling', description: 'Your tree has sprouted!', achieved: true },
    { percent: 50, label: 'Growing', description: 'Leaves are appearing!', achieved: false },
    { percent: 75, label: 'Blooming', description: 'Flowers will bloom!', achieved: false },
    { percent: 100, label: 'Full Tree', description: 'Complete and thriving!', achieved: false }
  ];

  getTreeState(): string {
    if (this.monthlyProgress >= 76) return 'full';
    if (this.monthlyProgress >= 51) return 'blooming';
    if (this.monthlyProgress >= 26) return 'growing';
    return 'seedling';
  }

  getTreeEmoji(): string {
    const state = this.getTreeState();
    switch (state) {
      case 'full': return '🌳';
      case 'blooming': return '🌲';
      case 'growing': return '🌿';
      default: return '🌱';
    }
  }
}
