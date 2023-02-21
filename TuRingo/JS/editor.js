const clickable = document.getElementById("canvas");
const menu = document.getElementById("menu");
const menu_nodo = document.getElementById("menu-nodo");
const outClick = document.getElementById("out-click");
let MOUSE_POSITION = { x: 0, y: 0 };
let NODES = [];
let LINES = [];

let pseudoCodigo = {};

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



//mostrar un modal solamente dentro de el editor
$(function () {
  //getting click event to show modal
  $("#ins_button").click(function () {
    console.log("pipopapo")
    console.log(NODES)
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
  console.log(Object.keys(colors).length)

  let dot = document.createElement("span");

  dot.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    e.stopPropagation();
    
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
    for (var i = 0; i < LINES.length; i++) {
      fixPosition(LINES[i]);
    }
  };
}

var elmWrapper = document.getElementById("wrapper"),
  curTranslate = { x: 0, y: 0 },
  lines = [];

function fixPosition(line) {
  console.log("-------- `fixPosition` was called");
  var rectWrapper = elmWrapper.getBoundingClientRect(),
    translate = {
      x: (rectWrapper.left + pageXOffset) * -1,
      y: (rectWrapper.top + pageYOffset) * -1,
    };
  if (translate.x !== 0 || translate.y !== 0) {
    // Update position of wrapper
    console.log("Fix wrapper");
    curTranslate.x += translate.x;
    curTranslate.y += translate.y;
    elmWrapper.style.transform =
      "translate(" + curTranslate.x + "px, " + curTranslate.y + "px)";
    // Update position of all lines
    console.log("Fix all lines");
    lines.forEach(function (line) {
      line.position();
    });
  } else if (line) {
    // Update position of target line
    console.log("Fix target line");
    line.position();
  }
}
const checkIfKeyExist = (objectName, keyName) => {
  let keyExist = Object.keys(objectName).some((key) => key === keyName);
  return keyExist;
};


//creamos una linea entre dos nodos y metemos la instrucción
function generate_line() {
  let e = document.getElementById("origen");
  let origen = e.options[e.selectedIndex].text;
  e = document.getElementById("destino");
  let destino = e.options[e.selectedIndex].text;

  fixPosition(); // Before adding new lines
  let line = new LeaderLine(NODES[origen], NODES[destino], {color: '#CECDCE'});

  e = document.getElementById("instruccion");
  
  line.setOptions({
    middleLabel: LeaderLine.captionLabel(e.value, {color: '#646476'})
  });


  LINES.push(line);
  elmWrapper.appendChild(
    document.querySelector("body>.leader-line:last-of-type")
  );

  fixPosition(); // Before adding new lines

  if (checkIfKeyExist(pseudoCodigo, origen)) {
    pseudoCodigo[origen].push({ next: destino, instruction: e.value });
  } else{
    pseudoCodigo[origen] =[{ next: destino, instruction: e.value }];
  }
}

document.getElementById("outer").addEventListener(
  "scroll",
  AnimEvent.add(function () {
    for (var i = 0; i < LINES.length; i++) {
      fixPosition(LINES[i]);
    }
  }),
  false
);
