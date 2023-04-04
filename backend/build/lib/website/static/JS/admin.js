function addInstruction() {
    let es = document.getElementById("entradasalida")

    console.log(es)

    let form = document.createElement('div'); // is a node
    form.innerHTML = '<div class="row g-3 pt-1 align-items-center">' +
    '<div class="col-auto">'+
    ' <label>Entrada:</label>'+
    '</div>'+
    '<div class="col-4">'+
    ' <input class="form-control mx-0" type="text" id="read" ></input>'+
    ' </div>'+
    '<div class="col-auto">'+
    '<label>Salida:</label>'+
    '</div>'+
    '<div class="col-4">'+
    ' <input class="form-control" type="text" id="write" ></input>'+
    '</div>'

    es.append(form)
}