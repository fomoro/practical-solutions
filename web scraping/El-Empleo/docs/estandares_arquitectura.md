# Estándares Técnicos y Reglas de Arquitectura

| Ítem | Estándar de Arquitectura | Justificación Técnica (Máx 100 carac.) |
| :--- | :--- | :--- |
| 1 | Verificación de Existencia DOM | Usar `.count() > 0` para validar presencia; `.is_visible()` falla si el CSS aún no renderiza. |
| 2 | Prohibición de Esperas Estáticas | Cero tiempos fijos. Usar eventos del DOM explícitos o el ciclo de vigilancia (polling) de 500ms. |
| 3 | Interacción de Bajo Nivel (JS) | Uso de page.evaluate para asegurar el clic saltando capas CSS o modales que bloqueen el puntero. |
| 4 | Selectores Determinísticos | Evitar ambigüedad responsive. Filtrar duplicados con clases como `.hidden-xs` o pseudo `:visible`. |
| 5 | Nomenclatura Semántica | Prefijo "_" para métodos privados y nombres verbo-acción para alta mantenibilidad. |
| 6 | Estrategia de Doble Disparador | Escucha simultánea de URL y alertas para manejar respuestas inciertas del servidor. |
| 7 | Desacoplamiento (JSON Brain) | Aísla lógica de negocio en JSON para cambiar el perfil sin modificar el código fuente. |
| 8 | Gestión de Excepciones | Captura preguntas nuevas en archivos pendientes sin romper el flujo de ejecución. |
| 9 | Normalización de Entradas | Mapeo dinámico de columnas (ID, URL) para ser compatible con cualquier formato CSV. |
| 10 | Control de Flujo con Escape | Pausas estratégicas para validación humana o salto de oferta preservando el historial. |
| 11 | Arquitectura Defensiva | Validación visual de tarjetas si la paginación falla, asegurando captura total. |