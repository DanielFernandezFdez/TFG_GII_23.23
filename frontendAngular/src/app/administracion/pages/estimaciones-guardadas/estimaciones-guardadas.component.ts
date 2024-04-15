import { Component, OnInit } from '@angular/core';
import { EstimacionService } from '../../../services/estimacion.service';
import Swal from 'sweetalert2';


interface Estimacion {
  id: number,
  masculino_generico: boolean, 
  numero_ninyas: number,
  numero_ninyos: number,
  numero_hombres: number
  numero_mujeres: number
  ubicacion: number, 
  res_actividades_hombre: string,
  res_actividades_mujer: string,
  titulo: string,
  isbn: string,
  nombre: string,
  apellido: string,
  correo: string,
  institucion: string,
}



@Component({
  selector: 'app-estimaciones-guardadas',
  templateUrl: './estimaciones-guardadas.component.html',
  styleUrl: './estimaciones-guardadas.component.css'
})
export class EstimacionesGuardadasComponent implements OnInit {

  estimaciones: Estimacion[] = [];
  constructor(private EstimacionService: EstimacionService) {

  }

  ngOnInit(): void {
    this.cargarEstimaciones()
  }

  cargarEstimaciones(): void {
    this.EstimacionService.listarEstimaciones().subscribe({
      next: (data) => {
        this.estimaciones = data;
      },
      error: (error) => {
       Swal.fire({
          title: "Error",
          text: "No se han podido cargar las estimaciones",
          icon: "error"
        });
      }
    });
  }


  eliminarEstimacion(id: number): void {
    this.EstimacionService.borrarEstimacion(id).subscribe({
      next: (data) => {
        Swal.fire({
          title: "Estimación eliminada",
          text: "La estimación ha sido eliminada correctamente",
          icon: "success"
        });
        this.cargarEstimaciones();

      },
      error: (error) => {
        Swal.fire({
          title: "Error",
          text: "No se ha podido eliminar la estimación",
          icon: "error"
        });
      }
    });
  }


  masInformacion(estimacion: Estimacion): void {
    Swal.fire({
      title: "Información de la estimación",
      html: `
      <p><strong>Título:</strong> ${estimacion.titulo}</p>
      <p><strong>ISBN:</strong> ${estimacion.isbn}</p>
      <p><strong>Nombre:</strong> ${estimacion.nombre}</p>
      <p><strong>Apellido:</strong> ${estimacion.apellido}</p>
      <p><strong>Correo:</strong> ${estimacion.correo}</p>
      <p><strong>Institución:</strong> ${estimacion.institucion}</p>
      <p><strong>Ubicación:</strong> ${estimacion.ubicacion}</p>
      <p><strong>Actividades hombre:</strong> ${estimacion.res_actividades_hombre}</p>
      <p><strong>Actividades mujer:</strong> ${estimacion.res_actividades_mujer}</p>
      `,
      icon: "info"
    });
  }






}
