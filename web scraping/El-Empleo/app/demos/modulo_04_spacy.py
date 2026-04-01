import os
import json
import spacy

FOLDER_RESPUESTAS = "data/respuestas"
FILE_PENDIENTES = "data/preguntas/preguntas_pendientes.json"
FILE_SUGERIDAS = "data/preguntas/respuestas_sugeridas.json"
UMBRAL_SIMILITUD = 0.80  # Umbral óptimo para comparar oraciones completas

def _cargar_recursos():
    try:
        nlp = spacy.load("es_core_news_lg")
    except OSError:
        print("❌ Error: No se encontró el modelo. Ejecuta: python -m spacy download es_core_news_lg")
        return None, {}

    banco_unificado = {}
    if os.path.exists(FOLDER_RESPUESTAS):
        for archivo in os.listdir(FOLDER_RESPUESTAS):
            if archivo.endswith(".json"):
                ruta = os.path.join(FOLDER_RESPUESTAS, archivo)
                try:
                    with open(ruta, mode="r", encoding="utf-8") as f:
                        banco_unificado.update(json.load(f))
                except Exception:
                    pass
    return nlp, banco_unificado

def _limpiar_texto(nlp, texto: str):
    doc = nlp(texto.lower().strip())
    tokens_limpios = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]
    return nlp(" ".join(tokens_limpios))

def _evaluar_coincidencia(doc_nueva, doc_banco) -> float:
    if not doc_nueva.vector_norm or not doc_banco.vector_norm:
        return 0.0
    return doc_nueva.similarity(doc_banco)

def _buscar_mejor_respuesta(nlp, pregunta_nueva: str, banco_respuestas: dict):
    doc_nueva = _limpiar_texto(nlp, pregunta_nueva)
    
    mejor_puntaje = 0.0
    mejor_pregunta_origen = None
    
    for pregunta_banco in banco_respuestas.keys():
        doc_banco = _limpiar_texto(nlp, pregunta_banco)
        puntaje = _evaluar_coincidencia(doc_nueva, doc_banco)
        
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_pregunta_origen = pregunta_banco
            
    respuesta = banco_respuestas.get(mejor_pregunta_origen) if mejor_pregunta_origen else None
    return respuesta, mejor_puntaje, mejor_pregunta_origen

def ejecutar_prediccion():
    print("\n🧠 INICIANDO MOTOR NLP - AUTENTICACIÓN DE RESPUESTAS")
    print("⏳ Cargando modelo NLP (es_core_news_lg)... [OK]")
    
    if not os.path.exists(FILE_PENDIENTES):
        print("✨ No hay archivo de preguntas pendientes. Todo al día.")
        return
        
    with open(FILE_PENDIENTES, mode="r", encoding="utf-8") as f:
        pendientes = json.load(f)
        
    if not pendientes:
        print("✨ La lista de pendientes está vacía.")
        return
        
    nlp, banco_respuestas = _cargar_recursos()
    if not nlp or not banco_respuestas:
        print("⚠️ No se pudo inicializar el motor o el banco de respuestas está vacío.")
        return
        
    print(f"📚 Banco de respuestas cargado: {len(banco_respuestas)} respuestas base.")
    print(f"🔎 Analizando {len(pendientes)} preguntas pendientes...\n")
    print("-" * 50)
    
    sugeridas = {}
    no_resueltas = {}
    
    # Cargar sugeridas previas si existen
    if os.path.exists(FILE_SUGERIDAS):
        try:
            with open(FILE_SUGERIDAS, mode="r", encoding="utf-8") as f:
                sugeridas = json.load(f)
        except Exception:
            pass

    contador = 1
    total = len(pendientes)
    
    for pregunta_cruda, tipo in pendientes.items():
        respuesta, puntaje, pregunta_origen = _buscar_mejor_respuesta(nlp, pregunta_cruda, banco_respuestas)
        
        if puntaje >= UMBRAL_SIMILITUD:
            print(f"[{contador}/{total}] ❓ PREGUNTA: \"{pregunta_cruda}\"")
            print(f"      🎯 MATCH ({(puntaje * 100):.1f}%): \"{pregunta_origen}\"")
            print(f"      ✅ ACCIÓN: Respuesta sugerida guardada.\n")
            sugeridas[pregunta_cruda] = respuesta
        else:
            print(f"[{contador}/{total}] ❓ PREGUNTA: \"{pregunta_cruda}\"")
            if pregunta_origen:
                print(f"      ❌ MATCH FALLIDO: El mejor puntaje fue {(puntaje * 100):.1f}% con \"{pregunta_origen}\" (Requiere {UMBRAL_SIMILITUD*100}%)")
            else:
                print(f"      ❌ MATCH FALLIDO: Ninguna similitud detectada.")
            print(f"      ⚠️ ACCIÓN: Requiere atención manual.\n")
            no_resueltas[pregunta_cruda] = tipo
            
        contador += 1
            
    print("-" * 50)
    
    os.makedirs(os.path.dirname(FILE_SUGERIDAS), exist_ok=True)
    with open(FILE_SUGERIDAS, mode="w", encoding="utf-8") as f:
        json.dump(sugeridas, f, indent=4, ensure_ascii=False)
        
    with open(FILE_PENDIENTES, mode="w", encoding="utf-8") as f:
        json.dump(no_resueltas, f, indent=4, ensure_ascii=False)
        
    print("\n🏁 Proceso finalizado.")
    
    # Cálculo seguro de nuevas resueltas
    nuevas_resueltas = len(pendientes) - len(no_resueltas)
    print(f"-> {nuevas_resueltas} nuevas respuestas listas para revisión en 'respuestas_sugeridas.json'.")
    print(f"-> {len(no_resueltas)} preguntas aún requieren tu atención manual en 'preguntas_pendientes.json'.")

if __name__ == "__main__":
    ejecutar_prediccion()