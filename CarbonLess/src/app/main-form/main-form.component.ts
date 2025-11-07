import { Component } from '@angular/core';
import {FormGroup, FormControl, ReactiveFormsModule} from '@angular/forms';
import { NzInputModule } from 'ng-zorro-antd/input';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-main-form',
  standalone: true,
  imports: [ReactiveFormsModule, NzInputModule],
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
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
