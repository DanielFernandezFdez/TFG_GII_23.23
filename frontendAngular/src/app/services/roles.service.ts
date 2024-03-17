import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RolesService {
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

  obtenerRoles(): Observable<any> {
    return this.http.get(`${this.apiUrl}/roles`, { headers: this.getHeaders() });
  }

  crearRol(datos: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/crear_rol`, datos, { headers: this.getHeaders() });
  }

  editarRol(id: number, datos: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/editar_rol/${id}`, datos, { headers: this.getHeaders() });
  }

  borrarRol(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/borrar_rol/${id}`, { headers: this.getHeaders() });
  }
}