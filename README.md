# Parcial-2-Proyecto-estructura-de-datos-II
Parcial 2 Proyecto estructura de datos II

# Proyecto 2 – Rendimiento con Algoritmos de Ordenamiento y Búsqueda

Este repositorio contiene la simulación de un catálogo de 50 productos para una tienda en línea y la evaluación del desempeño de algoritmos de ordenamiento y búsqueda sobre objetos `Producto`. El objetivo es comparar técnicas clásicas (Insertion Sort, Merge Sort y Quick Sort) al ordenar por precio y calificación, además de medir búsquedas binarias por `id` y lineales por subcadenas en el nombre.

## Requisitos

- Python 3.10 o superior.
- No se necesitan dependencias externas: el proyecto usa únicamente la biblioteca estándar.

## Ejecución

```bash
python3 main.py
```

El programa genera automáticamente los 50 productos con una semilla fija (42) para asegurar reproducibilidad. Al finalizar se muestran:

1. Tabla de tiempos en milisegundos para cada algoritmo y criterio de ordenamiento.
2. Tiempo total de 20 búsquedas por `id` (10 existentes y 10 inexistentes) mediante búsqueda binaria.
3. Tiempo total de 20 búsquedas por nombre (10 subcadenas con coincidencias y 10 sin coincidencias) mediante búsqueda lineal.
4. Una muestra de cinco productos ordenados por precio (Quick Sort) y otra por calificación (Merge Sort).




