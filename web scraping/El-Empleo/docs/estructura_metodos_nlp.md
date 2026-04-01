# Guía de Diseño: Módulo 04 (Motor NLP)

⚙️ Estructura de Métodos y Flujo spaCy

├── Métodos Públicos (Orquestación):
│   └── ejecutar_prediccion()         # Coordina lectura de pendientes, cruce NLP y guardado en respuestas_sugeridas.json.
│
└── Métodos Privados (Lógica interna):
    ├── _cargar_recursos()            # Carga el modelo es_core_news_lg y unifica los 7 JSON de respuestas.
    ├── _limpiar_texto()              # Lematiza, pasa a minúsculas y elimina palabras vacías (Stop Words).
    ├── _extraer_entidades()          # Aplica NER para aislar tecnologías clave y evitar falsos positivos.
    ├── _evaluar_coincidencia()       # Calcula el % de similitud vectorial validando que las entidades coincidan.
    └── _buscar_mejor_respuesta()     # Itera el banco buscando la coincidencia máxima (Umbral mínimo del 85%).

