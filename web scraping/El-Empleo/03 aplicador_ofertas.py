import os
import csv
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

FOLDER_APPROVED = "ofertas_seleccionadas"
FOLDER_POSTULACIONES = "postulaciones"
SESSION_FILE = "config/sesion.json"
TIMEOUT_MS = 3000

FILE_APLICADAS = os.path.join(FOLDER_POSTULACIONES, "aplicadas.csv")
FILE_RECHAZADAS = os.path.join(FOLDER_POSTULACIONES, "rechazadas.csv")
FILE_NO_EXITOSAS = os.path.join(FOLDER_POSTULACIONES, "no_exitosas.csv")

SELECTOR_BOTON = "button.js-apply-offer"
SELECTOR_ALERTA_APLICADO = "div.js-alert-already-applied"
SELECTOR_ALERTA_EXITO = "div.js-alert-offer.new-alert-success"

def _preparar_archivos_historial():
    os.makedirs(FOLDER_POSTULACIONES, exist_ok=True)
    encabezados = ["id", "empleo_buscado", "titulo", "empresa", "ciudad", "tags", "cargos_relacionados", "fecha", "motivo", "url"]
    
    for archivo in [FILE_APLICADAS, FILE_RECHAZADAS, FILE_NO_EXITOSAS]:
        if not os.path.exists(archivo):
            with open(archivo, mode="w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerow(encabezados)

def _extraer_url(encabezados: list, fila: list) -> str:
    encabezados_norm = [e.lower().strip() for e in encabezados]
    if "url" in encabezados_norm:
        idx = encabezados_norm.index("url")
        return fila[idx] if idx < len(fila) else fila[-1]
    return fila[-1]

def _normalizar_oferta(encabezados: list, fila: list) -> dict:
    encabezados_norm = [e.lower().strip() for e in encabezados]
    oferta = {}
    for campo in ["id", "empleo_buscado", "titulo", "empresa", "ciudad", "tags", "cargos_relacionados", "url"]:
        if campo in encabezados_norm:
            idx = encabezados_norm.index(campo)
            oferta[campo] = fila[idx] if idx < len(fila) else ""
        else:
            oferta[campo] = fila[-1] if campo == "url" else ""
    return oferta

def _cargar_ofertas_pendientes() -> tuple:
    urls_bloqueadas = set()
    conteo_historial = {"aplicadas.csv": 0, "rechazadas.csv": 0, "no_exitosas.csv": 0}

    # Leer historial: Solo bloqueamos si están en aplicadas o rechazadas
    for archivo in [FILE_APLICADAS, FILE_RECHAZADAS, FILE_NO_EXITOSAS]:
        nombre_base = os.path.basename(archivo)
        if os.path.exists(archivo):
            with open(archivo, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                encabezados = next(reader, None)
                if not encabezados: continue
                for row in reader:
                    if row:
                        url = _extraer_url(encabezados, row)
                        if nombre_base != "no_exitosas.csv":
                            urls_bloqueadas.add(url)
                        conteo_historial[nombre_base] += 1

    ofertas_pendientes = []
    total_encontradas = 0

    # Cargar entrada dinámica
    if os.path.exists(FOLDER_APPROVED):
        for archivo in os.listdir(FOLDER_APPROVED):
            if archivo.endswith(".csv"):
                ruta = os.path.join(FOLDER_APPROVED, archivo)
                with open(ruta, mode="r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    encabezados = next(reader, None)
                    if not encabezados: continue
                    for row in reader:
                        if row:
                            total_encontradas += 1
                            url = _extraer_url(encabezados, row)
                            if url not in urls_bloqueadas:
                                oferta_norm = _normalizar_oferta(encabezados, row)
                                ofertas_pendientes.append(oferta_norm)
                                urls_bloqueadas.add(url) # Evitar procesar dos veces en la misma sesión
                                
    return ofertas_pendientes, total_encontradas, conteo_historial

def _validar_estado_sesion() -> bool:
    if not os.path.exists(SESSION_FILE):
        print(f"❌ Error: No se encontró el archivo de sesión en {SESSION_FILE}. Ejecuta el módulo de autenticación primero.")
        return False
    return True

def _guardar_resultado(oferta: dict, archivo_destino: str, motivo: str = ""):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(archivo_destino, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            oferta["id"], oferta["empleo_buscado"], oferta["titulo"], 
            oferta["empresa"], oferta["ciudad"], oferta["tags"], 
            oferta["cargos_relacionados"], fecha, motivo, oferta["url"]
        ])

def _procesar_oferta_individual(page, oferta: dict) -> str:
    url = oferta["url"]
    try:
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        if page.locator(SELECTOR_ALERTA_APLICADO).first.is_visible(timeout=TIMEOUT_MS):
            return "ya_aplicada"

        boton = page.locator(SELECTOR_BOTON).first
        if boton.count() == 0:
            return "boton_no_encontrado"

        respuesta = input("🤔 ¿Aplicar a esta oferta? (Enter = Sí, n = No, s = Salir): ").strip().lower()
        if respuesta == 's':
            return "salir"
        if respuesta == 'n':
            return "rechazada"

        print("🖱️ Haciendo clic vía JavaScript para aplicar...")
        page.evaluate(f'document.querySelector("{SELECTOR_BOTON}").click()')

        try:
            page.wait_for_selector(SELECTOR_ALERTA_EXITO, timeout=5000)
            return "aplicada"
        except PlaywrightTimeoutError:
            confirmacion = input("⚠️ No se vio alerta de éxito. ¿Fue exitosa? (Enter = Sí, n = No): ").strip().lower()
            return "aplicada" if confirmacion != 'n' else "sin_confirmacion_usuario"

    except Exception as e:
        return f"error_{str(e)[:20]}"

def ejecutar_postulacion():
    print("\n🚀 INICIANDO POSTULACIÓN AUTOMÁTICA\n")
    
    if not _validar_estado_sesion():
        return
        
    _preparar_archivos_historial()
    ofertas, total_encontradas, conteo_historial = _cargar_ofertas_pendientes()
    ya_procesadas = total_encontradas - len(ofertas)
    
    print(f"📊 Total ofertas encontradas: {total_encontradas}")
    print(f"📁 Ya procesadas (omitidas): {ya_procesadas}")
    print(f"🎯 A procesar: {len(ofertas)}")
    print(f"   - aplicadas.csv: {conteo_historial['aplicadas.csv']} registros")
    print(f"   - rechazadas.csv: {conteo_historial['rechazadas.csv']} registros")
    print(f"   - no_exitosas.csv: {conteo_historial['no_exitosas.csv']} registros\n")
    
    if not ofertas:
        print("✨ ¡Todo al día! No hay ofertas nuevas por procesar.")
        return

    if input("¿Comenzar proceso? (Enter = Sí, n = No): ").strip().lower() == 'n':
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        for i, oferta in enumerate(ofertas, 1):
            print(f"\n[{i}/{len(ofertas)}] {oferta['titulo']} - {oferta['empresa']}")
            print(f"URL: {oferta['url']}")
            
            resultado = _procesar_oferta_individual(page, oferta)

            if resultado == "salir":
                print("🛑 Proceso detenido por el usuario.")
                break
            elif resultado in ("aplicada", "ya_aplicada"):
                _guardar_resultado(oferta, FILE_APLICADAS)
                print(f"✅ Registrada como: {resultado}")
            elif resultado == "rechazada":
                _guardar_resultado(oferta, FILE_RECHAZADAS)
                print("⏭️ Omitida y enviada a rechazadas.")
            else:
                _guardar_resultado(oferta, FILE_NO_EXITOSAS, resultado)
                print(f"❌ No exitosa. Motivo: {resultado}")

        browser.close()
    print("\n🏁 Proceso de postulación finalizado.")

if __name__ == "__main__":
    ejecutar_postulacion()