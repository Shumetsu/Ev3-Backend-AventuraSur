# Aventuras del Sur

## Credenciales de prueba
Contrasena de todos los usuarios: `Aventura2026!`

| Rol           | Usuario    |
|---------------|------------|
| Administrador | `admin`    |
| Guia          | `guia1`    |
| Guia          | `guia2`    |
| Turista       | `turista1` |
| Turista       | `turista2` |

## Puesta en marcha
1. Restaurar `respaldo_ecoparque.sql` (incluye datos de prueba), o crear la base:
   `CREATE DATABASE ecoparque CHARACTER SET utf8mb4;`
2. `pip install -r requirements.txt`
3. Configurar la conexion a MySQL en `inventarioAventura/settings.py`
4. `python manage.py migrate`
5. `python manage.py cargar_datos` (solo si no se restauro el respaldo)
6. `python manage.py runserver` y abrir http://127.0.0.1:8000/

## Tecnologias
Django 5.0 · MySQL · AdminLTE 4 (Bootstrap 5.3) · DataTables · Chart.js

## Secciones por rol
- **Administrador:** categorias, experiencias, reservas, usuarios, guias, reportes, calendario y configuracion
- **Guia:** sus experiencias, detalle del grupo con asistencia y estado de ruta, calendario
- **Turista:** catalogo, detalle de experiencia, reservas y valoraciones

La aplicacion usa AdminLTE por CDN, asi que requiere conexion a internet.