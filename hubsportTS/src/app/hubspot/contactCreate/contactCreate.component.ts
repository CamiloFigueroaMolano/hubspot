import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HubspotService } from '../services/hubspot.service';

@Component({
    selector: 'app-contact-create',
    templateUrl: './contactCreate.component.html',
    styleUrls: ['./contactCreate.component.css'],
})
export class ContactCreateComponent implements OnInit {


  newContactData: any;

  ngOnInit(): void {
    this.newContactData = {
      properties: {
        firstname: '',
        lastname: '',
        email: ''
      }
    };
  }

  constructor(  private hubSpotService: HubspotService,
                private router: Router
                ) {}

  public data: any[]=[];



  createContact(): void {
    this.hubSpotService.createContact('contacts',this.newContactData)
      .subscribe((response) => {
        this.data=response;
        console.log('Nuevo contacto creado:', this.data);
        this.router.navigate(['']);
      });
  }

}

