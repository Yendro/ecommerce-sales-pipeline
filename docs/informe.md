# Informe Técnico: Canal de Análisis de Ventas de Amazon

## Explicación del Caso

El proyecto implicó la creación de un canal de datos completo para estandarizar y analizar los datos de ventas de Amazon para una empresa de comercio electrónico. El principal reto fue transformar datos de ventas sin procesar e inconsistentes en un conjunto de datos limpio y fiable.

## Suposiciones Realizadas

### Estructura y Contenido de los Datos

- El conjunto de datos contenía columnas esenciales de comercio electrónico: detalles del producto, precios, calificaciones, categorías y reseñas de clientes.
- Los símbolos de moneda india (₹ y €) estaban presentes en las columnas de precio y requerían un manejo especial.
- Los recuentos de calificaciones contenían comas separadoras para los miles.
- Los porcentajes de descuento se almacenaron como cadenas con el símbolo '%'.

### Manejo de la Calidad de los Datos

- Los productos sin `product_id` o `product_name` se consideraron inválidos y se eliminaron.
- Las calificaciones faltantes se completaron con el valor de la mediana para evitar sesgos en los promedios.
- Los valores cero en los recuentos de calificaciones se aceptaron como válidos (productos sin calificaciones).
- Se eliminaron las entradas duplicadas basadas en combinaciones de producto, usuario y reseña.

### Lógica de Negocios

- El margen de beneficio se calculó como `precio_real` - `precio_descuento`.
- La tasa de descuento se calculó como `precio_descuento` / `precio_real`.
- El recuento de calificaciones se utilizó como proxy del producto. Popularidad/volumen de ventas

## Enfoque y metodología de la solución

### Enfoque elegido

Seleccioné una **tubería ETL basada en Python** con **Streamlit para visualización** porque:

1. **Ecosistema Python**: Bibliotecas completas para el procesamiento de datos (pandas) y la visualización (plotly)
2. **Prototipado rápido**: Streamlit permite el desarrollo rápido de paneles de control sin la complejidad del frontend
3. **Tubería integral**: Pila tecnológica única desde la limpieza de datos hasta la visualización
4. **Demostración del portafolio**: Muestra capacidades completas de ingeniería de datos

### Estrategia de implementación

- **Desarrollo incremental**: Creación y prueba de cada componente por separado (ETL → BD → Panel de control)
- **Programación defensiva**: Incorporación de gestión integral de errores y validación de datos
- **Diseño centrado en el usuario**: Creación de filtros interactivos y visualizaciones intuitivas
- **Código listo para producción**: Incluyó registro, gestión de configuración y Documentación

> Aunque algunas correcciones se abordaron mediante IA para encontrar soluciones a circunstancias inusuales.

## Resultados Clave y Visualizaciones

### Resultados del Procesamiento de Datos

- Se depuraron con éxito **1465 registros de productos** con un formato de moneda complejo
- Se redujeron las inconsistencias de datos mediante la **estandarización de más de 15 columnas**
- Se generaron **2 nuevas métricas de negocio** (margen de beneficio, tasa de descuento)

### Información del Panel de Control

- **Productos Principales**: Se identificaron los productos mejor valorados y con más reseñas
- **Distribución por Categorías**: Se revelaron las categorías de productos dominantes y su contribución a los ingresos
- **Estrategia de Precios**: Se mostró la correlación entre los descuentos y las valoraciones de los clientes
- **Análisis de Rentabilidad**: Se visualizó la distribución del margen en toda la cartera de productos

### Logros Técnicos

- Se creó un **canal de ETL totalmente funcional** que gestiona los desafíos de datos del mundo real
- Se creó un **panel de control interactivo** con 6 vistas analíticas distintas
- Se implementó una **limpieza de datos robusta** para formatos de moneda internacionales
- Se entregó código de **calidad de producción** con la gestión y documentación de errores adecuadas

## Mejoras Futuras y Ajustes

### Mejoras inmediatas

- Añadir reglas automatizadas de validación de datos y controles de calidad
- Implementar pruebas unitarias para funciones críticas de transformación de datos
- Crear ejecución programada de pipelines (p. ej., actualizaciones diarias de datos)

### Consideraciones de escalabilidad

- Migración de bases de datos de SQLite a PostgreSQL para producción
- Añadir particionamiento de datos para gestionar conjuntos de datos más grandes
- Implementar mecanismos de almacenamiento en caché para mejorar el rendimiento del panel

##Reflexiones personales

Este proyecto demostró la importancia de la **ingeniería de datos práctica**, más allá del conocimiento teórico. El aspecto más desafiante fue gestionar las inconsistencias de los datos reales, en particular los símbolos de la moneda india, que requerían múltiples enfoques de codificación.

Disfruté especialmente la **naturaleza integral** de este proyecto, desde los datos sin procesar hasta la información empresarial. Reforzó cómo las decisiones de limpieza de datos impactan directamente en los resultados analíticos y las decisiones empresariales.

La experiencia puso de manifiesto que una **visualización intuitiva** es tan crucial como un procesamiento de datos robusto. La creación del panel me ayudó a comprender cómo el trabajo técnico se traduce en valor empresarial a través de información accesible.
