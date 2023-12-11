import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ContactCreateComponent } from './contactCreate/contactCreate.component';
import { ContactsComponent } from './contacts/contacts.component';
import { EditContactComponent } from './editContact/editContact.component';

const routes: Routes = [
  {
    path:'',
    component: ContactsComponent
  },
  { path: ':id',
    component: EditContactComponent
  },
  { path: 'create',
    component: ContactCreateComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HubspotRoutingModule { }
