const Pannable = (elViewport) => {
  const start = { x: 0, y: 0 };
  let isPan = false;

  // Función para capturar el evento de inicio del arrastre
  const panStart = (ev) => {
    ev.preventDefault();
    isPan = true;
    start.x = elViewport.scrollLeft + ev.clientX;
    start.y = elViewport.scrollTop + ev.clientY;
  };

  // Función para capturar el evento de arrastre
  const panMove = (ev) => {
    if (!isPan) return;
    // Calcula la nueva posición de la vista restando las coordenadas del mouse en el evento actual
    elViewport.scrollTo(start.x - (ev.clientX), start.y - (ev.clientY));
  };

  // Función para capturar el evento de finalización del arrastre
  const panEnd = (ev) => {
    isPan = false;
  };

  // Agregar los eventos necesarios al viewport
  elViewport.addEventListener("mousedown", panStart);
  addEventListener("mousemove", panMove);
  addEventListener("mouseup", panEnd);
};

// Seleccionar todos los elementos con clase "outer-scroll" y aplicarles la función Pannable
document.querySelectorAll(".outer-scroll").forEach(Pannable);


const outer = document.getElementById("outer");
const inner = document.getElementById("canvas")


outer.scrollTo( (outer.scrollWidth - outer.offsetWidth)/2, (outer.scrollHeight - outer.offsetHeight) / 2);
