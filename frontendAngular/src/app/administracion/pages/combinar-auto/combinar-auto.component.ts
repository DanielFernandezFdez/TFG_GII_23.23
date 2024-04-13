import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { LibrosService } from '../../../services/libros.service';

export interface Libro {
  auto_id: string;
  logo: string;
  disponible: boolean;
  titulo: string;
  isbn: string;
  editorial: string;
  descripcion: string;
  anyo_publicacion: string;
  url_imagen: string;
}


@Component({
  selector: 'app-combinar-auto',
  templateUrl: './combinar-auto.component.html',
  styleUrl: './combinar-auto.component.css'
})
export class CombinarAutoComponent implements OnInit{
  libroForm: FormGroup;
  imagenPrevisualizada: string | null = null;
  libros: Libro[] = [];
  opcionesTitulos: any[] = [];
  opcionesISBNs: any[] = [];
  opcionesEditoriales: any[] = [];
  opcionesDescripcion: any[] = [];
  opcionesAnyo_Publicacion: any[] = [];
  opcionesUrl_imagen: any[] = [];

  constructor(private fb: FormBuilder, private libroService: LibrosService, private router:Router) {
    this.libroForm = this.fb.group({
      titulo: ['', Validators.required],
      isbn: ['', Validators.required],
      editorial: ['', Validators.required],
      descripcion: ['', Validators.required],
      anyo_publicacion: ['', Validators.required],
      puntuacion: [null, Validators.required],
      ubicacion_estudio: ['', Validators.required],
      url_imagen: ['', Validators.required]
    });

    this.libroForm.get('url_imagen')?.valueChanges.subscribe((url) => {
      this.previsualizarImagen(url);
    });
  }

  ngOnInit(): void {
      this.obtenerLibros();
  }

  obtenerLibros(): void {
    this.libroService.listarLibrosAutomaticos().subscribe(
      (libros :  Libro[]) => {
        this.libros = libros;
        this.opcionesTitulos = libros.map(libro => ({ label: libro.titulo, value: libro.titulo }));
        this.opcionesISBNs = libros.map(libro => ({ label: libro.isbn, value: libro.isbn }));
        this.opcionesEditoriales = libros.map(libro => ({ label: libro.editorial, value: libro.editorial }));
        this.opcionesDescripcion = libros.map(libro => ({ label: libro.descripcion, value: libro.descripcion }));
        this.opcionesAnyo_Publicacion = libros.map(libro => ({ label: libro.anyo_publicacion, value: libro.anyo_publicacion }));
        this.opcionesUrl_imagen = libros.map(libro => ({ label: libro.url_imagen, value: libro.url_imagen }));

      },
      (error) => {
        Swal.fire({
          icon: "error",
          title: "Error al obtener los libros",
          showConfirmButton: false,
          timer: 1500
        });
      }
    );
  }

  guardarLibro() {
    if (this.libroForm.valid) {
      const nuevoLibro = this.libroForm.value;
      this.libroService.agregarLibro(nuevoLibro).subscribe(
        (response) => {
        Swal.fire({
          icon: "success",
          title: "Libro agregado correctamente",
          showConfirmButton: false,
          timer: 1500
        });
        this.libroForm.reset();
        this.imagenPrevisualizada = null;
        },
        (error) => {
          
          Swal.fire({
            icon: "error",
            title: "Error al agregar el libro",
            showConfirmButton: false,
            timer: 1500
          });
          this.libroForm.reset();
          
        }
      );
    }
  }

  previsualizarImagen(url: string) {
    if (url) {
      this.imagenPrevisualizada = url;
    }
  }
}
