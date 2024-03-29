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
  imagenPrevisualizada: string | ArrayBuffer | null = null;

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

  guardarLibro() {
    if (this.libroForm.valid) {
      const nuevoLibro = this.libroForm.value;
      this.libroService.agregarLibro(nuevoLibro,0).subscribe(
        (response) => {
        Swal.fire({
          icon: "success",
          title: "Libro agregado correctamente",
          showConfirmButton: false,
          timer: 1500
        });
        this.libroForm.reset();
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
