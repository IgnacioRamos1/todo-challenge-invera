
# Invera ToDo-List Challenge

Una ToDo-List API creada con Django Rest Framework y Python. Es capaz de:

- Autenticarse
- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma
- Obtener logs
- Correr Tests

## IMPORTANTE

En el caso de tener una MacM1 por favor corra:
```bash
  $ export DOCKER_DEFAULT_PLATFORM=linux/amd64

```

## Instalación

Para instalar el proyecto puede instalarlo desde la fuente o también puede usar el archivo docker-compose.yml que instalará todo en un solo lugar.

### Instalar usando Docker
Clone el repositorio y acceda a la carpeta recién creada

```bash
  git clone git@github.com:IgnacioRamos1/todo-challenge-invera.git
  cd my-project
```

Por favor chequear que Docker este corriendo en su máquina y que PostgreSQL no.

Finalmente levante la imagen de Docker:

```bash
  docker compose up
```

### Instalar de la fuente
Clone el repositorio y acceda a la carpeta recién creada

```bash
  git clone git@github.com:IgnacioRamos1/todo-challenge-invera.git
  cd my-project
```

Abra el archivo settings.py dentro de la carpeta todolist/ y modifique el "HOST" de la base de datos a "localhost" de la siguiente manera:
```bash
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.environ.get('DATABASE_NAME')),
        'USER': str(os.environ.get('DATABASE_USER')),
        'PASSWORD': str(os.environ.get('DATABASE_PASSWORD')),
        'HOST': 'localhost',  # Modificar aquí.
        'PORT': '5432',
    }
}
```

Instale los paquetes necesarios:
```bash
  pip install -r requirements.txt
```

Asegúrese que PostgreSQL está corriendo correctamente:
```bash
  service postgresql status
```

Finalmente, asegúrese que está en el directorio raíz y ya puede correr la API:
```bash
  python manage.py runserver
```
## Environment Variables

Para ejecutar este proyecto, deberá agregar las siguientes variables de entorno a su archivo .env.

El archivo .env debe encontrarse en la raíz del proyecto.

`SECRET_KEY`

`DEBUG`

`DATABASE_NAME`

`DATABASE_USER`

`DATABASE_PASSWORD`
## First Steps

Se recomienda el uso de Postman para una mejor y más fácil experiencia. 

Postman es un cliente GUI REST. Al importar las colecciones, puede explorar la API y obtener una mejor comprensión de las solicitudes y respuestas.

### Postman Requests Import

Puede descargar las requests necesarias [aquí](https://drive.google.com/file/d/1mXbYJ_6z-LUmmh_us0aXEnP-NRbghrcR/view?usp=sharing). Y luego importarlas a su cliente.

## Autenticación
### Registration

Para poder registrarse deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/auth/register/
```

(Cuidado con enviar un Token de autenticación como header).

Deberá enviarle un POST request con el siguiente formato de JSON:
```bash
{
    "username": "your username",
    "password": "your password"
}
```

### Login
Para poder loguearse deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/auth/login/
```

Deberá enviarle un POST request con el siguiente formato de JSON:
```bash
{
    "username": "your registered username",
    "password": "your registered password"
}
```

Y le devolverá un access token y refresh token que podrá usar en los CRUD endpoints.
```bash
 {
    "refresh": "refresh_token",
    "access": "access_token"
}
```

### Logout
Para poder desloguearse deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/auth/logout/
```

Deberá enviarle un POST request con el siguiente formato de JSON:
```bash
{
    "refresh_token": "your_refresh_token",
}
```
Y también deberá pasar su access token como header de autenticación.

## CRUD API

Para poder acceder a todos los siguientes endopoints, en cada request, debe enviar su access token como header.

### Get Tasks
Para poder obtener una lista de todas sus tareas deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/tasks/
```

Deberá enviarle un GET request.

### Create Task

Para poder crear una nueva tarea deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/tasks/
```

Deberá enviarle un POST request con el siguiente formato de JSON:
```bash
{
    "title": "your title",
    "description": "your description",
    "complete": false,
    "expiration_date": "2020-12-12 12:12:12"
}
```
El único campo obligatorio  es el "title", el resto si no se desea enviarlos no es necesario que los complete.

### Delete Task

Para poder eliminar una nueva tarea deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/tasks/{task_id}/
```

Deberá enviarle un DELETE request.

### Update Task
Para poder actualizar una nueva tarea deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/tasks/{task_id}/
```

Deberá enviarle un PATCH request con el siguiente formato de JSON:
```bash
{
    "title": "your new title",
    "description": "your new description",
    "complete": false,
    "expiration_date": "2020-12-12 12:12:12"
}
```

### Refresh Token
Si desea actualizar sus credenciales deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/auth/login/refresh/
```
Deberá enviarle un POST request con el siguiente formato de JSON:
```bash
{
    "refresh_token": "your_refresh_token",
}
```

### Logs
Los logs están divididos en las siguientes categorías:
- Critical
- Debug
- Error
- Info
- Warning

Si desea acceder a los logs deberá acceder al siguiente endopoint:
```bash
  http://localhost:8000/logs/{categoria}/
```


### Docs
Si desea acceder a la documentación de la API deberá acceder al siguiente endpoint:
```bash
  http://localhost:8000/docs/
```


## Tests
Para poder correr los tests en primer lugar debe seguir las instrucciones en la sección "Instalar de la fuente".
Finalmente:
```bash
  python manage.py test
```
El codigo cuenta con una covertura del 84% como se muestra a continuación:

![test_coverage](https://user-images.githubusercontent.com/85854096/207335684-423a85e2-2ba0-4dc7-81be-e3f593bb8216.png)

## Aclaraciones
- Se puede reducir el tiempo de vida del JWT Access Token ya que si una persona se desloguea, hasta que la vida útil del Token no se venza, el Token sigue siendo válido y puede ser utilizado para realizar requests.
- El endpoint de los logs no tienen permisos para una mayor facilidad cuando alguien los quiera ver al momento de la corrección. En el hipotético caso de que se realice un deploy de la API no sería un endpoint público.
- Devuelvo el ID de las tareas en el endpoint Get Tasks por simplicidad ya que luego si se desea eliminar o actualizar la tarea se conoce fácilmente su ID. En el hipotético caso de que se realice un deploy de la API no se mostrarían los ID's de las tareas.
