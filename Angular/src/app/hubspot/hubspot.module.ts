import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { FormsModule } from '@angular/forms';
import { ContactCreateComponent } from './contactCreate/contactCreate.component';
import { ContactsComponent } from './contacts/contacts.component';
import { EditContactComponent } from './editContact/editContact.component';
import { HubspotRoutingModule } from './hubspot-routing.module';


@NgModule({
  declarations: [
    ContactsComponent,
    EditContactComponent,
    ContactCreateComponent,
  ],
  imports: [
    CommonModule,
    HubspotRoutingModule,
    FormsModule
  ]
})
export class HubspotModule { }
