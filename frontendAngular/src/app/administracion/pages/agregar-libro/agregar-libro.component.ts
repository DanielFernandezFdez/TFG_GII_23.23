import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LibrosService } from '../../../services/libros.service';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-agregar-libro',
  templateUrl: './agregar-libro.component.html',
  styleUrls: ['./agregar-libro.component.css']
})
export class AgregarLibroComponent {
  libroForm: FormGroup;
  imagenPrevisualizada: string | null = null;


  constructor(private fb: FormBuilder, private libroService: LibrosService, private router:Router) {
    this.libroForm = this.fb.group({
      titulo: ['', Validators.required],
      isbn: ['', Validators.required],
      editorial: ['', Validators.required],
      descripcion: ['', Validators.required],
      anyo_publicacion: ['', Validators.required],
      puntuacion: [null, Validators.required],
      ubicacion_estudio: ['', Validators.required],
      url_imagen: ['', Validators.required],
      puntuacion_masculino_generico: [0, Validators.required],
      puntuacion_menores: [0, Validators.required],
      puntuacion_adultos: [0, Validators.required],
      puntuacion_ubicacion: [0, Validators.required],
      puntuacion_actividades: [0, Validators.required]
    });

    this.libroForm.get('url_imagen')?.valueChanges.subscribe((url) => {
      this.previsualizarImagen(url);
    });

    this.libroService.libroInfo.subscribe(libroInfo => {
      if (libroInfo) {
        this.prellenarFormulario(libroInfo);
      }
    });
  }

  prellenarFormulario(libroInfo: any) {
    this.libroForm.patchValue({
      titulo: libroInfo.titulo,
      isbn: libroInfo.isbn,
      editorial: libroInfo.editorial,
      descripcion: libroInfo.descripcion,
      anyo_publicacion: libroInfo.anyo_publicacion,
      url_imagen: libroInfo.url_imagen,
      

    });
    this.previsualizarImagen(libroInfo.url_imagen);
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
