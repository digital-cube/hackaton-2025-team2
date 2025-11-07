import { Component } from '@angular/core';
import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-main-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './main-form.component.html',
  styleUrls: ['./main-form.component.scss']
})
export class MainFormComponent {
  mainForm = new FormGroup({
    location: new FormControl(''),
    transport: new FormControl(''),
    days: new FormControl('')
  })

  onSubmit() {
    console.log('forma submit', this.mainForm)
  }
}
