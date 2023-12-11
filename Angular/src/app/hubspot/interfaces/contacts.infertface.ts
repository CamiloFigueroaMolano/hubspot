
//estrcutura para envio de solicitudes a hubspot

export interface Ipropierty{
  properties : IConstacts
}

export interface IConstacts{
    id?         : number;
    firstname   : string;
    email       : string;
    lastname    : string;
}

// Estructura de respueta de hubspot

export interface IAnsweHubpot {
  results: Result[];
}

export interface Result {
  id:         string;
  properties: Properties;
  createdAt:  string;
  updatedAt:  string;
  archived:   boolean;
}

export interface Properties {
  createdate:       string;
  email:            string;
  firstname:        string;
  hs_object_id:     string;
  lastmodifieddate: string;
  lastname:         string;
}
