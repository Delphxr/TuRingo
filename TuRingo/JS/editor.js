const clickable = document.getElementById("canvas");
const menu = document.getElementById("menu");
const menu_nodo = document.getElementById("menu-nodo");
const outClick = document.getElementById("out-click");
let MOUSE_POSITION = { x: 0, y: 0 };
let NODES = [];
let LINES = [];

let pseudoCodigo = {};

let CURRENT_CLICKED_NODE; //nodo al que le hicimos click izquierdo actualmente

document.getElementById("canvas").addEventListener("contextmenu", setPosition);

clickable.addEventListener("contextmenu", (e) => {
  e.preventDefault();

  menu.style.top = `${e.clientY}px`;
  menu.style.left = `${e.clientX}px`;
  menu.classList.add("show");

  outClick.style.display = "block";
});

outClick.addEventListener("click", () => {
  menu.classList.remove("show");
  menu_nodo.classList.remove("show");
  outClick.style.display = "none";
});

//manejor del modal de nueva instruccion
$(function () {
  //getting click event to show modal
  $("#ins_button").click(function () {
    $("#modal_instruccion").modal("show");

    $("#origen").empty();
    $("#destino").empty();
    for (var i = 0; i < NODES.length; i++) {
      $("#origen").append(`<option value">${i}</option>`);
      $("#destino").append(`<option value">${i}</option>`);
    }
  });

  //end just to prove actions outside modal
});

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function getPosition(e) {
  let rect = e.target.getBoundingClientRect();
  let x = e.clientX - rect.left;
  let y = e.clientY - rect.top;
  return {
    x,
    y,
  };
}

function setPosition(e) {
  let position = getPosition(e);
  MOUSE_POSITION.x = Math.round(position.x);
  MOUSE_POSITION.y = Math.round(position.y);
  console.log(position);
}

//generamos un nodo en el canvas
function generate_circle() {
  let colors = {};
  //añádimos colores de la forma [fondo, borde]
  colors[1] = ["#448EFF", "#3C78DA"]; //azul
  colors[2] = ["#FF404A", "#CF383F"]; //rojo
  colors[3] = ["#00C958", "#00A542"]; //verde
  colors[4] = ["#FFDA00", "#D49B02"]; //amarillo
  colors[5] = ["#AD40FF", "#882DCE"]; //morado
  colors[6] = ["#FFAA00", "#E89B00"]; //naranja
  colors[7] = ["#00C0EA", "#028FBC"]; //cyan
  //colors[8] = ["#ED2CD5", "#D614C2"]; //rosado
  //colors[9] = ["#FF4A76", "#cc003d"]; //fuczia

  let color = colors[getRandomInt(Object.keys(colors).length) + 1]; //elegimos un color al azar
  console.log(Object.keys(colors).length);

  let dot = document.createElement("span");

  //manejo de click
  dot.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    e.stopPropagation();

    CURRENT_CLICKED_NODE = e.target;

    menu_nodo.style.top = `${e.clientY}px`;
    menu_nodo.style.left = `${e.clientX}px`;
    menu_nodo.classList.add("show");

    outClick.style.display = "block";
    menu.classList.remove("show");
  });

  let ID = NODES.length;
  NODES.push(dot);
  const text_id = document.createTextNode(ID); //aqui colocamos el ID del elemento
  dot.appendChild(text_id);

  dot.classList.add("dot"); //hacemos que sea un circulo

  dot.style.backgroundColor = color[0];
  dot.style.borderColor = color[1];

  const element = document.getElementById("canvas");
  element.appendChild(dot);
  dot.style.transform =
    "translate(" + MOUSE_POSITION.x + "px, " + MOUSE_POSITION.y + "px)"; //lo colocamos en la posicion del mouse

  let draggable = new PlainDraggable(dot); //lo volvemos un draggable

  draggable.onDragStart = function (pointerXY) {
    dot.style.boxShadow = "0 0 10px #373737";
  };

  draggable.onDragEnd = function (pointerXY) {
    dot.style.boxShadow = "0px 0px 0px";
  };

  draggable.onMove = function (newPosition) {
    fixAllLines();
  };
}

var elmWrapper = document.getElementById("wrapper"),
  curTranslate = { x: 0, y: 0 },
  lines = [];

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

//generamos una nueva instrucción
function new_instruction(){
  let mover = document.getElementById("cinta").value;
  let placeholder = "{1 -> write: 0}"

  let instruction = placeholder + " " + mover 
  generate_line(instruction)
}

//creamos una linea entre dos nodos y metemos la instrucción
function generate_line(instruction) {
  let origen = CURRENT_CLICKED_NODE;
  e = document.getElementById("destino");
  let destino = e.options[e.selectedIndex].text;

  fixPosition(); // Before adding new lines

  let line = new LeaderLine(origen, NODES[destino], {
    color: "#CECDCE",
    path: "magnet",
  });

  e = document.getElementById("instruccion");

  line.setOptions({
    middleLabel: LeaderLine.captionLabel(instruction, { color: "#646476" }),
  });

  let line_element = document.querySelector("body>.leader-line:last-of-type");

  elmWrapper.appendChild(line_element);

  LINES.push([line, line_element]);

  fixPosition(); // Before adding new lines

  if (checkIfKeyExist(pseudoCodigo, origen)) {
    pseudoCodigo[origen].push({ next: destino, instruction: e.value });
  } else {
    pseudoCodigo[origen] = [{ next: destino, instruction: e.value }];
  }
}



function remove_circle() {
  let tempLines = [];
  for (const element of LINES) {
    //tenemos que encontrar las lineas y eliminarlas
    if (
      element[0].end.isEqualNode(CURRENT_CLICKED_NODE) ||
      element[0].start.isEqualNode(CURRENT_CLICKED_NODE)
    ) {
      document.body.appendChild(element[1]);
      element[1].remove();
    } else {
      tempLines.push(element); //vamos guardando para una nueva lista sin los eliminados
    }
  }
  CURRENT_CLICKED_NODE.remove();
  LINES = tempLines;
}

//funciones de manejo de zoom
function increase_zoom() {
  let elem = document.getElementById("canvas");
  let style = getComputedStyle(elem);

  let zoomValue = style.zoom;
  zoomValue = zoomValue * 100;
  zoomValue += 10;
  let StringZoom = zoomValue + "%";

  document.getElementById("canvas").style.zoom = StringZoom;
  document.getElementById("wrapper").style.zoom = StringZoom;
}

function decrease_zoom() {
  let elem = document.getElementById("canvas");
  let style = getComputedStyle(elem);

  let zoomValue = style.zoom;
  zoomValue = zoomValue * 100;
  zoomValue -= 10;
  if (zoomValue < 40) {
    zoomValue = 40;
  }
  let StringZoom = zoomValue + "%";

  document.getElementById("canvas").style.zoom = StringZoom;
  document.getElementById("wrapper").style.zoom = StringZoom;
}
