import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ColaboradoresService {
  private apiUrl = 'https://tfg-gii-23-23.onrender.com'; 
  //private apiUrl = 'http://127.0.0.1:5000';
  constructor(private http: HttpClient) { }

  private getHeaders() {
    let headers = new HttpHeaders();
    const token = localStorage.getItem('token');
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }


  listarColaboradores(): Observable<any> {
    return this.http.get(`${this.apiUrl}/colaboradores/listarColaboradores`, { headers: this.getHeaders() });
  }

  crearColaboradores(datos: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/colaboradores/agregarColaborador`, datos, { headers: this.getHeaders() });
  }

  editarColaboradores(datos: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/colaboradores/editarColaborador`, datos, { headers: this.getHeaders() });
  }

  borraColaboradores(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/colaboradores/eliminarColaborador/${id}`, { headers: this.getHeaders() });
  }
}