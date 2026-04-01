# Guía de Configuración del Banco de Respuestas

Esta guía explica cómo organizar y redactar las respuestas en formato JSON para que los módulos de postulación automática (Módulo 03 y Módulo 04) funcionen correctamente.

## 1. Lectura Unificada (El Cerebro del Robot)
El sistema está diseñado para leer automáticamente **todos** los archivos `.json` que se encuentren dentro de la carpeta `data/respuestas/`. No importa si tienes un solo archivo o diez; el robot unificará todas las preguntas y respuestas en su memoria antes de empezar a llenar formularios.

## 2. Organización Sugerida (Dominios)
Para mantener un orden lógico y facilitar las actualizaciones, se sugiere dividir el banco de respuestas en tres (3) archivos principales basados en dominios técnicos:

* **`perfil_general.json`**: Contiene información personal, académica y condiciones laborales.
    * *Ejemplos:* Aspiración salarial, nivel de inglés, disponibilidad de traslado, modalidad de trabajo, certificaciones generales.
* **`cloud_infraestructura.json`**: Enfocado exclusivamente en infraestructura, plataformas y despliegue.
    * *Ejemplos:* Experiencia en AWS/Azure, Docker, Kubernetes, Linux, servidores.
* **`desarrollo.json`**: Abarca la lógica de negocio, integración, bases de datos y backend.
    * *Ejemplos:* Años de experiencia en lenguajes (C#, Python), SQL, creación/consumo de APIs, microservicios, ETLs.

## 3. La Regla de los Corchetes `[ ]` (Manejo de Controles)
Los portales de empleo pueden hacer la misma pregunta usando diferentes controles visuales (un cuadro de texto libre, o botones de selección única/radio). Para evitar tener respuestas duplicadas, el sistema usa la **Regla de los Corchetes**.

**Estructura obligatoria:**
`"Pregunta exacta de la página": "[Opción Corta] Respuesta profesional completa."`

### ¿Cómo lo interpreta el robot?
1.  **Si la página muestra un Cuadro de Texto Libre (`textarea`):**
    El robot ignora los corchetes y escribe la frase completa para dar una respuesta robusta.
    * *Lo que escribe:* "Tengo nivel B1 en formación continua con 2 horas diarias de práctica."
2.  **Si la página muestra Botones de Selección (Radio / Lista Desplegable):**
    El robot ignora la frase larga, extrae estrictamente lo que está dentro del corchete y busca la opción exacta en la pantalla para hacer clic.
    * *Lo que selecciona:* "B1"

### Ejemplos Prácticos de Redacción
Asegúrate de que el texto dentro del corchete coincida exactamente con las opciones que suele dar la plataforma.

* **Nivel de Idioma:**
    `"¿Cuál es tu nivel de inglés?": "[B1] Tengo nivel B1 en formación continua con 2 horas diarias de práctica."`
* **Certificaciones Múltiples:**
    `"Cuentas con alguna de estas certificaciones:": "[Ninguna] Mi enfoque técnico ha estado en la experiencia aplicada en arquitectura cloud y .NET."`
* **Preguntas de Sí/No:**
    `"¿Estás de acuerdo con modalidad híbrida en Bogotá?": "[Sí] Estoy totalmente de acuerdo y tengo disponibilidad para esquema híbrido en Bogotá."`