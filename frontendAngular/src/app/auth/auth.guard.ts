import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { BotonesService } from '../services/botones.service';
import Swal from 'sweetalert2';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router, private botonesService: BotonesService) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Promise<boolean> | boolean{
    if (this.authService.usuarioActualValor == null) {
      this.router.navigate(['/login']);
      return false;
    }
  
    const nombre_boton = state.url.split('/')[1];
    const idusuario = parseInt(this.authService.idValue ?? "0");
    if (nombre_boton == "panel-admin" && idusuario != 0){
      return true;
    }
    
  
    return this.getCurrentButton(nombre_boton, idusuario)
      .then(permitido => {
        if (permitido == 1) {
          return true;
        } else {
          Swal.fire({
            title: "Acción denegada",
            text: "No tiene permisos para acceder a esta página",
            icon: "error"
          });
          return false;
        }
      }).catch(error => {
        console.error('Error al consultar el botón:', error);
        this.router.navigate(['/login']);
        return false;
      });
    
 
  }

  getCurrentButton(nombre_boton: string, idUsuario: number): Promise<number> {
    return new Promise((resolve, reject) => {
      this.botonesService.consultarBoton([nombre_boton], idUsuario)
        .subscribe(
          (data) => {
            console.log(data);
            const permitido = data[0]?.autorizado || 0; 
            resolve(permitido);
          },
          (error) => {
            console.error('Error al consultar el botón:', error);
            reject(error);
          }
        );
    });
  }




}
