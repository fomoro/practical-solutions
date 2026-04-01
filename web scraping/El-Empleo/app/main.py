import os
from modules import modulo_00_autenticacion
from modules import modulo_02_scraper_ofertas_empleo_filter
from modules import modulo_03_aplicador_ofertas_preguntas

def main():
    while True:
        print("\n🚀 Iniciando Sistema de Automatización de Empleo")
        print("1. Iniciar/Actualizar sesión (Módulo 00)")
        print("2. Buscar y extraer nuevas ofertas (Módulo 02)")
        print("3. Aplicar a ofertas pendientes (Módulo 03)")    
        print("5. Salir")
        
        opcion = input("\nElige el proceso a ejecutar: ").strip()
        
        if opcion == '1':
            modulo_00_autenticacion.ejecutar_autenticacion() 
        elif opcion == '2':
            modulo_02_scraper_ofertas_empleo_filter.ejecutar_extraccion()
        elif opcion == '3':
            modulo_03_aplicador_ofertas_preguntas.ejecutar_postulacion()
        elif opcion == '5':
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()