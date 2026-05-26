# SISTEMA DE GESTION DE EMPLEADOS - VERSION 3
# Proyecto de estructura de datos - Tercer semestre
#
# Estructura general:
# 1. Lista doblemente enlazada circular para almacenar empleados
# 2. Arbol AVL para buscar empleados por nombre de forma eficiente
# 3. Grafo ponderado para zonas de acceso, con Kruskal y Gale-Shapley

import re


# ===========================================================
# SECCION 1: LISTA DOBLEMENTE ENLAZADA CIRCULAR
# ===========================================================

class Nodo:
    """Nodo de la lista de empleados."""

    def __init__(self, id_empleado, nombre, cargo, zona_acceso):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.cargo = cargo
        self.zona_acceso = zona_acceso
        self.anterior = None
        self.siguiente = None

    def a_diccionario(self):
        return {
            "id": self.id_empleado,
            "nombre": self.nombre,
            "cargo": self.cargo,
            "zona": self.zona_acceso,
        }


class ListaEmpleados:
    """Lista doblemente enlazada circular que guarda todos los empleados."""

    def __init__(self):
        self.cabeza = None
        self.cantidad = 0

    def esta_vacia(self):
        return self.cabeza is None

    def contar_empleados(self):
        return self.cantidad

    def validar_nombre(self, nombre):
        if nombre is None or nombre.strip() == "":
            return False
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$"
        return re.match(patron, nombre) is not None

    def id_existe(self, id_empleado):
        if self.esta_vacia():
            return False
        actual = self.cabeza
        while True:
            if actual.id_empleado == id_empleado:
                return True
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return False

    def agregar_al_inicio(self, id_empleado, nombre, cargo, zona_acceso):
        if id_empleado is None or id_empleado.strip() == "":
            print("\nEl ID del empleado no puede estar vacio.")
            return False
        if self.id_existe(id_empleado):
            print(f"\nYa existe un empleado con ID '{id_empleado}'.")
            return False
        if not self.validar_nombre(nombre):
            print(f"\nNombre invalido: '{nombre}'. Solo letras y espacios.")
            return False
        if cargo is None or cargo.strip() == "":
            print("\nEl cargo no puede estar vacio.")
            return False
        if zona_acceso is None or zona_acceso.strip() == "":
            print("\nLa zona de acceso no puede estar vacia.")
            return False

        nuevo = Nodo(id_empleado, nombre, cargo, zona_acceso)

        if self.esta_vacia():
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            self.cabeza = nuevo
        else:
            ultimo = self.cabeza.anterior
            nuevo.siguiente = self.cabeza
            nuevo.anterior = ultimo
            ultimo.siguiente = nuevo
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo

        self.cantidad += 1
        print(f"\nEmpleado '{nombre}' agregado correctamente.")
        return True

    def imprimir_lista(self):
        if self.esta_vacia():
            print("\n[!] La lista esta vacia. No hay empleados registrados.")
            return

        print("\n========== LISTA DE EMPLEADOS ==========")
        actual = self.cabeza
        contador = 1

        while True:
            print(f"\nEmpleado #{contador}")
            print(f"  ID     : {actual.id_empleado}")
            print(f"  Nombre : {actual.nombre}")
            print(f"  Cargo  : {actual.cargo}")
            print(f"  Zona   : {actual.zona_acceso}")
            actual = actual.siguiente
            contador += 1
            if actual == self.cabeza:
                break

        print(f"\nTotal de empleados: {self.cantidad}")

    def buscar_por_id(self, id_buscado):
        if self.esta_vacia():
            print("\n[!] La lista esta vacia. No se puede buscar.")
            return None
        if id_buscado is None or id_buscado.strip() == "":
            print("\n[ERROR] El ID a buscar no puede estar vacio.")
            return None

        actual = self.cabeza
        while True:
            if actual.id_empleado == id_buscado:
                print("\nEmpleado encontrado:")
                print(f"  ID     : {actual.id_empleado}")
                print(f"  Nombre : {actual.nombre}")
                print(f"  Cargo  : {actual.cargo}")
                print(f"  Zona   : {actual.zona_acceso}")
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break

        print(f"\n[X] No se encontro ningun empleado con ID: {id_buscado}")
        return None


# ===========================================================
# SECCION 2: ARBOL AVL INDEXADO POR NOMBRE
# ===========================================================

class NodoAVL:
    """Nodo del arbol AVL indexado por nombre."""

    def __init__(self, nombre, datos_empleado):
        self.clave = nombre.lower()
        self.nombre = nombre
        self.empleados = [datos_empleado]
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolAVL:
    """Arbol AVL que permite buscar y listar empleados por nombre."""

    def __init__(self):
        self.raiz = None

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.izq) - self._altura(nodo.der)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    def _rotar_derecha(self, y):
        x = y.izq
        t2 = x.der
        x.der = y
        y.izq = t2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x):
        y = x.der
        t2 = y.izq
        y.izq = x
        x.der = t2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _balancear(self, nodo, clave):
        self._actualizar_altura(nodo)
        bal = self._balance(nodo)

        # Izquierda - Izquierda
        if bal > 1 and clave < nodo.izq.clave:
            return self._rotar_derecha(nodo)
        # Derecha - Derecha
        if bal < -1 and clave > nodo.der.clave:
            return self._rotar_izquierda(nodo)
        # Izquierda - Derecha
        if bal > 1 and clave > nodo.izq.clave:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)
        # Derecha - Izquierda
        if bal < -1 and clave < nodo.der.clave:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)

        return nodo

    def _insertar(self, nodo, nombre, datos_empleado):
        clave = nombre.lower()

        if nodo is None:
            return NodoAVL(nombre, datos_empleado)

        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, nombre, datos_empleado)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, nombre, datos_empleado)
        else:
            nodo.empleados.append(datos_empleado)
            return nodo

        return self._balancear(nodo, clave)

    def insertar(self, nombre, datos_empleado):
        self.raiz = self._insertar(self.raiz, nombre, datos_empleado)

    def _buscar_fragmento(self, nodo, fragmento, resultados):
        if nodo is None:
            return
        self._buscar_fragmento(nodo.izq, fragmento, resultados)
        if fragmento in nodo.clave:
            resultados.extend(nodo.empleados)
        self._buscar_fragmento(nodo.der, fragmento, resultados)

    def buscar_por_nombre(self, texto):
        fragmento = texto.strip().lower()
        resultados = []
        self._buscar_fragmento(self.raiz, fragmento, resultados)
        return resultados

    def _inorden(self, nodo, lista):
        if nodo is None:
            return
        self._inorden(nodo.izq, lista)
        lista.extend(nodo.empleados)
        self._inorden(nodo.der, lista)

    def listar_alfabetico(self):
        lista = []
        self._inorden(self.raiz, lista)
        return lista


# ===========================================================
# SECCION 3: GRAFO DE ZONAS DE ACCESO
# ===========================================================

class GrafoZonas:
    """Grafo no dirigido y ponderado para modelar zonas de acceso."""

    def __init__(self):
        self.vertices = set()
        self.adyacencia = {}

    def insertar_zona(self, zona):
        zona = zona.strip()
        if zona == "":
            print("\nZona vacia.")
            return False
        if zona in self.vertices:
            print("\nLa zona ya existe.")
            return False

        self.vertices.add(zona)
        self.adyacencia[zona] = []
        print(f"\nZona '{zona}' agregada.")
        return True

    def eliminar_zona(self, zona):
        zona = zona.strip()
        if zona not in self.vertices:
            print("\nZona no encontrada.")
            return False

        self.vertices.remove(zona)
        del self.adyacencia[zona]

        for v in self.vertices:
            self.adyacencia[v] = [(vecino, peso) for vecino, peso in self.adyacencia[v] if vecino != zona]

        print(f"\nZona '{zona}' eliminada.")
        return True

    def insertar_conexion(self, zona1, zona2, peso):
        zona1 = zona1.strip()
        zona2 = zona2.strip()

        if zona1 not in self.vertices or zona2 not in self.vertices:
            print("\nZona invalida.")
            return False
        if zona1 == zona2:
            print("\nConexion invalida.")
            return False
        if peso <= 0:
            print("\nPeso invalido.")
            return False
        if any(vecino == zona2 for vecino, _ in self.adyacencia[zona1]):
            print("\nLa conexion ya existe.")
            return False

        self.adyacencia[zona1].append((zona2, peso))
        self.adyacencia[zona2].append((zona1, peso))
        print(f"\nConexion agregada entre '{zona1}' y '{zona2}'.")
        return True

    def eliminar_conexion(self, zona1, zona2):
        zona1 = zona1.strip()
        zona2 = zona2.strip()

        if zona1 not in self.vertices or zona2 not in self.vertices:
            print("\nZona invalida.")
            return False

        existe = any(v == zona2 for v, _ in self.adyacencia[zona1])
        if not existe:
            print("\nConexion no encontrada.")
            return False

        self.adyacencia[zona1] = [(v, p) for v, p in self.adyacencia[zona1] if v != zona2]
        self.adyacencia[zona2] = [(v, p) for v, p in self.adyacencia[zona2] if v != zona1]
        print(f"\nConexion eliminada entre '{zona1}' y '{zona2}'.")
        return True

    def buscar_conexion(self, zona1, zona2):
        zona1 = zona1.strip()
        zona2 = zona2.strip()

        if zona1 not in self.vertices or zona2 not in self.vertices:
            print("\nZona invalida.")
            return None

        for vecino, peso in self.adyacencia[zona1]:
            if vecino == zona2:
                print(f"\nConexion encontrada. Peso: {peso}")
                return peso

        print("\nNo existe conexion.")
        return None

    def mostrar_grafo(self):
        if not self.vertices:
            print("\nGrafo vacio.")
            return

        print("\n========== GRAFO ==========")
        for zona in sorted(self.vertices):
            if self.adyacencia[zona]:
                conexiones = ", ".join(f"{v}({p})" for v, p in self.adyacencia[zona])
                print(f"{zona} --> {conexiones}")
            else:
                print(f"{zona} --> sin conexiones")

    def _raiz(self, padre, x):
        if padre[x] != x:
            padre[x] = self._raiz(padre, padre[x])
        return padre[x]

    def _unir(self, padre, rango, x, y):
        rx = self._raiz(padre, x)
        ry = self._raiz(padre, y)

        if rango[rx] < rango[ry]:
            padre[rx] = ry
        elif rango[rx] > rango[ry]:
            padre[ry] = rx
        else:
            padre[ry] = rx
            rango[rx] += 1

    def kruskal_mst(self):
        aristas = []
        vistos = set()

        for zona in self.vertices:
            for vecino, peso in self.adyacencia[zona]:
                clave = tuple(sorted((zona, vecino)))
                if clave not in vistos:
                    vistos.add(clave)
                    aristas.append((peso, zona, vecino))

        aristas.sort()

        padre = {v: v for v in self.vertices}
        rango = {v: 0 for v in self.vertices}
        mst = []
        costo_total = 0

        for peso, z1, z2 in aristas:
            if self._raiz(padre, z1) != self._raiz(padre, z2):
                mst.append((z1, z2, peso))
                costo_total += peso
                self._unir(padre, rango, z1, z2)

        print("\n========== KRUSKAL ==========")
        for z1, z2, peso in mst:
            print(f"{z1} <--({peso})--> {z2}")
        print(f"\nCosto total: {costo_total}")

        return mst

    def gale_shapley(self, preferencias_empleados, preferencias_zonas):
        empleados = list(preferencias_empleados.keys())
        siguiente = {e: 0 for e in empleados}
        asignado = {e: None for e in empleados}
        ocupada = {z: None for z in preferencias_zonas}

        ranking = {
            z: {emp: i for i, emp in enumerate(lista)}
            for z, lista in preferencias_zonas.items()
        }

        libres = empleados[:]

        while libres:
            emp = libres.pop(0)
            prefs = preferencias_empleados.get(emp, [])

            if siguiente[emp] >= len(prefs):
                continue

            zona = prefs[siguiente[emp]]
            siguiente[emp] += 1

            actual = ocupada.get(zona)

            if actual is None:
                ocupada[zona] = emp
                asignado[emp] = zona
            else:
                nuevo = ranking.get(zona, {}).get(emp, float("inf"))
                viejo = ranking.get(zona, {}).get(actual, float("inf"))

                if nuevo < viejo:
                    ocupada[zona] = emp
                    asignado[emp] = zona
                    asignado[actual] = None
                    libres.append(actual)
                else:
                    libres.append(emp)

        print("\n========== GALE SHAPLEY ==========")
        for emp in asignado:
            print(f"{emp} --> {asignado[emp]}")

        return asignado


# ===========================================================
# SECCION 4: REGISTRO DE ACCESOS Y HORARIOS
# ===========================================================
# Esta seccion acerca el sistema a la descripcion del proyecto.
# Aqui se registran:
# - Entradas y salidas
# - Tiempo de permanencia
# - Historial de movimientos
# - Reportes simples
#
# Cada acceso queda guardado como un diccionario dentro de una lista.
# Esto simula una pequena base de datos en memoria.

class RegistroAccesos:

    # zonas permitidas segun el cargo
    # esto permite simular areas restringidas
    zonas_permitidas = {
        "Administrador": ["Entrada", "Oficina", "Servidor", "Bodega"],
        "Seguridad": ["Entrada", "Bodega"],
        "Empleado": ["Entrada", "Oficina"]
    }

    def __init__(self):
        self.registros = []

    # registrar entrada de empleado
    def registrar_entrada(self, id_empleado, nombre, cargo, zona, hora):

        registro = {
            "id": id_empleado,
            "nombre": nombre,
            "zona": zona,
            "hora_entrada": hora,
            "hora_salida": None,
            "movimientos": [zona]
        }

        # validar acceso segun el cargo
        permitidas = self.zonas_permitidas.get(cargo, [])

        if zona not in permitidas:
            print("Acceso denegado. Zona restringida para este cargo.")
            return False

        self.registros.append(registro)

        print(f"Entrada registrada para {nombre}.")

    # registrar salida
    def registrar_salida(self, id_empleado, hora_salida):

        for registro in reversed(self.registros):

            if registro["id"] == id_empleado and registro["hora_salida"] is None:

                registro["hora_salida"] = hora_salida

                print(f"Salida registrada para {registro['nombre']}.")
                return True

        print("No se encontro una entrada activa para ese empleado.")
        return False

    # mostrar historial completo
    # registrar movimiento entre zonas
    def registrar_movimiento(self, id_empleado, nueva_zona):

        for registro in reversed(self.registros):

            if registro["id"] == id_empleado and registro["hora_salida"] is None:

                registro["movimientos"].append(nueva_zona)

                print(f"Movimiento registrado hacia {nueva_zona}.")
                return True

        print("No existe una entrada activa para ese empleado.")
        return False

    def mostrar_registros(self):

        if not self.registros:
            print("No hay registros guardados.")
            return

        print("========== REGISTRO DE ACCESOS ==========")

        for i, r in enumerate(self.registros, 1):

            print(f"Registro #{i}")
            print(f"Empleado : {r['nombre']}")
            print(f"ID       : {r['id']}")
            print(f"Zona     : {r['zona']}")
            print(f"Entrada  : {r['hora_entrada']}")
            print(f"Salida   : {r['hora_salida']}")
            print(f"Movimientos: {' -> '.join(r['movimientos'])}")

    # reporte por empleado
    def reporte_empleado(self, id_empleado):

        encontrados = [r for r in self.registros if r['id'] == id_empleado]

        if not encontrados:
            print("No hay registros para ese empleado.")
            return

        print("========== REPORTE DEL EMPLEADO ==========")

        for r in encontrados:

            print(f"Nombre   : {r['nombre']}")
            print(f"Zona     : {r['zona']}")
            print(f"Entrada  : {r['hora_entrada']}")
            print(f"Salida   : {r['hora_salida']}")


# ===========================================================
# SECCION 5: FUNCIONES DE INTERFAZ EN CONSOLA
# ===========================================================

def mostrar_menu():
    print("\n╔═════════════════════════════════════════╗")
    print("║   SISTEMA DE GESTION DE EMPLEADOS V3    ║")
    print("╠═════════════════════════════════════════╣")
    print("║  FUNCIONES DE LISTA                     ║")
    print("║  1. Verificar si la lista esta vacia    ║")
    print("║  2. Contar empleados registrados        ║")
    print("║  3. Ver todos los empleados             ║")
    print("║  4. Agregar nuevo empleado              ║")
    print("║  5. Buscar empleado por ID              ║")
    print("╠═════════════════════════════════════════╣")
    print("║  FUNCIONES DEL ARBOL AVL                ║")
    print("║  6. Buscar empleados por nombre         ║")
    print("║  7. Ver empleados en orden alfabetico   ║")
    print("╠═════════════════════════════════════════╣")
    print("║  FUNCIONES DEL GRAFO                    ║")
    print("║  8. Ver red de zonas                    ║")
    print("║  9. Agregar zona al grafo               ║")
    print("║ 10. Agregar conexion entre zonas        ║")
    print("║ 11. Eliminar zona del grafo             ║")
    print("║ 12. Eliminar conexion entre zonas       ║")
    print("║ 13. Buscar conexion entre dos zonas     ║")
    print("║ 14. Kruskal                             ║")
    print("║ 15. Gale Shapley                        ║")
    print("║ 16. Registrar entrada                   ║")
    print("║ 17. Registrar salida                    ║")
    print("║ 18. Ver historial de accesos            ║")
    print("║ 19. Reporte por empleado                ║")
    print("╠═════════════════════════════════════════╣")
    print("║  0. Salir                               ║")
    print("╚═════════════════════════════════════════╝")
    print("Seleccione una opcion: ", end="")


def mostrar_empleado(emp):
    print(f"ID: {emp['id']}")
    print(f"Nombre: {emp['nombre']}")
    print(f"Cargo: {emp['cargo']}")
    print(f"Zona: {emp['zona']}")


def ingresar_preferencias_gale():
    preferencias_emp = {}
    preferencias_zona = {}

    n_empleados = int(input("Cantidad de empleados: ").strip())
    for _ in range(n_empleados):
        emp = input("Nombre del empleado: ").strip()
        prefs = input("Zonas por prioridad separadas por coma: ").strip().split(",")
        preferencias_emp[emp] = [z.strip() for z in prefs if z.strip()]

    n_zonas = int(input("Cantidad de zonas: ").strip())
    for _ in range(n_zonas):
        zona = input("Nombre de la zona: ").strip()
        prefs = input("Empleados por prioridad separados por coma: ").strip().split(",")
        preferencias_zona[zona] = [e.strip() for e in prefs if e.strip()]

    return preferencias_emp, preferencias_zona


# ===========================================================
# SECCION 5: FUNCION PRINCIPAL
# ===========================================================

def main():
    lista = ListaEmpleados()
    accesos = RegistroAccesos()
    avl = ArbolAVL()
    grafo = GrafoZonas()

    print("\nBienvenido al Sistema de Gestion de Empleados V3")

    while True:
        mostrar_menu()
        opcion = input().strip()

        if opcion == "1":
            if lista.esta_vacia():
                print("\nLa lista esta vacia.")
            else:
                print(f"\nHay {lista.contar_empleados()} empleado(s).")

        elif opcion == "2":
            print(f"\nTotal de empleados: {lista.contar_empleados()}")

        elif opcion == "3":
            lista.imprimir_lista()

        elif opcion == "4":
            id_emp = input("ID: ").strip()
            nombre = input("Nombre: ").strip()
            cargo = input("Cargo: ").strip()
            zona = input("Zona: ").strip()

            if lista.agregar_al_inicio(id_emp, nombre, cargo, zona):
                avl.insertar(nombre, {
                    "id": id_emp,
                    "nombre": nombre,
                    "cargo": cargo,
                    "zona": zona,
                })

        elif opcion == "5":
            id_buscar = input("ID a buscar: ").strip()
            lista.buscar_por_id(id_buscar)

        elif opcion == "6":
            texto = input("Nombre o fragmento: ").strip()
            resultados = avl.buscar_por_nombre(texto)

            if resultados:
                for i, emp in enumerate(resultados, 1):
                    print(f"\nResultado {i}")
                    mostrar_empleado(emp)
            else:
                print("\nNo se encontraron resultados.")

        elif opcion == "7":
            empleados = avl.listar_alfabetico()
            if empleados:
                for i, emp in enumerate(empleados, 1):
                    print(f"{i}. [{emp['id']}] {emp['nombre']} | {emp['cargo']} | {emp['zona']}")
            else:
                print("\nNo hay empleados registrados.")

        elif opcion == "8":
            grafo.mostrar_grafo()

        elif opcion == "9":
            zona = input("Zona: ").strip()
            grafo.insertar_zona(zona)

        elif opcion == "10":
            zona1 = input("Zona 1: ").strip()
            zona2 = input("Zona 2: ").strip()
            try:
                peso = int(input("Peso: ").strip())
                grafo.insertar_conexion(zona1, zona2, peso)
            except ValueError:
                print("\nPeso invalido.")

        elif opcion == "11":
            zona = input("Zona a eliminar: ").strip()
            grafo.eliminar_zona(zona)

        elif opcion == "12":
            zona1 = input("Zona 1: ").strip()
            zona2 = input("Zona 2: ").strip()
            grafo.eliminar_conexion(zona1, zona2)

        elif opcion == "13":
            zona1 = input("Zona 1: ").strip()
            zona2 = input("Zona 2: ").strip()
            grafo.buscar_conexion(zona1, zona2)

        elif opcion == "14":
            grafo.kruskal_mst()

        elif opcion == "15":
            preferencias_emp, preferencias_zona = ingresar_preferencias_gale()
            grafo.gale_shapley(preferencias_emp, preferencias_zona)

        elif opcion == "16":

            id_emp = input("ID empleado: ").strip()
            nombre = input("Nombre: ").strip()
            cargo = input("Cargo: ").strip()
            zona = input("Zona de acceso: ").strip()
            hora = input("Hora de entrada (HH:MM): ").strip()

            if zona not in grafo.vertices:
                print("La zona no existe en el grafo.")
            else:
                accesos.registrar_entrada(id_emp, nombre, cargo, zona, hora)

        elif opcion == "17":

            id_emp = input("ID empleado: ").strip()
            hora = input("Hora de salida (HH:MM): ").strip()

            accesos.registrar_salida(id_emp, hora)

        elif opcion == "18":

            accesos.mostrar_registros()

        elif opcion == "19":

            id_emp = input("ID empleado: ").strip()
            accesos.reporte_empleado(id_emp)

        elif opcion == "0":
            print("\nHasta luego.")
            break

        else:
            print("\nOpcion invalida.")


if __name__ == "__main__":
    main()
