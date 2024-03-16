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

  constructor(
    private route: ActivatedRoute,
    private LibrosService: LibrosService // Inyecta tu servicio de libros aquí
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
}
