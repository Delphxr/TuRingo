const tape = document.querySelector(".tape");
const tapeContainer = document.querySelector(".tape-container");
const moveLeftBtn = document.querySelector("#moveLeftBtn");
const moveRightBtn = document.querySelector("#moveRightBtn");
const inputValue = document.querySelector("#inputValue");
const updateValueBtn = document.querySelector("#updateValueBtn");

let activeIndex = 2; // Índice del elemento activo
let cellWidth = tape.querySelector(".tape-cell").offsetWidth; // Ancho de la celda
let tapeWidth = tapeContainer.offsetWidth; // Ancho de la cinta

// Actualizar la posición de la cinta
function updateTapePosition() {
  tape.style.transform = `translateX(calc(-${activeIndex * cellWidth}px + ${
    tapeWidth / 2 - cellWidth / 2
  }px))`;
  tape.children[activeIndex].classList.add("active");
}

// Mover la cinta a la izquierda
function moveTapeLeft() {
  if (activeIndex > 0) {
    tape.children[activeIndex].classList.remove("active");
    activeIndex--;

    updateTapePosition();
  }
}

// Mover la cinta a la derecha
function moveTapeRight() {
  if (activeIndex < tape.children.length - 1) {
    tape.children[activeIndex].classList.remove("active");
    activeIndex++;

    updateTapePosition();
  }
}

// Actualizar el valor del elemento activo
function updateActiveValue() {
  tape.children[activeIndex].textContent = inputValue.value;
}

// Eventos de botón
moveLeftBtn.addEventListener("click", moveTapeLeft);
moveRightBtn.addEventListener("click", moveTapeRight);
updateValueBtn.addEventListener("click", updateActiveValue);

// Actualizar la posición de la cinta en la carga inicial de la página
updateTapePosition();
