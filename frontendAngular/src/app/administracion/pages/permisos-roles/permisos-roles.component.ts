import { Component, OnInit } from '@angular/core';
import { RolesService } from '../../../services/roles.service';
import { BotonesService } from '../../../services/botones.service';
import { ActivatedRoute } from '@angular/router';
import Swal from 'sweetalert2';


interface Permiso {
  alias: string;
  descripcion: string;
  permitido: boolean;
  nombre: string;
}

interface Boton{
  id:number;
  nombre:string;
  alias:string;
  roles_asociados: string[];
}


interface Rol{
  id:number;
  nombre_rol:string;
}


@Component({
  selector: 'app-permisos-roles',
  templateUrl: './permisos-roles.component.html',
  styleUrl: './permisos-roles.component.css'
})
export class PermisosRolesComponent implements OnInit{
  nombreRol: string ="";
  botones : Boton[] = []; 
  permisos: Permiso[] = [
    { alias: 'Gestión de usuarios', descripcion: 'Permite gestionar a los usuarios.', permitido: false ,  nombre: 'gestion-usuarios' },
    //!Meter mas permisos
  ];


  constructor(private RolesService: RolesService,  private BotonesService: BotonesService,private route: ActivatedRoute) {
    
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      const id = params['id'];
      this.obtenerPermisos(id);
    });
   
  }


  obtenerPermisos(id: number) {
    this.RolesService.consulatarRol(id).subscribe((data: Rol) => {
    this.nombreRol = data.nombre_rol;
    });

    this.BotonesService.listarBotones().subscribe((data: any) => {
      this.botones = data;
      this.botones.forEach(boton => {
        if(boton.roles_asociados.includes(this.nombreRol)){
          this.permisos.some(permiso => {
            if(permiso.nombre === boton.nombre){
              permiso.permitido = true;
              return true;
            }
            return false;
          });
        }
      });
    });
  }

  guardarCambios() {
    const datosParaEnviar = {
      botones: this.permisos.map(permiso => {

        const boton = this.botones.find(b => b.nombre === permiso.nombre);
        if (!boton) return null;
        

        return permiso.permitido ? 
          { nombre_boton: boton.nombre, roles_autorizados: this.nombreRol } : 
          { nombre_boton: boton.nombre, rol_solicitado: this.nombreRol };
      }).filter(boton => boton !== null)
    };
    this.BotonesService.editarBoton(datosParaEnviar).subscribe({
      next: (respuesta) => {
        Swal.fire('Guardado', 'Cambios guardados correctamente', 'success');

      },
      error: (error) => {
        Swal.fire('Error', 'Ha ocurrido un error al guardar los cambios', 'error');
      }
    });
  }


  onToggle(permiso: Permiso) {
    permiso.permitido = !permiso.permitido;
    console.log(permiso)
  }
}
