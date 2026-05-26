# SISTEMA DE GESTION DE EMPLEADOS
# Proyecto de estructura de datos - Tercer semestre
# Implementacion con Lista Doblemente Enlazada Circular
# Integrante 1: David Santiago Cediel Remolina - 2250933
# Integrante 2: David Santiago Gomez Caicedo - 2252119
# Integrante 3: Daniel Andres Floraz Duran - 2251786
# Integrante 4: Alejandro Ramirez Mejia - 2250930
# Integrante 5: Mateo Amaya  - 2250921

import re  # VALIDACION: se usa para comprobar que el nombre solo tenga letras y espacios esta parte se hizo con chat gpt pq es algo nuevo


# CLASE NODO
# Cada nodo guarda la informacion de un empleado
# y tiene dos punteros: uno al nodo anterior y otro al siguiente
class Nodo:
    def __init__(self, id_empleado, nombre, cargo, zona_acceso):
        # Datos del empleado
        self.id_empleado = id_empleado   # Identificador unico del empleado
        self.nombre = nombre             # Nombre completo
        self.cargo = cargo               # Cargo o rol en la empresa
        self.zona_acceso = zona_acceso   # Zona a la que tiene acceso

        # Punteros de la lista doblemente enlazada
        self.anterior = None  # Apunta al nodo de atras
        self.siguiente = None  # Apunta al nodo de adelante


# CLASE LISTA DOBLEMENTE ENLAZADA CIRCULAR
# Aqui se guardan todos los nodos
# El ultimo nodo apunta al primero 
class ListaEmpleados:
    def __init__(self):
        # La lista empieza vacia, sin ningun nodo
        self.cabeza = None  # Primer nodo de la lista
        self.cantidad = 0   # Contador de empleados registrados

    # METODO 1: Verificar si la lista esta vacia
    # Retorna True si no hay empleados, False si hay al menos uno
    def esta_vacia(self):
        return self.cabeza is None

    # METODO 2: Contar la cantidad de empleados en la lista
    # Retorna el numero total de nodos existentes
    def contar_empleados(self):
        return self.cantidad

    # METODO 3: Imprimir todos los empleados de la lista
    # Recorre desde la cabeza hasta volver a la cabeza (circular)
    def imprimir_lista(self):
        # Primero verificamos si hay algo que mostrar
        if self.esta_vacia():
            print("\n[!] La lista esta vacia. No hay empleados registrados.")
            return

        print("LISTA DE EMPLEADOS")
        nodo_actual = self.cabeza  # Empezamos desde el primer nodo

        # Recorremos la lista hasta dar la vuelta completa
        contador = 1
        while True:
            print(f"\nEmpleado #{contador}")
            print(f"  ID        : {nodo_actual.id_empleado}")
            print(f"  Nombre    : {nodo_actual.nombre}")
            print(f"  Cargo     : {nodo_actual.cargo}")
            print(f"  Zona      : {nodo_actual.zona_acceso}")

            # Avanzamos al siguiente nodo
            nodo_actual = nodo_actual.siguiente
            contador += 1

            # Si volvimos al inicio, terminamos el recorrido
            if nodo_actual == self.cabeza:
                break

        print(f"\nTotal de empleados: {self.cantidad}")

    # METODO 4a: Verificar si el ID ya existe en la lista
    # Retorna True si existe, False si no
    def id_existe(self, id_empleado):
        # VALIDACION: si la lista esta vacia, no existe el ID
        if self.esta_vacia():
            return False

        nodo_actual = self.cabeza
        while True:
            # VALIDACION: comprobamos igualdad de IDs
            if nodo_actual.id_empleado == id_empleado:
                return True
            nodo_actual = nodo_actual.siguiente
            if nodo_actual == self.cabeza:
                break
        return False

    # METODO AUXILIAR: validar nombre (solo letras, espacios y acentos)
    def validar_nombre(self, nombre):
        # VALIDACION: el nombre no puede estar vacio y debe contener solo letras y espacios
        if nombre.strip() == "":
            return False
        # Regex permite letras mayúsculas/minúsculas, tildes, ñ y espacios
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$"
        return re.match(patron, nombre) is not None

    # METODO 4: Agregar un empleado AL INICIO de la lista
    # El nuevo nodo se convierte en la nueva cabeza
    def agregar_al_inicio(self, id_empleado, nombre, cargo, zona_acceso):
        # VALIDACION: verificar que el ID no este vacio
        if id_empleado is None or id_empleado.strip() == "":
            print("\nEl ID del empleado no puede estar vacio. Empleado NO agregado.")
            return False  # No se agrega

        # VALIDACION: verificar que el ID no este repetido
        if self.id_existe(id_empleado):
            print(f"\nYa existe un empleado con ID '{id_empleado}'. Empleado NO agregado.")
            return False  # No se agrega

        # VALIDACION: verificar que el nombre sea valido (solo letras y espacios)
        if not self.validar_nombre(nombre):
            print(f"\nNombre invalido: '{nombre}'. Debe contener solo letras y espacios. Empleado NO agregado.")
            return False  # No se agrega

        # VALIDACION: verificar que el cargo no este vacio
        if cargo is None or cargo.strip() == "":
            print("\nEl cargo no puede estar vacio. Empleado NO agregado.")
            return False  # No se agrega

        # VALIDACION: verificar que la zona no este vacia
        if zona_acceso is None or zona_acceso.strip() == "":
            print("\nLa zona de acceso no puede estar vacia. Empleado NO agregado.")
            return False  # No se agrega

        # Creamos el nuevo nodo con los datos del empleado (si pasaron las validaciones)
        nuevo_nodo = Nodo(id_empleado, nombre, cargo, zona_acceso)

        # CASO 1: La lista esta vacia
        # El nodo se apunta a si mismo (es el unico elemento)
        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo  # Se apunta a si mismo
            nuevo_nodo.anterior = nuevo_nodo   # Se apunta a si mismo
            self.cabeza = nuevo_nodo           # Se convierte en la cabeza

        # CASO 2: La lista ya tiene elementos
        else:
            # Guardamos referencia al ultimo nodo 
            ultimo_nodo = self.cabeza.anterior

            # Conectamos el nuevo nodo con la cabeza actual
            nuevo_nodo.siguiente = self.cabeza    # El nuevo apunta a la vieja cabeza
            nuevo_nodo.anterior = ultimo_nodo     # El nuevo apunta al ultimo

            # Actualizamos los punteros de los nodos existentes
            self.cabeza.anterior = nuevo_nodo     # La vieja cabeza apunta atras al nuevo
            ultimo_nodo.siguiente = nuevo_nodo    # El ultimo apunta adelante al nuevo

            # El nuevo nodo ahora es la cabeza
            self.cabeza = nuevo_nodo

        # Aumentamos el contador
        self.cantidad += 1
        print(f"\nEmpleado '{nombre}' agregado correctamente al inicio de la lista.")
        return True

    # METODO 5: Buscar un empleado por su ID
    # Recorre la lista y retorna el nodo si lo encuentra
    def buscar_por_id(self, id_buscado):
        # VALIDACION: Si la lista esta vacia, no hay nada que buscar
        if self.esta_vacia():
            print("\n[!] La lista esta vacia. No se puede buscar.")
            return None

        # VALIDACION: verificar que el ID buscado no este vacio
        if id_buscado is None or id_buscado.strip() == "":
            print("\n[ERROR] El ID a buscar no puede estar vacio.")
            return None

        nodo_actual = self.cabeza  # Empezamos desde el primer nodo

        # Recorremos la lista buscando el ID
        while True:
            # Comparamos el ID del nodo actual con el que buscamos
            if nodo_actual.id_empleado == id_buscado:
                print(f"\nEmpleado encontrado:")
                print(f"  ID        : {nodo_actual.id_empleado}")
                print(f"  Nombre    : {nodo_actual.nombre}")
                print(f"  Cargo     : {nodo_actual.cargo}")
                print(f"  Zona      : {nodo_actual.zona_acceso}")
                return nodo_actual  # Retornamos el nodo encontrado

            # Avanzamos al siguiente nodo
            nodo_actual = nodo_actual.siguiente

            # Si ya dimos la vuelta completa y no encontramos nada, salimos
            if nodo_actual == self.cabeza:
                break

        # Si llegamos aqui, el empleado no existe en la lista
        print(f"\n[X] No se encontro ningun empleado con ID: {id_buscado}")
        return None


# -------------------------------------------------------
# MENU PRINCIPAL
# Interfaz de consola para interactuar con el sistema
# -------------------------------------------------------
def mostrar_menu():
    print("\n  SISTEMA DE GESTION DE EMPLEADOS    ")
    print("\n 1. Verificar si la lista esta vacia ")
    print("  2. Contar empleados registrados     ")
    print("  3. Ver todos los empleados          ")
    print("  4. Agregar nuevo empleado           ")
    print("  5. Buscar empleado por ID           ")
    print("  6. Cargar datos de ejemplo          ")
    print("  0. Salir                            ")

    print("Seleccione una opcion: ", end="")

# datos para el ejemplo
def cargar_datos_ejemplo(lista):
    """Carga algunos empleados de prueba para ver el sistema funcionando"""
    lista.agregar_al_inicio("E001", "Carlos Ramirez",   "Gerente",        "Edificio A - Piso 3")
    lista.agregar_al_inicio("E002", "Ana Torres",       "Desarrolladora", "Edificio B - Piso 1")
    lista.agregar_al_inicio("E003", "Luis Gomez",       "Seguridad",      "Edificio A - Entrada")
    lista.agregar_al_inicio("E004", "Maria Perez",      "Contabilidad",   "Edificio C - Piso 2")
    lista.agregar_al_inicio("E005", "Jorge Mendoza",    "Sistemas",     "Edificio B - Piso 2")
    print("\nDatos de ejemplo cargados correctamente.")


# FUNCION PRINCIPAL
# Punto de entrada del programa

def main():
    # Creamos la lista donde se guardaran los empleados
    lista = ListaEmpleados()

    print("\nBienvenido al Sistema de Gestion de Empleados")
    print("Empresa: Control de Accesos y Zonas")

    # Bucle principal del menu
    while True:
        mostrar_menu()
        opcion = input().strip()

        # Opcion 1: Verificar si esta vacia
        if opcion == "1":
            if lista.esta_vacia():
                print("\nLa lista SI esta vacia. No hay empleados registrados.")
            else:
                print(f"\nLa lista NO esta vacia. Hay {lista.contar_empleados()} empleado(s).")

        # Opcion 2: Contar empleados
        elif opcion == "2":
            total = lista.contar_empleados()
            print(f"\n[INFO] Total de empleados en el sistema: {total}")

        # Opcion 3: Ver todos los empleados
        elif opcion == "3":
            lista.imprimir_lista()

        # Opcion 4: Agregar empleado al inicio
        elif opcion == "4":
            print("\n--- AGREGAR NUEVO EMPLEADO ---")
            id_emp   = input("Ingrese el ID del empleado : ").strip()
            nombre   = input("Ingrese el nombre completo : ").strip()
            cargo    = input("Ingrese el cargo : ").strip()
            zona     = input("Ingrese la zona de acceso : ").strip()

            # Validamos que los campos no esten vacios
            if id_emp and nombre and cargo and zona:
                # intentamos agregar; agregar_al_inicio ya realiza validaciones adicionales
                agregado = lista.agregar_al_inicio(id_emp, nombre, cargo, zona)
                if not agregado:
                    # Si no se pudo agregar, mensaje ya fue impreso por agregar_al_inicio
                    pass
            else:
                print("\n[!] Todos los campos son obligatorios. Empleado no agregado.")

        # Opcion 5: Buscar empleado por ID
        elif opcion == "5":
            print("\nBUSCAR EMPLEADO")
            id_buscar = input("Ingrese el ID a buscar (ej: E003): ").strip()
            lista.buscar_por_id(id_buscar)

        # Opcion 6: Cargar datos de ejemplo
        elif opcion == "6":
            cargar_datos_ejemplo(lista)

        # Opcion 0: Salir
        elif opcion == "0":
            print("\nHasta luego. El sistema ha sido cerrado.\n")
            break

        # Opcion invalida
        else:
            print("\nOpcion no invalida por favor ingrese un numero del 0 al 6.")


# Punto de entrada del script
if __name__ == "__main__":
    main()