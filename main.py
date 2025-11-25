"""Simulación de catálogo y evaluación de algoritmos de ordenamiento/búsqueda."""

import random  # Generación de números y selecciones aleatorias para datos de prueba
import time  # Medición de tiempo de ejecución (benchmarking)
from copy import deepcopy  # Copia profunda de listas para no alterar la original al ordenar
from dataclasses import dataclass  # Creación rápida de clases contenedoras de datos
from typing import Callable, Iterable, List, Tuple  # Tipos para validación estática y legibilidad


@dataclass
class Producto:
    """Modelo base de un producto del catálogo de la tienda."""

    id: int  # Identificador único del producto
    nombre: str  # Nombre comercial del producto
    precio: float  # Precio unitario en moneda local
    categoria: str  # Categoría a la que pertenece (Electrónica, Hogar, etc.)
    stock: int  # Cantidad de unidades disponibles en inventario
    calificacionPromedio: float  # Calificación de usuarios (1.0 a 5.0)

    def __str__(self) -> str:
        # Método para representación en cadena amigable
        return (
            f"ID: {self.id:02d} | {self.nombre} | {self.categoria} | "
            f"${self.precio:8.2f} | Stock: {self.stock:3d} | ⭐ {self.calificacionPromedio:.1f}"
        )


# Lista constante de nombres base para generar productos aleatorios
NOMBRES = [
    "Auriculares Bluetooth",
    "Camisa de algodón",
    "Libro de programación",
    "Sartén antiadherente",
    "Smartphone Android",
    "Zapatillas deportivas",
    "Teclado mecánico",
    "Cafetera eléctrica",
    "Monitor LED",
    "Cargador portátil",
    "Reloj inteligente",
    "Mochila escolar",
    "Lámpara de escritorio",
    "Campera impermeable",
    "Mouse inalámbrico",
    "Parlante portátil",
    "Cámara web HD",
    "Toalla de baño",
    "Alfombra decorativa",
    "Set de cuchillos",
]

# Lista constante de categorías posibles
CATEGORIAS = ["Electrónica", "Ropa", "Libros", "Hogar"]


def generar_productos(cantidad: int, *, semilla: int = 42) -> List[Producto]:
    """Crea `cantidad` de productos pseudoaleatorios usando una semilla fija."""
    random.seed(semilla)  # Inicializa el generador para resultados reproducibles
    productos: List[Producto] = []  # Lista vacía para acumular productos
    for i in range(1, cantidad + 1):  # Itera desde 1 hasta cantidad
        nombre = f"{random.choice(NOMBRES)} #{i}"  # Elige nombre al azar y agrega índice
        precio = round(random.uniform(5.0, 1000.0), 2)  # Precio aleatorio entre 5 y 1000
        categoria = random.choice(CATEGORIAS)  # Categoría aleatoria
        stock = random.randint(0, 500)  # Stock entero aleatorio
        calificacion = round(random.uniform(1.0, 5.0), 1)  # Calificación entre 1.0 y 5.0
        # Crea instancia y añade a la lista
        productos.append(Producto(i, nombre, precio, categoria, stock, calificacion))
    return productos  # Devuelve la lista generada


def insertion_sort(arr: Iterable[Producto], key: Callable[[Producto], float]) -> List[Producto]:
    """Implementación clásica de Insertion Sort adaptada a objetos Producto."""
    a = deepcopy(list(arr))  # Copia profunda para no alterar la lista original
    for i in range(1, len(a)):  # Recorre desde el segundo elemento hasta el final
        actual = a[i]  # Elemento a insertar en la parte ordenada
        j = i - 1  # Índice del elemento anterior
        # Mueve elementos mayores que 'actual' una posición adelante
        while j >= 0 and key(a[j]) > key(actual):
            a[j + 1] = a[j]  # Desplaza elemento
            j -= 1  # Retrocede índice
        a[j + 1] = actual  # Inserta 'actual' en su posición correcta
    return a  # Retorna lista ordenada


def merge_sort(arr: Iterable[Producto], key: Callable[[Producto], float]) -> List[Producto]:
    """Divide y conquista: retorna la lista ordenada usando Merge Sort."""
    lista = list(arr)  # Convierte iterable a lista
    if len(lista) <= 1:  # Caso base: lista de 0 o 1 elemento ya está ordenada
        return lista
    mid = len(lista) // 2  # Encuentra el punto medio
    # Llamada recursiva para mitad izquierda
    izquierda = merge_sort(lista[:mid], key)
    # Llamada recursiva para mitad derecha
    derecha = merge_sort(lista[mid:], key)
    # Mezcla las sublistas ordenadas
    return merge(izquierda, derecha, key)


def merge(izquierda: List[Producto], derecha: List[Producto], key: Callable[[Producto], float]) -> List[Producto]:
    """Mezcla dos listas ya ordenadas respetando el criterio indicado."""
    resultado: List[Producto] = []  # Lista acumuladora
    i = j = 0  # Índices para izquierda (i) y derecha (j)
    while i < len(izquierda) and j < len(derecha):  # Mientras haya elementos en ambas
        if key(izquierda[i]) <= key(derecha[j]):  # Compara elementos según key
            resultado.append(izquierda[i])  # Agrega el menor (izquierda)
            i += 1  # Avanza índice izquierda
        else:
            resultado.append(derecha[j])  # Agrega el menor (derecha)
            j += 1  # Avanza índice derecha
    resultado.extend(izquierda[i:])  # Agrega remanentes de izquierda si hay
    resultado.extend(derecha[j:])  # Agrega remanentes de derecha si hay
    return resultado  # Retorna lista mezclada


def quick_sort(arr: Iterable[Producto], key: Callable[[Producto], float]) -> List[Producto]:
    """Quick Sort funcional que particiona por un pivote central."""
    lista = list(arr)  # Convierte a lista
    if len(lista) <= 1:  # Caso base
        return lista
    pivote = lista[len(lista) // 2]  # Selecciona pivote (elemento central)
    # Crea sublista con elementos menores al pivote
    menores = [x for x in lista if key(x) < key(pivote)]
    # Crea sublista con elementos iguales al pivote
    iguales = [x for x in lista if key(x) == key(pivote)]
    # Crea sublista con elementos mayores al pivote
    mayores = [x for x in lista if key(x) > key(pivote)]
    # Concatena resultados recursivos
    return quick_sort(menores, key) + iguales + quick_sort(mayores, key)


def medir_tiempo(
    algoritmo: Callable[[Iterable[Producto], Callable[[Producto], float]], List[Producto]],
    lista: Iterable[Producto],
    key: Callable[[Producto], float],
) -> Tuple[float, List[Producto]]:
    """Ejecuta un algoritmo de ordenamiento y devuelve (tiempo_ms, lista)."""
    inicio = time.perf_counter()  # Marca tiempo inicial
    resultado = algoritmo(lista, key)  # Ejecuta algoritmo
    fin = time.perf_counter()  # Marca tiempo final
    return round((fin - inicio) * 1000, 5), resultado  # Retorna ms y lista ordenada


def busqueda_binaria(lista: List[Producto], id_buscado: int) -> Producto | None:
    """Realiza búsqueda binaria por `id` sobre una lista previamente ordenada."""
    inicio = 0  # Límite inferior
    fin = len(lista) - 1  # Límite superior
    while inicio <= fin:  # Mientras el rango sea válido
        mitad = (inicio + fin) // 2  # Calcula punto medio
        if lista[mitad].id == id_buscado:  # Si encuentra coincidencia
            return lista[mitad]  # Retorna producto encontrado
        if lista[mitad].id < id_buscado:  # Si ID buscado es mayor
            inicio = mitad + 1  # Busca en mitad derecha
        else:  # Si ID buscado es menor
            fin = mitad - 1  # Busca en mitad izquierda
    return None  # Retorna None si no se encuentra


def busqueda_lineal_nombre(lista: Iterable[Producto], subcadena: str) -> List[Producto]:
    """Filtra productos cuyo nombre contiene la subcadena indicada (case-insensitive)."""
    subcadena = subcadena.lower()  # Normaliza búsqueda a minúsculas
    # Retorna lista por comprensión filtrando por nombre
    return [p for p in lista if subcadena in p.nombre.lower()]


def imprimir_tabla_tiempos(resultados: list[str]):
    """Muestra en consola la tabla formateada de resultados de ordenamiento."""
    print("\nRESULTADOS DE TIEMPOS (ms)\n")  # Encabezado
    print(f"{'Criterio':24} {'Algoritmo':18} {'Tiempo'}")  # Columnas
    for linea in resultados:  # Itera sobre resultados formateados
        print(linea)  # Imprime cada línea


def main():
    """Orquesta la generación de datos, mediciones y reportes en consola."""
    # 1. Generación de datos
    productos = generar_productos(50)  # Genera 50 productos de prueba

    # 2. Definición de criterios de ordenamiento (lambdas)
    criterios = {
        "Precio ascendente": lambda p: p.precio,  # Ordenar por precio menor a mayor
        "Calificación descendente": lambda p: -p.calificacionPromedio,  # Mayor a menor (signo negativo)
    }

    # 3. Definición de algoritmos a probar
    algoritmos = {
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
    }

    resultados_tabla: list[str] = []  # Lista para guardar strings de reporte
    productos_por_criterio: dict[str, dict[str, List[Producto]]] = {}  # Estructura para guardar resultados

    # 4. Ejecución de pruebas de ordenamiento
    for nombre_criterio, funcion_criterio in criterios.items():  # Recorre criterios
        productos_por_criterio[nombre_criterio] = {}  # Inicializa diccionario para este criterio
        for nombre_algoritmo, algoritmo in algoritmos.items():  # Recorre algoritmos
            # Mide tiempo de ejecución
            tiempo, ordenados = medir_tiempo(algoritmo, productos, funcion_criterio)
            # Guarda lista ordenada para verificación posterior
            productos_por_criterio[nombre_criterio][nombre_algoritmo] = ordenados
            # Agrega resultado formateado a la tabla
            resultados_tabla.append(f"{nombre_criterio:24} {nombre_algoritmo:18} {tiempo} ms")

    # 5. Imprimir tabla de resultados
    imprimir_tabla_tiempos(resultados_tabla)

    # 6. Preparación para búsqueda binaria (requiere orden previo por ID)
    # Ordenamos por ID usando Merge Sort para tener una base confiable
    productos_ordenados_id = merge_sort(productos, lambda p: p.id)
    # Seleccionamos 10 IDs que sabemos existen (del 1 al 50)
    ids_existentes = random.sample(range(1, 51), 10)
    # Seleccionamos 10 IDs que sabemos NO existen (fuera de rango)
    ids_inexistentes = random.sample(range(100, 150), 10)

    # 7. Benchmarking de Búsqueda Binaria
    inicio_bin = time.perf_counter()  # Inicio cronómetro
    for x in ids_existentes:  # Busca IDs existentes
        busqueda_binaria(productos_ordenados_id, x)
    for x in ids_inexistentes:  # Busca IDs inexistentes
        busqueda_binaria(productos_ordenados_id, x)
    fin_bin = time.perf_counter()  # Fin cronómetro
    tiempo_total_binaria = round((fin_bin - inicio_bin) * 1000, 5)  # Cálculo total ms

    # 8. Preparación para búsqueda lineal
    # Palabras clave que es probable que existan en los nombres generados
    subcadenas_existentes = [
        "camisa",
        "sartén",
        "libro",
        "bluetooth",
        "parlante",
        "android",
        "mochila",
        "cámara",
        "cargador",
        "zapatillas",
    ]
    # Palabras clave absurdas que no deberían estar
    subcadenas_inexistentes = [
        "alfiler",
        "pintura",
        "lentes",
        "flor",
        "bicicleta",
        "piano",
        "perfume",
        "queso",
        "cama",
        "pelota",
    ]

    # 9. Benchmarking de Búsqueda Lineal
    inicio_lin = time.perf_counter()  # Inicio cronómetro
    for s in subcadenas_existentes:  # Busca palabras existentes
        busqueda_lineal_nombre(productos, s)
    for s in subcadenas_inexistentes:  # Busca palabras inexistentes
        busqueda_lineal_nombre(productos, s)
    fin_lin = time.perf_counter()  # Fin cronómetro
    tiempo_total_lineal = round((fin_lin - inicio_lin) * 1000, 5)  # Cálculo total ms

    # 10. Imprimir resultados de búsqueda
    print("\nRESULTADOS DE BÚSQUEDAS\n")
    print(f"Tiempo total búsqueda binaria por id: {tiempo_total_binaria} ms")
    print(f"Tiempo total búsqueda lineal por nombre: {tiempo_total_lineal} ms")

    # 11. Verificación visual: Imprimir muestras de catálogos ordenados
    print("\nMUESTRA DE CATÁLOGO ORDENADO POR PRECIO (Quick Sort)\n")
    # Obtiene resultado guardado previamente
    catalogo_ordenado = productos_por_criterio["Precio ascendente"]["Quick Sort"]
    for producto in catalogo_ordenado[:5]:  # Imprime primeros 5
        print(producto)

    print("\nMUESTRA DE CATÁLOGO ORDENADO POR CALIFICACIÓN (Merge Sort)\n")
    # Obtiene resultado guardado previamente
    catalogo_calificacion = productos_por_criterio["Calificación descendente"]["Merge Sort"]
    for producto in catalogo_calificacion[:5]:  # Imprime primeros 5
        print(producto)


if __name__ == "__main__":
    main()  # Ejecuta la función principal si es el script principal
