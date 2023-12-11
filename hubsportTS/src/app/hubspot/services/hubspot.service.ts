import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';
import { env } from '../environments/hubspot.environments';



@Injectable({
  providedIn: 'root'
})
export class HubspotService {


  private apiUrl: string = env.HUBSPOT_API_BASE_URL;
  private encabezados = new HttpHeaders({
    'Authorization': `Bearer ${env.BEARER_TOKEN}`,
    'Content-Type': 'application/json'
  });

  constructor(private httpClient: HttpClient) { }

  getItems(link:string ): Observable<any[]> {
    const url: string = `${this.apiUrl}/${link}`;
    const headers = this.encabezados;
    return this.httpClient.get<any[]>(url, { headers })
      .pipe(
        catchError((error) => {
          return throwError('Acción incorrecta. Detalles del error: ' + error.message);
        }));
  }

  getContactById(id: string): Observable<any> {
    const url: string = `${this.apiUrl}/contacts/${id}`;
    const headers = this.encabezados;
    return this.httpClient.get<any>(url, { headers })
      .pipe(
        catchError((error) => {
          return throwError('Error al obtener el contacto. Detalles del error: ' + error.message);
        })
      );
  }

  createContact(link:string , contactData: any): Observable<any> {
    const url: string =`${this.apiUrl}/${link}`;
    console.log(url)
    console.log(contactData)
    const headers = this.encabezados;
    return this.httpClient.post<any>(url, contactData, { headers })
      .pipe(
        catchError((error) => {
          return throwError('Error al crear el contacto. Detalles del error: ' + error.message);
        })
      );
  }

  updateContact(id: string, updatedData: any): Observable<any> {
    const url: string = `${this.apiUrl}/contacts/${id}`;
    const headers = this.encabezados;
    console.log(this.httpClient.patch<any>(url, updatedData, { headers }))
    return this.httpClient.patch<any>(url, updatedData, { headers })
      .pipe(
        catchError((error) => {
          return throwError('Error al actualizar el contacto. Detalles del error: ' + error.message);
        })
      );
  }


  eliminarContacto(id: string): Observable<any> {
    const url: string = `${this.apiUrl}/contacts/${id}`;
    const headers = this.encabezados
    return this.httpClient.delete<any>(url, { headers })
      .pipe(
        catchError((error) => {
          return throwError('Error al eliminar el contacto. Detalles del error: ' + error.message);
        })
      );
  }
}
