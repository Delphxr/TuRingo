import json

debug = True


class TuringMachine:
    def __init__(self):
        # Inicializa la máquina con el JSON de entrada y el estado actual 'q0'
        self.input_json = ""
        self.current_state = '_'
        self.vacio = "_"

    def set_code(self, code):
        self.input_json = json.loads(code)  # guardamos el json

        # buscamos el estado inicial
        for i in self.input_json:
            print(self.input_json[i]["inicial"])
            if (self.input_json[i]["inicial"] == "True"):
                self.current_state = i
                return

    def set_blank(self, blank_character):
        self.vacio = blank_character

    def run(self, entrada):

        if self.current_state == "_":
            return {'error': 'no hay nodo inicial'}

        # Inicializa la cinta y el índice inicial
        margin_index = 100
        margenes = self.vacio * margin_index
        index = margin_index
        if (entrada == None):
            entrada = margenes
        cinta = margenes + entrada + margenes
        cinta_inicial = cinta

        # Crea una lista vacía para guardar las instrucciones de cada estado
        instrucciones = []

        # Ciclo principal que se ejecuta mientras el estado actual tenga instrucciones
        end = True
        sin_salida = True
        while end:
            sin_salida = True
            # Obtiene las instrucciones para el estado actual del JSON de entrada
            state = self.input_json[self.current_state]

            # iteramos las intrucciones
            for instruction in state['instrucciones']:
                print(instruction["leer"], cinta[index])
                # Actualiza la cinta y el índice según la instrucción
                if (instruction["leer"] != cinta[index]):
                    continue

                sin_salida = False

                if instruction['direccion'] == "R":
                    cinta = cinta[:index] + \
                        instruction['escribir'] + cinta[index+1:]
                    index += 1
                elif instruction['direccion'] == "L":
                    cinta = cinta[:index] + \
                        instruction['escribir'] + cinta[index+1:]
                    index -= 1

                # Agrega la instrucción actual a la lista de instrucciones
                instrucciones.append({
                    "movimiento": instruction['direccion'],
                    "valorNuevo": instruction['escribir'],
                    "nodo": self.current_state
                })

                if (index < 0 or len(cinta) <= index):
                    end = False
                    break  # nos salimos al finalizar la cinta
                # Actualiza el estado actual de la máquina con el estado siguiente de la instrucción
                self.current_state = instruction['estado_siguiente']

            print(sin_salida)
            if (sin_salida):
                end = False

        # Crea un diccionario con la información final y lo devuelve
        output_dict = {
            "indexInicial": margin_index,
            "cintaInicial": cinta_inicial,
            "instrucciones": instrucciones
        }
        return output_dict


# code = '{"q0":{"inicial":"True","apodo":"","instrucciones":[{"leer":" ","escribir":"_","direccion":"R","estado_siguiente":"q4"}]},"q3":{"inicial":"False","apodo":"","instrucciones":[{"leer":"_","escribir":"_","direccion":"R","estado_siguiente":"q2"}]},"q4":{"inicial":"False","apodo":"","instrucciones":[{"leer":"_","escribir":"0","direccion":"R","estado_siguiente":"q3"}]},"q2":{"inicial":"False","apodo":"","instrucciones":[{"leer":"_","escribir":"1","direccion":"R","estado_siguiente":"q0"}]}}'

# maquina = TuringMachine()
# maquina.set_code(code)

# print(maquina.run(None))
