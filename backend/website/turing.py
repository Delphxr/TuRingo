import json

debug = True

max_steps = 150 #numero total de pasos que la maquina puede hacer, así evitamos maquinas que tengan un loop infinito


class TuringMachine:
    def __init__(self):
        # Inicializa la máquina con el JSON de entrada y el estado actual 'q0'
        self.input_json = ""
        self.current_state = '_'
        self.vacio = "_"
        self.margin_index = 100

    def set_code(self, code):
        self.input_json = json.loads(code)  # guardamos el json

        # buscamos el estado inicial
        for i in self.input_json:
            #print(self.input_json[i]["inicial"])
            if (self.input_json[i]["inicial"] == "True"):
                self.current_state = i
                return

    def set_blank(self, blank_character):
        self.vacio = blank_character

    def get_margin_input(self, entrada):
        margenes = self.vacio * self.margin_index
        if (entrada == None):
            entrada = margenes
        return margenes + entrada + margenes
    

    def run(self, entrada):

        if self.current_state == "_":
            return {'error': 'no hay nodo inicial'}
        # Inicializa la cinta y el índice inicial
        current_step = 0
        cinta = self.get_margin_input(entrada)
        index = self.margin_index
        cinta_inicial = cinta

        # Crea una lista vacía para guardar las instrucciones de cada estado
        instrucciones = []

        # Ciclo principal que se ejecuta mientras el estado actual tenga instrucciones
        end = True
        sin_salida = True #si entramos en un nodo, y no hay ninguna transicion viable, llegamos a un callejon sin salida
        while end:
            sin_salida = True
            # Obtiene las instrucciones para el estado actual del JSON de entrada
            state = self.input_json[self.current_state]

            # iteramos las intrucciones
            for instruction in state['instrucciones']:
                
                #si lo que queremos leer no es igual al elemento actual de la cinta, no podemos hacer nada
                if (instruction["leer"] != cinta[index]):
                    continue

                current_step += 1

                sin_salida = False

                cinta = cinta[:index] + instruction['escribir'] + cinta[index+1:]
                
                if instruction['direccion'] == "R":
                    index += 1
                elif instruction['direccion'] == "L":
                    index -= 1

                # Agrega la instrucción actual a la lista de instrucciones
                instrucciones.append({
                    "movimiento": instruction['direccion'],
                    "valorNuevo": instruction['escribir'],
                    "nodo": instruction['estado_siguiente']
                })

                if (index < 0 or len(cinta) <= index): # nos salimos al llegar al final de la cinta
                    end = False
                    break  

                # Actualiza el estado actual de la máquina con el estado siguiente de la instrucción
                self.current_state = instruction['estado_siguiente']
                break

            #print(sin_salida)
            if (sin_salida or current_step > max_steps):
                end = False

        # Crea un diccionario con la información final y lo devuelve
        output_dict = {
            "indexInicial": self.margin_index,
            "cintaInicial": cinta_inicial,
            "instrucciones": instrucciones
        }
        return output_dict

    def run_cinta(self, entrada):

        if self.current_state == "_":
            return {'error': 'no hay nodo inicial'}

        # Inicializa la cinta y el índice inicial
        cinta = self.get_margin_input(entrada)
        index = self.margin_index
        cinta_inicial = cinta
        current_step = 0

        # Crea una lista vacía para guardar las instrucciones de cada estado
        instrucciones = []

        # Ciclo principal que se ejecuta mientras el estado actual tenga instrucciones
        end = True
        sin_salida = True #si entramos en un nodo, y no hay ninguna transicion viable, llegamos a un callejon sin salida
        while end:
            sin_salida = True
            # Obtiene las instrucciones para el estado actual del JSON de entrada
            state = self.input_json[self.current_state]

            # iteramos las intrucciones
            for instruction in state['instrucciones']:
                
                #si lo que queremos leer no es igual al elemento actual de la cinta, no podemos hacer nada
                if (instruction["leer"] != cinta[index]):
                    continue

                current_step += 1

                sin_salida = False

                cinta = cinta[:index] + instruction['escribir'] + cinta[index+1:]
                
                if instruction['direccion'] == "R":
                    index += 1
                elif instruction['direccion'] == "L":
                    index -= 1

                # Agrega la instrucción actual a la lista de instrucciones
                instrucciones.append({
                    "movimiento": instruction['direccion'],
                    "valorNuevo": instruction['escribir'],
                    "nodo": instruction['estado_siguiente']
                })

                if (index < 0 or len(cinta) <= index): # nos salimos al llegar al final de la cinta
                    end = False
                    break  

                # Actualiza el estado actual de la máquina con el estado siguiente de la instrucción
                self.current_state = instruction['estado_siguiente']
                break

            #print(sin_salida)
            if (sin_salida or current_step > max_steps):
                end = False

        # Crea un diccionario con la información final y lo devuelve
        output_dict = {
            "cintaInicial": cinta_inicial,
            "cintaFinal": cinta
        }
        return output_dict

    def get_nota(self, casos):

        nota_div = len(casos)
        nota = 0

        lista = []

        for caso in casos:
            
            input_case = caso["entrada"]
            resultado_case = self.run_cinta(input_case)
            resultado_estudiante = resultado_case["cintaFinal"]

            entrada_margin = self.get_margin_input(caso["salida"])
            

            if resultado_estudiante == entrada_margin:
                nota += 1
            
            lista.append({
                "input": caso["entrada"],
                "respuesta" : entrada_margin,
                "estudiante": resultado_estudiante
            })
        return lista
        return (nota*100)/nota_div


#esto es un ejempl
malo = '{"q0":{"inicial":"True","apodo":"","instrucciones":[{"leer":"a","escribir":"_","direccion":"R","estado_siguiente":"q2"},{"leer":"b","escribir":"_","direccion":"R","estado_siguiente":"q1"}]},"q1":{"inicial":"False","apodo":"","instrucciones":[{"leer":"a","escribir":"a","direccion":"R","estado_siguiente":"q1"},{"leer":"b","escribir":"b","direccion":"R","estado_siguiente":"q1"}]},"q2":{"inicial":"False","apodo":"","instrucciones":[{"leer":"a","escribir":"a","direccion":"R","estado_siguiente":"q2"},{"leer":"b","escribir":"b","direccion":"R","estado_siguiente":"q2"}]}}'
bueno = '{"q0":{"inicial":"True","apodo":"","instrucciones":[{"leer":"b","escribir":"_","direccion":"R","estado_siguiente":"q1"},{"leer":"a","escribir":"_","direccion":"R","estado_siguiente":"q2"}]},"q1":{"inicial":"False","apodo":"","instrucciones":[{"leer":"a","escribir":"a","direccion":"R","estado_siguiente":"q1"},{"leer":"b","escribir":"b","direccion":"R","estado_siguiente":"q1"}]},"q2":{"inicial":"False","apodo":"","instrucciones":[{"leer":"a","escribir":"a","direccion":"R","estado_siguiente":"q2"},{"leer":"b","escribir":"b","direccion":"R","estado_siguiente":"q2"}]}}'

maquina = TuringMachine()
maquina.set_code(malo)
maquina.set_blank("_")

print("\n\n\nMALO:\n\n\n")

print(maquina.run("abba"))

print("\n\n\nBUENO:\n\n\n")

maquina.set_code(bueno)
print(maquina.run("abba"))
