import { Component, OnInit } from '@angular/core';
import { LibrosService } from '../../../services/libros.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-agregar-auto',
  templateUrl: './agregar-auto.component.html',
  styleUrl: './agregar-auto.component.css'
})
export class AgregarAutoComponent implements OnInit {
  libros: any[] = [];
  cargando: boolean = false;

  constructor(private librosService: LibrosService, private route: ActivatedRoute) { }

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
        // Manejar error
      }
    });
  }
}
