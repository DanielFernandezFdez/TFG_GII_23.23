import { Component,  OnInit } from '@angular/core';
import { ColaboradoresService } from '../../../services/colaboradores.service';

interface Colaborador {
  nombre: string;
  apellido: string;
  institucion: string;
  
}

@Component({
  selector: 'app-colaboradores',
  templateUrl: './colaboradores.component.html',
  styleUrls: ['./colaboradores.component.css']
})
export class ColaboradoresComponent implements OnInit{

colaboradores : Colaborador[] = [];

  constructor(public colaboradoresService : ColaboradoresService) {
  }

  ngOnInit(): void {
    this.obtenerColaboradores();
  }


  obtenerColaboradores() {
    this.colaboradoresService.listarColaboradores().subscribe((data: any) => {
      this.colaboradores = data;
    });
  }
}

