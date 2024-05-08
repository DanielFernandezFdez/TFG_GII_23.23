import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BotonesService {
  private apiUrl = 'http://127.0.0.1:5000'; 

  constructor(private http: HttpClient) { }

  private getHeaders() {
    let headers = new HttpHeaders();
    const token = localStorage.getItem('token');
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  consultarBoton(nombresBotones: string[], id:number): Observable<any> {
    return this.http.post(`${this.apiUrl}/botones/consultar_boton/${id}`, {nombre_botones: nombresBotones}, { headers: this.getHeaders() });
  }

  listarBotones(): Observable<any> {
    return this.http.get(`${this.apiUrl}/botones/buscar_botones`, { headers: this.getHeaders() });
  }

  crearBoton(datos: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/botones/crear_boton`, datos, { headers: this.getHeaders() });
  }

  editarBoton(datos: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/botones/editar_boton`, datos, { headers: this.getHeaders() });
  }

  borrarBoton(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/botones/borrar_boton/${id}`, { headers: this.getHeaders() });
  }
}