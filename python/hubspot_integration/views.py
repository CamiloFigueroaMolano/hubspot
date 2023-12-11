import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .forms import HubspotUserForm
from django.shortcuts import render, redirect

####################### TOKENS DE ACCESO Y CONECCION A HUBSPOT########################################

HUBSPOT_API_BASE_URL = "https://api.hubapi.com/crm/v3/objects/contacts/"
BEARER_TOKEN = "pat-na1-510d140a-4841-429b-8a02-2fa727f869b5"

##################### SE DA MANEJO A LOS ENDPONTS DESDE LOS TEMPLATAES TENIENDO INTERECCION CON EL USUARIO################

#Metodo para agregar usuario
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        form = HubspotUserForm(request.POST)
        if form.is_valid():
            # Obtener datos validados del formulario
            firstname = form.cleaned_data.get('firstname', '')
            lastname = form.cleaned_data.get('lastname', '')
            email = form.cleaned_data.get('email', '')

            # Crear el objeto de datos para enviar a HubSpot
            hubspot_data = {
                'properties': {
                    'email': email,
                    'firstname': firstname,
                    'lastname': lastname
                    # Puedes agregar más campos según sea necesario
                }
            }

            # URL de la API de HubSpot
            hubspot_url = 'https://api.hubapi.com/crm/v3/objects/contacts/'

            # Realizar la solicitud POST a HubSpot con manejo de excepciones
            try:
                response = requests.post(hubspot_url, json=hubspot_data,
                                         headers={"Authorization": f"Bearer {BEARER_TOKEN}",
                                                  "Content-Type": "application/json"})
                response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP no exitosos

                if response.status_code == 201:
                    # Redirigir a la lista de usuarios
                    return render(request, 'add_user.html',
                                  {'form': form, 'success_message': 'Usuario creado con éxito'})
                else:
                    return JsonResponse(
                        {'error': f'Error al crear usuario en HubSpot. Código de estado: {response.status_code}'}, status=500)
            except requests.exceptions.RequestException as e:
                error_message = f'Error al realizar la solicitud a HubSpot: {str(e)}'
                print(error_message)  # Imprimir el mensaje de error en la consola

                try:
                    # Intentar obtener más detalles desde la respuesta de la API
                    error_details = response.json()
                    print('Detalles del error:', error_details)
                except json.JSONDecodeError:
                    print('No se pudo decodificar el contenido de la respuesta como JSON')

                return JsonResponse({'error': error_message}, status=500)
    else:
        form = HubspotUserForm()

    return render(request, 'add_user.html', {'form': form})

#Metodo para listar usuarios
@csrf_exempt
@require_http_methods(["GET"])
def list_users(request):
    # Obtener el parámetro de paginación
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('size', 100)

    # Construir la URL de la solicitud
    url = HUBSPOT_API_BASE_URL + "?limit={size}&offset={offset}".format(
        size=page_size, offset=(page_number - 1) * page_size
    )

    # Realizar la solicitud a la API
    response = requests.get(url, headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    data = response.json().get('results', [])

    # Obtener solo las propiedades necesarias
    users = [{'id': user['id'],
              'email': user['properties']['email'],
              'firstname': user['properties']['firstname'],
              'lastname': user['properties']['lastname']} for user in data]

    return render(request, 'list_users.html', {'users': users, 'page_number': page_number})

#Metodo para modificar usuarios
@csrf_exempt
def update_user(request, user_id):
    if request.method == 'POST':
        form = HubspotUserForm(request.POST)
        if form.is_valid():
            # Crear el objeto de datos para enviar a HubSpot
            hubspot_data = {
                'properties': {
                    'email': form.cleaned_data['email'],
                    'firstname': form.cleaned_data['firstname'],
                    'lastname': form.cleaned_data['lastname']
                    # Puedes agregar más campos según sea necesario
                }
            }

            # URL de la API de HubSpot para actualizar un contacto específico
            hubspot_url = f'https://api.hubapi.com/crm/v3/objects/contacts/{user_id}'

            # Realizar la solicitud PATCH a HubSpot con manejo de excepciones
            try:
                response = requests.patch(hubspot_url, json=hubspot_data,
                                          headers={"Authorization": f"Bearer {BEARER_TOKEN}",
                                                   "Content-Type": "application/json"})
                response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP no exitosos

                if response.status_code == 200:
                    # Redirigir a la lista de usuarios o a una página de éxito
                    return render(request, 'add_user.html',
                                  {'form': form, 'success_message': 'Usuario modificado con éxito'})
                else:
                    return JsonResponse(
                        {'error': f'Error al actualizar usuario en HubSpot. Código de estado: {response.status_code}'},
                        status=500)
            except requests.exceptions.RequestException as e:
                error_message = f'Error al realizar la solicitud a HubSpot: {str(e)}'
                print(error_message)  # Imprimir el mensaje de error en la consola

                try:
                    # Intentar obtener más detalles desde la respuesta de la API
                    error_details = response.json()
                    print('Detalles del error:', error_details)
                except json.JSONDecodeError:
                    print('No se pudo decodificar el contenido de la respuesta como JSON')

                return JsonResponse({'error': error_message}, status=500)
    else:
        # Obtener los datos existentes de HubSpot para prellenar el formulario
        hubspot_url = f'https://api.hubapi.com/crm/v3/objects/contacts/{user_id}'

        try:
            response = requests.get(hubspot_url, headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
            response.raise_for_status()
            hubspot_user_data = response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Error al obtener datos de usuario de HubSpot: {str(e)}'}, status=500)

        # Crear el formulario con los datos de HubSpot
        form = HubspotUserForm(initial={
            'email': hubspot_user_data['properties'].get('email', ''),
            'firstname': hubspot_user_data['properties'].get('firstname', ''),
            'lastname': hubspot_user_data['properties'].get('lastname', ''),
            # Puedes agregar más campos según sea necesario
        })

    return render(request, 'update_user.html', {'form': form, 'user_id': user_id})

#Metodo para eliminar usuarios
@csrf_exempt
def delete_user(request, user_id):
    # URL de la API de HubSpot para eliminar un contacto específico
    hubspot_url = f'https://api.hubapi.com/crm/v3/objects/contacts/{user_id}'

    # Realizar la solicitud DELETE a HubSpot con manejo de excepciones
    try:
        response = requests.delete(hubspot_url,
                                   headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP no exitosos

        if response.status_code == 204:  # 204 No Content indica éxito en una solicitud DELETE
            # Redirigir a la lista de usuarios después de la eliminación
            return redirect('list_users')
        else:
            return JsonResponse(
                {'error': f'Error al eliminar usuario en HubSpot. Código de estado: {response.status_code}'}, status=500)
    except requests.exceptions.RequestException as e:
        error_message = f'Error al realizar la solicitud a HubSpot: {str(e)}'
        print(error_message)  # Imprimir el mensaje de error en la consola

        try:
            # Intentar obtener más detalles desde la respuesta de la API
            error_details = response.json()
            print('Detalles del error:', error_details)
        except json.JSONDecodeError:
            print('No se pudo decodificar el contenido de la respuesta como JSON')

        return JsonResponse({'error': error_message}, status=500)





