# Tarea 4: Introducción a Series de Tiempo

Business Intelligence, Facultad de Ingeniería, Universidad del Istmo de Guatemala.

En esta tarea simulé procesos AR(1) para entender la autocorrelación y después trabajé con los datos de *Online Retail* (UCI): limpié las transacciones, armé la serie de venta neta diaria, probé varios modelos de pronóstico y al final miré a los clientes con un análisis RFM.

## Qué hay en este repositorio

- `tarea 4.ipynb`: el notebook con todo el análisis, de la Parte 0 a la Parte 6. Corre de principio a fin.
- `limpiar.pyw`: la función `limpiar(df)` de la Parte 1.5, en su propio archivo. GitHub no me dejó subirlo como `.py`, así que está como `.pyw` (es el mismo código de Python).
- `TAREA_4.pdf`: el documento con la derivación de 0.1, el análisis de cada parte, la bitácora de limpieza, las tablas y las figuras.
- `TAREA 4.tex`: el código LaTeX del documento.
- `Figuras.zip`: las 7 imágenes (`.png`) que genera el notebook y que usa el documento. Las subí en zip porque la carpeta no se podía subir directamente.

## Cómo correrlo

1. Descargar `Online Retail.xlsx` de https://archive.ics.uci.edu/dataset/352/online+retail. No lo subí al repositorio porque pesa mucho.
2. Poner en una misma carpeta: `Online Retail.xlsx`, `tarea 4.ipynb` y `limpiar.pyw`. Cambiarle el nombre a `limpiar.pyw` por **`limpiar.py`**, porque el notebook hace `from limpiar import limpiar`.
3. Instalar las librerías:
   `pip install numpy pandas matplotlib scipy scikit-learn statsmodels openpyxl jupyter`
4. Abrir el notebook y correr **Kernel → Restart Kernel and Run All Cells**.
5. Esperar unos minutos. Lo más lento es leer el Excel y la Parte 5, porque ahí se reajustan los modelos SARIMA en cada origen. Al terminar se guardan las figuras en una carpeta `figuras/` y unas tablas en `.csv`.

Para recompilar el documento: descomprimir `Figuras.zip` para que quede una carpeta `figuras/` al lado de `TAREA 4.tex` y correr `pdflatex "TAREA 4.tex"` (dos veces). Si el `.tex` no encuentra las figuras, hay que revisar que la carpeta se llame exactamente `figuras`.

## Semillas

| Parte | Semilla |
|---|---|
| 0.2, trayectorias | 1 |
| 0.2, 5 000 réplicas (φ = 0, 0.5, 0.9, 1) | 100, 101, 102, 103 |
| 0.4, tendencia, patrón semanal y ruido blanco | 200, 201, 300 |
| Verificación de Ljung–Box | 5 |
| 5.2(a), validación cruzada | 0 a 9 |
| 6.2, desempate del RFM | 2026 |

## Cómo limpié los datos

Apliqué las reglas en este orden, porque el orden cambia los conteos de la bitácora:

1. Duplicados exactos.
2. Facturas que no empiezan con dígito ni con C (las A son un ajuste de deuda, no una venta).
3. `StockCode` que no es producto (envío, comisiones, descuentos, vouchers, etc.). Dejé los códigos DCGS porque sí son productos, y también dejé las filas `M` de facturas C, porque son créditos que revierten ventas reales.
4. Precio menor o igual a cero.
5. Cantidad negativa en facturas que no son cancelaciones.

Las filas sin `CustomerID` las dejé para la serie de ventas, porque son ventas reales, y las quité en la Parte 6, donde sí necesito saber quién compró. Después de limpiar quedan 531 449 de las 541 909 filas.

Un detalle: al principio mi regla 3 eliminaba también las filas `M` de facturas C, y eso dejaba una venta falsa de £38 970 el 10 de junio de 2011. Lo expliqué en la sección 1.4 del documento y por eso el notebook calcula las dos versiones de la bitácora.

## Cosas importantes del análisis

- El último día de los datos (9 de diciembre de 2011) está incompleto y lo descarté.
- Entrenamiento: hasta el 30 de septiembre de 2011. Prueba: del 3 de octubre al 8 de diciembre de 2011.
- En la prueba gana el SARIMA(0,1,1)(0,1,1)₆ (S2), porque se adapta al nivel reciente de ventas y los demás modelos se quedan cortos en la temporada alta.
- Agregar la media móvil centrada como predictor hace que el modelo se vea mejor, pero es fuga de información: esa media usa días que todavía no han pasado.
