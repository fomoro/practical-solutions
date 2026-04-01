# Configuración de spaCy (Entorno Estable)

1. Verificación de Versiones (Pre-flight)
   Ejecutar 'py -0' para listar las versiones instaladas. 
   Si no aparece la 3.12, descargar e instalar desde python.org.

2. Creación del Entorno (Python 3.12)
   Forzar el uso de la versión estable para evitar errores de compilación: 
   py -3.12 -m venv venv

3. Activación del Entorno
   En PowerShell: .\venv\Scripts\Activate
   (Aparecerá '(venv)' en la línea de comandos).

4. Instalación de Dependencias
   python -m pip install --upgrade pip
   pip install spacy

5. Descarga del Modelo Pesado (LG)
   Instalar el motor de vectores para español:
   python -m spacy download es_core_news_lg

6. Sanity Check
   Validar carga: python -c "import spacy; spacy.load('es_core_news_lg'); print('OK')"


# Fases del Motor NLP (Pipeline de spaCy)


Procesos internos automáticos (El trabajo sucio):
1. Tokenización: palabras y signos de puntuación.
2. Etiquetado Gramatical: sustantivo, un verbo, un adjetivo, etc.
3. Análisis Sintáctico: cómo se conectan las palabras entre sí.

4. Lematización y Limpieza: eliminar términos vacíos.
5. Reconocimiento de Entidades (NER): Clasifica palabras clave.
6. Similitud Semántica (Vectores): porcentaje de similitud (ej. 85%).
