# Sport_Booking_EV3
# SportBooking – Sistema de Gestión de Canchas Deportivas

## 1. Información del proyecto

**Asignatura:** Programación Back End (TI3041)  
**Evaluación:** Sumativa N.º 3  
**Unidad:** Framework Back End  
**Organización o plataforma:** SportBooking  
**Giro:** Gestión de instalaciones y servicios deportivos

**Integrantes:**
- [Jerson Concha]

## 2. Descripción del proyecto

SportBooking es una aplicación web desarrollada con Python y Django, orientada a facilitar la gestión de canchas deportivas.

La plataforma permite a los usuarios consultar las canchas disponibles, buscar por nombre, filtrar por disciplina y revisar sus características y tarifas.

También incorpora un sistema de selección temporal de canchas mediante sesiones HTTP, donde los usuarios pueden indicar horas y cantidad de personas, consultar los costos estimados y generar un comprobante simulado.

Los administradores cuentan con herramientas para registrar, modificar y desactivar canchas de manera segura.

## 3. Objetivo

Desarrollar una aplicación web que facilite la consulta y administración de canchas deportivas, utilizando Django, una base de datos relacional, operaciones CRUD, autenticación y manejo de sesiones.

## 4. Tecnologías utilizadas

- Python
- Django 5.2.19
- SQLite
- HTML5 y CSS3
- Bootstrap 5
- Pillow
- python-dotenv
- Git y GitHub

## 5. Modelo de datos

**Entidad de contexto:** Disciplina

Permite clasificar las canchas según el deporte, como fútbol, pádel, tenis, básquetbol y voleibol.

**Entidad principal:** Cancha

Almacena nombre, código, disciplina, descripción, precio, capacidad, estado, imagen y vigencia.

**Entidad complementaria:** Perfil

Almacena información adicional del usuario, como RUT, teléfono y rol.

Las canchas se relacionan con las disciplinas mediante ForeignKey con PROTECT.

## 6. Funcionalidades

### Catálogo público
- Visualización de canchas deportivas.
- Búsqueda por nombre, código y descripción.
- Filtros por disciplina.
- Ordenamiento por precio.
- Paginación y ficha de detalles.

### Administración
- Crear canchas.
- Modificar información.
- Desactivar canchas sin eliminarlas físicamente.
- Administración personalizada mediante Django Admin.

### Usuarios y seguridad
- Registro de clientes.
- Inicio y cierre de sesión.
- Perfiles con RUT, teléfono y rol.
- Restricción de operaciones administrativas.
- Protección CSRF y validaciones de formularios.

### Selección temporal
- Agregar canchas.
- Modificar horas y personas.
- Quitar elementos.
- Vaciar la selección.
- Calcular subtotal e IVA del 19%.
- Generar comprobantes simulados.

## 7. Instalación en Windows

### Requisitos
- Python instalado.
- Git.
- Conexión a internet para instalar dependencias.

### Descargar el proyecto

git clone https://github.com/Jerson-Lab/Sport_Booking_EV3.git

cd Sport_Booking_EV3

### Crear el entorno virtual

py -m venv .venv

.\.venv\Scripts\Activate.ps1

### Instalar dependencias

python -m pip install -r requirements.txt

### Configurar variables de entorno

Copiar `.env.example` a un nuevo archivo `.env`.

Generar una clave secreta con:

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Copiar la clave generada en DJANGO_SECRET_KEY dentro de `.env`.

### Preparar la base de datos

python manage.py migrate

### Cargar los datos iniciales

python manage.py poblar_datos

El comando carga disciplinas, canchas y usuarios de prueba. Las contraseñas de los usuarios se establecen de forma interactiva.

### Ejecutar el servidor

python manage.py runserver

Abrir:

http://127.0.0.1:8000/

## 8. Usuarios de prueba

**Administrador:** admin_demo

**Cliente:** cliente_demo

Las contraseñas se configuran al ejecutar el comando poblar_datos y no se almacenan en el repositorio.

## 9. Pruebas

Para comprobar la configuración:

python manage.py check

Para ejecutar las pruebas automatizadas:

python manage.py test reservas

## 10. Alcance del sistema

SportBooking es un proyecto académico.

La selección de canchas funciona mediante request.session. No confirma reservas reales, no bloquea horarios y no procesa pagos.

Los comprobantes corresponden a solicitudes simuladas con cálculos estimados.

## 11. Uso de inteligencia artificial

Se utilizó ChatGPT version Plus como herramienta de apoyo en el desarrollo, especialmente para comprender Django ORM, implementar sesiones y comprobar mecanismos de seguridad.

El código fue escrito, adaptado y probado durante el desarrollo del proyecto.

La bitácora de prompts utilizados se documenta a continuación.

## 12. Bitácora de uso de inteligencia artificial

Durante el desarrollo de SportBooking utilicé ChatGPT como una herramienta de apoyo para resolver algunas dudas que fueron apareciendo mientras trabajaba con Django. Principalmente, me sirvió para entender mejor ciertas funciones del framework, revisar algunos errores y conocer distintas formas de implementar las funcionalidades del sistema.

A continuación, presento tres consultas técnicas relacionadas con el desarrollo del proyecto. Las preguntas están reformuladas para explicar mejor los temas que consulté.

### Consulta 1. Relación entre los modelos en Django

**Pregunta técnica reformulada:**

¿Cómo puedo relacionar los modelos Disciplina y Cancha utilizando ForeignKey en Django y aplicar validaciones para evitar que se ingresen valores incorrectos?

**Respuesta obtenida:**

Se explicó cómo funciona `ForeignKey` para relacionar dos modelos y cómo utilizar `on_delete=models.PROTECT` para evitar que se elimine una disciplina que tenga canchas asociadas. También se revisó el uso de `MinValueValidator` para validar los valores numéricos.

**Cómo lo apliqué en SportBooking:**

Utilicé esta información para organizar los modelos del proyecto y establecer la relación entre las canchas y sus respectivas disciplinas. También agregué validaciones en los campos de precio y capacidad para evitar que se ingresaran valores negativos o incorrectos.

Después realicé las migraciones y comprobé desde Django Admin que los registros se guardaran correctamente.

### Consulta 2. Manejo de sesiones para seleccionar canchas

**Pregunta técnica reformulada:**

¿Cómo puedo guardar temporalmente las canchas seleccionadas por un usuario utilizando request.session y permitir que pueda modificar o eliminar elementos de su selección?

**Respuesta obtenida:**

Se revisó cómo Django permite guardar información temporal mediante `request.session`, utilizando diccionarios para almacenar los datos de cada cancha. También se explicó cómo recuperar y actualizar esa información sin necesidad de guardarla directamente en la base de datos.

**Cómo lo apliqué en SportBooking:**

Apliqué este funcionamiento en la sección Mi selección, donde el usuario puede agregar canchas, indicar la cantidad de horas y personas, modificar estos datos o quitar una cancha.

También incorporé el cálculo del subtotal, IVA y total de la solicitud.

En esta parte tuve algunos problemas al recuperar los datos de la sesión, principalmente por errores al escribir las claves del diccionario. Después de corregirlos, realicé distintas pruebas hasta comprobar que los valores se actualizaran correctamente.

### Consulta 3. Seguridad y permisos de usuarios

**Pregunta técnica reformulada:**

¿Cómo puedo controlar el acceso a las funciones administrativas de Django para que los clientes puedan consultar las canchas, pero solamente los administradores puedan crearlas, modificarlas o desactivarlas?

**Respuesta obtenida:**

Se revisó el uso de `login_required` y `user_passes_test` para restringir el acceso a determinadas vistas. También se explicó cómo utilizar `is_staff` para identificar a los usuarios con permisos administrativos y la importancia de proteger los formularios mediante CSRF.

**Cómo lo apliqué en SportBooking:**

Utilicé estos mecanismos para separar las funciones de los clientes y administradores. Los clientes pueden ingresar al catálogo y utilizar la selección de canchas, mientras que las opciones de administración quedan restringidas a los usuarios autorizados.

Para comprobarlo, inicié sesión con diferentes cuentas e intenté acceder a las funciones administrativas. Esto me permitió verificar que las restricciones estuvieran funcionando correctamente.

### Conclusión de la bitácora

El uso de ChatGPT me ayudó a resolver dudas durante el desarrollo de SportBooking, especialmente en las partes donde necesitaba comprender mejor cómo funcionaban algunas herramientas de Django.

Además de consultar información, fui realizando pruebas en Visual Studio Code para comprobar que las funcionalidades trabajaran correctamente. En varias ocasiones tuve que revisar errores de sintaxis, ajustar algunas líneas de código y repetir las pruebas hasta obtener el resultado esperado.

En general, esta herramienta fue un apoyo para entender mejor algunos conceptos y avanzar en el desarrollo del proyecto, complementando lo aprendido en clases y la práctica que fui adquiriendo durante la programación.