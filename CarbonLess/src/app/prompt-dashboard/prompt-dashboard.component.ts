import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { ReactiveFormsModule } from '@angular/forms';
import { FormGroup, FormControl } from '@angular/forms';
import { NzButtonModule } from 'ng-zorro-antd/button';

@Component({
  selector: 'app-prompt-dashboard',
  standalone: true,
  imports: [CommonModule, NzSelectModule, ReactiveFormsModule, NzButtonModule],
  templateUrl: './prompt-dashboard.component.html',
  styleUrls: ['./prompt-dashboard.component.scss']
})
export class PromptDashboardComponent {
  vehicleForm: FormGroup;
  foodForm: FormGroup;

  vehicles = [
    { label: 'Bike', value: 'bike' },
    { label: 'Car', value: 'car' },
    { label: 'On Foot', value: 'on_foot' }
  ];

  foods = [
    { label: 'Pizza', value: 'pizza' },
    { label: 'Burger', value: 'burger' },
    { label: 'Pasta', value: 'pasta' },
    { label: 'Sushi', value: 'sushi' },
    { label: 'Tacos', value: 'tacos' },
    { label: 'Salad', value: 'salad' },
    { label: 'Sandwich', value: 'sandwich' },
    { label: 'Steak', value: 'steak' },
    { label: 'Chicken', value: 'chicken' },
    { label: 'Fish', value: 'fish' },
    { label: 'Rice Bowl', value: 'rice_bowl' },
    { label: 'Soup', value: 'soup' },
    { label: 'Noodles', value: 'noodles' },
    { label: 'Curry', value: 'curry' },
    { label: 'Burrito', value: 'burrito' },
    { label: 'Ramen', value: 'ramen' }
  ];

  constructor() {
    this.vehicleForm = new FormGroup({
      vehicle: new FormControl(null)
    });

    this.foodForm = new FormGroup({
      food: new FormControl(null)
    });
  }

  submitVehicle() {
    console.log('Vehicle submitted:', this.vehicleForm.value);
    // Add your submission logic here
  }

  submitFood() {
    console.log('Food submitted:', this.foodForm.value);
    // Add your submission logic here
  }
}
