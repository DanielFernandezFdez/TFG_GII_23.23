import { Component, OnInit, ViewChild } from '@angular/core';
import { ColaboradoresService } from '../../../services/colaboradores.service';
import Swal from 'sweetalert2';
import { OverlayPanel } from 'primeng/overlaypanel';

@Component({
  selector: 'app-gestion-colaboradores',
  templateUrl: './gestion-colaboradores.component.html',
  styleUrl: './gestion-colaboradores.component.css'
})
export class GestionColaboradoresComponent implements OnInit {
  colaboradores: any[] = [];
  roles: any[] = [];
  colaboradorEditado: any = {};
  colaboradorNuevo: any = {};

  @ViewChild('modificar') modificar?: OverlayPanel;
  @ViewChild('nuevo') nuevo?: OverlayPanel;

  constructor(private colaboradoresService: ColaboradoresService) {}

  ngOnInit(): void {
    this.cargarColaboradores();
  }

  cargarColaboradores(): void {
    this.colaboradoresService.listarColaboradores().subscribe({
      next: (data) => {
        this.colaboradores = data;
      },
      error: (error) => {
        console.error('Error al obtener los colaboradores', error);
      }
    });
  }

  nuevoColaborador(event:MouseEvent): void {
    
    if(this.nuevo){
      this.nuevo.toggle(event);
    }
    
  }

  guardarCambiosNuevo(): void {
    this.colaboradoresService.crearColaboradores(this.colaboradorNuevo).subscribe({
      next: () => {
       Swal.fire({
          toast:true,
          position: 'top-end',
          title: 'Colaborador creado',
          icon: 'success',
          showConfirmButton: false,
          timer: 1500
        });
        this.cargarColaboradores();
        if(this.nuevo){
          this.nuevo.hide();
          this.limpiarCampos();
        }
        
      },
      error: (error) => {
        this.cargarColaboradores();
        Swal.fire('Error', 'Ha ocurrido un error al crear el colaborador', 'error');
        this.limpiarCampos();
      }
    });
  }

  limpiarCampos() {
    this.colaboradorNuevo = {
      nombre: '',
      apellido: '',
      institucion: ''
    };
  }

  editarColaborador(id: number, event:MouseEvent): void {
    const usuario = this.colaboradores.find(u => u.id === id);
    this.colaboradorEditado = JSON.parse(JSON.stringify(usuario));

    if(this.modificar){
      this.modificar.toggle(event);
    }
    
  }
  guardarCambiosModificacion(): void {
    this.colaboradoresService.editarColaboradores(this.colaboradorEditado).subscribe({
      next: () => {
        Swal.fire({
          toast:true,
          position: 'top-end',
          icon: 'success',
          title: 'Colaborador actualizado correctamente',
          showConfirmButton: false,
          timer: 1500
        });
        this.cargarColaboradores();
        if(this.modificar){
          this.modificar.hide();
        }
        
      },
      error: (error) => {
        this.cargarColaboradores();
        Swal.fire('Error', 'Ha ocurrido un error al actualizar el colaborador', 'error');
      }
    });
  }


  eliminarColaborador(id: number): void {
    Swal.fire({
      title: '¿Estás seguro?',
      text: 'No podrás recuperar el Colaborador',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar'
    }).then((result) => {
      if (result.isConfirmed) {
        this.colaboradoresService.borraColaboradores(id).subscribe({
          next: () => {
            Swal.fire('Colaborador eliminado', 'El Colaborador ha sido eliminado correctamente', 'success');
            this.cargarColaboradores();
          }
        });
      }
    });
  }
}
