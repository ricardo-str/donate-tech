from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from werkzeug.utils import secure_filename
from database.db import *
from utils.validations import *
import os

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # 16 MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_donacion', methods=['GET', 'POST'])
def agregar_donacion():
    if request.method == 'POST':
        print("Formulario recibido:")
        for key, value in request.form.items():
            print(f"{key}: {value}")
        print("Archivos recibidos:")
        for key, value in request.files.items():
            print(f"{key}: {value.filename}")
        
        # Obtener datos del formulario
        form_data = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'celular': request.form.get('celular', ''),
            'region': request.form['region'],
            'comuna': request.form['comuna'],
            'dispositivos': []
        }

        # Procesar datos de los dispositivos
        nombres_dispositivos = request.form.getlist('nombre-dispositivo')
        descripciones = request.form.getlist('descripcion')
        tipos_donacion = request.form.getlist('tipo-donacion')
        anhos_uso = request.form.getlist('anhos-uso')
        estados_funcionamiento = request.form.getlist('estado-funcionamiento')
        fotos = request.files.getlist('foto')

        # Agrupar los datos de cada dispositivo
        for i in range(len(nombres_dispositivos)):
            dispositivo = {
                'nombre': nombres_dispositivos[i],
                'descripcion': descripciones[i],
                'tipo': tipos_donacion[i],
                'anhos': anhos_uso[i],
                'estado': estados_funcionamiento[i],
                'fotos': [fotos[j] for j in range(len(fotos)) if j % len(nombres_dispositivos) == i]
            }
            form_data['dispositivos'].append(dispositivo)

        # Validar formulario
        is_valid, errors = validar_formulario(form_data)
        if not is_valid:
            for error in errors:
                flash(error, 'error')
            return render_template('agregar-donacion.html', form=form_data)

        # Guardar contacto
        contacto_id = create_contacto(form_data['nombre'], form_data['email'], form_data['celular'], form_data['comuna'], form_data['region'])

        # Guardar dispositivos
        for dispositivo in form_data['dispositivos']:
            fotos_dispositivo = []
            for foto in dispositivo['fotos']:
                if foto and allowed_file(foto.filename):
                    filename = secure_filename(foto.filename)
                    foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    fotos_dispositivo.append(filename)

            try:
                create_dispositivo(
                    contacto_id, 
                    dispositivo['nombre'],
                    dispositivo['descripcion'],
                    dispositivo['tipo'],
                    int(dispositivo['anhos']),
                    dispositivo['estado'],
                    fotos_dispositivo
                )
            except Exception as e:
                flash(f'Error al guardar el dispositivo: {str(e)}', 'error')

        return redirect(url_for('index'))

    return render_template('agregar-donacion.html')

@app.route('/ver_dispositivos')
def ver_dispositivos():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    dispositivos, total = get_dispositivos(page, per_page)
    return render_template('ver-dispositivos.html', dispositivos=dispositivos, page=page, per_page=per_page, total=total)

@app.route('/informacion_dispositivo/<int:id>')
def informacion_dispositivo(id):
    dispositivo = get_dispositivo_info(id)
    comentarios = get_comentarios_by_dispositivo(id)

    if dispositivo:
        return render_template('informacion-dispositivo.html', dispositivo=dispositivo, comentarios=comentarios)
    else:
        flash('Dispositivo no encontrado', 'error')
        return redirect(url_for('ver_dispositivos'))
    
@app.route('/agregar_comentario/<int:id>', methods=['POST'])
def agregar_comentario(id):
    autor = request.form['autor']
    contenido = request.form['contenido']

    form_data = {
        'autor': autor,
        'contenido': contenido
    }

    # Validar comentario
    is_valid, errors = validar_comentario(form_data)

    if not is_valid:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('informacion_dispositivo', id=id))
    
    if autor and contenido:
        try:
            create_comentario(autor, contenido, id)
            flash('Comentario añadido exitosamente', 'success')
        except Exception as e:
            flash(f'Error al añadir comentario: {str(e)}', 'error')
    else:
        flash('Todos los campos son obligatorios', 'error')
    
    return redirect(url_for('informacion_dispositivo', id=id))

@app.route("/menu", methods=['GET'])
def menu():
    return render_template('menu.html')

@app.route("/stats", methods=['GET'])
def stats():
    return render_template('stats.html')

@app.route("/get-stats-data")
def get_stats_data():
    try:
        data = get_dispositivos_por_tipo()
        print("Datos a enviar:", data)  
        return jsonify(data)
    except Exception as e:
        print("Error al obtener datos:", str(e))  
        return jsonify({'error': str(e)}), 500
    
@app.route("/stats2", methods=['GET'])
def stats2():
    return render_template('stats2.html')

@app.route("/get-contact-stats")
def get_contact_stats():
    try:
        data = get_contactos_por_comuna()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)