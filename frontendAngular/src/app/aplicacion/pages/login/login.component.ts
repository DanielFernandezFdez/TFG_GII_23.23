import { Component } from '@angular/core';
import { AuthService } from '../../../services/auth.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  correo: string = '';
  contrasenya: string = '';
  

  constructor(private authService: AuthService) {}

  iniciarSesion() {
    this.authService.login({ correo: this.correo, contrasenya: this.contrasenya }).subscribe(
      respuesta => {
        console.log('Inicio de sesión exitoso');
        
      },
      error => {
        console.error('Error al iniciar sesión', error);
      }
    );
  }
}