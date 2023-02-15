let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");

let cameraOffset = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
let cameraZoom = 1;
let MAX_ZOOM = 5;
let MIN_ZOOM = 0.1;
let SCROLL_SENSITIVITY = 0.0005;

let MOUSE_POSITION = { x: 0, y: 0 };

function draw() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  // Translate to the canvas centre before zooming - so you'll always zoom on what you're looking directly at
  ctx.translate(window.innerWidth / 2, window.innerHeight / 2);
  ctx.scale(cameraZoom, cameraZoom);
  ctx.translate(
    -window.innerWidth / 2 + cameraOffset.x,
    -window.innerHeight / 2 + cameraOffset.y
  );
  
  ctx.fillStyle = "#991111";
  drawRect(-50, -50, 100, 100);


  
  requestAnimationFrame(draw);
}

// Gets the relevant location from a mouse or single touch event
function getEventLocation(e) {
  if (e.touches && e.touches.length == 1) {
    return { x: e.touches[0].clientX, y: e.touches[0].clientY };
  } else if (e.clientX && e.clientY) {
    return { x: e.clientX, y: e.clientY };
  }
}

function drawRect(x, y, width, height) {
  ctx.fillRect(x, y, width, height);
}

function drawText(text, x, y, size, font) {
  ctx.font = `${size}px ${font}`;
  ctx.fillText(text, x, y);
}

let isDragging = false;
let dragStart = { x: 0, y: 0 };

function onPointerDown(e) {
  if (e.button == 0) {
    isDragging = true;
    dragStart.x = getEventLocation(e).x / cameraZoom - cameraOffset.x;
    dragStart.y = getEventLocation(e).y / cameraZoom - cameraOffset.y;
  } else {
    MOUSE_POSITION.x = 30  / cameraZoom - cameraOffset.x;
    MOUSE_POSITION.y = 30  / cameraZoom - cameraOffset.y;
  }
}

function onPointerUp(e) {
  if (e.button == 0) {
    isDragging = false;
    lastZoom = cameraZoom;
  }
}

function onPointerMove(e) {
  if (isDragging) {
    cameraOffset.x = getEventLocation(e).x / cameraZoom - dragStart.x;
    cameraOffset.y = getEventLocation(e).y / cameraZoom - dragStart.y;
  }
}

function adjustZoom(zoomAmount, zoomFactor) {
  if (!isDragging) {
    if (zoomAmount) {
      cameraZoom -= zoomAmount;
    } else if (zoomFactor) {

      cameraZoom = zoomFactor * lastZoom;
    }

    cameraZoom = Math.min(cameraZoom, MAX_ZOOM);
    cameraZoom = Math.max(cameraZoom, MIN_ZOOM);


  }
}

canvas.addEventListener("mousedown", onPointerDown);
canvas.addEventListener("mouseup", onPointerUp);
canvas.addEventListener("mousemove", onPointerMove);
canvas.addEventListener("wheel", (e) =>
  adjustZoom(e.deltaY * SCROLL_SENSITIVITY)
);

// Ready, set, go
draw();
