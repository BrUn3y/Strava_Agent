"""
Script de ejemplos funcionales de la API de Strava
Basado en la documentación oficial: https://developers.strava.com/docs/reference/
"""
import asyncio
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class StravaAPIExamples:
    """Ejemplos funcionales de uso de la API de Strava"""
    
    def __init__(self):
        self.base_url = "https://www.strava.com/api/v3"
        self.access_token = self._get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
    
    def _get_access_token(self) -> str:
        """Obtiene un token de acceso válido"""
        client_id = os.getenv("STRAVA_CLIENT_ID")
        client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        
        if not all([client_id, client_secret, refresh_token]):
            raise ValueError("Faltan credenciales de Strava en .env")
        
        print("🔄 Obteniendo token de acceso...")
        response = requests.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        print("✅ Token obtenido\n")
        return data["access_token"]
    
    def example_1_get_athlete_profile(self):
        """Ejemplo 1: Obtener perfil del atleta autenticado"""
        print("=" * 80)
        print("EJEMPLO 1: Obtener Perfil del Atleta")
        print("=" * 80)
        print("Endpoint: GET /athlete")
        print()
        
        response = requests.get(
            f"{self.base_url}/athlete",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        profile = response.json()
        
        print("✅ Perfil obtenido:")
        print(f"   ID: {profile.get('id')}")
        print(f"   Nombre: {profile.get('firstname')} {profile.get('lastname')}")
        print(f"   Usuario: {profile.get('username')}")
        print(f"   Ubicación: {profile.get('city')}, {profile.get('country')}")
        print(f"   Peso: {profile.get('weight')} kg")
        print(f"   FTP: {profile.get('ftp')} watts")
        print(f"   Amigos: {profile.get('friend_count')}")
        print(f"   Seguidores: {profile.get('follower_count')}")
        print()
        
        return profile
    
    def example_2_get_recent_activities(self, per_page=10):
        """Ejemplo 2: Obtener actividades recientes"""
        print("=" * 80)
        print(f"EJEMPLO 2: Obtener Últimas {per_page} Actividades")
        print("=" * 80)
        print(f"Endpoint: GET /athlete/activities?per_page={per_page}")
        print()
        
        response = requests.get(
            f"{self.base_url}/athlete/activities",
            headers=self.headers,
            params={"per_page": per_page, "page": 1},
            timeout=10
        )
        response.raise_for_status()
        activities = response.json()
        
        print(f"✅ {len(activities)} actividades obtenidas:\n")
        
        total_distance = 0
        total_time = 0
        total_elevation = 0
        heartrates = []
        
        for i, activity in enumerate(activities, 1):
            distance_km = activity.get('distance', 0) / 1000
            time_min = activity.get('moving_time', 0) / 60
            elevation = activity.get('total_elevation_gain', 0)
            hr = activity.get('average_heartrate')
            
            total_distance += activity.get('distance', 0)
            total_time += activity.get('moving_time', 0)
            total_elevation += elevation
            if hr:
                heartrates.append(hr)
            
            print(f"   {i}. {activity.get('name')}")
            print(f"      📅 Fecha: {activity.get('start_date_local')}")
            print(f"      🏃 Tipo: {activity.get('type')}")
            print(f"      📏 Distancia: {distance_km:.2f} km")
            print(f"      ⏱️  Tiempo: {time_min:.0f} min")
            print(f"      ⛰️  Elevación: {elevation:.0f} m")
            if hr:
                print(f"      ❤️  FC Promedio: {hr:.0f} bpm")
            print()
        
        # Resumen
        print("📊 RESUMEN:")
        print(f"   Distancia total: {total_distance/1000:.2f} km")
        print(f"   Tiempo total: {total_time/60:.0f} min ({total_time/3600:.1f} hrs)")
        print(f"   Elevación total: {total_elevation:.0f} m")
        if heartrates:
            print(f"   FC promedio: {sum(heartrates)/len(heartrates):.0f} bpm")
        print()
        
        return activities
    
    def example_3_get_activity_details(self, activity_id):
        """Ejemplo 3: Obtener detalles completos de una actividad"""
        print("=" * 80)
        print(f"EJEMPLO 3: Detalles de Actividad {activity_id}")
        print("=" * 80)
        print(f"Endpoint: GET /activities/{activity_id}?include_all_efforts=true")
        print()
        
        response = requests.get(
            f"{self.base_url}/activities/{activity_id}",
            headers=self.headers,
            params={"include_all_efforts": True},
            timeout=10
        )
        response.raise_for_status()
        activity = response.json()
        
        print("✅ Detalles de la actividad:")
        print(f"   Nombre: {activity.get('name')}")
        print(f"   Descripción: {activity.get('description', 'N/A')}")
        print(f"   Tipo: {activity.get('type')}")
        print(f"   Distancia: {activity.get('distance', 0)/1000:.2f} km")
        print(f"   Tiempo en movimiento: {activity.get('moving_time', 0)/60:.0f} min")
        print(f"   Tiempo total: {activity.get('elapsed_time', 0)/60:.0f} min")
        print(f"   Elevación ganada: {activity.get('total_elevation_gain', 0):.0f} m")
        print(f"   Calorías: {activity.get('calories', 0):.0f}")
        print(f"   Dispositivo: {activity.get('device_name', 'N/A')}")
        
        if activity.get('average_heartrate'):
            print(f"   FC Promedio: {activity.get('average_heartrate'):.0f} bpm")
            print(f"   FC Máxima: {activity.get('max_heartrate'):.0f} bpm")
        
        if activity.get('average_watts'):
            print(f"   Potencia Promedio: {activity.get('average_watts'):.0f} W")
        
        # Splits
        splits = activity.get('splits_metric', [])
        if splits:
            print(f"\n   📊 Splits (primeros 5):")
            for i, split in enumerate(splits[:5], 1):
                pace_min_km = split.get('moving_time', 0) / 60
                print(f"      {i}. {split.get('distance', 0)/1000:.1f} km - {pace_min_km:.2f} min/km")
        
        # Segmentos
        segments = activity.get('segment_efforts', [])
        if segments:
            print(f"\n   🏔️  Segmentos ({len(segments)} total):")
            for i, segment in enumerate(segments[:3], 1):
                print(f"      {i}. {segment.get('name')}")
                print(f"         Tiempo: {segment.get('elapsed_time', 0)/60:.1f} min")
        
        print()
        return activity
    
    def example_4_get_athlete_stats(self, athlete_id):
        """Ejemplo 4: Obtener estadísticas del atleta"""
        print("=" * 80)
        print(f"EJEMPLO 4: Estadísticas del Atleta {athlete_id}")
        print("=" * 80)
        print(f"Endpoint: GET /athletes/{athlete_id}/stats")
        print()
        
        response = requests.get(
            f"{self.base_url}/athletes/{athlete_id}/stats",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        stats = response.json()
        
        print("✅ Estadísticas obtenidas:\n")
        
        # Estadísticas de ciclismo
        recent_rides = stats.get('recent_ride_totals', {})
        all_rides = stats.get('all_ride_totals', {})
        
        if recent_rides.get('count', 0) > 0:
            print("   🚴 CICLISMO RECIENTE (últimas 4 semanas):")
            print(f"      Actividades: {recent_rides.get('count', 0)}")
            print(f"      Distancia: {recent_rides.get('distance', 0)/1000:.2f} km")
            print(f"      Tiempo: {recent_rides.get('moving_time', 0)/3600:.1f} hrs")
            print(f"      Elevación: {recent_rides.get('elevation_gain', 0):.0f} m")
            print()
        
        if all_rides.get('count', 0) > 0:
            print("   🚴 CICLISMO TOTAL:")
            print(f"      Actividades: {all_rides.get('count', 0)}")
            print(f"      Distancia: {all_rides.get('distance', 0)/1000:.2f} km")
            print(f"      Tiempo: {all_rides.get('moving_time', 0)/3600:.1f} hrs")
            print(f"      Elevación: {all_rides.get('elevation_gain', 0):.0f} m")
            print()
        
        # Estadísticas de carrera
        recent_runs = stats.get('recent_run_totals', {})
        all_runs = stats.get('all_run_totals', {})
        
        if recent_runs.get('count', 0) > 0:
            print("   🏃 CARRERA RECIENTE (últimas 4 semanas):")
            print(f"      Actividades: {recent_runs.get('count', 0)}")
            print(f"      Distancia: {recent_runs.get('distance', 0)/1000:.2f} km")
            print(f"      Tiempo: {recent_runs.get('moving_time', 0)/3600:.1f} hrs")
            print(f"      Elevación: {recent_runs.get('elevation_gain', 0):.0f} m")
            print()
        
        if all_runs.get('count', 0) > 0:
            print("   🏃 CARRERA TOTAL:")
            print(f"      Actividades: {all_runs.get('count', 0)}")
            print(f"      Distancia: {all_runs.get('distance', 0)/1000:.2f} km")
            print(f"      Tiempo: {all_runs.get('moving_time', 0)/3600:.1f} hrs")
            print(f"      Elevación: {all_runs.get('elevation_gain', 0):.0f} m")
            print()
        
        # Records
        print("   🏆 RECORDS:")
        print(f"      Mayor distancia en bici: {stats.get('biggest_ride_distance', 0)/1000:.2f} km")
        print(f"      Mayor escalada: {stats.get('biggest_climb_elevation_gain', 0):.0f} m")
        print()
        
        return stats
    
    def example_5_get_activity_zones(self, activity_id):
        """Ejemplo 5: Obtener zonas de una actividad"""
        print("=" * 80)
        print(f"EJEMPLO 5: Zonas de Actividad {activity_id}")
        print("=" * 80)
        print(f"Endpoint: GET /activities/{activity_id}/zones")
        print()
        
        response = requests.get(
            f"{self.base_url}/activities/{activity_id}/zones",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        zones = response.json()
        
        if not zones:
            print("⚠️  No hay datos de zonas para esta actividad")
            print()
            return None
        
        print("✅ Zonas obtenidas:\n")
        
        for zone_data in zones:
            zone_type = zone_data.get('type', 'unknown')
            print(f"   📊 Tipo: {zone_type.upper()}")
            
            buckets = zone_data.get('distribution_buckets', [])
            for i, bucket in enumerate(buckets, 1):
                min_val = bucket.get('min', 0)
                max_val = bucket.get('max', -1)
                time_sec = bucket.get('time', 0)
                time_min = time_sec / 60
                
                if max_val == -1:
                    range_str = f">{min_val}"
                else:
                    range_str = f"{min_val}-{max_val}"
                
                print(f"      Zona {i}: {range_str} - {time_min:.1f} min")
            print()
        
        return zones
    
    def example_6_get_clubs(self):
        """Ejemplo 6: Obtener clubes del atleta"""
        print("=" * 80)
        print("EJEMPLO 6: Clubes del Atleta")
        print("=" * 80)
        print("Endpoint: GET /athlete/clubs")
        print()
        
        response = requests.get(
            f"{self.base_url}/athlete/clubs",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        clubs = response.json()
        
        if not clubs:
            print("⚠️  No perteneces a ningún club")
            print()
            return []
        
        print(f"✅ {len(clubs)} club(es) encontrado(s):\n")
        
        for i, club in enumerate(clubs, 1):
            print(f"   {i}. {club.get('name')}")
            print(f"      ID: {club.get('id')}")
            print(f"      Deporte: {club.get('sport_type')}")
            print(f"      Ubicación: {club.get('city')}, {club.get('country')}")
            print(f"      Miembros: {club.get('member_count')}")
            print()
        
        return clubs


async def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "=" * 80)
    print("🏃‍♂️ EJEMPLOS DE API DE STRAVA 🚴‍♀️")
    print("=" * 80)
    print()
    
    try:
        examples = StravaAPIExamples()
        
        # Ejemplo 1: Perfil
        profile = examples.example_1_get_athlete_profile()
        athlete_id = profile.get('id')
        
        input("Presiona Enter para continuar...")
        print()
        
        # Ejemplo 2: Actividades recientes
        activities = examples.example_2_get_recent_activities(per_page=10)
        
        if activities:
            input("Presiona Enter para continuar...")
            print()
            
            # Ejemplo 3: Detalles de la primera actividad
            first_activity_id = activities[0].get('id')
            examples.example_3_get_activity_details(first_activity_id)
            
            input("Presiona Enter para continuar...")
            print()
            
            # Ejemplo 5: Zonas de la primera actividad
            examples.example_5_get_activity_zones(first_activity_id)
        
        input("Presiona Enter para continuar...")
        print()
        
        # Ejemplo 4: Estadísticas del atleta
        examples.example_4_get_athlete_stats(athlete_id)
        
        input("Presiona Enter para continuar...")
        print()
        
        # Ejemplo 6: Clubes
        examples.example_6_get_clubs()
        
        print("=" * 80)
        print("✅ ¡Todos los ejemplos completados exitosamente!")
        print("=" * 80)
        print()
        print("💡 NOTA: Estos ejemplos muestran cómo usar la API de Strava directamente.")
        print("   Para usar con el agente de BeeAI, consulta el archivo strava-tool-fixed.yaml")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob