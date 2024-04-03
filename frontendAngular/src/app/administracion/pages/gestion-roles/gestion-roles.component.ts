import { Component } from '@angular/core';
import Swal from 'sweetalert2';
import { RolesService } from '../../../services/roles.service';
import { AuthService } from '../../../services/auth.service';


@Component({
  selector: 'app-gestion-roles',
  templateUrl: './gestion-roles.component.html',
  styleUrl: './gestion-roles.component.css'
})
export class GestionRolesComponent {
  roles: any[] = [];

  constructor(private RolesService: RolesService, private AuthService: AuthService) {}

  ngOnInit(): void {
    this.cargarRoles();
  }

  cargarRoles(): void {
    this.RolesService.obtenerRoles().subscribe({
      next: (data) => {
        this.roles = data;
      },
      error: (error) => {
        console.error('Error al obtener los roles', error);
      }
    });
  }

  editarRol(id: number): void {
    console.log('Editar usuario', id);
  }


  eliminarRol(id: number): void {
    Swal.fire({
      title: '¿Estás seguro?',
      text: 'No podrás recuperar el Rol',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar'
    }).then((result) => {
      if (result.isConfirmed) {
        //!Hay que comprobar si existen usuarios con ese rol. Si los hay, no se puede eliminar
        this.AuthService.listarUsuarios().subscribe({
          next: (data) => {
            for (let i = 0; i < data.length; i++) {
              if (data[i].rol_id === id) {
                Swal.fire('Error', 'No se puede eliminar el rol porque hay usuarios con ese rol', 'error');
                return;
              }
            }
          }
        });
        this.RolesService.borrarRol(id).subscribe({
          next: () => {
            Swal.fire('Rol eliminado', 'El Rol ha sido eliminado correctamente', 'success');
            this.cargarRoles();
            return;
          }
        });
      }
    });
  }
}
