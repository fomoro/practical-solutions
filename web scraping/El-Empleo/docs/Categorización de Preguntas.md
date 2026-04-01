# 🗂️ Arquitectura de Datos: Categorización de Preguntas

| Categoría | Archivo JSON | Descripción del Dominio |
| :--- | :--- | :--- |
| 1. Información Personal y Disponibilidad | personal_disponibilidad.json | Agrupa datos estáticos de contacto (teléfono, ubicación) y reglas de movilidad (modalidad híbrida, traslado, disponibilidad de ingreso). |
| 2. Formación Académica | formacion_academica.json | Contiene exclusivamente los respaldos educativos formales (título de Ingeniero de Sistemas, universidad). |
| 3. Experiencia General | experiencia_general.json | Consolida la trayectoria de alto nivel: años totales de experiencia (17+), sectores (financiero, salud) y listado de empresas empleadoras. |
| 4. Liderazgo y Gestión | liderazgo_gestion.json | Centraliza el perfil gerencial y metodológico: roles como Tech Lead/Arquitecto, tamaño de equipos a cargo, prácticas QA y metodologías ágiles (Scrum). |
| 5. Habilidades Técnicas Core | habilidades_tecnicas_core.json | Define el stack principal de desarrollo: lenguajes (C#, Python, JS), ecosistema .NET, diseño de APIs, middleware, herramientas DevOps y estándares de seguridad (OWASP). |
| 6. Datos, Cloud e Infraestructura | datos_cloud_infraestructura.json | Enfocado en la arquitectura de backend profundo: SQL avanzado, modelamiento relacional/NoSQL, Data Lakes, proveedores Cloud (Azure/AWS), y orquestación (Docker/Kubernetes). |
| 7. Condiciones Laborales | condiciones_laborales.json | Aísla los datos transaccionales de la negociación y extras: expectativas salariales, licencias y validación del nivel de inglés (B1/Smart). |

## Justificación Técnica de la División (Separation of Concerns)

1. Optimización del Motor NLP (spaCy): Al clasificar las preguntas por dominio, el futuro módulo de procesamiento de lenguaje natural puede limitar su espacio de búsqueda vectorial solo al archivo correspondiente, reduciendo el consumo de memoria y aumentando la precisión de la similitud semántica.
2. Mantenibilidad: Los datos volátiles (como la aspiración salarial o el nivel de inglés en curso) están aislados de los datos históricos inmutables (como el título universitario o la experiencia pasada).
3. Desacoplamiento: El aplicador web (Módulo 03) puede iterar dinámicamente sobre la carpeta de respuestas sin importar cuántos archivos o categorías se agreguen en el futuro, gracias a la función de consolidación en memoria.