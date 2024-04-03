import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../services/auth.service';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-gestion-usuario',
  templateUrl: './gestion-usuario.component.html',
  styleUrls: ['./gestion-usuario.component.css']
})
export class GestionUsuarioComponent implements OnInit {
  usuarios: any[] = [];

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.authService.listarUsuarios().subscribe({
      next: (data) => {
        this.usuarios = data;
      },
      error: (error) => {
        console.error('Error al obtener los usuarios', error);
      }
    });
  }

  editarUsuario(id: number): void {
    console.log('Editar usuario', id);
  }


  eliminarUsuario(id: number): void {
    Swal.fire({
      title: '¿Estás seguro?',
      text: 'No podrás recuperar el usuario',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar'
    }).then((result) => {
      if (result.isConfirmed) {
        this.authService.eliminarUsuario(id).subscribe({
          next: () => {
            Swal.fire('Usuario eliminado', 'El usuario ha sido eliminado correctamente', 'success');
            this.cargarUsuarios();
          }
        });
      }
    });
  }
}
