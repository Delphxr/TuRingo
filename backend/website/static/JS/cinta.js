const tape = document.querySelector(".tape");
const tapeContainer = document.querySelector(".tape-container");

const compBtn = document.getElementById("compile-button")
const playBtn = document.getElementById("play-button")
const stopBtn = document.getElementById("stop-button")
const backBtn = document.getElementById("back-button")
const nextBtn = document.getElementById("next-button")


let activeIndex = 0; // Índice del elemento activo
let startindex = 0; //indice para reiniciar
let startTape = "" //cinta para reiniciar

let EXECUTING = false;
let STOP = false

let current_instruction = 0;
let localInstrucciones = "_"

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function SetCinta(newCinta) {
  if (newCinta == "_") {
    return;
  };

  let cinta = newCinta.cintaInicial.split('');
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
}


async function entregarTarea() {
  console.log("start")
  if (EXECUTING) {
    return;
  }

  let entrada = document.getElementById("entradaCinta").value
  let vacio = document.getElementById("vacioCinta").value


  console.log("entrada y vacio")

  if (vacio === "") {
    vacio = "_"
  }

  let circle = startLoading()


  console.log("llamando api")
  try {
    const response = await fetch('http://140.84.172.6:5000/entregar-tarea', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(JSON.parse(pseudoCodigo.obtenerCodigoJson(entrada, vacio)))
    })
    const code = await response.json();
    console.log("respuesta", code)


    makeLog("Compilacion correcta!", code)

  } catch {
    console.log("hubo un error al conectarse con el API")
    circle.remove()
  }
}




async function compileCode() {
  console.log("start")
  if (EXECUTING) {
    return;
  }

  let entrada = document.getElementById("entradaCinta").value
  let vacio = document.getElementById("vacioCinta").value


  console.log("entrada y vacio")

  if (vacio === "") {
    vacio = "_"
  }

  let circle = startLoading()


  console.log("llamando api")
  try {
    const response = await fetch('http://140.84.172.6:5000/turing-compiler', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: pseudoCodigo.obtenerCodigoJson(entrada, vacio)
    })
    const code = await response.json();
    console.log("respuesta", code)


    circle.remove()


    if (code.hasOwnProperty('error')) {
      console.log("error en el codigo")
      console.log(code)
    } else {
      updateCompilationTime()
      localInstrucciones = code;
      console.log("compilation_complete")
    }

  } catch {
    console.log("hubo un error al conectarse con el API")
    circle.remove()
  }
}


//ejecutamos codigo, llamamos el API y lo mandamos luego a dibujar
async function executeCode() {
  if (EXECUTING) {
    return;
  }
  try{
    animateCode(localInstrucciones)
  } catch {
    console.log("No se puede correr el codigo, verifique que este compilado correctamente")
  }

}

async function animateCode(instrucciones) {
  if (EXECUTING) {
    return;
  }
  STOP = false
  EXECUTING = true;

  // Obtenemos la cinta inicial y la convertimos en un array para poder modificarla
  SetCinta(instrucciones)

  // Obtenemos el índice inicial
  let index = instrucciones.indexInicial
  activeIndex = index
  startindex = index
  updateTapePosition();

  // Iteramos por las instrucciones
  let audio = playSound("/static/assets/audio/gear.ogg", true)
  for (const element of instrucciones.instrucciones) {
    if (STOP) { //reiniciamos todo si hay un stop a media ejecucion
      SetCinta(localInstrucciones)
      activeIndex = startindex
      updateTapePosition()
      break
    };

    let instruccion = element

    await sleep(500);

    try {
      setExecutingNode(instruccion.nodo)
    } catch {
      console.log("El nodo que desea seleccionar no existe")
    }
    if (tape.children[activeIndex].textContent != instruccion.valorNuevo) {
      playSound("/static/assets/audio/key.ogg")
    }
    updateActiveValue(instruccion.valorNuevo);
    await sleep(250);

    // Modificamos la cinta en función de la instrucción
    if (instruccion.movimiento === "L") {
      moveTapeLeft();
    } else if (instruccion.movimiento === "R") {
      moveTapeRight();
    }




  }
  audio.pause()

  EXECUTING = false

}

async function nextInstruction() {
  if (EXECUTING) {
    return;
  }
  if (localInstrucciones == "_") {
    return
  }
  if (current_instruction == localInstrucciones.instrucciones.length) {
    return;
  }


  

  let insActual = localInstrucciones.instrucciones[current_instruction]


  try {
    setExecutingNode(insActual.nodo)
  } catch {
    console.log("El nodo que desea seleccionar no existe")
  }

  if (tape.children[activeIndex].textContent != insActual.valorNuevo) {
    playSound("/static/assets/audio/key.ogg")
  }
  updateActiveValue(insActual.valorNuevo);
  await sleep(250);

  // Modificamos la cinta en función de la instrucción
  if (insActual.movimiento === "L") {
    moveTapeLeft();
  } else if (insActual.movimiento === "R") {
    moveTapeRight();
  }

  current_instruction++;

}


function stopExecution() {
  try {
    setExecutingNode(null, true)
  } catch {
    console.log("El nodo que desea seleccionar no existe")
  }

  if (EXECUTING) {
    current_instruction = 0;
    STOP = true;
  } else {
    current_instruction = 0;
    STOP = true;
    SetCinta(localInstrucciones)
    activeIndex = startindex
    updateTapePosition()
  }
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
compBtn.addEventListener("click", compileCode);
playBtn.addEventListener("click", executeCode);
nextBtn.addEventListener("click", nextInstruction);
stopBtn.addEventListener("click", stopExecution);

// Actualizar la posición de la cinta en la carga inicial de la página
updateTapePosition();
