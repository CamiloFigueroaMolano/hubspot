import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Result } from '../interfaces/contacts.infertface';
import { HubspotService } from '../services/hubspot.service';

@Component({
  selector: 'app-contacts',
  templateUrl: './contacts.component.html',
  styleUrls: ['./contacts.component.scss']
})
export class ContactsComponent implements  OnInit {

ngOnInit(): void {
  this.getContacts();
}

    constructor(private hubSpotCrud: HubspotService,
        private route: ActivatedRoute,
        private router: Router,) {}

    public contacts?: any[];
    public data?: any[];
    errorMessage: string = '';
    errorMessage2: string = "No se encuentran coincidencias";
    contactosFiltrados: Result[] | null = [];
    searchText: string = '';
    hasTouchedSearch: boolean = false;


    getContacts(): void {
      this.hubSpotCrud.getItems("contacts")
      .subscribe(response => {
        if (!response) return ('No se encontraron contactos ');
        this.contacts = Object.values(response);
        this.data=this.contacts[0]
        return;
      })
    }

    redirectToCreateContact(): void {
      this.router.navigate(['/create']);
    }


    modificarContacto(id: string): void {
      this.router.navigate(['/', id]);
    }

    buscarContactos(): void {
      this.filtrarContactos();
      this.hasTouchedSearch = true;
    }

    filtrarContactos(): void {
      this.contactosFiltrados = this.contacts?.[0]?.filter((contacto: { id:string, properties: { firstname: string; lastname: string; email:string}; }) =>
        contacto.properties.firstname.toLowerCase().includes(this.searchText.toLowerCase()) ||
        contacto.properties.lastname.toLowerCase().includes(this.searchText.toLowerCase()) ||
        contacto.properties.email.toLowerCase().includes(this.searchText.toLowerCase()) ||
        contacto.id.includes(this.searchText)
      );
    }

    eliminarContacto(id: string): void {
      this.hubSpotCrud.eliminarContacto(id)
        .subscribe( () => {
            this.getContacts();
          },(error) => {
            console.error(error);
            this.errorMessage = 'Error al eliminar el contacto. Detalles del error: ' + error.message;
          }
        );
        }

    errorSearch():boolean{
      if(this.contactosFiltrados?.length == 0 &&  this.hasTouchedSearch === true ) return true;
      return false;
    }
}
