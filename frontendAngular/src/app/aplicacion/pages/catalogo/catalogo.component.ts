import { Component, OnInit } from '@angular/core';
import { LibrosService } from '../../../services/libros.service';
import { ActivatedRoute, Router } from '@angular/router';
import Swal from 'sweetalert2';
import { SugerenciaService } from '../../../services/sugerencia.service';

interface Sugerencia {
  nombre: string,
  apellidos: string,
  correo: string,
  titulo: string,
  isbn: string
}

@Component({
  selector: 'app-catalogo',
  templateUrl: './catalogo.component.html',
  styleUrl: './catalogo.component.css'
})
export class CatalogoComponent implements OnInit{
  libros: any[] =[];
  busqueda: string = '';
  fecha_modif: any;

  constructor(private LibrosService: LibrosService, private router : Router, private activatedRouter: ActivatedRoute, private  SugerenciaService: SugerenciaService ) {}

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
        Swal.fire({
          title: 'Error',
          text: 'No se han podido obtener los libros',
          icon: 'error'
        });
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


  crearSugerencia() {
    Swal.fire({
      title: 'Sugerir libro',
      html: `
      <input id="nombre" class="swal2-input" placeholder="Nombre">
      <input id="apellidos" class="swal2-input" placeholder="Apellidos">
      <input id="correo" class="swal2-input" placeholder="Correo">
      <input id="titulo" class="swal2-input" placeholder="Título">
      <input id="isbn" class="swal2-input" placeholder="ISBN">
      `,
      focusConfirm: false,
      preConfirm: () => {
        const nombre = (document.getElementById('nombre') as HTMLInputElement).value;
        const apellidos = (document.getElementById('apellidos') as HTMLInputElement).value;
        const correo = (document.getElementById('correo') as HTMLInputElement).value;
        const titulo = (document.getElementById('titulo') as HTMLInputElement).value;
        const isbn = (document.getElementById('isbn') as HTMLInputElement).value;

        if (!nombre || !apellidos || !correo || !titulo || !isbn) {
          Swal.showValidationMessage('Todos los campos son obligatorios');
        }

        return { nombre: nombre, apellidos: apellidos, correo: correo, titulo: titulo, isbn: isbn };
      }
    }).then((result) => {
      if (result.value) {
        const sugerencia: Sugerencia = result.value;
        this.SugerenciaService.crearSugerencia(sugerencia).subscribe({
          next: (data) => {
            Swal.fire({
              title: 'Sugerencia enviada',
              text: 'Gracias por tu sugerencia',
              icon: 'success'
            });
          },
          error: (error) => {
            console.error('Error al enviar la sugerencia', error);
            Swal.fire({
              title: 'Error',
              text: 'No se ha podido enviar la sugerencia',
              icon: 'error'
            });
          }
        });
      }
    });


  
  }
}