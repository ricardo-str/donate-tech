// JS para abrir la imagen grande
var modal = document.getElementById("myModal");
var img = document.getElementById("foto");
var modalImg = modal.querySelector("img");
var span = document.getElementsByClassName("close")[0];

img.onclick = function(){
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}


// Validación de comentarios
function validarComentario() {
  const nombre = document.getElementById('autor').value.trim();
  const comentario = document.getElementById('contenido').value.trim();
  const validationBox = document.getElementById('val-box');
  const validationMessage = document.getElementById('val-msg');
  const validationList = document.getElementById('val-list');
  const successMessage = document.getElementById('success-message');

  let isValid = true;
  let invalidInputs = [];

  // Validación del nombre (campo 'autor')
  if (nombre.length < 3 || nombre.length > 80) {
    invalidInputs.push("El nombre debe tener entre 3 y 80 caracteres.");
    isValid = false;
  }

  // Validación del comentario (campo 'contenido')
  if (comentario.length < 5) {
    invalidInputs.push("El comentario debe tener al menos 5 caracteres.");
    isValid = false;
  }

  if (!isValid) {
    // Limpiar lista de validación anterior
    validationList.innerHTML = "";

    // Agregar mensajes de validación
    for (let input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationList.appendChild(listElement);
    }

    // Mostrar mensaje de error
    validationMessage.innerText = "Por favor, corrige los siguientes errores:";
    validationBox.hidden = false; // Mostrar caja de validación
    successMessage.hidden = true; // Ocultar mensaje de éxito
    validationBox.scrollIntoView({ behavior: 'smooth', block: 'start' }); // Desplazar a la caja de validación
  } else {
    // Ocultar caja de validación y mostrar mensaje de éxito
    validationBox.hidden = true;
    successMessage.hidden = false;
    successMessage.scrollIntoView({ behavior: 'smooth', block: 'start' }); // Desplazar al mensaje de éxito

    // Limpiar el formulario
    document.getElementById('form-comentario').reset();
  }
}

