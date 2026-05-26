# SISTEMA DE GESTION DE EMPLEADOS - VERSION 2
# Proyecto de estructura de datos - Tercer semestre
# Implementacion con Lista Doblemente Enlazada Circular + Arbol AVL
#
# MEJORA VERSION 2: Se agrega un Arbol AVL indexado por nombre de empleado.
# Esto permite:
#   - Buscar empleados por nombre (o fragmento) de forma eficiente
#   - Listar todos los empleados en orden alfabetico por nombre
#   - El arbol se autobalancea (AVL) para garantizar busquedas en O(log n)
#     en lugar del O(n) lineal que tenia la lista enlazada
#
# Integrante 1: David Santiago Cediel Remolina - 2250933
# Integrante 2: David Santiago Gomez Caicedo   - 2252119
# Integrante 3: Daniel Andres Floraz Duran     - 2251786
# Integrante 4: Alejandro Ramirez Mejia        - 2250930
# Integrante 5: Mateo Amaya                    - 2250921

import re  # Para validar que el nombre solo tenga letras y espacios


# SECCION 1: LISTA DOBLEMENTE ENLAZADA CIRCULAR
# (Se conserva de la Entrega 1 sin cambios)

class Nodo:
    """
    Nodo de la Lista Doblemente Enlazada Circular.
    Guarda los datos de un empleado y dos punteros (anterior / siguiente).
    """
    def __init__(self, id_empleado, nombre, cargo, zona_acceso):
        self.id_empleado = id_empleado
        self.nombre      = nombre
        self.cargo       = cargo
        self.zona_acceso = zona_acceso
        self.anterior    = None
        self.siguiente   = None


class ListaEmpleados:
    """Lista Doblemente Enlazada Circular que almacena todos los empleados."""

    def __init__(self):
        self.cabeza   = None  # Primer nodo
        self.cantidad = 0     # Total de empleados

    #  Metodos de la Entrega 1 (sin modificar)

    def esta_vacia(self):
        return self.cabeza is None

    def contar_empleados(self):
        return self.cantidad

    def imprimir_lista(self):
        if self.esta_vacia():
            print("\n[!] La lista esta vacia. No hay empleados registrados.")
            return
        print("\n========== LISTA DE EMPLEADOS ==========")
        nodo_actual = self.cabeza
        contador    = 1
        while True:
            print(f"\nEmpleado #{contador}")
            print(f"  ID     : {nodo_actual.id_empleado}")
            print(f"  Nombre : {nodo_actual.nombre}")
            print(f"  Cargo  : {nodo_actual.cargo}")
            print(f"  Zona   : {nodo_actual.zona_acceso}")
            nodo_actual = nodo_actual.siguiente
            contador   += 1
            if nodo_actual == self.cabeza:
                break
        print(f"\nTotal de empleados: {self.cantidad}")

    def id_existe(self, id_empleado):
        if self.esta_vacia():
            return False
        nodo_actual = self.cabeza
        while True:
            if nodo_actual.id_empleado == id_empleado:
                return True
            nodo_actual = nodo_actual.siguiente
            if nodo_actual == self.cabeza:
                break
        return False

    def validar_nombre(self, nombre):
        if nombre.strip() == "":
            return False
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$"
        return re.match(patron, nombre) is not None

    def agregar_al_inicio(self, id_empleado, nombre, cargo, zona_acceso):
        if id_empleado is None or id_empleado.strip() == "":
            print("\nEl ID del empleado no puede estar vacio. Empleado NO agregado.")
            return False
        if self.id_existe(id_empleado):
            print(f"\nYa existe un empleado con ID '{id_empleado}'. Empleado NO agregado.")
            return False
        if not self.validar_nombre(nombre):
            print(f"\nNombre invalido: '{nombre}'. Solo letras y espacios. Empleado NO agregado.")
            return False
        if cargo is None or cargo.strip() == "":
            print("\nEl cargo no puede estar vacio. Empleado NO agregado.")
            return False
        if zona_acceso is None or zona_acceso.strip() == "":
            print("\nLa zona de acceso no puede estar vacia. Empleado NO agregado.")
            return False

        nuevo_nodo = Nodo(id_empleado, nombre, cargo, zona_acceso)

        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior  = nuevo_nodo
            self.cabeza          = nuevo_nodo
        else:
            ultimo_nodo               = self.cabeza.anterior
            nuevo_nodo.siguiente      = self.cabeza
            nuevo_nodo.anterior       = ultimo_nodo
            self.cabeza.anterior      = nuevo_nodo
            ultimo_nodo.siguiente     = nuevo_nodo
            self.cabeza               = nuevo_nodo

        self.cantidad += 1
        print(f"\nEmpleado '{nombre}' agregado correctamente.")
        return True

    def buscar_por_id(self, id_buscado):
        if self.esta_vacia():
            print("\n[!] La lista esta vacia. No se puede buscar.")
            return None
        if id_buscado is None or id_buscado.strip() == "":
            print("\n[ERROR] El ID a buscar no puede estar vacio.")
            return None
        nodo_actual = self.cabeza
        while True:
            if nodo_actual.id_empleado == id_buscado:
                print(f"\nEmpleado encontrado:")
                print(f"  ID     : {nodo_actual.id_empleado}")
                print(f"  Nombre : {nodo_actual.nombre}")
                print(f"  Cargo  : {nodo_actual.cargo}")
                print(f"  Zona   : {nodo_actual.zona_acceso}")
                return nodo_actual
            nodo_actual = nodo_actual.siguiente
            if nodo_actual == self.cabeza:
                break
        print(f"\n[X] No se encontro ningun empleado con ID: {id_buscado}")
        return None


#
# SECCION 2: ARBOL AVL INDEXADO POR NOMBRE  ← NUEVO EN V2

# ¿Por que un Arbol AVL?
# En la Entrega 1, buscar un empleado por nombre requeria
# recorrer TODA la lista (O(n)). Con un Arbol AVL:
#   - La insercion y busqueda son 0(log n) gracias al
#     autobalanceo (rotaciones simples y dobles).
#   - El recorrido Inorden entrega los empleados ordenados
#     alfabeticamente de forma automatica.
#   - Permite buscar por FRAGMENTO de nombre: util cuando
#     el usuario no recuerda el nombre completo.

# El arbol no reemplaza la lista; la complementa.
# La lista sigue siendo la estructura principal de
# almacenamiento; el AVL es un INDICE de busqueda por nombre.

class NodoAVL:
    """
    Nodo del Arbol AVL.
    La clave es el nombre del empleado (en minusculas para
    comparaciones insensibles a mayusculas).
    Cada nodo puede guardar varios empleados con el mismo
    nombre (lista de datos), aunque en la practica los IDs
    son unicos.
    """
    def __init__(self, nombre, datos_empleado):
        self.clave    = nombre.lower()          # Clave de comparacion
        self.nombre   = nombre                  # Nombre original (para mostrar)
        self.empleados = [datos_empleado]       # Lista de empleados con ese nombre
        self.izq      = None
        self.der      = None
        self.altura   = 1


class ArbolAVL:
    """
    Arbol AVL autobalanceado indexado por nombre de empleado.

    Funcionalidades nuevas que aporta al sistema:
      1. insertar(nombre, datos)  agrega un empleado al indice
      2. buscar_por_nombre(texto) busca empleados cuyo nombre
                                  contenga el texto buscado
      3. listar_alfabetico()    muestra todos los empleados
                                ordenados A hasta Z por nombre
    """

    #  Utilidades internas del AVL 

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        return self._altura(nodo.izq) - self._altura(nodo.der) if nodo else 0

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    def _rotar_derecha(self, y):
        x      = y.izq
        T2     = x.der
        x.der  = y
        y.izq  = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x):
        y      = x.der
        T2     = y.izq
        y.izq  = x
        x.der  = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _balancear(self, nodo, clave):
        self._actualizar_altura(nodo)
        bal = self._balance(nodo)

        # Caso Izquierda-Izquierda
        if bal > 1 and clave < nodo.izq.clave:
            return self._rotar_derecha(nodo)
        # Caso Derecha-Derecha
        if bal < -1 and clave > nodo.der.clave:
            return self._rotar_izquierda(nodo)
        # Caso Izquierda-Derecha
        if bal > 1 and clave > nodo.izq.clave:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)
        # Caso Derecha-Izquierda
        if bal < -1 and clave < nodo.der.clave:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)
        return nodo

    #  Operaciones publicas 

    def __init__(self):
        self.raiz = None

    def _insertar(self, nodo, nombre, datos_empleado):
        clave = nombre.lower()
        if nodo is None:
            return NodoAVL(nombre, datos_empleado)
        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, nombre, datos_empleado)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, nombre, datos_empleado)
        else:
            # Nombre identico: agrego a la lista del mismo nodo
            nodo.empleados.append(datos_empleado)
            return nodo
        return self._balancear(nodo, clave)

    def insertar(self, nombre, datos_empleado):
        """Inserta un empleado en el indice AVL."""
        self.raiz = self._insertar(self.raiz, nombre, datos_empleado)

    # --- Busqueda por fragmento de nombre ---
    def _buscar_fragmento(self, nodo, fragmento, resultados):
        """
        Recorre TODO el arbol (InOrden) buscando nodos cuya
        clave contenga el fragmento. Retorna lista de coincidencias.
        Complejidad: O(n) en el peor caso, pero el orden del
        recorrido ya viene ordenado A→Z.
        """
        if nodo is None:
            return
        self._buscar_fragmento(nodo.izq, fragmento, resultados)
        if fragmento in nodo.clave:
            for emp in nodo.empleados:
                resultados.append(emp)
        self._buscar_fragmento(nodo.der, fragmento, resultados)

    def buscar_por_nombre(self, texto):
        """
        Busca empleados cuyo nombre contenga 'texto' (insensible
        a mayusculas). Retorna la lista de empleados encontrados
        ya ordenada alfabeticamente gracias al recorrido InOrden.
        """
        fragmento  = texto.strip().lower()
        resultados = []
        self._buscar_fragmento(self.raiz, fragmento, resultados)
        return resultados

    # --- Listado alfabetico completo ---
    def _inorden(self, nodo, lista):
        if nodo is None:
            return
        self._inorden(nodo.izq, lista)
        for emp in nodo.empleados:
            lista.append(emp)
        self._inorden(nodo.der, lista)

    def listar_alfabetico(self):
        """
        Retorna la lista de todos los empleados ordenada
        alfabeticamente A→Z por nombre gracias al recorrido InOrden.
        """
        lista = []
        self._inorden(self.raiz, lista)
        return lista


# ===========================================================
# SECCION 3: MENU Y PROGRAMA PRINCIPAL
# ===========================================================

def mostrar_menu():
    print("\n╔══════════════════════════════════════════╗")
    print("║   SISTEMA DE GESTION DE EMPLEADOS  V2   ║")
    print("╠══════════════════════════════════════════╣")
    print("║  --- Funciones de la Lista (Entrega 1) ──║")
    print("║  1. Verificar si la lista esta vacia     ║")
    print("║  2. Contar empleados registrados         ║")
    print("║  3. Ver todos los empleados (lista)      ║")
    print("║  4. Agregar nuevo empleado               ║")
    print("║  5. Buscar empleado por ID               ║")
    print("║  6. Cargar datos de ejemplo              ║")
    print("╠══════════════════════════════════════════╣")
    print("║  --- Funciones del Arbol AVL (NUEVO) ────║")
    print("║  7. Buscar empleados por nombre          ║")
    print("║  8. Ver empleados en orden alfabetico    ║")
    print("╠══════════════════════════════════════════╣")
    print("║  0. Salir                                ║")
    print("╚══════════════════════════════════════════╝")
    print("Seleccione una opcion: ", end="")


def cargar_datos_ejemplo(lista, avl):
    """
    Carga empleados de prueba en AMBAS estructuras:
    la lista enlazada y el arbol AVL.
    """
    empleados_ejemplo = [
        ("E001", "Carlos Ramirez",  "Gerente",        "Edificio A - Piso 3"),
        ("E002", "Ana Torres",      "Desarrolladora", "Edificio B - Piso 1"),
        ("E003", "Luis Gomez",      "Seguridad",      "Edificio A - Entrada"),
        ("E004", "Maria Perez",     "Contabilidad",   "Edificio C - Piso 2"),
        ("E005", "Jorge Mendoza",   "Sistemas",       "Edificio B - Piso 2"),
        ("E006", "Sofia Castillo",  "Recursos H.",    "Edificio C - Piso 1"),
        ("E007", "Andres Vargas",   "Seguridad",      "Edificio A - Entrada"),
        ("E008", "Camila Herrera",  "Desarrolladora", "Edificio B - Piso 1"),
    ]
    for eid, nombre, cargo, zona in empleados_ejemplo:
        agregado = lista.agregar_al_inicio(eid, nombre, cargo, zona)
        if agregado:
            # Solo insertamos en el AVL si se agrego correctamente a la lista
            avl.insertar(nombre, {
                "id": eid, "nombre": nombre,
                "cargo": cargo, "zona": zona
            })
    print("\nDatos de ejemplo cargados correctamente en lista y arbol AVL.")


def mostrar_empleado(emp):
    """Funcion auxiliar para imprimir un empleado de forma uniforme."""
    print(f"  ID     : {emp['id']}")
    print(f"  Nombre : {emp['nombre']}")
    print(f"  Cargo  : {emp['cargo']}")
    print(f"  Zona   : {emp['zona']}")


def main():
    lista = ListaEmpleados()  # Estructura principal (Entrega 1)
    avl   = ArbolAVL()        # Indice por nombre (NUEVO Entrega 2)

    print("\nBienvenido al Sistema de Gestion de Empleados - Version 2")
    print("Empresa: Control de Accesos y Zonas")

    while True:
        mostrar_menu()
        opcion = input().strip()

        # ---------- Opciones heredadas de la Entrega 1 ----------

        if opcion == "1":
            if lista.esta_vacia():
                print("\nLa lista SI esta vacia. No hay empleados registrados.")
            else:
                print(f"\nLa lista NO esta vacia. Hay {lista.contar_empleados()} empleado(s).")

        elif opcion == "2":
            print(f"\n[INFO] Total de empleados: {lista.contar_empleados()}")

        elif opcion == "3":
            lista.imprimir_lista()

        elif opcion == "4":
            print("\n--- AGREGAR NUEVO EMPLEADO ---")
            id_emp = input("ID del empleado  : ").strip()
            nombre = input("Nombre completo  : ").strip()
            cargo  = input("Cargo            : ").strip()
            zona   = input("Zona de acceso   : ").strip()

            if id_emp and nombre and cargo and zona:
                agregado = lista.agregar_al_inicio(id_emp, nombre, cargo, zona)
                if agregado:
                    # Tambien insertamos en el arbol AVL
                    avl.insertar(nombre, {
                        "id": id_emp, "nombre": nombre,
                        "cargo": cargo, "zona": zona
                    })
            else:
                print("\n[!] Todos los campos son obligatorios.")

        elif opcion == "5":
            print("\nBUSCAR POR ID")
            id_buscar = input("ID a buscar (ej: E003): ").strip()
            lista.buscar_por_id(id_buscar)

        elif opcion == "6":
            cargar_datos_ejemplo(lista, avl)

        # ---------- Opciones NUEVAS del Arbol AVL ----------

        elif opcion == "7":
            # NUEVA FUNCIONALIDAD: Busqueda por nombre usando el Arbol AVL
            print("\n╔══════════════════════════════════╗")
            print("║  BUSCAR POR NOMBRE (Arbol AVL)  ║")
            print("╚══════════════════════════════════╝")
            print("Ingrese el nombre o un fragmento del nombre")
            print("(Ejemplo: 'ana', 'gomez', 'car'): ", end="")
            texto = input().strip()

            if texto == "":
                print("\n[!] Debe ingresar al menos un caracter para buscar.")
            else:
                resultados = avl.buscar_por_nombre(texto)
                if resultados:
                    print(f"\nSe encontraron {len(resultados)} resultado(s) para '{texto}':")
                    print("(Resultados ordenados alfabeticamente)")
                    print("-" * 40)
                    for i, emp in enumerate(resultados, 1):
                        print(f"\nResultado #{i}")
                        mostrar_empleado(emp)
                else:
                    print(f"\n[X] No se encontro ningun empleado con '{texto}' en el nombre.")
            print()
            print("VENTAJA DEL ARBOL AVL:")
            print("  La busqueda recorre el arbol de forma ordenada.")
            print("  Los resultados ya vienen en orden A->Z sin necesidad")
            print("  de ordenarlos despues. Con la lista de la Entrega 1,")
            print("  habria que recorrer todos los nodos SIN orden garantizado.")

        elif opcion == "8":
            # FUNCIONALIDAD AVL: Listar empleados en orden alfabetico
            print("\n╔══════════════════════════════════════════╗")
            print("║  EMPLEADOS EN ORDEN ALFABETICO (AVL)    ║")
            print("╚══════════════════════════════════════════╝")
            empleados_ordenados = avl.listar_alfabetico()
            if not empleados_ordenados:
                print("\n[!] No hay empleados en el arbol. Agregue o cargue datos primero.")
            else:
                print(f"\nTotal: {len(empleados_ordenados)} empleado(s) ordenados A→Z:\n")
                for i, emp in enumerate(empleados_ordenados, 1):
                    print(f"  {i:>2}. [{emp['id']}] {emp['nombre']:<20} | {emp['cargo']:<16} | {emp['zona']}")
            print()
            print("VENTAJA DEL ARBOL AVL:")
            print("  El recorrido InOrden del arbol entrega los nombres")
            print("  en orden alfabetico de forma automatica (O(n)).")
            print("  Con la lista enlazada, habria que ordenar primero (O(n log n)).")

        elif opcion == "0":
            print("\nHasta luego. El sistema ha sido cerrado.\n")
            break

        else:
            print("\n[!] Opcion invalida. Ingrese un numero del 0 al 8.")


if __name__ == "__main__":
    main()
