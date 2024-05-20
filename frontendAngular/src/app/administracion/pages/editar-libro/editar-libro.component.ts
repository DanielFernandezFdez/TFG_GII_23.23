import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { LibrosService } from '../../../services/libros.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-editar-libro',
  templateUrl: './editar-libro.component.html',
  styleUrls: ['./editar-libro.component.css']
})
export class EditarLibroComponent implements OnInit {
  libroForm: FormGroup;
  imagenPrevisualizada: string | ArrayBuffer | null = null;
  libroId: string = '';

  constructor(
    private fb: FormBuilder, 
    private libroService: LibrosService, 
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.libroForm = this.fb.group({
      titulo: ['', Validators.required],
      isbn: ['', Validators.required],
      editorial: ['', Validators.required],
      descripcion: ['', Validators.required],
      anyo_publicacion: ['', Validators.required],
      puntuacion: [null, Validators.required],
      ubicacion_estudio: [''],
      url_imagen: ['', Validators.required],
      puntuacion_masculino_generico: [0, Validators.required],
      puntuacion_menores: [0, Validators.required],
      puntuacion_adultos: [0, Validators.required],
      puntuacion_ubicacion: [0, Validators.required],
      puntuacion_actividades: [0, Validators.required]
    });
  }

  ngOnInit() {
    this.libroId = this.route.snapshot.paramMap.get('id') as string;
    this.libroService.obtenerInfoLibro(parseInt(this.libroId)).subscribe(libro => {
      this.libroForm.patchValue(libro);
      this.previsualizarImagen(libro.url_imagen);
    });
  }

  guardarLibro() {
    if (this.libroForm.valid) {
      const libroActualizado = this.libroForm.value;
      this.libroService.editarLibro(parseInt(this.libroId),libroActualizado).subscribe(
        response => {
          Swal.fire("Éxito", "Libro actualizado correctamente", "success");
          this.router.navigate(['/gestion-catalogo']);
        },
        error => {
          Swal.fire("Error", "Hubo un problema al actualizar el libro", "error");
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