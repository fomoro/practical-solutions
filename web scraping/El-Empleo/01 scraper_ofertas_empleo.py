import os
import csv
from math import ceil
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Locator

# 1. CONFIGURACIÓN
BASE_URL = "https://www.elempleo.com"
QUERY = "PublishDate=hoy"
FOLDER_NAME = "ofertas_scraped"
LIMITE_PAGINAS = 10

EMPLEOS = [
    "azure", "sql", "scrum", "python", "togaf", "full-stack", "fullstack", "angular", "data mesh", "data factory", "ssis", "mcp", "docker"
]

TAGS_INTERES = [
    "azure", "devops", "arquitecto de soluciones", "arquitecto de software", ".net", "sql", "sql server", "scrum", "aws", "python", "full-stack",
    "fullstack", "graphQL", "angular", "wcf", "java", "data mesh", "data factory", "ssis", "llm", "etl", "togaf", "mcp", "docker", "cosmos db",
    "microservices", "software architecture", "solution architecture", "enterprise architecture", "cloud architecture", "azure architecture", "aks",
    "cloud migration", "kubernetes", "azure devops", "event-driven", "clean architecture", "api design", "software governance", "redis", "postgresql",
    "ingeniero de sistemas", "desarrollador de software", "data warehouse", "inteligencia artificial", "desarrollador", "software"
]

CARGOS = [
    "Desarrollador", "Arquitecto de software", "Desarrollador de software", "Ingeniero de sistemas", "Ingeniero DevOps"
]

def _normalizar_lista(lista: list) -> list:
    return [item.lower().strip() for item in lista]

def _construir_url_busqueda(termino: str, pagina: int) -> str:
    ruta = f"/co/ofertas-empleo/trabajo-{termino}"
    if pagina == 1:
        return f"{BASE_URL}{ruta}?{QUERY}"
    return f"{BASE_URL}{ruta}/{pagina}?{QUERY}"

def _aceptar_cookies_si_existen(page: Page):
    banner = page.locator('button.btnAcceptPolicyNavigationCO')
    if banner.is_visible():
        banner.click()

def _calcular_total_paginas(page: Page) -> int:
    try:
        total_texto = page.locator("strong.js-total-results").first.inner_text().strip().replace(".", "")
        total_resultados = int(total_texto)
        resultados_por_pagina = int(page.locator("select#ResultsByPage option[selected]").first.get_attribute("value"))
        return ceil(total_resultados / resultados_por_pagina)
    except:
        return 0

def _extraer_datos_tarjeta(item: Locator) -> dict:
    data_url = item.locator("div.area-bind").first.get_attribute("data-url")
    if not data_url:
        return None
        
    job_id = data_url.split("-")[-1]
    titulo = item.locator("h2.item-title a.js-offer-title").inner_text().strip()
    url_completa = BASE_URL + data_url
    
    try:
        empresa = item.locator(".js-offer-company").inner_text().strip()
    except: 
        empresa = "N/A"
        
    try:
        ciudad = item.locator(".js-offer-city").inner_text().strip()
    except: 
        ciudad = "N/A"

    try:
        tags_elementos = item.locator(".content-tags span").all_inner_texts()
        tags_pagina = [t.strip().lower() for t in tags_elementos if t.strip()]
    except: 
        tags_pagina = []

    try:
        # Extrae los cargos relacionados
        cargos_texto = item.locator("p:has-text('Cargos relacionados') + span").first.inner_text().strip()
        cargos_pagina = [c.strip().lower() for c in cargos_texto.split(",") if c.strip()]
    except:
        cargos_pagina = []

    return {
        "id": job_id,
        "titulo": titulo,
        "empresa": empresa,
        "ciudad": ciudad,
        "tags": tags_pagina,
        "cargos": cargos_pagina,
        "url": url_completa
    }

def _obtener_categoria(datos_oferta: dict, tags_norm: list, cargos_norm: list) -> str:
    cumple_tags = any(t_int in t_pag for t_int in tags_norm for t_pag in datos_oferta["tags"])
    cumple_cargos = any(c_int in c_pag for c_int in cargos_norm for c_pag in datos_oferta["cargos"])

    if cumple_tags and cumple_cargos:
        return "ambos"
    if cumple_tags:
        return "tags"
    if cumple_cargos:
        return "cargos"
    return "descartados"

def _exportar_csv(nombre_archivo: str, datos: list):
    if not datos:
        return
    os.makedirs(FOLDER_NAME, exist_ok=True)
    ruta = os.path.join(FOLDER_NAME, nombre_archivo)
    encabezados = ["id", "empleo_buscado", "titulo", "empresa", "ciudad", "tags", "cargos_relacionados", "url"]
    
    with open(ruta, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(encabezados)
        writer.writerows(datos)

def ejecutar_extraccion():
    tags_interes_norm = _normalizar_lista(TAGS_INTERES)
    cargos_interes_norm = _normalizar_lista(CARGOS)
    ofertas_procesadas = set()
    
    resultados = {
        "ambos": [],
        "tags": [],
        "cargos": [],
        "descartados": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        cookies_aceptadas = False

        for termino in EMPLEOS:
            print(f">>> Buscando: {termino}")
            page.goto(_construir_url_busqueda(termino, 1), wait_until="domcontentloaded")
            
            if not cookies_aceptadas:
                _aceptar_cookies_si_existen(page)
                cookies_aceptadas = True

            total_paginas = _calcular_total_paginas(page)
            if total_paginas == 0:
                print(f"  Sin resultados para '{termino}'")
                continue

            paginas_a_procesar = min(total_paginas, LIMITE_PAGINAS)

            for pagina_num in range(1, paginas_a_procesar + 1):
                if pagina_num > 1:
                    page.goto(_construir_url_busqueda(termino, pagina_num), wait_until="domcontentloaded")

                print(f"  Procesando página {pagina_num} de {paginas_a_procesar} para '{termino}'...")
                ofertas = page.locator("div.result-item")
                
                for i in range(ofertas.count()):
                    datos_oferta = _extraer_datos_tarjeta(ofertas.nth(i))
                    if not datos_oferta:
                        continue
                        
                    job_id = datos_oferta["id"]
                    if job_id in ofertas_procesadas:
                        continue
                        
                    ofertas_procesadas.add(job_id)

                    tags_str = " - ".join(datos_oferta["tags"])
                    cargos_str = " - ".join(datos_oferta["cargos"])
                    fila = [
                        job_id, termino, datos_oferta["titulo"], datos_oferta["empresa"], 
                        datos_oferta["ciudad"], tags_str, cargos_str, datos_oferta["url"]
                    ]

                    categoria = _obtener_categoria(datos_oferta, tags_interes_norm, cargos_interes_norm)
                    resultados[categoria].append(fila)

        browser.close()

    fecha_hoy = datetime.now().strftime("%Y%m%d")
    _exportar_csv(f"{fecha_hoy}_Habilidades_clave_y_Perfiles.csv", resultados["ambos"])
    _exportar_csv(f"{fecha_hoy}_Habilidades_clave.csv", resultados["tags"])
    _exportar_csv(f"{fecha_hoy}_Perfiles.csv", resultados["cargos"])
    _exportar_csv(f"{fecha_hoy}_Descartados.csv", resultados["descartados"])

    print(f"\nExtracción finalizada. Ofertas únicas procesadas: {len(ofertas_procesadas)}")
    print(f"-> {len(resultados['ambos'])} en Habilidades clave y Perfiles.")
    print(f"-> {len(resultados['tags'])} en Habilidades clave.")
    print(f"-> {len(resultados['cargos'])} en Perfiles.")
    print(f"-> {len(resultados['descartados'])} en Descartados.")

if __name__ == "__main__":
    ejecutar_extraccion()