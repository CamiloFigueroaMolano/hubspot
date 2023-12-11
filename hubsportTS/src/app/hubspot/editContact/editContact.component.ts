
import { Component, type OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HubspotService } from '../services/hubspot.service';

@Component({
    selector: 'app-edit-contact',
    templateUrl: './editContact.component.html',
    styleUrls: ['./editContact.component.css'],
})
export class EditContactComponent implements OnInit {

  contactId: string = '';
  contactData: any = {};
  public data? :any;
  updatedData: any = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private hubSpotCrud: HubspotService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.contactId = params['id'];
      this.loadContactData();
    });
  }

  loadContactData(): void {
    this.hubSpotCrud.getContactById(this.contactId)
      .subscribe(response => {
        this.contactData = response;
        this.data ={
            "properties": {
                "email": this.contactData.properties.email,
                "firstname": this.contactData.properties.firstname,
                "lastname": this.contactData.properties.lastname
            }
          }
        this.updatedData = { properties: {} }
        }
        );
  }

  updateData(property: string, event: any): void {
    const value = event?.target?.value;
    if (value !== null && value !== undefined) {
        if(property === 'email') this.data.properties.email= value;
        if(property === 'firstname')this.data.properties.firstname= value;
        if(property === 'lastname') this.data.properties.lastname= value;
        return;
    }
  }


  saveChanges(): void {
    console.log('Datos antes de guardar:', this.data);
  this.hubSpotCrud.updateContact(this.contactId, this.data)
    .subscribe(response => {
      console.log('Respuesta del servidor:', response);
      this.router.navigate(['/']);
    });
  }

  goBack(): void {
    // Navega de vuelta a la lista de contactos
    this.router.navigate(['/']);
  }
}
