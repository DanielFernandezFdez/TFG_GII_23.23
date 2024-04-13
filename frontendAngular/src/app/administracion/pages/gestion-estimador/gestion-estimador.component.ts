import { Component, OnInit } from '@angular/core';
import Swal from 'sweetalert2';
import { EstimacionService } from '../../../services/estimacion.service';
import { ChangeDetectorRef } from '@angular/core';
import { Table } from 'primeng/table';
import { ViewChild } from '@angular/core';

export interface Actividad {
  nombre: string;
  categoria: string;
  Puntuacion_extra: string;
}




@Component({
  selector: 'app-gestion-estimador',
  templateUrl: './gestion-estimador.component.html',
  styleUrl: './gestion-estimador.component.css'
})
export class GestionEstimadorComponent implements OnInit{
  @ViewChild('dt') dataTable!: Table ;
  actividades_produccion: any[] = [];
  actividades_poder: any[] = [];
  actividades_mantenimiento: any[] = [];
  actividades_hombre: any[] = [];
  actividades_mujer: any[] = [];
  Actividades: Actividad[] = [];


  constructor( private estimadorService : EstimacionService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.cargarActividades();
  }

  cargarActividades(): void {
    
    
    this.estimadorService.obtenerListados().subscribe({
      next: (data) => {
        this.actividades_produccion = data.actividades_produccion;
        this.actividades_poder = data.actividades_poder;
        this.actividades_mantenimiento = data.actividades_mantenimiento;
        this.actividades_hombre = data.actividades_hombre;
        this.actividades_mujer = data.actividades_mujer;
        this.Actividades=[]
        this.organizarActividades();
        this.cdr.detectChanges();
    this.dataTable.reset();
      },
      error: (error) => {
        console.error('Error al obtener las  actividades', error);
      }
    });
  }

  organizarActividades(): void {
    this.actividades_produccion.forEach((actividad) => {
      var puntuacion_extra = '';
      if(this.actividades_hombre.includes(actividad)){
        puntuacion_extra = 'Hombre';
      }
      if(this.actividades_mujer.includes(actividad)){
        puntuacion_extra = 'Mujer';
      }
      this.Actividades.push({
        nombre: actividad,
        categoria: 'Producción',
        Puntuacion_extra: puntuacion_extra
      });
    });

    this.actividades_poder.forEach((actividad) => {
      var puntuacion_extra = '';
      if(this.actividades_hombre.includes(actividad)){
        puntuacion_extra = 'Hombre';
      }
      if(this.actividades_mujer.includes(actividad)){
        puntuacion_extra = 'Mujer';
      }
      this.Actividades.push({
        nombre: actividad,
        categoria: 'Poder',
        Puntuacion_extra: puntuacion_extra
      });
    });
    this.actividades_mantenimiento.forEach((actividad) => {
      var puntuacion_extra = '';
      if(this.actividades_hombre.includes(actividad)){
        puntuacion_extra = 'Hombre';
      }
      if(this.actividades_mujer.includes(actividad)){
        puntuacion_extra = 'Mujer';
      }
      this.Actividades.push({
        nombre: actividad,
        categoria: 'Mantenimiento',
        Puntuacion_extra: puntuacion_extra
      });
    });
    
  }


  crearActividad(): void {
    Swal.fire({
      title: 'Crear Actividad',
      html:
        '<input id="nombre" class="swal2-input" placeholder="Nombre de la actividad">' +
        '<select id="categoria" class="swal2-input">' +
          '<option value="Producción">Producción</option>' +
          '<option value="Poder">Poder</option>' +
          '<option value="Mantenimiento">Mantenimiento</option>' +
        '</select>' +
        '<select id="puntuacion_extra" class="swal2-input">' +
          '<option value="Hombre">Hombre</option>' +
          '<option value="Mujer">Mujer</option>' +
        '</select>',
      showCancelButton: true,
      confirmButtonText: 'Crear',
      preConfirm: () => {
        const nombre = (document.getElementById('nombre') as HTMLInputElement).value;
        const categoria = (document.getElementById('categoria') as HTMLInputElement).value;
        const puntuacion_extra = (document.getElementById('puntuacion_extra') as HTMLInputElement).value;
        
        if (nombre === '') {
          Swal.showValidationMessage('El nombre de la actividad es obligatorio');
        }
      this.añadirActividad(nombre, categoria, puntuacion_extra);

      this.enviarListadosAlBackend(() => {
        this.cargarActividades();
      });
      

      }
  })
}

private añadirActividad(nombre: string, categoria: string, puntuacion_extra: string) {

  const nuevaActividad = nombre;
  if (categoria === 'Producción') {
    this.actividades_produccion.push(nuevaActividad);
  } else if (categoria === 'Poder') {
    this.actividades_poder.push(nuevaActividad);
  } else if (categoria === 'Mantenimiento') {
    this.actividades_mantenimiento.push(nuevaActividad);
  }

  if (puntuacion_extra === 'Hombre') {
    this.actividades_hombre.push(nuevaActividad);
  } else if (puntuacion_extra === 'Mujer') {
    this.actividades_mujer.push(nuevaActividad);
  }
}

private enviarListadosAlBackend(callback: () => void) {
  const listados = {
    actividades_produccion: this.actividades_produccion,
    actividades_poder: this.actividades_poder,
    actividades_mantenimiento: this.actividades_mantenimiento,
    actividades_hombre: this.actividades_hombre,
    actividades_mujer: this.actividades_mujer
  };
  this.estimadorService.GenerarListados(listados).subscribe({
    next: (respuesta) => {
      Swal.fire('¡Éxito!', 'La actividad ha sido creada.', 'success');
      callback();
    },
    error: (error) => {
      Swal.fire('Error', 'Hubo un problema al crear la actividad.', 'error');
    }
  });


}

borrarActividad(actividad: Actividad): void {
  Swal.fire({
    title: '¿Estás seguro?',
    text: "No podrás revertir esto.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Sí, borrarlo.'
  }).then((result) => {
    if (result.isConfirmed) {

      this.eliminarActividad(actividad);
      this.enviarListadosAlBackend(() => {
        this.cargarActividades();
      });
      Swal.fire(
        '¡Borrado!',
        'La actividad ha sido eliminada.',
        'success'
      )
    }
  })
}

eliminarActividad(actividad: Actividad) {
  if (actividad.categoria === 'Producción') {
    this.actividades_produccion = this.actividades_produccion.filter(a => a !== actividad.nombre);
  }

  if (actividad.categoria === 'Poder') {
    this.actividades_poder = this.actividades_poder.filter(a => a !== actividad.nombre);
  }

  if (actividad.categoria === 'Mantenimiento') {
    this.actividades_mantenimiento = this.actividades_mantenimiento.filter(a => a !== actividad.nombre);
  }

  if (actividad.Puntuacion_extra === 'Hombre') {
    this.actividades_hombre = this.actividades_hombre.filter(a => a !== actividad.nombre);
  }

  if (actividad.Puntuacion_extra === 'Mujer') {
    this.actividades_mujer = this.actividades_mujer.filter(a => a !== actividad.nombre);
  }

  this.Actividades = this.Actividades.filter(a => a !== actividad);
}


editarActividad(actividadOriginal: Actividad): void {
  Swal.fire({
    title: 'Editar Actividad',
    html:
      `<input id="nombre" class="swal2-input" value="${actividadOriginal.nombre}" placeholder="Nombre de la actividad">` +
      `<select id="categoria" class="swal2-input">` +
        `<option value="Producción" ${actividadOriginal.categoria === 'Producción' ? 'selected' : ''}>Producción</option>` +
        `<option value="Poder" ${actividadOriginal.categoria === 'Poder' ? 'selected' : ''}>Poder</option>` +
        `<option value="Mantenimiento" ${actividadOriginal.categoria === 'Mantenimiento' ? 'selected' : ''}>Mantenimiento</option>` +
      `</select>` +
      `<select id="puntuacion_extra" class="swal2-input">` +
        `<option value="Hombre" ${actividadOriginal.Puntuacion_extra === 'Hombre' ? 'selected' : ''}>Hombre</option>` +
        `<option value="Mujer" ${actividadOriginal.Puntuacion_extra === 'Mujer' ? 'selected' : ''}>Mujer</option>` +
      `</select>`,
    showCancelButton: true,
    confirmButtonText: 'Guardar Cambios',
    preConfirm: () => {
      const nombre = (document.getElementById('nombre') as HTMLInputElement).value;
      const categoria = (document.getElementById('categoria') as HTMLInputElement).value;
      const puntuacion_extra = (document.getElementById('puntuacion_extra') as HTMLInputElement).value;

      if (nombre === '') {
        Swal.showValidationMessage('El nombre de la actividad es obligatorio');
        return;
      }

      this.actualizarActividad(actividadOriginal, { nombre, categoria, Puntuacion_extra: puntuacion_extra });
    }
  });
}


actualizarActividad(actividadOriginal: Actividad, actividadEditada: Actividad): void {
  this.eliminarActividad(actividadOriginal);
  this.añadirActividad(actividadEditada.nombre, actividadEditada.categoria, actividadEditada.Puntuacion_extra);


  this.enviarListadosAlBackend(() => {
    this.cargarActividades();
  });
}


}

