import { Component, OnInit } from '@angular/core';
import { LibrosService } from '../../../services/libros.service';
import { ActivatedRoute, Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-agregar-auto',
  templateUrl: './agregar-auto.component.html',
  styleUrl: './agregar-auto.component.css'
})
export class AgregarAutoComponent implements OnInit {
  libros: any[] = [];
  cargando: boolean = false;

  constructor(private librosService: LibrosService, private route: ActivatedRoute,private router : Router) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const elemento = params.get('elemento');
      if (elemento) {
        const nombreDecodificado = decodeURIComponent(elemento);
        this.cargarLibros(nombreDecodificado);
      }
    });
  }

  cargarLibros(elemento: string): void {
    this.cargando = true;
    this.librosService.buscarLibroAutomatico(elemento).subscribe({
      next: (data) => {
        this.libros = data;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Ha ocurrido un error al buscar los libros'
        });
      }
    });
  }

  elegirLibroParaAgregar(libro: any) {
    this.librosService.conexionLibroInfo(libro);
    this.router.navigate(['/agregar']);
  }


  irAgregarManual() {
    this.router.navigate(['/agregar']);
  }
  combinarFuentes(){
    this.router.navigate(['/combinar_auto']);
  }
}
