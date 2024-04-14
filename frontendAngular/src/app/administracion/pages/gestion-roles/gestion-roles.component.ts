import { Component } from '@angular/core';
import Swal from 'sweetalert2';
import { RolesService } from '../../../services/roles.service';
import { AuthService } from '../../../services/auth.service';
import { Router } from '@angular/router';



@Component({
  selector: 'app-gestion-roles',
  templateUrl: './gestion-roles.component.html',
  styleUrl: './gestion-roles.component.css'
})
export class GestionRolesComponent {
  roles: any[] = [];
  Router: any;


  constructor(private RolesService: RolesService, private AuthService: AuthService, private router : Router) {}

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

  agregarRol(): void {
    Swal.fire({
      title: 'Agregar nuevo Rol',
      text: 'Ingrese el nombre del nuevo rol',
      inputPlaceholder: 'Mínimo 2 caracteres',
      input: 'text',
      inputAttributes: {
        autocapitalize: 'off'
      },
      showCancelButton: true,
      confirmButtonText: 'Guardar',
      showLoaderOnConfirm: true,
      preConfirm: (nombreRol:string) => {
        console.log(nombreRol);
        if (!nombreRol) {
          Swal.showValidationMessage("Debe ingresar un nombre para el rol");
          return;
        }
        if (nombreRol.length < 2) {
          Swal.showValidationMessage("El nombre del rol debe tener al menos 2 caracteres");
          return;
        }
        const nuevoRol = { nombre_rol: nombreRol.toString() };
  
        return this.RolesService.crearRol(nuevoRol).toPromise().then(response => {
          Swal.fire('Rol agregado', 'El Rol ha sido agregado correctamente', 'success');
          this.cargarRoles();
        }).catch(error => {
          Swal.fire('Error', 'Ha ocurrido un error al agregar el rol', 'error');
        });
      },
      allowOutsideClick: () => !Swal.isLoading()
    });
  }

  editarRol(id: number): void {
    Swal.fire({
      title: 'Editar Rol',
      text: 'Ingrese el nuevo nombre del rol',
      inputPlaceholder: 'Mínimo 2 caracteres',
      input: 'text',
      inputAttributes: {
        autocapitalize: 'off'
      },
      showCancelButton: true,
      confirmButtonText: 'Guardar',
      showLoaderOnConfirm: true,
      preConfirm: (nombreRol) => {
        if (!nombreRol) {
          Swal.showValidationMessage("Debe ingresar un nombre para el rol");
          return;
        }
        if (nombreRol.length < 2) {
          Swal.showValidationMessage("El nombre del rol debe tener al menos 2 caracteres");
          return;
        }
        const nuevoRol = { nombre_rol: nombreRol };
  
        return this.RolesService.editarRol(id, nuevoRol).toPromise().then(response => {
          Swal.fire('Rol editado', 'El Rol ha sido editado correctamente', 'success');
          this.cargarRoles();
        }).catch(error => {
          if (error.status == 406) {
            Swal.fire('Error', 'Nombre de rol existente', 'error');
            return;
          }
          Swal.fire('Error', 'Ha ocurrido un error al editar el rol', 'error');
        });
      },
      allowOutsideClick: () => !Swal.isLoading()
    });
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
        this.AuthService.listarUsuarios().subscribe({
          next: (data) => {
            for (let i = 0; i < data.length; i++) {
              console.log(data[i].rol_id);
              console.log(id);
              if (data[i].rol_id == id) {
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
          },
          error: (error) => {
           error.status == 400 ? Swal.fire('Error', 'Este rol no se puede eliminar', 'error') :
            Swal.fire('Error', 'Ha ocurrido un error al borrar el rol', 'error');
          }
        });
      }
    });
  }

  modificarPermisos(id:number): void {
    this.router.navigate(['/gestion-permisos', id]);
  }
              
}
