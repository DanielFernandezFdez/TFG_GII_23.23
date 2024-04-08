import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { EstimacionService } from '../../../services/estimacion.service';
import { MenuItem } from 'primeng/api';
import { SelectItem } from 'primeng/api';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-estimador',
  templateUrl: './estimador.component.html',
  styleUrls: ['./estimador.component.css']
})
export class EstimadorComponent implements OnInit {
  estimacionForm: FormGroup;
  actividades_produccion: string[] = [];
  actividades_poder: string[] = [];
  actividades_mantenimiento: string[] = [];
  resultadoEstimacion: number | null = null;
  activeIndex: number = 0;
  items: MenuItem[] = [];

  constructor(private fb: FormBuilder, private estimacionService: EstimacionService) {
    this.estimacionForm = this.fb.group({
      masculino_generico: [false],
      numero_ninyos: [0],
      numero_ninyas: [0],
      numero_hombres: [0],
      numero_mujeres: [0],
      res_actividades_hombre_produccion: [[]],
      res_actividades_hombre_poder: [[]],
      res_actividades_hombre_mantenimiento: [[]],
      res_actividades_mujer_produccion: [[]],
      res_actividades_mujer_poder: [[]],
      res_actividades_mujer_mantenimiento: [[]],
      ubicacion: [0]
    });
  }

  ngOnInit(): void {
    this.cargarListados();
  }


  ubicacionOptions: SelectItem[] = [
    { label: 'Mujeres solo en ambientes domésticos y hombres solo en ambientes exteriores', value: 0 },
    { label: 'Mujeres en ambientes domésticos y solo alguna en el exterior', value: 25 },
    { label: 'Hombres y mujeres en ambientes exteriores e interiores, pero hay desigualdad.', value: 50 },
    { label: 'Hombres y mujeres en ambientes exteriores e interiores, casi sin desigualdad', value: 75 },
    { label: 'Hombres y mujeres en ambientes exteriores e interiores por igual.', value: 100 }
  ];

  cargarListados(): void {
    this.estimacionService.obtenerListados().subscribe({
      next: (data) => {
        this.actividades_produccion = data.actividades_produccion;
        this.actividades_poder = data.actividades_poder;
        this.actividades_mantenimiento = data.actividades_mantenimiento;
      },
      error: (error) => {
        console.error('Hubo un error al obtener los listados', error);
      }
    });
  }

  calcularEstimacion(): void {
    const formValues = this.estimacionForm.value;


    const actividadesHombre = [
      ...formValues.res_actividades_hombre_produccion,
      ...formValues.res_actividades_hombre_poder,
      ...formValues.res_actividades_hombre_mantenimiento,
    ];

    const actividadesMujer = [
      ...formValues.res_actividades_mujer_produccion,
      ...formValues.res_actividades_mujer_poder,
      ...formValues.res_actividades_mujer_mantenimiento,
    ];

    const valoresEstimacion = {
      masculino_generico: formValues.masculino_generico,
      numero_ninyos: formValues.numero_ninyos,
      numero_ninyas: formValues.numero_ninyas,
      numero_hombres: formValues.numero_hombres,
      numero_mujeres: formValues.numero_mujeres,
      res_actividades_hombre: actividadesHombre,
      res_actividades_mujer: actividadesMujer,
      ubicacion: formValues.ubicacion.value,
    };
    if(valoresEstimacion.numero_hombres == 0 && valoresEstimacion.numero_mujeres == 0){
      Swal.fire("Error", "Debe introducir al menos un hombre o una mujer", "error");
      return;
    }
    if(valoresEstimacion.numero_ninyos == null || valoresEstimacion.numero_ninyas == null || valoresEstimacion.numero_hombres == null || valoresEstimacion.numero_mujeres == null){
      Swal.fire("Error", "Debe introducir un número en los campos vacios", "error");
      return;
    }
    if(valoresEstimacion.ubicacion == undefined) {
      Swal.fire("Error", "Debe seleccionar una ubicación", "error");
      return;
    }
    console.log(valoresEstimacion);


    this.estimacionService.calcularEstimacion(valoresEstimacion).subscribe({
      next: (resultado) => {
        this.resultadoEstimacion = resultado.resultado;
        Swal.fire({
          title: "Resultado del estudio:"+ this.resultadoEstimacion,
          text: "¿Le gustaría enviar los resultados para su estudio?",
          icon: "info",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Enviar datos",
          cancelButtonText:"No, gracias"
        }).then((result) => {
          if (result.isConfirmed) {
            //!Mostramos el formulario para guardar datos
          }
        });
      },
      error: (error) => {
        Swal.fire({
          title: "Ha ocurrido un error",
          icon: "error",
        })
      }
    });
  }
}

