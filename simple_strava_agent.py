#!/usr/bin/env python3
"""
Agente Simple de Strava - Implementación directa sin BeeAI
Usa la API de Strava directamente con un wrapper conversacional simple.
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class SimpleStravaAgent:
    """Agente simple para consultar la API de Strava."""
    
    def __init__(self):
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.access_token = None
        self.base_url = "https://www.strava.com/api/v3"
        
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("Faltan credenciales de Strava en .env")
        
        self._refresh_access_token()
    
    def _refresh_access_token(self):
        """Refresca el token de acceso."""
        print("🔄 Refrescando token de Strava...")
        response = requests.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        self.access_token = data["access_token"]
        print("✅ Token refrescado exitosamente")
    
    def _get_headers(self):
        """Retorna headers con autenticación."""
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def get_profile(self):
        """Obtiene el perfil del atleta."""
        response = requests.get(
            f"{self.base_url}/athlete",
            headers=self._get_headers(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def get_activities(self, per_page=10):
        """Obtiene las últimas actividades."""
        response = requests.get(
            f"{self.base_url}/athlete/activities",
            headers=self._get_headers(),
            params={"per_page": per_page},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def get_activity_details(self, activity_id):
        """Obtiene detalles de una actividad específica."""
        response = requests.get(
            f"{self.base_url}/activities/{activity_id}",
            headers=self._get_headers(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def get_stats(self, athlete_id):
        """Obtiene estadísticas del atleta."""
        response = requests.get(
            f"{self.base_url}/athletes/{athlete_id}/stats",
            headers=self._get_headers(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def format_activity(self, activity):
        """Formatea una actividad para mostrar."""
        distance_km = activity.get('distance', 0) / 1000
        moving_time_min = activity.get('moving_time', 0) / 60
        date = datetime.fromisoformat(activity.get('start_date', '').replace('Z', '+00:00'))
        
        result = f"""
📍 {activity.get('name', 'Sin nombre')}
   • Tipo: {activity.get('type', 'N/A')}
   • Distancia: {distance_km:.2f} km
   • Tiempo: {moving_time_min:.0f} min
   • Fecha: {date.strftime('%Y-%m-%d %H:%M')}"""
        
        if activity.get('average_heartrate'):
            result += f"\n   • FC promedio: {activity.get('average_heartrate'):.0f} bpm"
        
        if activity.get('average_speed'):
            speed_kmh = activity.get('average_speed') * 3.6
            result += f"\n   • Velocidad: {speed_kmh:.1f} km/h"
        
        return result
    
    def analyze_activities(self, count=10):
        """Analiza las últimas actividades."""
        print(f"\n🔍 Analizando tus últimas {count} actividades...\n")
        
        activities = self.get_activities(per_page=count)
        
        if not activities:
            return "No se encontraron actividades."
        
        result = f"📊 Resumen de tus últimas {len(activities)} actividades:\n"
        result += "=" * 60 + "\n"
        
        total_distance = 0
        total_time = 0
        types = {}
        
        for i, activity in enumerate(activities, 1):
            result += f"\n{i}. {self.format_activity(activity)}\n"
            
            # Acumular estadísticas
            total_distance += activity.get('distance', 0)
            total_time += activity.get('moving_time', 0)
            activity_type = activity.get('type', 'Unknown')
            types[activity_type] = types.get(activity_type, 0) + 1
        
        # Resumen general
        result += "\n" + "=" * 60
        result += f"\n\n📈 Resumen General:"
        result += f"\n   • Distancia total: {total_distance/1000:.2f} km"
        result += f"\n   • Tiempo total: {total_time/60:.0f} min ({total_time/3600:.1f} horas)"
        result += f"\n   • Tipos de actividades:"
        for activity_type, count in types.items():
            result += f"\n     - {activity_type}: {count}"
        
        return result
    
    def get_profile_summary(self):
        """Obtiene un resumen del perfil."""
        profile = self.get_profile()
        
        result = f"""
👤 Perfil de Atleta
==================
Nombre: {profile.get('firstname', '')} {profile.get('lastname', '')}
Usuario: {profile.get('username', 'N/A')}
Ciudad: {profile.get('city', 'N/A')}, {profile.get('country', 'N/A')}
Peso: {profile.get('weight', 'N/A')} kg
Amigos: {profile.get('friend_count', 0)}
Seguidores: {profile.get('follower_count', 0)}
"""
        return result
    
    def run(self, query):
        """Procesa una consulta del usuario."""
        query_lower = query.lower()
        
        try:
            if "perfil" in query_lower or "profile" in query_lower:
                return self.get_profile_summary()
            
            elif "actividad" in query_lower or "activity" in query_lower or "últimas" in query_lower:
                # Extraer número si está presente
                import re
                numbers = re.findall(r'\d+', query)
                count = int(numbers[0]) if numbers else 10
                return self.analyze_activities(count)
            
            elif "estadística" in query_lower or "stats" in query_lower:
                profile = self.get_profile()
                stats = self.get_stats(profile['id'])
                
                result = "\n📊 Estadísticas Totales\n"
                result += "=" * 60 + "\n"
                
                if 'all_run_totals' in stats:
                    run = stats['all_run_totals']
                    result += f"\n🏃 Carrera (Total):"
                    result += f"\n   • Actividades: {run.get('count', 0)}"
                    result += f"\n   • Distancia: {run.get('distance', 0)/1000:.2f} km"
                    result += f"\n   • Tiempo: {run.get('moving_time', 0)/3600:.1f} horas"
                
                if 'all_ride_totals' in stats:
                    ride = stats['all_ride_totals']
                    result += f"\n\n🚴 Ciclismo (Total):"
                    result += f"\n   • Actividades: {ride.get('count', 0)}"
                    result += f"\n   • Distancia: {ride.get('distance', 0)/1000:.2f} km"
                    result += f"\n   • Tiempo: {ride.get('moving_time', 0)/3600:.1f} horas"
                
                return result
            
            else:
                return """
No entendí tu consulta. Puedes preguntarme:
• "Muéstrame mi perfil"
• "Muéstrame mis últimas 10 actividades"
• "Dame mis estadísticas"
"""
        
        except Exception as e:
            return f"❌ Error: {e}"


def main():
    """Función principal."""
    print("\n" + "=" * 80)
    print("🏃‍♂️ AGENTE SIMPLE DE STRAVA 🚴‍♀️")
    print("=" * 80 + "\n")
    
    agent = SimpleStravaAgent()
    
    # Ejemplos de consultas
    queries = [
        "Muéstrame mi perfil",
        "Muéstrame mis últimas 5 actividades",
        "Dame mis estadísticas"
    ]
    
    for query in queries:
        print(f"\n🤖 Usuario: {query}")
        print("🤔 Procesando...\n")
        result = agent.run(query)
        print(result)
        print("\n" + "-" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob