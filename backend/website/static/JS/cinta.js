const tape = document.querySelector(".tape");
const tapeContainer = document.querySelector(".tape-container");
const playBtn = document.getElementById("play-button")
const stopBtn = document.getElementById("stop-button")
const backBtn = document.getElementById("back-button")
const nextBtn = document.getElementById("next-button")


let activeIndex = 2; // Índice del elemento activo
let current_instruction = 0;
let EXECUTING = false;
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let instrucciones = {
  "indexInicial": 7,
  "cintaInicial": "00000010111010000",
  "instrucciones": [
    {
      "movimiento": "R",
      "valorNuevo": "0",
      "nodo": "q0"
    },
    {
      "movimiento": "L",
      "valorNuevo": "1",
      "nodo": "q0"
    },
    {
      "movimiento": "R",
      "valorNuevo": "1",
      "nodo": "q1"
    },
    {
      "movimiento": "L",
      "valorNuevo": "0",
      "nodo": "q1"
    },
    {
      "movimiento": "L",
      "valorNuevo": "1",
      "nodo": "q2"
    },
    {
      "movimiento": "R",
      "valorNuevo": "0",
      "nodo": "q3"
    },
    {
      "movimiento": "R",
      "valorNuevo": "1",
      "nodo": "q4"
    },
    {
      "movimiento": "R",
      "valorNuevo": "0",
      "nodo": "q3"
    },
    {
      "movimiento": "L",
      "valorNuevo": "1",
      "nodo": "q5"
    },
    {
      "movimiento": "L",
      "valorNuevo": "0",
      "nodo": "q6"
    }
  ]
}



async function executeCode() {

  if (EXECUTING == true) {
    return;
  }

  EXECUTING = true;

  // Obtenemos la cinta inicial y la convertimos en un array para poder modificarla
  let cinta = instrucciones.cintaInicial.split('')

  // Obtenemos el contenedor de la cinta
  let contenedor = document.getElementById('tape')

  // Limpiamos el contenido actual del contenedor
  contenedor.innerHTML = ''

  // Generamos los elementos div y los añadimos al contenedor
  for (const element of cinta) {
    let div = document.createElement('div')
    div.className = 'tape-cell'
    div.innerText = element
    contenedor.appendChild(div)
  }

  // Obtenemos el índice inicial
  let index = instrucciones.indexInicial
  activeIndex = index
  updateTapePosition();

  // Iteramos por las instrucciones
  let audio = playSound("/static/assets/audio/gear.ogg", true)
  for (const element of instrucciones.instrucciones) {
    let instruccion = element

    try {
      setExecutingNode(instruccion.nodo)
    } catch {
      console.log("El nodo que desea seleccionar no existe")
    }
    

    // Modificamos la cinta en función de la instrucción
    if (instruccion.movimiento === "L") {
      moveTapeLeft();

    } else if (instruccion.movimiento === "R") {
      moveTapeRight();

    }
    await sleep(500);

    if (tape.children[activeIndex].textContent != instruccion.valorNuevo) {
      playSound("/static/assets/audio/key.ogg")
    }
    updateActiveValue(instruccion.valorNuevo);
    await sleep(250);


  }
  audio.pause()
  audio.remove()
  EXECUTING = false

  try {
    setExecutingNode(null, true)
  } catch {
    console.log("El nodo que desea seleccionar no existe")
  }
  
}

async function nextInstruction() {
  if (EXECUTING == true) {
    return;
  }

  if (current_instruction == instrucciones.instrucciones.length -1) {
    return;
  }
  current_instruction++;

  let insActual = instrucciones.instrucciones[current_instruction]


  try {
    setExecutingNode(insActual.nodo)
  } catch {
    console.log("El nodo que desea seleccionar no existe")
  }
  

  if (insActual.movimiento === "L") {
    moveTapeLeft();

  } else if (insActual.movimiento === "R") {
    moveTapeRight();

  }
  await sleep(250);

  if (tape.children[activeIndex].textContent != insActual.valorNuevo) {
    playSound("/static/assets/audio/key.ogg")
  }
  updateActiveValue(insActual.valorNuevo);
}

async function backInstruction() {
  if (EXECUTING == true) {
    return;
  }
  if (current_instruction == 0) {
    return;
  }
  current_instruction--;

  let insActual = instrucciones.instrucciones[current_instruction]

  try {
    setExecutingNode(insActual.nodo)
  } catch {
    console.log("El nodo que desea seleccionar no existe")
  }

  if (insActual.movimiento === "L") {
    moveTapeLeft();

  } else if (insActual.movimiento === "R") {
    moveTapeRight();

  }
  await sleep(250);

  if (tape.children[activeIndex].textContent != insActual.valorNuevo) {
    playSound("/static/assets/audio/key.ogg")
  }
  updateActiveValue(insActual.valorNuevo);
}


function stopExecution(){
  try {
    setExecutingNode(null, true)
  } catch {
    console.log("El nodo que desea seleccionar no existe")
  }
  current_instruction = 0;
}


// Actualizar la posición de la cinta
function updateTapePosition() {
  let cellWidth = tape.querySelector(".tape-cell").offsetWidth; // Ancho de la celda
  let tapeWidth = tapeContainer.offsetWidth; // Ancho de la cinta

  tape.style.transform = `translateX(calc(-${activeIndex * cellWidth}px + ${tapeWidth / 2 - cellWidth / 2
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
function updateActiveValue(value) {
  tape.children[activeIndex].textContent = value;
}



// Eventos de botón
playBtn.addEventListener("click", executeCode);
nextBtn.addEventListener("click", nextInstruction);
backBtn.addEventListener("click", backInstruction);
stopBtn.addEventListener("click", stopExecution);

// Actualizar la posición de la cinta en la carga inicial de la página
updateTapePosition();
