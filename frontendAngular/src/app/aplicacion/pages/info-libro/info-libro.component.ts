import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { LibrosService } from '../../../services/libros.service';

@Component({
  selector: 'app-info-libro',
  templateUrl: './info-libro.component.html',
  styleUrl: './info-libro.component.css'
})
export class InfoLibroComponent implements OnInit {
  libro: any;
  puntuacion: number = 0;
  valoresPuntuaciones: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private LibrosService: LibrosService
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = params['id']; 
      this.cargarLibro(id);
      
    });
  }

  cargarLibro(id: number): void {
    this.LibrosService.obtenerInfoLibro(id).subscribe({
      next: (data) => {
        this.libro = data;
        this.puntuacion = this.libro.puntuacion;
        this.establecerPuntuacion();
      },
      error: (error) => {
        console.error('Error al obtener los libros', error);
      },
      complete: () => {
        console.log('Carga de libros completada');
      }
    })
  };

  imagenPorDefecto(event: Event) {
    (event.target as HTMLImageElement).src = 'assets/images/imagen_no_disponible.webp';

  }

  establecerPuntuacion(): void {
    if (!this.libro.puntuacion_menores ) {
      this.valoresPuntuaciones = [
        { label: 'Masculino Genérico Max 20% :', color: '#34d399', value: this.libro.puntuacion_masculino_generico },
        { label: 'Puntuación adultos Max 30% :', color: '#60a5fa', value: this.libro.puntuacion_adultos },
        { label: 'Puntuación ubicación Max 20% :', color: '#c084fc', value: this.libro.puntuacion_ubicacion },
        { label: 'Puntuación Actividades Max 30% :', color: '#c084fc', value: this.libro.puntuacion_actividades }
      ]
    }
    else{
       this.valoresPuntuaciones = [
        { label: 'Masculino Genérico Max 20% :', color: '#34d399', value: this.libro.puntuacion_masculino_generico },
        { label: 'Puntuación menores Max 15% :', color: '#fbbf24', value: this.libro.puntuacion_menores },
        { label: 'Puntuación adultos Max 15% :', color: '#60a5fa', value: this.libro.puntuacion_adultos },
        { label: 'Puntuación ubicación Max 20% :', color: '#c084fc', value: this.libro.puntuacion_ubicacion },
        { label: 'Puntuación Actividades Max 30% :', color: '#c084fc', value: this.libro.puntuacion_actividades }
      ]
    }
  }





}
