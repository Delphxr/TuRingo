class PseudoCodigo {
  constructor() {
    this.codigo = {};
    this.apodos = {};
    this.id = 0;
  }

  generateId() {
    let newID = "q" + this.id;
    this.id = this.id + 1;
    return newID;
  }

  definirApodo(Id, apodo) {
    this.apodos[Id] = apodo;
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

  obtenerCodigoJson() {
    const codigo = {};

    for (let origen in this.codigo) {
      const instrucciones = this.codigo[origen];
      const apodo = this.apodos[origen] || "";

      codigo[origen] = {
        apodo: apodo,
        instrucciones: instrucciones,
      };
    }

    return JSON.stringify(codigo, null, 2);
  }

  eliminarNodo(Id) {
    for (let i in this.codigo) {
      const instrucciones = this.codigo[i];
      for (let j in instrucciones) {
        if (instrucciones[j]["estado_siguiente"] == Id) {
            delete instrucciones[j];
            instrucciones.splice(j,1);
        }
      }
    }

    delete this.codigo[Id];
    delete this.apodos[Id];
  }
}
