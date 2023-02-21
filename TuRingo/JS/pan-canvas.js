const Pannable = (elViewport) => {
  const start = { x: 0, y: 0 };
  let isPan = false;

  const panStart = (ev) => {
    ev.preventDefault();
    isPan = true;
    start.x = elViewport.scrollLeft + ev.clientX;
    start.y = elViewport.scrollTop + ev.clientY;
  };

  const panMove = (ev) => {
    if (!isPan) return;
    elViewport.scrollTo(start.x - (ev.clientX), start.y - (ev.clientY));
  };

  const panEnd = (ev) => {
    isPan = false;
  };

  elViewport.addEventListener("mousedown", panStart);
  addEventListener("mousemove", panMove);
  addEventListener("mouseup", panEnd);
};

document.querySelectorAll(".outer-scroll").forEach(Pannable);
const outer = document.getElementById("outer");
const inner = document.getElementById("canvas")
outer.scrollTo( (outer.scrollWidth - outer.offsetWidth)/2, (outer.scrollHeight - outer.offsetHeight) / 2);
