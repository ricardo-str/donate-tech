# Tarea 3 CC5002 Desarrollo Aplicaciones Web 

Nombre: Ricardo Sepúlveda Tritini

## Requisitos

Tener Python 3.x instalado en tu equipo.

## Instalación

1. Descargar este proyecto en tu dispositivo:

2. Instala las dependencias desde el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
3. Si tienes problemas con el comando anterior, elimina la carpeta venv del proyecto e intenta de nuevo.

**nota**: a veces no se instalan bien las versiones de las dependencias que están requirements.txt, así que hay que instalarlas 'a mano'.

## Uso

Ejecuta la aplicación utilizando el comando

```bash
python app.py
```

## Estructura del Proyecto

```
TAREA 3/
│         
├── database/        
│   └── db.py
│   └── region-comuna.sql
│   └── sentencias.sql
│   └── tarea2.sql          
├── static/
│   └── css/
│   └── js/
│   └── media/ 
│   └── uploads/            
├── templates/
│   └── agregar-donacion.html
│   └── index.html 
│   └── informacion-dispositivo.html 
│   └── ver-dispositivos.html
│   └── menu.html
│   └── stats.html
│   └── stats2.html 
├── utils/            
│   └── validations.py  
├── app.py   
└── requirements.txt  
```
## Bases de Datos

El proyecto contiene tres archivos sql. Para poder almacenar los datos utilizando mysql debemos ejecutar el contenido de tarea2.sql para la creación de esquemas y de tablas en donde se guardará la información. Posteriormente se debe ejecutar el contenido del archivo region-comuna.sql para poder almacenar las regiones y sus respectivas comunas en la tabla correspondiente. Finalmente, se debe ejecutar el archivo sentencias.sql, aquí es donde crearemos el usuario y le daremos sus correspondientes privilegios/permisos para el correcto funcionamiento de la aplicación. 

Se hace uso del archivo llamado sentencias.json, el cual contiene las querys utilizadas durante el proyecto para insertar u obtener la información necesaria. 

Por último, se incluye también el archivo db.py, que es donde se conecta la base de datos y se ejecutan las consultas desde el archivo sentencias.json.

## Validaciones

El proyecto hace "validaciones" en el frontend a través de Javascript, tal y como se hizo en la Tarea 1. Adicionalmente se crea el archivo validations.py para realizar las verdaderas validaciones en el backend para cada entrada, incluyendo una sanitización del texto para prevenir ataques de tipo XSS.

Se incluyen las nuevas validaciones tanto en el frontend (utilizando Javascript) como en el backend para los comentarios de los dispositivos.

## Correcciones 

El proyecto presenta correcciones respecto a problemas que ocurrian en la entrega pasada:

- **No poder insertar más de un dispositivo a la vez**: cuando se intentaba agregar dos o más dispositivos en el formulario de agregar donación, solo se se insertaba el primero y se mostraba en la página de "Ver Donaciones", ahora se pueden agregar correctamente múltiples dispositivos simultáneamente.

- **No limitar el tamaño de archivo**: en la versión anterior de la tarea, no existía un mecanismo para limitar el tamaño máximo de un archivo, lo que podría ser peligroso. Se solucionó utilizando 'MAX_CONTENT_LENGTH' en el archivo app.py.

- **Permitir archivos PDF**: en la versión anterior de la tarea se aceptaban archivos PDF cuando no era una extensión permitida, ahora cuando se intenta seleccionar un archivo .pdf no se puede enviar el formulario de agregar-donacion. 

## Novedades Tarea 3

- **Comentarios**: se incluye un nuevo formulario en la URL de 'informacion-dispositivo' que solicita el nombre y el texto del comentario. Si no cumple las validaciones, se informa al usuario y se deja visible el formulario para corregir. 

   También se pueden ver los comentarios asociados al dispositivo en la misma URL, con el nombre del comentarista, el texto y la fecha de envío.

- **Gráficos**: se agregó una nueva opción en el menú inicial, en donde se puede acceder a una nueva página que contiene dos opciones de gráficos distintos: *Tipo de Dispositivos* y *Contactos por Comuna*. Ambos gráficos fueron hechos correctamente utilizando AJAX y Highcharts. 
