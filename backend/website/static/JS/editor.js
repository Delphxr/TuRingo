const clickable = document.getElementById("canvas");
const menu = document.getElementById("menu");
const menu_nodo = document.getElementById("menu-nodo");
const outClick = document.getElementById("out-click");
let MOUSE_POSITION = { x: 0, y: 0 };
let NODES = [];
let LINES = [];

const pseudoCodigo = new PseudoCodigo(); //IMPORTANTE con esto vamos generando el codigo

let CURRENT_CLICKED_NODE; //nodo al que le hicimos click izquierdo actualmente
let CURRENT_START_NODE; //nodo inicio
let CURRENT_EXECUTING_NODE; //nodo inicio

document.getElementById("canvas").addEventListener("contextmenu", setPosition);


let dropdowns = document.querySelectorAll('.dropdown-toggle')
dropdowns.forEach((dd) => {
  dd.addEventListener('click', function (e) {
    var el = this.nextElementSibling
    el.style.display = el.style.display === 'block' ? 'none' : 'block'
  })
})

//para sacar el menu de nuevo nodo
clickable.addEventListener("contextmenu", (e) => {
  e.preventDefault();

  menu.style.top = `${e.clientY}px`;
  menu.style.left = `${e.clientX}px`;
  menu.classList.add("show");

  outClick.style.display = "block";
});

//cerrar menus al dar click por fiera
outClick.addEventListener("click", () => {
  menu.classList.remove("show");
  menu_nodo.classList.remove("show");
  outClick.style.display = "none";
});

//cerrar menus al hacer click en una opcion
menu.addEventListener("click", () => {
  menu.classList.remove("show");
  outClick.style.display = "none";
});
//cerrar menus al hacer click en una opcion
menu_nodo.addEventListener("click", () => {
  menu_nodo.classList.remove("show");
  outClick.style.display = "none";
});

//manejor del modal de nueva instruccion
document.addEventListener("DOMContentLoaded", function () {
  let insButton = document.getElementById("ins_button");
  let destinoSelect = document.getElementById("destino");

  insButton.addEventListener("click", function () {
    $("#modal_instruccion").modal("show");

    destinoSelect.innerHTML = "";
    for (const element of NODES) {
      let option = document.createElement("option");
      option.value = element[0];
      option.text = pseudoCodigo.obtenerApodo(element[0]);
      destinoSelect.add(option);
    }
  });
});

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

//obtenemos la posicion del mouse
function getPosition(e) {
  let rect = e.target.getBoundingClientRect();
  let x = e.clientX - rect.left;
  let y = e.clientY - rect.top;
  return {
    x,
    y,
  };
}

//colocamos la pocision actual del mouse en una variable global
function setPosition(e) {
  let position = getPosition(e);
  MOUSE_POSITION.x = Math.round(position.x);
  MOUSE_POSITION.y = Math.round(position.y);
}

// Genera un nuevo círculo en el canvas
function generate_circle() {
  let colors = {};

  // Añade colores para los círculos en formato [fondo, borde]
  colors[1] = ["var(--mint)", "var(--mint-shadow)"]; // mentA
  colors[2] = ["var(--red)", "var(--red-shadow)"]; // Rojo
  colors[3] = ["var(--green)", "var(--green-shadow)"]; // Verde
  colors[4] = ["var(--pink)", "var(--pink-shadow)"]; // rosado
  colors[5] = ["var(--purple)", "var(--purple-shadow)"]; // Morado
  colors[6] = ["var(--cyan)", "var(--cyan-shadow)"]; // Cyan
  colors[7] = ["var(--light-green)", "var(--light-green-shadow)"]; // VERDE CLARO

  // Elige un color al azar para el círculo
  let color = colors[getRandomInt(Object.keys(colors).length) + 1];

  // Crea un nuevo elemento span que será el círculo
  let dot = document.createElement("span");

  // Maneja el evento de click derecho (menú de opciones)
  dot.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    e.stopPropagation();

    // Establece el nodo actualmente clickeado como el nodo seleccionado
    let currentId = NODES.find((element) => element[1] === e.currentTarget)[0];
    CURRENT_CLICKED_NODE = [currentId, e.currentTarget];

    // Muestra el menú de opciones
    menu_nodo.style.top = `${e.clientY}px`;
    menu_nodo.style.left = `${e.clientX}px`;
    menu_nodo.classList.add("show");

    // Muestra el div de "outClick" para poder cerrar el menú de opciones
    outClick.style.display = "block";
    menu.classList.remove("show");
  });

  // Establece el ID del círculo como el largo actual de la matriz NODES
  let ID = pseudoCodigo.generateId();

  // Crea un nodo de texto que muestra el ID del círculo
  let text_id = document.createElement("div");
  text_id.textContent = ID;
  text_id.classList.add("dot-text");
  text_id.style.setProperty("--shadow", color[0]);

  dot.appendChild(text_id);
  // Establece la clase del elemento como "dot" para que tenga la forma de un círculo
  dot.classList.add("dot");

  NODES.push([ID, dot]);
  // Establece el color de fondo y el borde del círculo
  dot.style.backgroundColor = color[0];
  dot.style.borderColor = color[1];

  // Agrega el círculo al canvas
  const element = document.getElementById("canvas");
  element.appendChild(dot);

  // Coloca el círculo en la posición actual del mouse
  dot.style.transform =
    "translate(" + MOUSE_POSITION.x + "px, " + MOUSE_POSITION.y + "px)";

  // Hacemos que el nodo sea draggable utilizando la librería PlainDraggable
  let draggable = new PlainDraggable(dot);

  // Manejamos el evento de arrastre para corregir las líneas que salen del nodo
  draggable.onMove = function (newPosition) {
    fixAllLines();
  };

  playSound("/static/assets/audio/pop2.ogg")

}

//definimos cual es el nodo inicial del codigo
function set_start_node() {
  try {
    CURRENT_START_NODE.classList.remove("inicial")
  } catch (e) {
    console.log("aun no hay nodo inicial")
  }
  CURRENT_CLICKED_NODE[1].classList.add("inicial");
  CURRENT_START_NODE = CURRENT_CLICKED_NODE[1];

  pseudoCodigo.setInicial(CURRENT_CLICKED_NODE[0])


}

function setExecutingNode(id, clear = false) {
  if (clear) {
    CURRENT_EXECUTING_NODE.classList.remove("actual")
    return;
  }

  let selectedNode = NODES.find((element) => element[0] === id)[1];
  try {
    CURRENT_EXECUTING_NODE.classList.remove("actual")
  } catch (e) {
    console.log("aun no hay nodo actual")
  }
  selectedNode.classList.add("actual");
  CURRENT_EXECUTING_NODE = selectedNode;
}

//eliminamos un nodo
function remove_circle() {
  let tempLines = []; //creamos una lista temporal para guardar las lineas que no se deben eliminar
  for (const element of LINES) {
    //recorremos la lista de lineas
    //tenemos que encontrar las lineas que tienen este nodo, para eliminarlas también
    if (
      element[0].end.isEqualNode(CURRENT_CLICKED_NODE[1]) || //si el nodo final de la linea es igual al nodo que queremos eliminar
      element[0].start.isEqualNode(CURRENT_CLICKED_NODE[1]) //o si el nodo inicial de la linea es igual al nodo que queremos eliminar
    ) {
      document.body.appendChild(element[1]); //movemos la linea al cuerpo del documento temporalmente
      element[1].remove(); //eliminamos la linea
    } else {
      tempLines.push(element); //vamos guardando para una nueva lista sin los eliminados
    }
  }

  let i = NODES.indexOf(
    NODES.find((element) => element[0] === CURRENT_CLICKED_NODE[0])
  );
  NODES.splice(i, 1);

  CURRENT_CLICKED_NODE[1].remove(); //eliminamos el nodo seleccionado
  pseudoCodigo.eliminarNodo(CURRENT_CLICKED_NODE[0]);
  LINES = tempLines; //actualizamos la lista de lineas

  playSound("/static/assets/audio/pop3.ogg")

}

function rename_circle() {
  let newNombre = document.getElementById("renombrar").value;

  CURRENT_CLICKED_NODE[1].firstElementChild.textContent = newNombre;
  pseudoCodigo.definirApodo(CURRENT_CLICKED_NODE[0], newNombre);

}

//aqui metemos las lineas
var elmWrapper = document.getElementById("wrapper"),
  curTranslate = { x: 0, y: 0 },
  lines = [];



//generamos una nueva instrucción
function new_instruction() {
  let origenId = CURRENT_CLICKED_NODE[0];
  let mover = document.getElementById("cinta").value; //L o R

  e = document.getElementById("destino");
  let destino = e.options[e.selectedIndex].value; // Obtenemos el nodo de destino seleccionado en el menú desplegable
  let instructionContainer = document.getElementById("listainstrucciones");
  let listaInstrucciones =
    instructionContainer.getElementsByClassName("instruccioninfo");

  let instruction = "";
  for (const element of listaInstrucciones) {

    

    let read = element.querySelector("#read-ins").value;
    if (read === "") {
      read = "_"
    }


    let write = element.querySelector("#write-ins").value;
    if (write === "") {
      write = "_"
    }

    console.log("despues = i[" + read + "] - j[" + write + "]")

    pseudoCodigo.agregarLinea(origenId, read, write, mover, destino);
    //(q1, 1) -> (q2, 0, L)
    let newInstruction = ""
    if (read != write) {
      newInstruction += read +
        " → " +
        write;
    }
    else {
      newInstruction += read;
    }
    newInstruction += " , " + mover + "\n";
    instruction += newInstruction;
  }
  //si el nodo destino y el nodo origen son diferentes, hacemos una linea que los conecte
  console.log(instruction)
  if (origenId != destino) {
    generate_line(instruction);
  } else {
    addSelfLine(instruction);
  }
  playSound("/static/assets/audio/pop1.ogg")

}

function addSelfLine(instruction) {
  let origen = CURRENT_CLICKED_NODE[1]; //obtenemos el nodo irgen al que le dimos click

  origen.innerHTML +=
    '<svg class="arrow" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev/svgjs" viewBox="0 0 800 800"><g stroke-width="16" stroke="#ffffff" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="matrix(0.8746197071393959,-0.4848096202463369,0.4848096202463369,0.8746197071393959,-450.77173095429305,61.07596524277645)" style="stroke:var(--line-color) !important;"><path d="M177.3860626220703 327.4269676208496Q954.3860626220703 159.4269676208496 375.3860626220703 525.4269676208496 " marker-end="url(#SvgjsMarker3954)"></path></g><defs><marker markerWidth="4.5" markerHeight="4.5" refX="2.25" refY="2.25" viewBox="0 0 4.5 4.5" orient="auto" id="SvgjsMarker3954"><polygon points="0,4.5 0,0 4.5,2.25" fill="#ffffff" style="fill: var(--line-color) !important;"></polygon></marker></defs><text style="stroke-linejoin: round; paint-order: stroke; stroke-width: 2.11118px; stroke: var(--color-secondary); fill: var(--text-color)" x="200px" y="100px" >' +
    instruction +
    '</text></svg>';
}

// Creamos una nueva línea de conexión entre dos nodos y añadimos la instrucción correspondiente
function generate_line(instruction) {
  let origen = CURRENT_CLICKED_NODE[1]; // Obtenemos el nodo de origen (al que le hicimos click derecho0)
  e = document.getElementById("destino");
  let destino = e.options[e.selectedIndex].value; // Obtenemos el nodo de destino seleccionado en el menú desplegable

  destino = NODES.find((element) => element[0] === destino)[1]; //obmos el elemento html usando el id

  fixPosition();

  let line = new LeaderLine(origen, destino,
    {
      // Creamos una nueva línea utilizando la librería LeaderLine
      color: "var(--line-color)", // Establecemos el color de la línea
      path: "magnet", // Establecemos el tipo de camino que seguirá la línea para conectar los nodos
    });

  line.setOptions({
    // Establecemos las opciones de la línea, en este caso, añadimos una etiqueta en el centro de la línea con la instrucción
    middleLabel: LeaderLine.captionLabel(instruction, { color: "var(--text-color)", outlineColor: "var(--color-secondary)" }),
  });

  let line_element = document.querySelector("body>.leader-line:last-of-type"); // Obtenemos el elemento HTML de la línea creada por LeaderLine

  elmWrapper.appendChild(line_element); // Añadimos el elemento HTML de la línea al wrapper que contiene todaslineass

  LINES.push([line, line_element]); // Agregamos la línea y su elemento HTML a la lista de líneas existentes

  fixPosition(); // Ajustamos las posiciones de los elementos existentes en el canvas después de agregar nuevas líneas

  if (checkIfKeyExist(pseudoCodigo, origen)) {
    pseudoCodigo[origen].push({ next: destino, instruction: e.value });
  } else {
    pseudoCodigo[origen] = [{ next: destino, instruction: e.value }];
  }
}

//se encarga de actualizar las posiciones de las lineas al desplazar la pantalla
function fixPosition(line) {
  var rectWrapper = elmWrapper.getBoundingClientRect(),
    translate = {
      x: (rectWrapper.left + pageXOffset) * -1,
      y: (rectWrapper.top + pageYOffset) * -1,
    };
  if (translate.x !== 0 || translate.y !== 0) {
    // Update position of wrapper

    curTranslate.x += translate.x;
    curTranslate.y += translate.y;
    elmWrapper.style.transform =
      "translate(" + curTranslate.x + "px, " + curTranslate.y + "px)";
    // Update position of all lines

    LINES.forEach(function (line) {
      line[0].position();
    });
  } else if (line) {
    // Update position of target line
    line.position();
  }
}

//le hacemos fix a todas las lineas a la vez
function fixAllLines() {
  for (const element of LINES) {
    try {
      fixPosition(element[0]);
    } catch (error) {
      console.log(element);
    }
  }
}

const checkIfKeyExist = (objectName, keyName) => {
  let keyExist = Object.keys(objectName).some((key) => key === keyName);
  return keyExist;
};

//funciones de manejo de zoom
function increase_zoom() {
  let elem = document.getElementById("canvas");
  let style = getComputedStyle(elem);

  let zoomValue = style.zoom;
  zoomValue = zoomValue * 100;
  zoomValue += 1;
  let StringZoom = zoomValue + "%";

  document.getElementById("canvas").style.zoom = StringZoom;
  document.getElementById("wrapper").style.zoom = StringZoom;
}
//funciones de manejo de zoom
function decrease_zoom() {
  let elem = document.getElementById("canvas");
  let style = getComputedStyle(elem);

  let zoomValue = style.zoom;
  zoomValue = zoomValue * 100;
  zoomValue -= 1;
  if (zoomValue < 40) {
    zoomValue = 40;
  }
  let StringZoom = zoomValue + "%";

  document.getElementById("canvas").style.zoom = StringZoom;
  document.getElementById("wrapper").style.zoom = StringZoom;
}


