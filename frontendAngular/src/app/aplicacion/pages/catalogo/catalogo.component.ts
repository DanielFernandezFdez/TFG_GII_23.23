import { Component, OnInit } from '@angular/core';
import { LibrosService } from '../../../services/libros.service';
import { ActivatedRoute, Router } from '@angular/router';


@Component({
  selector: 'app-catalogo',
  templateUrl: './catalogo.component.html',
  styleUrl: './catalogo.component.css'
})
export class CatalogoComponent implements OnInit{
  libros: any[] =[];
  busqueda: string = '';
  fecha_modif: any;

  constructor(private LibrosService: LibrosService, private router : Router, private activatedRouter: ActivatedRoute ) {}

  ngOnInit(): void {
    this.cargaLibros();
    this.fecha();
    this.activatedRouter.queryParams.subscribe(params => {
      this.busqueda = params['q'] || '';
      this.cargaLibroBusqueda();
    });
  }

  cargaLibros(): void {
    this.LibrosService.listarLibros().subscribe({
      next: (data) => {
        this.libros = data;
      },
      error: (error) => {
        console.error('Error al obtener los libros', error);
      },
      complete: () => {
        console.log('Carga de libros completada');
      }
    });
  }

  cargaLibroBusqueda(): void {
    if (this.busqueda === '') {
      this.cargaLibros();
      return;
    }
    this.LibrosService.buscarLibro(this.busqueda).subscribe({
      next: (data) => {
        this.libros = data;
      },
      error: (error) => {
        console.error('Error al obtener los libros', error);
      },
      complete: () => {
        console.log('Carga de libros completada');
      }
    });
  }

  imagenPorDefecto(event: Event) {
    (event.target as HTMLImageElement).src = 'assets/images/imagen_no_disponible.webp';

  }

  masInformacion(id: number) {
    this.router.navigate(['/info_libro', id]);
  }

  fecha() {
    this.LibrosService.fecha().subscribe({
      next: (data) => {
        this.fecha_modif= data.dato;
        console.log(data);
      },
      error: (error) => {
        console.error('Error al obtener la fecha', error);
      },
      complete: () => {
        console.log('Carga de fecha completada');
      }
    });
  }

  
}