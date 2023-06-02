class PseudoCodigo {
  constructor() {
    this.codigo = {};
    this.apodos = {};
    this.inicial = -1;
    this.id = 0;
  }

  generateId() {
    let newID = "q" + this.id;
    this.id = this.id + 1;
    
    this.codigo[newID] = [];

    return newID;
  }

  definirApodo(Id, apodo) {
    this.apodos[Id] = apodo;
  }

  setInicial(Id) {
    this.inicial = Id;
  }

  //retorna el apodo si existe, o si no el ID
  obtenerApodo(Id) {
    return this.apodos.hasOwnProperty(Id) ? this.apodos[Id] : Id;
  }

  agregarLinea(Id, leer, escribir, direccion, estadoSiguiente) {
    // verificar si origen ya existe en el código
    if (this.codigo[Id]) {
      this.codigo[Id].push({
        leer: leer,
        escribir: escribir,
        direccion: direccion,
        estado_siguiente: estadoSiguiente,
      });
    } else {
      this.codigo[Id] = [
        {
          leer: leer,
          escribir: escribir,
          direccion: direccion,
          estado_siguiente: estadoSiguiente,
        },
      ];
    }
  }

  obtenerCodigoJson(entrada, vacio) {
    const codigo = {};

    for (let id in this.codigo) {
      const instrucciones = this.codigo[id];
      const apodo = this.apodos[id] || "";
      const inicial = ((id == this.inicial) ? 'True' : 'False');

      codigo[id] = {
        inicial: inicial,
        apodo: apodo,
        instrucciones: instrucciones,
      };
    }

    const codigoConInfo = {
      codigo: codigo,
      entrada: entrada,
      vacio: vacio
    };

    return JSON.stringify(codigoConInfo, null, 2);
  }

  guardarCodigoActual(){
    let entrada = document.getElementById("entradaCinta").value
    let vacio = document.getElementById("vacioCinta").value

    if (vacio === "") {
      vacio = "_"
    }
    
    var pseudoCodigoSaved = JSON.stringify(this.codigo);;
    var apodosSaved = JSON.stringify(this.apodos)
    var inicialSaved = this.inicial
    var idSaved = this.id

    saveEditorVariables();

    localStorage.setItem('pseudoCodigoSaved', pseudoCodigoSaved);
    localStorage.setItem('apodosSaved', apodosSaved);
    localStorage.setItem('inicialSaved', inicialSaved);
    localStorage.setItem('idSaved', idSaved);
    console.log("Maquina guardada")
  }

  cargarCodigoActual(){
    var pseudoCodigoString = localStorage.getItem('pseudoCodigoSaved');
    var apodosString = localStorage.getItem('apodosSaved');

    var inicialSaved = localStorage.getItem('inicialSaved');
    var idSaved = localStorage.getItem('idSaved');
    var idIntSaved = parseInt(idSaved);

    var pseudoCodigoSaved = JSON.parse(localStorage.getItem("pseudoCodigoSaved"));
    var apodosSaved = JSON.parse(apodosString);

    loadEditorVariables();

    this.codigo = pseudoCodigoSaved;
    this.apodos = apodosSaved;
    this.inicial = inicialSaved;
    this.id = idIntSaved;

    console.log("Codigo cargado")
  }

  eliminarNodo(Id) {
    for (let i in this.codigo) {
      const instrucciones = this.codigo[i];
      for (let j in instrucciones) {
        if (instrucciones[j]["estado_siguiente"] == Id) {
          delete instrucciones[j];
          instrucciones.splice(j, 1);
        }
      }
    }

    delete this.codigo[Id];
    delete this.apodos[Id];
  }
}

