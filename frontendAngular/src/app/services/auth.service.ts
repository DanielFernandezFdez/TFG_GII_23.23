import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Router } from '@angular/router';
import Swal from 'sweetalert2'

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  //private apiUrl = 'http://127.0.0.1:5000';
  private apiUrl = 'https://tfg-gii-23-23.onrender.com';
  private usuarioActual = new BehaviorSubject<string | null>(null);
  usuarioActualValor = this.usuarioActual.asObservable();
  private token = new BehaviorSubject<string | null>(null);
  tokenValor = this.token.asObservable();
  private id = new BehaviorSubject<string | null>(null);
  idValor = this.token.asObservable();


  constructor(private http : HttpClient , private router: Router) { 
    this.cargarUsuarioActual();
    this.cargarToken();
    this.cargarId();
  }

  public get usuarioActualValue(): string | null {

    return this.usuarioActual.value;
  }

  public get tokenValue(): string | null {
    return this.token.value;
  }
  public get idValue(): string | null {
    return this.id.value;
  }
  

  private getHeaders() {
    let headers = new HttpHeaders();
    const token = localStorage.getItem('token'); 
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  private cargarUsuarioActual(): void {
    const usuario = localStorage.getItem('usuarioActual');
    if (usuario) {
      this.usuarioActual.next(usuario);
    }
  }
  private cargarToken(): void {
    const token = localStorage.getItem('token');
    if (token) {
      this.token.next(token);
    }
  }
  private cargarId(): void {
    const id = localStorage.getItem('id');
    if (id) {
      this.id.next(id);
    }
  }

  estaAutenticado(): boolean {
    return this.token != null;
  }


  login(datos: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/usuarios/login`, datos)
      .pipe(map(respuesta => {
        if (respuesta && respuesta.token) {


          localStorage.setItem('token', respuesta.token);
          localStorage.setItem('usuarioActual', respuesta.nombre);
          localStorage.setItem('id', respuesta.id);
  
          this.usuarioActual.next(respuesta.nombre);
          this.token.next(respuesta.token);
          this.id.next(respuesta.id);
          this.router.navigate(['/catalogo']);
          this.msgInicioCorrecto();
        }
      }),
      catchError(error => {
        if (error.status === 401) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Correo o contraseña incorrectos'
          });
        }
        throw error;
      }));
      
    }

  logout(): void {
    localStorage.removeItem('usuarioActual');
    localStorage.removeItem('token');
    localStorage.removeItem('id');
    this.usuarioActual.next(null);
    this.token.next(null);
    this.id.next(null);
    this.router.navigate(['/catalogo']);

  }

  registrarUsuario(datos: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/usuarios/registro`, datos, { headers: this.getHeaders() });
  }

  modificarUsuario(id: number, datos: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/usuarios/modificar_usuario/${id}`, datos, { headers: this.getHeaders() });
  }

  eliminarUsuario(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/usuarios/eliminar_usuario/${id}`, { headers: this.getHeaders() });
  }

  obtenerInfoUsuario(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/usuarios/info_usuario/${id}`, { headers: this.getHeaders() });
  }

  listarUsuarios(): Observable<any> {
    return this.http.get(`${this.apiUrl}/usuarios/usuarios`, { headers: this.getHeaders() });
  }







  msgInicioCorrecto= () => {
    const Toast = Swal.mixin({
      toast: true,
      position: "bottom-end",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
      }
    });
    Toast.fire({
      icon: "success",
      title: "Inicio de sesión exitoso"
    });
  }
}
