import json
import os
import random
import time
import sys
import msvcrt
#  RUNTIME GENERAL
class GameRuntime:
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            print(f"No se encontró el archivo: {config_file}")
            sys.exit(1)

        with open(config_file, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        nombre = self.config.get("nombre_juego", "").lower()
        if "snake" in nombre:
            self.juego = SnakeGame(self.config)
        else:
            print("No se reconoce el tipo de juego en la configuración.")
            sys.exit(1)

    def run(self):
        self.juego.run()
#  CLASE BASE PARA JUEGOS
class BaseGame:
    def __init__(self, config):
        self.config = config

    def run(self):
        raise NotImplementedError
#  IMPLEMENTACIÓN DE SNAKE
class SnakeGame(BaseGame):
    def __init__(self, config):
        super().__init__(config)
        self.ancho = config.get("ancho", 40)
        self.alto = config.get("alto", 30)
        self.velocidad = config.get("velocidad", 5)
        self.longitud_inicial = config.get("longitud_inicial", 3)
        self.comidas = config.get("comidas", [])
        self.color_serpiente = config.get("color_serpiente", "verde")
        self.controles = config.get("controles", {
            "mover_izquierda": "a",
            "mover_derecha": "d",
            "mover_arriba": "w",
            "mover_abajo": "s"
        })
        # Estado inicial
        self.snake = [(self.ancho//2, self.alto//2)]
        self.direccion = "derecha"
        self.puntaje = 0
        self.fruta = None
        self.generar_fruta()
        # Ajuste visual a 640x480
        os.system("mode con: cols=80 lines=30")
    #  DIBUJAR TABLERO
    def mostrar_tablero(self):
        os.system("cls")
        print(f"{self.config['nombre_juego']} | Puntaje: {self.puntaje}")
        print("╔" + "═"*self.ancho + "╗")
        for y in range(self.alto):
            fila = ""
            for x in range(self.ancho):
                if (x, y) in self.snake:
                    fila += "O"
                elif self.fruta and self.fruta["pos"] == (x, y):
                    tipo = self.fruta["tipo"]
                    if tipo == "bonus":
                        fila += "+"
                    else:
                        fila += "*"
                else:
                    fila += " "
            print("║" + fila + "║")
        print("╚" + "═"*self.ancho + "╝")
        print("Usa W, A, S, D para moverte. Presiona Q para salir.")
    #  ENTRADAS
    def leer_tecla(self):
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            try:
                t = tecla.decode("latin-1").lower()
                if t in ["w", "a", "s", "d", "q"]:
                    return t
            except:
                if tecla == b'\xe0':
                    k = msvcrt.getch()
                    if k == b'H': return "w"  # ↑
                    elif k == b'P': return "s"  # ↓
                    elif k == b'K': return "a"  # ←
                    elif k == b'M': return "d"  # →
        return None
    #  DIRECCIÓN Y MOVIMIENTO
    def actualizar_direccion(self, tecla):
        if tecla == "w" and self.direccion != "abajo":
            self.direccion = "arriba"
        elif tecla == "s" and self.direccion != "arriba":
            self.direccion = "abajo"
        elif tecla == "a" and self.direccion != "derecha":
            self.direccion = "izquierda"
        elif tecla == "d" and self.direccion != "izquierda":
            self.direccion = "derecha"
    def mover_snake(self):
        cabeza_x, cabeza_y = self.snake[0]
        if self.direccion == "arriba": cabeza_y -= 1
        elif self.direccion == "abajo": cabeza_y += 1
        elif self.direccion == "izquierda": cabeza_x -= 1
        elif self.direccion == "derecha": cabeza_x += 1
        nueva_cabeza = (cabeza_x, cabeza_y)
        # Colisiones
        if (nueva_cabeza in self.snake or
            cabeza_x < 0 or cabeza_x >= self.ancho or
            cabeza_y < 0 or cabeza_y >= self.alto):
            os.system("cls")
            print("¡Game Over!")
            print(f"Puntaje final: {self.puntaje}")
            time.sleep(2)
            sys.exit(0)
        self.snake.insert(0, nueva_cabeza)
        # Comer fruta
        if self.fruta and self.fruta["pos"] == nueva_cabeza:
            puntos = self.fruta.get("puntos", 10)
            incremento = self.fruta.get("incremento", 1)
            self.puntaje += puntos
            for _ in range(abs(incremento)):
                self.snake.append(self.snake[-1])
            # Generar solo una nueva fruta después de comer
            self.generar_fruta()
        else:
            self.snake.pop()
    #  FRUTA
    def generar_fruta(self):
        fruta_tipo = random.choice(self.comidas)
        while True:
            pos = (random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1))
            if pos not in self.snake:
                break
        fruta_instancia = dict(fruta_tipo)
        fruta_instancia["tipo"] = fruta_tipo["nombre"]
        fruta_instancia["pos"] = pos
        self.fruta = fruta_instancia  # solo una fruta activa
    #  BUCLE PRINCIPAL
    def run(self):
        print("Iniciando Snake... Presiona Q para salir.")
        time.sleep(1)
        while True:
            tecla = self.leer_tecla()
            if tecla == "q":
                print("Juego terminado por el usuario.")
                break
            if tecla:
                self.actualizar_direccion(tecla)
            self.mover_snake()
            self.mostrar_tablero()
            time.sleep(1 / self.velocidad)
#  EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    runtime = GameRuntime("config_snake.ast")
    runtime.run()







