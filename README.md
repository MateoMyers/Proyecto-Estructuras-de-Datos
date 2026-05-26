# Proyecto-Estructuras-de-Datos
Repositorio del proyecto final de Estructuras de Datos 2026-1
# Sistema de Gestión de Empleados — Versión 3
**Proyecto de Estructuras de Datos · Tercer Semestre**

---

## Integrantes

| # | Nombre | Código |
|---|--------|--------|
| 1 | David Santiago Cediel Remolina | 2250933 |
| 2 | David Santiago Gómez Caicedo | 2252119 |
| 3 | Daniel Andrés Florez Durán | 2251786 |
| 4 | Alejandro Ramírez Mejía | 2250930 |
| 5 | Mateo Amaya Moreno | 2250921 |

---

## Descripción General del Problema

El sistema gestiona el control de acceso y zonas de una empresa mediante el registro de empleados. Cada empleado tiene un **ID único**, un **nombre**, un **cargo** y una **zona de acceso**.

En la **Entrega 1** se implementó una **Lista Doblemente Enlazada Circular** como estructura principal de almacenamiento. Esta permitía agregar empleados al inicio, recorrer la lista y buscar por ID. Sin embargo, cualquier búsqueda por nombre requería recorrer *todos* los nodos en orden secuencial (O(n)), lo que se vuelve ineficiente a medida que crece la cantidad de empleados.

En la **Entrega 2** se incorpora un **Árbol AVL** como índice de búsqueda por nombre, complementando la lista sin reemplazarla.

---

## Mejora Implementada: Árbol AVL como Índice por Nombre

### ¿Por qué un Árbol AVL?

Un Árbol AVL es un árbol binario de búsqueda **autobalanceado**. Esto significa que después de cada inserción, el árbol se reorganiza automáticamente mediante **rotaciones** para garantizar que la diferencia de altura entre los subárboles izquierdo y derecho de cualquier nodo nunca supere 1.

Esto garantiza que las operaciones de inserción y búsqueda se mantengan en **O(log n)** en el peor caso, a diferencia del **O(n)** de la lista enlazada.

### Ventajas concretas en el sistema

| Operación | Lista Enlazada (Entrega 1) | Árbol AVL (Entrega 2) |
|-----------|--------------------------|----------------------|
| Buscar por nombre | O(n) — recorre toda la lista | O(log n) — desciende por el árbol |
| Listar alfabéticamente | O(n log n) — requiere ordenar | O(n) — recorrido InOrden ya ordenado |
| Buscar por fragmento | O(n) sin orden garantizado | O(n) con resultados en orden A→Z |

### Relación entre las dos estructuras

> **El árbol NO reemplaza la lista.** La lista sigue siendo la estructura principal de almacenamiento. El árbol AVL actúa como un **índice de búsqueda por nombre**, de la misma manera en que un índice en un libro no reemplaza el contenido, sino que agiliza la búsqueda dentro de él.

Cada vez que se agrega un empleado a la lista, también se inserta en el árbol AVL. Ambas estructuras permanecen sincronizadas.

---

## Funcionalidad Nueva: Búsqueda por Fragmento de Nombre

La funcionalidad principal agregada en esta entrega es la **búsqueda por fragmento de nombre** a través del árbol AVL.

### ¿Cómo funciona?

El usuario puede ingresar cualquier parte de un nombre y el sistema devolverá todos los empleados cuyo nombre contenga ese fragmento, **sin importar mayúsculas o minúsculas**.

**Ejemplo:**
- Buscar `"gom"` encuentra al empleado `"Luis Gómez"` → devuelve **true**
- Buscar `"ana"` encontraría `"Ana Torres"` y `"Anamaría López"` si existiera
- Buscar `"car"` encontraría `"Carlos Ramírez"`

El árbol realiza un **recorrido InOrden** completo verificando si el fragmento está contenido en la clave de cada nodo. Al ser InOrden (izquierda → raíz → derecha), los resultados quedan automáticamente ordenados de A a Z **sin necesidad de un paso adicional de ordenamiento**.

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│              SISTEMA DE GESTIÓN V2                  │
├──────────────────────────┬──────────────────────────┤
│   Lista Doblemente       │      Árbol AVL            │
│   Enlazada Circular      │   (Índice por Nombre)     │
│                          │                           │
│  [E008] ↔ [E007] ↔ ...  │         [Luis]            │
│     ↑________________↓   │        /       \          │
│                          │    [Carlos]  [María]      │
│  Almacenamiento principal│   /      \               │
│  Búsqueda por ID: O(n)   │ [Ana] [Jorge]             │
│                          │                           │
│                          │  Índice de búsqueda       │
│                          │  Búsqueda por nombre:     │
│                          │  O(log n)                 │
└──────────────────────────┴──────────────────────────┘
```

---

## Documentación de Funciones

### Sección 1: Lista Doblemente Enlazada Circular (sin cambios respecto a Entrega 1)

#### `Nodo.__init__`
- **Propósito:** Crear un nodo de la lista con los datos de un empleado.
- **Parámetros:** `id_empleado`, `nombre`, `cargo`, `zona_acceso`.
- **Funcionamiento:** Inicializa los atributos del empleado y establece los punteros `anterior` y `siguiente` en `None`.

#### `ListaEmpleados.__init__`
- **Propósito:** Inicializar la lista vacía.
- **Funcionamiento:** Establece `cabeza = None` y `cantidad = 0`.

#### `esta_vacia`
- **Propósito:** Verificar si la lista no contiene empleados.
- **Retorna:** `True` si `cabeza` es `None`, `False` en caso contrario.

#### `contar_empleados`
- **Propósito:** Obtener el total de empleados registrados.
- **Retorna:** El atributo `cantidad`.

#### `imprimir_lista`
- **Propósito:** Mostrar todos los empleados en consola.
- **Funcionamiento:** Recorre la lista desde `cabeza` hasta volver a `cabeza` (estructura circular), imprimiendo los datos de cada nodo.

#### `id_existe`
- **Propósito:** Verificar si un ID ya está registrado en el sistema.
- **Parámetros:** `id_empleado` (string).
- **Funcionamiento:** Recorre la lista comparando el ID de cada nodo con el buscado. Retorna `True` si encuentra coincidencia.

#### `validar_nombre`
- **Propósito:** Asegurar que el nombre ingresado solo contenga letras y espacios.
- **Funcionamiento:** Aplica una expresión regular que acepta letras del español (incluyendo tildes y ñ) y espacios. Retorna `False` si el nombre está vacío o contiene caracteres inválidos.

#### `agregar_al_inicio`
- **Propósito:** Insertar un nuevo empleado al comienzo de la lista.
- **Funcionamiento:** Valida todos los campos antes de insertar. Si la lista está vacía, el nodo se apunta a sí mismo. Si no, redirige los punteros del último nodo y la cabeza actual para incorporar el nuevo nodo al inicio. Retorna `True` si el empleado fue agregado correctamente.

#### `buscar_por_id`
- **Propósito:** Encontrar un empleado dado su ID.
- **Funcionamiento:** Recorre la lista comparando el ID de cada nodo. Imprime los datos si lo encuentra o un mensaje de error si no existe.

---

### Sección 2: Árbol AVL — NUEVO EN VERSIÓN 2

#### `NodoAVL.__init__`
- **Propósito:** Crear un nodo del árbol AVL que almacena los datos de un empleado.
- **Parámetros:** `nombre` (nombre del empleado), `datos_empleado` (diccionario con `id`, `cargo` y `zona`).
- **Funcionamiento:** Inicializa la clave de comparación en minúsculas (`nombre.lower()`), guarda el nombre original, crea la lista de empleados asociados al nodo (`[datos_empleado]`), establece los hijos `izq` y `der` en `None`, y fija la altura inicial en `1`.

#### `ArbolAVL.__init__`
- **Propósito:** Crear e inicializar el árbol AVL vacío.
- **Funcionamiento:** Establece `self.raiz = None`, dejando el árbol listo para recibir inserciones.

#### `_altura`
- **Propósito:** Obtener la altura de un nodo de forma segura.
- **Parámetros:** `nodo` (nodo del árbol o `None`).
- **Funcionamiento:** Retorna `nodo.altura` si el nodo existe, o `0` si es `None`. Esto evita errores al consultar nodos hoja o nulos.

#### `_balance`
- **Propósito:** Calcular el factor de balance de un nodo para detectar desbalances.
- **Parámetros:** `nodo` (nodo del árbol).
- **Funcionamiento:** Resta la altura del subárbol derecho a la del izquierdo. Un valor fuera del rango `[-1, 1]` indica que el árbol necesita rebalancearse.

#### `_actualizar_altura`
- **Propósito:** Mantener actualizada la altura de un nodo tras una inserción o rotación.
- **Parámetros:** `nodo` (nodo cuya altura se va a recalcular).
- **Funcionamiento:** Asigna al nodo `1 + max(altura_izq, altura_der)`, reflejando correctamente la profundidad del subárbol.

#### `_rotar_derecha`
- **Propósito:** Corregir un desbalance de tipo **Izquierda-Izquierda** mediante una rotación simple.
- **Parámetros:** `y` (nodo desbalanceado).
- **Funcionamiento:** Eleva el hijo izquierdo `x` como nueva raíz del subárbol. El subárbol derecho de `x` pasa a ser el subárbol izquierdo de `y`. Actualiza las alturas de ambos nodos. Retorna `x` como nueva raíz.

```
    y                x
   / \             /   \
  x   T3   →    T1      y
 / \                   / \
T1  T2               T2   T3
```

#### `_rotar_izquierda`
- **Propósito:** Corregir un desbalance de tipo **Derecha-Derecha** mediante una rotación simple.
- **Parámetros:** `x` (nodo desbalanceado).
- **Funcionamiento:** Eleva el hijo derecho `y` como nueva raíz del subárbol. El subárbol izquierdo de `y` pasa a ser el subárbol derecho de `x`. Actualiza las alturas. Retorna `y` como nueva raíz.

```
  x                  y
 / \               /   \
T1   y    →       x     T3
    / \          / \
   T2  T3      T1   T2
```

#### `_balancear`
- **Propósito:** Detectar el tipo de desbalance y aplicar la rotación adecuada para restaurar la propiedad AVL.
- **Parámetros:** `nodo` (nodo a balancear), `clave` (clave del elemento recién insertado).
- **Casos manejados:**

| Factor de balance | Condición adicional | Tipo de caso | Rotación aplicada |
|---|---|---|---|
| > 1 | clave < clave del hijo izquierdo | Izquierda-Izquierda | Rotar derecha |
| < -1 | clave > clave del hijo derecho | Derecha-Derecha | Rotar izquierda |
| > 1 | clave > clave del hijo izquierdo | Izquierda-Derecha | Rotar izquierda al hijo, luego derecha |
| < -1 | clave < clave del hijo derecho | Derecha-Izquierda | Rotar derecha al hijo, luego izquierda |

#### `_insertar`
- **Propósito:** Insertar recursivamente un empleado en el subárbol correcto según su nombre.
- **Parámetros:** `nodo`, `nombre`, `datos_empleado`.
- **Funcionamiento:** Compara la clave del nuevo empleado con la del nodo actual. Si es menor, va al subárbol izquierdo; si es mayor, al derecho; si es igual (nombre duplicado), agrega el empleado a la lista del nodo existente. Al retroceder en la recursión, llama a `_balancear` para mantener la propiedad AVL.

#### `insertar`
- **Propósito:** Punto de entrada público para agregar un empleado al índice AVL.
- **Parámetros:** `nombre`, `datos_empleado`.
- **Funcionamiento:** Llama a `_insertar` desde la raíz y actualiza `self.raiz` con el resultado (que puede ser un nodo diferente si hubo rotaciones).

#### `_buscar_fragmento`
- **Propósito:** Recorrer el árbol buscando todos los nodos cuyo nombre contenga un fragmento dado.
- **Parámetros:** `nodo`, `fragmento` (texto en minúsculas), `resultados` (lista acumuladora).
- **Funcionamiento:** Realiza un recorrido **InOrden** completo. En cada nodo verifica si `fragmento in nodo.clave`; de ser así, agrega todos los empleados del nodo a los resultados. Al ser InOrden, los resultados quedan ordenados de A a Z automáticamente.

#### `buscar_por_nombre`
- **Propósito:** Punto de entrada público para buscar empleados por nombre o fragmento de nombre.
- **Parámetros:** `texto` (nombre o fragmento ingresado por el usuario).
- **Funcionamiento:** Normaliza el texto a minúsculas, inicializa una lista vacía y llama a `_buscar_fragmento` desde la raíz. Retorna la lista de empleados encontrados ya ordenada alfabéticamente.

#### `_inorden`
- **Propósito:** Recorrer el árbol en orden para recolectar todos los empleados de A a Z.
- **Parámetros:** `nodo`, `lista` (lista acumuladora).
- **Funcionamiento:** Visita recursivamente el subárbol izquierdo, luego agrega los empleados del nodo actual, y finalmente visita el subárbol derecho. Esto garantiza orden alfabético sin pasos adicionales.

#### `listar_alfabetico`
- **Propósito:** Obtener la lista completa de empleados ordenada de A a Z.
- **Funcionamiento:** Inicializa una lista vacía, llama a `_inorden` desde la raíz y retorna la lista resultante.

#### `mostrar_empleado`
- **Propósito:** Imprimir un diccionario con los datos de un empleado.
- **Parámetros:** `diccionario` (diccionario con los datos del empleado).
- **Funcionamiento:** Recibe un diccionario con los datos del empleado (proveniente del AVL o de la lista) y lo imprime con un formato limpio y legible. Esto evita duplicar código de impresión en las diferentes opciones del menú.
 

#### `cargar_datos_ejemplo`
- **Propósito:** Facilitar las pruebas del sistema sin necesidad de ingreso manual.
- **Funcionamiento:** Contiene una lista de tuplas con datos predefinidos. Itera sobre ellos llamando a agregar_al_inicio de la lista y, si la validación es exitosa, llama a insertar en el Árbol AVL. Es clave para demostrar el autobalanceo del árbol con un volumen de datos inmediato.

---

## Menú del Sistema

| Opción | Función | Estructura usada |
|--------|---------|-----------------|
| 1 | Verificar si la lista está vacía | Lista |
| 2 | Contar empleados registrados | Lista |
| 3 | Ver todos los empleados | Lista |
| 4 | Agregar nuevo empleado | Lista + AVL |
| 5 | Buscar empleado por ID | Lista |
| 6 | Cargar datos de ejemplo | Lista + AVL |
| 7 | **Buscar por nombre/fragmento** | **AVL** ← NUEVO |
| 8 | **Ver empleados en orden alfabético** | **AVL** ← NUEVO |
| 0 | Salir | — |

---

## Ejemplo de Ejecución

### Búsqueda por fragmento (Opción 7)

```
BUSCAR POR NOMBRE (Árbol AVL)
Ingrese el nombre o un fragmento del nombre
(Ejemplo: 'ana', 'gomez', 'car'): gom

Se encontraron 1 resultado(s) para 'gom':
(Resultados ordenados alfabéticamente)

Resultado #1
  ID     : E003
  Nombre : Luis Gomez
  Cargo  : Seguridad
  Zona   : Edificio A - Entrada
```

### Listado alfabético (Opción 8)

```
EMPLEADOS EN ORDEN ALFABÉTICO (AVL)
Total: 8 empleado(s) ordenados A→Z:

   1. [E007] Andres Vargas        | Seguridad        | Edificio A - Entrada
   2. [E002] Ana Torres           | Desarrolladora   | Edificio B - Piso 1
   3. [E008] Camila Herrera       | Desarrolladora   | Edificio B - Piso 1
   4. [E001] Carlos Ramirez       | Gerente          | Edificio A - Piso 3
   5. [E005] Jorge Mendoza        | Sistemas         | Edificio B - Piso 2
   6. [E003] Luis Gomez           | Seguridad        | Edificio A - Entrada
   7. [E004] Maria Perez          | Contabilidad     | Edificio C - Piso 2
   8. [E006] Sofia Castillo       | Recursos H.      | Edificio C - Piso 1
```

---

## Análisis de Complejidad

| Operación | Lista Enlazada | Árbol AVL |
|-----------|---------------|-----------|
| Inserción | O(1) al inicio | O(log n) |
| Búsqueda por ID | O(n) | No aplica |
| Búsqueda por nombre exacto | O(n) | O(log n) |
| Búsqueda por fragmento | O(n) sin orden | O(n) con orden A→Z |
| Listado alfabético | O(n log n) con ordenamiento extra | O(n) vía InOrden |

---

## Conclusión

La incorporación del Árbol AVL como índice de búsqueda por nombre representa una mejora significativa en la eficiencia del sistema. La estructura principal (lista enlazada circular) se conserva intacta para el almacenamiento y la búsqueda por ID, mientras que el árbol AVL aporta capacidades nuevas: búsqueda por fragmento de nombre y listado alfabético automático, ambas con mejor complejidad que las alternativas basadas únicamente en la lista.

El autobalanceo del árbol AVL garantiza que el rendimiento no se degrade con el crecimiento del número de empleados, manteniendo siempre O(log n) para las operaciones de inserción y búsqueda por nombre exacto.


---

# NUEVAS FUNCIONALIDADES — VERSIÓN 3

La Versión 3 mantiene intacta toda la estructura desarrollada en las entregas anteriores (Lista Doblemente Enlazada Circular + Árbol AVL), pero incorpora nuevas estructuras y algoritmos que amplían el alcance del sistema hacia un modelo más completo de gestión y control de accesos empresariales.

Las nuevas funcionalidades agregadas son:

- Implementación de un **Grafo ponderado** para representar zonas de acceso.
- Implementación del algoritmo de **Kruskal** para encontrar conexiones mínimas entre zonas.
- Implementación del algoritmo de **Gale-Shapley** para asignaciones estables entre empleados y zonas.
- Sistema de **registro de accesos y horarios**.
- Historial de movimientos y reportes por empleado.

---

## NUEVA ESTRUCTURA: GRAFO DE ZONAS DE ACCESO

En esta versión se agrega un **grafo no dirigido y ponderado** para modelar las zonas de acceso dentro de la empresa.

### ¿Qué representa el grafo?

- Cada **vértice** representa una zona de acceso.
- Cada **arista** representa una conexión entre zonas.
- El **peso** representa costo, distancia o nivel de seguridad.

### Funcionalidades del Grafo

| Función | Descripción |
|---|---|
| Insertar zona | Agrega una nueva zona al sistema |
| Eliminar zona | Elimina una zona y sus conexiones |
| Insertar conexión | Conecta dos zonas con un peso |
| Eliminar conexión | Elimina la relación entre zonas |
| Buscar conexión | Verifica si existe conexión |
| Mostrar grafo | Visualiza toda la red de zonas |

### Ejemplo conceptual

```text
Entrada ----(3)---- Oficina
   |                    |
  (5)                  (2)
   |                    |
Bodega -----(4)---- Servidor
```

---

# ALGORITMOS NUEVOS IMPLEMENTADOS

## Algoritmo de Kruskal

### ¿Para qué se usa?

Kruskal permite encontrar un **Árbol de Expansión Mínima (MST)** dentro del grafo.

Esto permite conectar todas las zonas utilizando el menor costo posible.

### Funcionamiento general

1. Ordena las conexiones por peso.
2. Selecciona primero las conexiones más baratas.
3. Evita ciclos utilizando la técnica Union-Find.

### Complejidad

| Algoritmo | Complejidad |
|---|---|
| Kruskal | O(E log E) |

### Ejemplo de salida

```text
========== KRUSKAL ==========
Entrada <--(2)--> Oficina
Oficina <--(3)--> Servidor
Servidor <--(4)--> Bodega

Costo total: 9
```

---

## Algoritmo de Gale-Shapley

### ¿Qué problema resuelve?

El algoritmo de Gale-Shapley permite realizar asignaciones estables entre empleados y zonas según preferencias.

### Aplicación en el proyecto

- Los empleados indican sus zonas preferidas.
- Las zonas indican sus empleados preferidos.
- El algoritmo genera asignaciones sin conflictos ni inestabilidad.

### Complejidad

| Algoritmo | Complejidad |
|---|---|
| Gale-Shapley | O(n²) |

### Ejemplo de salida

```text
========== GALE SHAPLEY ==========
Carlos --> Oficina
Ana --> Entrada
Luis --> Bodega
```

---

# NUEVA SECCIÓN: REGISTRO DE ACCESOS Y HORARIOS

La versión 3 incorpora un módulo de control de accesos más cercano a un sistema real.

## Funcionalidades

- Registrar entrada de empleados.
- Registrar salida.
- Registrar movimientos entre zonas.
- Mostrar historial completo.
- Generar reportes individuales.

---

## Validación de acceso por cargo

El sistema verifica automáticamente si un empleado tiene permiso para ingresar a determinada zona.

### Ejemplo de permisos

| Cargo | Zonas permitidas |
|---|---|
| Administrador | Entrada, Oficina, Servidor, Bodega |
| Seguridad | Entrada, Bodega |
| Empleado | Entrada, Oficina |

### Ejemplo de restricción

```text
Acceso denegado. Zona restringida para este cargo.
```

---

# ARQUITECTURA GENERAL ACTUALIZADA — VERSIÓN 3

```text
┌───────────────────────────────────────────────┐
│      SISTEMA DE GESTIÓN DE EMPLEADOS V3       │
├───────────────────────────────────────────────┤
│ Lista Doblemente Enlazada Circular            │
│  - Almacenamiento principal                   │
│  - Búsqueda por ID                            │
├───────────────────────────────────────────────┤
│ Árbol AVL                                     │
│  - Índice por nombre                          │
│  - Búsqueda eficiente                         │
│  - Orden alfabético                           │
├───────────────────────────────────────────────┤
│ Grafo de Zonas                                │
│  - Modelado de accesos                        │
│  - Kruskal                                    │
│  - Gale-Shapley                               │
├───────────────────────────────────────────────┤
│ Registro de Accesos                           │
│  - Entradas y salidas                         │
│  - Movimientos                                │
│  - Historial                                  │
└───────────────────────────────────────────────┘
```

---

# NUEVAS OPCIONES DEL MENÚ — VERSIÓN 3

| Opción | Función |
|---|---|
| 8 | Ver red de zonas |
| 9 | Agregar zona al grafo |
| 10 | Agregar conexión entre zonas |
| 11 | Eliminar zona |
| 12 | Eliminar conexión |
| 13 | Buscar conexión |
| 14 | Ejecutar Kruskal |
| 15 | Ejecutar Gale-Shapley |
| 16 | Registrar entrada |
| 17 | Registrar salida |
| 18 | Ver historial |
| 19 | Reporte por empleado |

---

# NUEVOS EJEMPLOS DE EJECUCIÓN

## Registro de Entrada

```text
ID empleado: E003
Nombre: Luis Gomez
Cargo: Seguridad
Zona de acceso: Bodega
Hora de entrada: 08:00

Entrada registrada para Luis Gomez.
```

---

## Registro de Movimiento

```text
Movimiento registrado hacia Oficina.
```

---

# CONCLUSIÓN ACTUALIZADA

La Versión 3 amplía significativamente el alcance del proyecto, manteniendo intactas las estructuras desarrolladas en entregas anteriores y agregando nuevas capacidades orientadas a la simulación de un sistema real de control de accesos empresariales.

La combinación de múltiples estructuras y algoritmos permite aprovechar las ventajas específicas de cada una:

- La Lista Doblemente Enlazada Circular mantiene el almacenamiento principal de empleados.
- El Árbol AVL optimiza las búsquedas por nombre y el ordenamiento alfabético.
- El Grafo ponderado permite modelar relaciones entre zonas.
- Kruskal optimiza conexiones dentro de la red.
- Gale-Shapley introduce asignaciones estables entre empleados y zonas.
- El Registro de Accesos agrega control de entradas, salidas e historial.

El proyecto demuestra la integración práctica de diferentes estructuras de datos y algoritmos clásicos dentro de un único sistema funcional y escalable.
