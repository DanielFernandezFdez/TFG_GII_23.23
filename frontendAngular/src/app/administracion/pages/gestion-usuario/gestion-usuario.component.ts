import { Component, OnInit, ViewChild } from '@angular/core';
import { AuthService } from '../../../services/auth.service';
import Swal from 'sweetalert2';
import { RolesService } from '../../../services/roles.service';
import { OverlayPanel } from 'primeng/overlaypanel';


@Component({
  selector: 'app-gestion-usuario',
  templateUrl: './gestion-usuario.component.html',
  styleUrls: ['./gestion-usuario.component.css']
})
export class GestionUsuarioComponent implements OnInit {
  usuarios: any[] = [];
  roles: any[] = [];
  usuarioEditado: any = {};
  usuarioNuevo: any = {};

  @ViewChild('modificar') modificar?: OverlayPanel;
  @ViewChild('nuevo') nuevo?: OverlayPanel;

  constructor(private authService: AuthService, private rolesService:RolesService) {}

  ngOnInit(): void {
    this.cargarUsuarios();
    this.cargarRoles();
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

  cargarRoles(): void {
    this.rolesService.obtenerRoles().subscribe({
      next: (roles) => {
        this.roles = roles;
      },
      error: (error) => {
        console.error('Error al obtener los roles', error);
      }
    });
  }

  nuevoUsuario(event:MouseEvent): void {
    
    if(this.nuevo){
      this.nuevo.toggle(event);
    }
    
  }

  guardarCambiosNuevo(): void {
    this.authService.registrarUsuario(this.usuarioNuevo).subscribe({
      next: () => {
       Swal.fire({
          title: 'Usuario creado',
          text: 'La  contraseña por defecto es 12345678. El usuario deberá cambiarla en su primer acceso por seguridad',
          icon: 'success',
          showConfirmButton: true,
          confirmButtonText: 'Aceptar'
        });
        this.cargarUsuarios();
        if(this.nuevo){
          this.nuevo.hide();
          this.limpiarCampos();
        }
        
      },
      error: (error) => {
        this.cargarUsuarios();
        Swal.fire('Error', 'Ha ocurrido un error al crear el usuario', 'error');
        this.limpiarCampos();
      }
    });
  }

  limpiarCampos() {
    this.usuarioNuevo = {
      nombre: '',
      correo: '',
      rol: ''
    };
  }

  editarUsuario(id: number, event:MouseEvent): void {
    const usuario = this.usuarios.find(u => u.id === id);
    this.usuarioEditado = JSON.parse(JSON.stringify(usuario));

    if(this.modificar){
      this.modificar.toggle(event);
    }
    
  }
  guardarCambiosModificacion(): void {
    this.authService.modificarUsuario(this.usuarioEditado.id, this.usuarioEditado).subscribe({
      next: () => {
        Swal.fire({
          toast:true,
          position: 'top-end',
          icon: 'success',
          title: 'Usuario actualizado correctamente',
          showConfirmButton: false,
          timer: 1500
        });
        this.cargarUsuarios();
        if(this.modificar){
          this.modificar.hide();
        }
        
      },
      error: (error) => {
        this.cargarUsuarios();
        Swal.fire('Error', 'Ha ocurrido un error al actualizar el usuario', 'error');
      }
    });
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
