import { Component, OnInit } from '@angular/core';
import { RolesService } from '../../../services/roles.service';
import { BotonesService } from '../../../services/botones.service';
import { ActivatedRoute } from '@angular/router';


interface Permiso {
  alias: string;
  descripcion: string;
  activo: boolean;
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
  nombre:string;
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
    { alias: 'Gestión de usuarios', descripcion: 'Permite a los miembros ver los canales por defecto (excepto los privados).', activo: false ,  nombre: 'gestion-usuarios' },
    // ... otros permisos
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
    this.nombreRol = data.nombre;
    });

    this.BotonesService.listarBotones().subscribe((data: any) => {
      this.botones = data;
      this.botones.forEach(boton => {
        if(boton.roles_asociados.includes(this.nombreRol)){
          this.permisos.some(permiso => {
            if(permiso.nombre === boton.nombre){
              permiso.activo = true;
              return true;
            }
            return false;
          });
        }
      });
    });
  }




  onToggle(permiso: Permiso) {
    permiso.activo = !permiso.activo;
  }
}
