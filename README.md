# Gestión de Roles en FastAPI con SQLAlchemy y OAuth2.0 + JWT

Este proyecto demuestra una API REST construida con FastAPI que muestra el manejo de roles usando las relaciones Many-to-Many de SQLAlchemy e implementa el estándar OAuth2.0 con JWT.

## Características

- **Gestión de Roles:** Utiliza SQLAlchemy para manejar roles de usuario con un esquema de relación Many-to-Many.
- **OAuth2.0 con JWT:** Implementa el estándar OAuth2.0 para autenticación y autorización utilizando tokens JWT.
- **Operaciones CRUD de Usuario:** Soporta operaciones de Crear, Leer, Actualizar y Eliminar usuarios y roles.
- **Documentación de Endpoints:** Genera automáticamente la documentación de la API a través de la interfaz Swagger UI de FastAPI.

## Requisitos

- Python 3.x
- FastAPI
- SQLAlchemy
- Bibliotecas de OAuth2.0 y JWT (según la implementación elegida)
- Otras dependencias (enumera las dependencias específicas aquí)

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/jhobahego/fastapi-roles.git
    ```

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Configura la URL de la base de datos en un archivo `.env`:

    ```env
    DB_URL="tu-url-de-la-base-de-datos"
    ```

4. Ejecuta la aplicación FastAPI:

    ```bash
    uvicorn main:app --reload
    ```

## Uso

- Accede a la documentación Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Utiliza los endpoints proporcionados para realizar operaciones relacionadas con usuarios, roles y autenticación.

## Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de enviar problemas (issues) o solicitudes de extracción (pull requests).

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

## Reconocimientos

Inspirado por este [articulo](https://www.gormanalysis.com/blog/many-to-many-relationships-in-fastapi/) ♥

## Contacto

Para consultas o comentarios, contáctame por [github](github.com/jhobahego).
