#!/usr/bin/env python3
"""
Script para obtener un nuevo token de Strava con los scopes correctos.
Este script te guiará paso a paso para obtener un refresh token válido.
"""

import os
import webbrowser
from dotenv import load_dotenv
import requests

load_dotenv()

def get_strava_token():
    """Guía al usuario para obtener un token de Strava con los scopes correctos."""
    
    print("\n" + "="*80)
    print("🔑 OBTENER TOKEN DE STRAVA CON SCOPES CORRECTOS")
    print("="*80 + "\n")
    
    # Obtener credenciales del .env
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Error: No se encontraron STRAVA_CLIENT_ID o STRAVA_CLIENT_SECRET en .env")
        print("   Por favor, configura estas variables primero.")
        return
    
    print(f"✅ Client ID encontrado: {client_id}")
    print(f"✅ Client Secret encontrado: {client_secret[:10]}...")
    print()
    
    # Paso 1: Generar URL de autorización
    scopes = "read,activity:read_all,profile:read_all"
    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri=http://localhost&"
        f"approval_prompt=force&"
        f"scope={scopes}"
    )
    
    print("📋 PASO 1: Autorizar la aplicación")
    print("-" * 80)
    print("Se abrirá tu navegador con la página de autorización de Strava.")
    print("Debes autorizar la aplicación con los siguientes permisos:")
    print("  • read - Leer información básica")
    print("  • activity:read_all - Leer todas tus actividades")
    print("  • profile:read_all - Leer tu perfil completo")
    print()
    print("URL de autorización:")
    print(auth_url)
    print()
    
    input("Presiona ENTER para abrir el navegador...")
    webbrowser.open(auth_url)
    
    print()
    print("📋 PASO 2: Copiar el código de autorización")
    print("-" * 80)
    print("Después de autorizar, serás redirigido a una URL como:")
    print("http://localhost/?state=&code=CODIGO_AQUI&scope=read,activity:read_all,profile:read_all")
    print()
    print("Copia el valor del parámetro 'code' de la URL.")
    print()
    
    auth_code = input("Pega el código de autorización aquí: ").strip()
    
    if not auth_code:
        print("❌ Error: No se proporcionó ningún código.")
        return
    
    print()
    print("📋 PASO 3: Intercambiar código por tokens")
    print("-" * 80)
    print("Intercambiando código por access token y refresh token...")
    
    try:
        response = requests.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": auth_code,
                "grant_type": "authorization_code"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        print("✅ ¡Tokens obtenidos exitosamente!")
        print()
        print("📋 PASO 4: Actualizar tu archivo .env")
        print("-" * 80)
        print("Copia y pega la siguiente línea en tu archivo .env:")
        print()
        print(f"STRAVA_REFRESH_TOKEN={data['refresh_token']}")
        print()
        print("Información adicional:")
        print(f"  • Access Token: {data['access_token'][:20]}...")
        print(f"  • Refresh Token: {data['refresh_token'][:20]}...")
        print(f"  • Expira en: {data['expires_in']} segundos")
        print(f"  • Scopes: {data.get('scope', 'N/A')}")
        print()
        print("✅ ¡Listo! Ahora puedes usar el agente de Strava.")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al intercambiar el código: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Respuesta del servidor: {e.response.text}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    try:
        get_strava_token()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso cancelado por el usuario.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

# Made with Bob
