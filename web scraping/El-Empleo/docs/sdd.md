# Diagramas de Arquitectura

## 1. Contexto General
Visión macro de los componentes del proyecto y su relación.

```mermaid
flowchart TD
    Usuario((Usuario))
    Sistema[Sistema de Automatización]
    Portal[Portal elempleo.com]
    Datos[(Archivos Locales)]
    NLP[Motor NLP - spaCy]

    Usuario -->|Opera y supervisa| Sistema
    Sistema <-->|Navega y aplica| Portal
    Sistema <-->|Lee y guarda| Datos
    NLP <-->|Autocompleta preguntas nuevas| Datos
```

## 2. Interacción Macro
Detalle interno de los componentes y flujos de comunicación externos.

```mermaid
flowchart TD
    Usuario((Usuario))
    Portal[Portal elempleo.com]
    NLP[Motor NLP - spaCy]

    subgraph Sistema [Sistema de Automatización]
        direction TB
        Menu[Menú Principal]
        Mod0[Módulo 00: Autenticación]
        Mod2[Módulo 02: Búsqueda]
        Mod3[Módulo 03: Postulación]
        
        Menu --> Mod0
        Menu --> Mod2
        Menu --> Mod3
    end

    subgraph Datos [Archivos Locales]
        direction TB
        Sesion[(Datos de Acceso)]
        Respuestas[(Banco de Respuestas)]
        Vacantes[(Vacantes Posibles y Aplicadas)]
    end

    Usuario -->|Inicia y aprueba pasos| Sistema
    Sistema <-->|Navega, extrae y aplica| Portal
    Sistema <-->|Consulta y guarda| Datos
    NLP <-->|Infiere y llena respuestas faltantes| Datos
```