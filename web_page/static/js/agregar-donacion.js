// 1: Cargar regiones y comunas desde archivo .json
// Usamos fetch para cargar las regiones y comunas del .json en el formulario HTML
const regionSelect = document.getElementById("region");
const comunaSelect = document.getElementById("comuna");

// Obtenemos los datos de regiones y comunas desde el archivo .json
fetch("/static/region_comuna.json")
  .then((response) => response.json())
  .then((data) => {
    // Agregamos las opciones de regiones al select
    for (const region of data.regiones) {
      const option = document.createElement("option");
      option.value = region.nombre;
      option.textContent = region.nombre;
      regionSelect.appendChild(option);
    }

    // Agregamos las opciones de comunas al select al seleccionar una región
    regionSelect.addEventListener("change", (event) => {
      // Limpiamos las opciones anteriores
      comunaSelect.innerHTML = "";

      // Obtenemos las comunas de la región seleccionada
      const comunas = data.regiones.find((element) => element.nombre === event.target.value)
        .comunas;

      // Agregamos las opciones de comunas al select
      for (const comuna of comunas) {
        const option = document.createElement("option");
        option.value = comuna.nombre;
        option.textContent = comuna.nombre;
        comunaSelect.appendChild(option);
      }
    });
  })
  .catch((error) => console.error(error));

// 2: Agregar formulario para añadir otro dispositivo al formulario de donación
document.getElementById('add-device-btn').addEventListener('click', function() {
    // Contenedor donde se añadirán las secciones de dispositivos
    const dispositivosContainer = document.getElementById('dispositivos-container');

    // Contar cuántos dispositivos ya están agregados
    const dispositivoForms = dispositivosContainer.querySelectorAll('.dispositivo-form');
    const newDeviceNumber = dispositivoForms.length + 1;

    // Clonar la primera sección de dispositivo
    const originalDeviceForm = dispositivoForms[0];
    const newDeviceForm = originalDeviceForm.cloneNode(true);

    // Actualizar el título de la nueva sección
    newDeviceForm.querySelector('h2').textContent = 'Información Dispositivo ' + newDeviceNumber;

    const labels = newDeviceForm.querySelectorAll('label');
    const inputs = newDeviceForm.querySelectorAll('input, select');

    labels.forEach(label => {
        const newId = label.getAttribute('for').replace(/-\d+$/, '-' + newDeviceNumber);
        label.setAttribute('for', newId);
    });

    inputs.forEach(input => {
        const newId = input.id.replace(/-\d+$/, '-' + newDeviceNumber);
        input.id = newId;
        input.value = ''; // Limpiar el valor del input clonado
    });

    dispositivosContainer.appendChild(newDeviceForm);
});

// 3: Validar formulario de donación
const validadorNombre = (nombre) => {
    if (!nombre) return false;
    let lenghtValid = 3 <= nombre.length && nombre.length <= 80;
    return lenghtValid;
}
  
const validadorEmail = (email) => {
    if (!email) return false;
    let lengthValid = email.length > 3;
    const reg_expression = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let formatValid = reg_expression.test(email);
    return lengthValid && formatValid;
}

const validadorNumero = (numero) => {
    if (!numero || numero.trim() === "") return true;
    numero = numero.replace(/\s+/g, '').replace(/^\+56/, '');
    const reg_expression = /^9\d{8}$/;
    return reg_expression.test(numero);
}

const validadorRegion = (region) => {  
    if (!region) {
      return false;
    } else {
      return true;
    }
}

const validadorComuna = (comuna) => {
  if (!comuna) {
    return false;
  } else {
    return true;
  }
}

const validadorNombreDispositivo = (nombre) => {
    if (!nombre) return false;
    let lenghtValid = 3 <= nombre.length && nombre.length <= 80;
    return lenghtValid;
}

const validadorDescripcion = (descripcion) => {
  if (!descripcion || descripcion.trim() === "") return true;
  return descripcion.length <= 120;
}

const validadorTipo = (tipo) => {
    if (!tipo) {
      return false;
    } else {
      return true;
    }
}
  
const validadorAnhosUso = (anhos) => {
    let parsedAnhos = parseInt(anhos);
    return Number.isInteger(parsedAnhos) && parsedAnhos >= 1 && parsedAnhos <= 99;
}

const validadorEstadoFuncionamiento = (estado) => {
    if (!estado) {
      return false;
    } else {
      return true;
    }
}

const validadorFoto = (fotos) => {
    if (!fotos) return false;
    let lenghtValid = 1 <= fotos.length && fotos.length <= 3;
    let typeValid = true;
    for (const foto of fotos) {
      let fotoFamily = foto.type.split("/")[0];
      typeValid &&= fotoFamily == "image";
    }
    return lenghtValid && typeValid;
}

const validadorFormulario = (event) => {
  event.preventDefault(); // Prevenir el envío automático del formulario

  let form = document.forms["formulario"];
  let nombreInput = form["nombre"].value;
  let emailInput = form["email"].value;
  let celularInput = form["celular"].value;
  let regionInput = form["region"].value;
  let comunaInput = form["comuna"].value;

  let invalidInputs = [];
  let isValid = true;  
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid = false;
  }

  if (!validadorNombre(nombreInput)) {
      setInvalidInput("Nombre");
  }

  if (!validadorEmail(emailInput)) {
      setInvalidInput("Email");
  }

  if (!validadorNumero(celularInput)) {
      setInvalidInput("Número celular");
  } 

  if (!validadorRegion(regionInput)) {
      setInvalidInput("Región");
  }

  if (!validadorComuna(comunaInput)) {
      setInvalidInput("Comuna");
  }

  // Validador para múltiples dispositivos
  const dispositivoForms = form.querySelectorAll('.dispositivo-form');
  dispositivoForms.forEach((dispositivoForm, index) => {
      let nombreDispositivo = dispositivoForm.querySelector('[name="nombre-dispositivo"]').value;
      let descripcion = dispositivoForm.querySelector('[name="descripcion"]').value;
      let tipo = dispositivoForm.querySelector('[name="tipo-donacion"]').value;
      let anhosUso = dispositivoForm.querySelector('[name="anhos-uso"]').value;
      let estadoFuncionamiento = dispositivoForm.querySelector('[name="estado-funcionamiento"]').value;
      let fotos = dispositivoForm.querySelector('[name="foto"]').files;

      if (!validadorNombreDispositivo(nombreDispositivo)) {
          setInvalidInput(`Nombre del dispositivo ${index + 1}`);
      }

      if (!validadorDescripcion(descripcion)) {
          setInvalidInput(`Descripción del dispositivo ${index + 1}`);
      } 

      if (!validadorTipo(tipo)) {
          setInvalidInput(`Tipo del dispositivo ${index + 1}`);
      }

      if (!validadorAnhosUso(anhosUso)) {
          setInvalidInput(`Años de uso del dispositivo ${index + 1}`);
      }

      if (!validadorEstadoFuncionamiento(estadoFuncionamiento)) {
          setInvalidInput(`Estado de funcionamiento del dispositivo ${index + 1}`);
      }

      if (!validadorFoto(fotos)) {
          setInvalidInput(`Foto(s) del dispositivo ${index + 1}`);
      }
  });

  let validationBox = document.getElementById("val-box");
  let validationMessage = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  const confirmButton = document.getElementById('confirm-donation');
  const cancelButton = document.getElementById('cancel-donation');
  const myDialog = document.getElementById('confirmation-modal');
  const successMessage = document.getElementById('success-message');

  if (!isValid) {
      validationListElem.textContent = "";

      for (input of invalidInputs) {
          let listElement = document.createElement("li");
          listElement.innerText = input;
          validationListElem.append(listElement);
      }

      validationMessage.innerText = "Los siguientes campos son inválidos o incompletos";
      validationBox.hidden = false;

      // Desplazamiento suave hacia el mensaje de validación
      validationBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
      validationBox.hidden = true;
      myDialog.hidden = false; // Mostrar el diálogo de confirmación

      // Esperar la confirmación del usuario
      confirmButton.addEventListener('click', () => {
          myDialog.hidden = true; // Ocultar el diálogo de confirmación
          successMessage.hidden = false; // Mostrar el mensaje de éxito
          successMessage.scrollIntoView({ behavior: 'smooth', block: 'start' });
          form.submit(); // Enviar el formulario una vez confirmada la acción
      });
      
      cancelButton.addEventListener('click', () => {
          myDialog.hidden = true; // Ocultar el diálogo si el usuario cancela
      });
  }
}

// Prevenir envio inmediato del formulario
document.getElementById("envio").addEventListener("click", validadorFormulario);

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('confirmation-modal').hidden = true;
});

