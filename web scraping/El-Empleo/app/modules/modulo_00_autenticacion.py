import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page

load_dotenv()

LOGIN_URL = "https://www.elempleo.com/co/iniciar-sesion"
HOME_URL = "https://www.elempleo.com/co/homeusuario"
SESSION_PATH = "config/sesion.json"

def _aceptar_cookies(page: Page):
    banner_cookies = page.locator('div.politics_cookie')
    if banner_cookies.is_visible():
        page.click('button.btnAcceptPolicyNavigationCO')

def _ingresar_credenciales(page: Page):
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    page.fill('input[name="EmailField"]', email)
    page.fill('input[name="PasswordField"]', password)
    page.click('button[type="submit"]')

def generar_sesion():
    os.makedirs("config", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        _aceptar_cookies(page)
        page.wait_for_timeout(3000)
        
        _ingresar_credenciales(page)
        page.wait_for_url(HOME_URL, wait_until="domcontentloaded")
        
        context.storage_state(path=SESSION_PATH)
        browser.close()

def validar_estado_sesion() -> bool:
    if not os.path.exists(SESSION_PATH):
        return False
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=SESSION_PATH)
        page = context.new_page()
        
        page.goto(HOME_URL, wait_until="commit")
        page.wait_for_timeout(3000)
        
        es_valida = "iniciar-sesion" not in page.url
        browser.close()
        return es_valida

def ejecutar_autenticacion():
    print("Verificando estado de la sesión...")
    
    if not validar_estado_sesion():
        print("Sesión inválida o inexistente. Generando nueva sesión en modo oculto...")
        generar_sesion()
        print("Sesión generada y guardada en config/sesion.json.")
    else:
        print("La sesión actual es válida.")
        
    print("Módulo de autenticación finalizado.")

if __name__ == "__main__":
    ejecutar_autenticacion()