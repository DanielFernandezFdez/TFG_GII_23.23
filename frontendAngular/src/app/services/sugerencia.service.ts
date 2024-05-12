import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SugerenciaService {
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



  crearSugerencia(sugerencia: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/sugerencias/crear_sugerencia`, sugerencia, { headers: this.getHeaders() });
  }
}