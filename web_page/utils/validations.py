import re

def sanitizar_texto(texto):
    """Sanitiza el texto para prevenir XSS."""
    return re.sub(r'[<>]', '', texto)  # Remueve < y >

def validar_nombre(nombre):
    """Valida que el nombre esté entre 3 y 80 caracteres."""
    nombre_sanitizado = sanitizar_texto(nombre)
    return 3 <= len(nombre_sanitizado) <= 80

def validar_email(email):
    """Valida el formato y longitud del email."""
    if not email or len(email) <= 3:
        return False
    email_sanitizado = sanitizar_texto(email).strip()
    regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(regex, email_sanitizado))

def validar_numero(numero):
    """Valida el número de celular, permitiendo vacío o formato específico."""
    if not numero or numero.strip() == "":
        return True
    numero = numero.replace(" ", "").replace("+56", "")
    return bool(re.match(r'^9\d{8}$', numero))

def validar_region(region):
    """Valida que la región no esté vacía."""
    region_sanitizada = sanitizar_texto(region)
    return bool(region_sanitizada)

def validar_comuna(comuna):
    """Valida que la comuna no esté vacía."""
    comuna_sanitizada = sanitizar_texto(comuna)
    return bool(comuna_sanitizada)

def validar_nombre_dispositivo(nombre):
    """Valida que el nombre del dispositivo esté entre 3 y 80 caracteres."""
    nombre_sanitizado = sanitizar_texto(nombre)
    return 3 <= len(nombre_sanitizado) <= 80

def validar_descripcion(descripcion):
    """Valida que la descripción no exceda los 120 caracteres, permitiendo vacío."""
    if descripcion:
        descripcion_sanitizada = sanitizar_texto(descripcion)
        return len(descripcion_sanitizada) <= 120
    return True

def validar_tipo(tipo):
    """Valida que el tipo no esté vacío."""
    tipo_sanitizado = sanitizar_texto(tipo)
    return bool(tipo_sanitizado)

def validar_anhos_uso(anhos):
    """Valida que los años de uso sean un número entre 1 y 99."""
    try:
        parsed_anhos = int(anhos)
        return 1 <= parsed_anhos <= 99
    except ValueError:
        return False

def validar_estado_funcionamiento(estado):
    """Valida que el estado de funcionamiento no esté vacío."""
    return estado in ["funciona perfecto", "funciona a medias", "no funciona"]

def validar_foto(fotos):
    """Valida el número y tipo de archivos de foto."""
    if not fotos or not isinstance(fotos, list):
        return False
    length_valid = 1 <= len(fotos) <= 3
    type_valid = all(foto.filename != '' and foto.content_type.startswith('image/') for foto in fotos if foto)
    return length_valid and type_valid

def validar_formulario(form):
    """Valida todo el formulario de donación."""
    invalid_inputs = []
    is_valid = True

    # Validaciones generales
    if not validar_nombre(form['nombre']):
        invalid_inputs.append("Nombre")
        is_valid = False

    if not validar_email(form['email']):
        invalid_inputs.append("Email")
        is_valid = False

    if not validar_numero(form['celular']):
        invalid_inputs.append("Número celular")
        is_valid = False

    if not validar_region(form['region']):
        invalid_inputs.append("Región")
        is_valid = False

    if not validar_comuna(form['comuna']):
        invalid_inputs.append("Comuna")
        is_valid = False

    # Validaciones para múltiples dispositivos
    dispositivos = form.get('dispositivos', [])
    for index, dispositivo in enumerate(dispositivos):
        if not validar_nombre_dispositivo(dispositivo['nombre']):
            invalid_inputs.append(f"Nombre del dispositivo {index + 1}")
            is_valid = False

        if not validar_descripcion(dispositivo['descripcion']):
            invalid_inputs.append(f"Descripción del dispositivo {index + 1}")
            is_valid = False

        if not validar_tipo(dispositivo['tipo']):
            invalid_inputs.append(f"Tipo del dispositivo {index + 1}")
            is_valid = False

        if not validar_anhos_uso(dispositivo['anhos']):
            invalid_inputs.append(f"Años de uso del dispositivo {index + 1}")
            is_valid = False

        if not validar_estado_funcionamiento(dispositivo['estado']):
            invalid_inputs.append(f"Estado de funcionamiento del dispositivo {index + 1}")
            is_valid = False

        if 'fotos' not in dispositivo or not validar_foto(dispositivo['fotos']):
            invalid_inputs.append(f"Foto(s) del dispositivo {index + 1}")
            is_valid = False

    return is_valid, invalid_inputs

# Validaciones para comentarios
def validar_autor_comentario(autor):
    """Valida que el nombre del autor esté entre 3 y 80 caracteres."""
    autor_sanitizado = sanitizar_texto(autor)
    return 3 <= len(autor_sanitizado) <= 80

def validar_contenido_comentario(contenido):
    """Valida que el contenido del comentario no esté vacío y sea menor o igual a 500 caracteres."""
    contenido_sanitizado = sanitizar_texto(contenido)
    return 1 <= len(contenido_sanitizado) <= 500

def validar_comentario(form):
    """Valida los campos del comentario."""
    invalid_inputs = []
    is_valid = True

    if not validar_autor_comentario(form.get('autor', '')):
        invalid_inputs.append("Nombre del autor")
        is_valid = False

    if not validar_contenido_comentario(form.get('contenido', '')):
        invalid_inputs.append("Contenido del comentario")
        is_valid = False

    return is_valid, invalid_inputs
