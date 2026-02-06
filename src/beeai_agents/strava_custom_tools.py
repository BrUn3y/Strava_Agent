"""
Custom Strava Tools for BeeAI
Based on functional code from simple_strava_agent.py
"""

import os
import requests
from dotenv import load_dotenv
from typing import Any, Dict
from beeai_framework.tools import Tool, StringToolOutput, ToolRunOptions
from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from pydantic import BaseModel, Field

load_dotenv()


class StravaAuth:
    """Handles OAuth2 authentication with Strava."""
    
    _instance = None
    _access_token = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.client_id = os.getenv("STRAVA_CLIENT_ID")
            self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
            self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
            self.base_url = "https://www.strava.com/api/v3"
            self.initialized = True
            
            if not all([self.client_id, self.client_secret, self.refresh_token]):
                raise ValueError("Missing Strava credentials in .env")
    
    def get_token(self) -> str:
        """Gets a valid access token, refreshing it if necessary."""
        if not self._access_token:
            self._refresh_token()
        return self._access_token or ""
    
    def _refresh_token(self):
        """Refreshes the access token."""
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
        self._access_token = data["access_token"]
    
    def get_headers(self):
        """Returns headers with authentication."""
        return {"Authorization": f"Bearer {self.get_token()}"}


# Global authentication instance
_auth = StravaAuth()


# ==================== INPUT SCHEMAS ====================

class EmptyInput(BaseModel):
    """Empty input for tools without parameters."""
    pass


class GetActivitiesInput(BaseModel):
    """Input for getting activities."""
    per_page: int = Field(
        default=10,
        description="Number of activities to get (1-200)",
        ge=1,
        le=200
    )


class GetActivityByIdInput(BaseModel):
    """Input for getting activity details."""
    activity_id: int = Field(
        description="Activity ID to query"
    )


class GetAthleteStatsInput(BaseModel):
    """Input for getting athlete statistics."""
    athlete_id: int = Field(
        description="Athlete ID (use profile ID)"
    )


class GetActivityZonesInput(BaseModel):
    """Input for getting activity zones."""
    activity_id: int = Field(
        description="Activity ID"
    )


class GetActivityLapsInput(BaseModel):
    """Input for getting activity laps."""
    activity_id: int = Field(
        description="Activity ID"
    )


class GetActivityStreamsInput(BaseModel):
    """Input for getting activity data streams."""
    activity_id: int = Field(
        description="Activity ID"
    )
    keys: str = Field(
        default="time,distance,heartrate,altitude,velocity_smooth",
        description="Data types separated by comma (time,distance,heartrate,altitude,velocity_smooth,watts,cadence,temp,grade_smooth)"
    )


class ExploreSegmentsInput(BaseModel):
    """Input for exploring segments in an area."""
    bounds: str = Field(
        description="Area coordinates in format: sw_lat,sw_lng,ne_lat,ne_lng (example: 37.821,-122.505,37.842,-122.466)"
    )
    activity_type: str = Field(
        default="riding",
        description="Activity type: 'running' or 'riding'"
    )


class GetSegmentByIdInput(BaseModel):
    """Input for getting segment details."""
    segment_id: int = Field(
        description="Segment ID"
    )


class GetSegmentLeaderboardInput(BaseModel):
    """Input for getting segment leaderboard."""
    segment_id: int = Field(
        description="Segment ID"
    )
    per_page: int = Field(
        default=10,
        description="Number of entries (1-200)",
        ge=1,
        le=200
    )


class GetRouteByIdInput(BaseModel):
    """Input for getting route details."""
    route_id: int = Field(
        description="Route ID"
    )


class GetAthleteRoutesInput(BaseModel):
    """Input for getting athlete routes."""
    athlete_id: int = Field(
        description="Athlete ID"
    )
    per_page: int = Field(
        default=10,
        description="Number of routes (1-200)",
        ge=1,
        le=200
    )


class GetClubByIdInput(BaseModel):
    """Input for getting club details."""
    club_id: int = Field(
        description="Club ID"
    )


class GetClubActivitiesInput(BaseModel):
    """Input for getting club activities."""
    club_id: int = Field(
        description="Club ID"
    )
    per_page: int = Field(
        default=10,
        description="Number of activities (1-200)",
        ge=1,
        le=200
    )


class GetClubMembersInput(BaseModel):
    """Input for getting club members."""
    club_id: int = Field(
        description="Club ID"
    )
    per_page: int = Field(
        default=30,
        description="Number of members (1-200)",
        ge=1,
        le=200
    )



class CompareRunningSessionsInput(BaseModel):
    """Input for comparing running sessions."""
    num_sessions: int = Field(
        default=5,
        description="Number of recent running sessions to compare (2-30)",
        ge=2,
        le=30
    )


class CompareSpecificRunsInput(BaseModel):
    """Input for comparing specific running sessions by date."""
    date1: str = Field(
        description="First date in format YYYY-MM-DD (e.g., 2026-01-18)"
    )
    date2: str = Field(
        description="Second date in format YYYY-MM-DD (e.g., 2026-02-01)"
    )


class RecommendTrainingInput(BaseModel):
    """Input for training recommendations."""
    num_sessions: int = Field(
        default=10,
        description="Number of recent sessions to analyze for recommendations (5-30)",
        ge=5,
        le=30
    )
    goal: str = Field(
        default="improve_performance",
        description="Training goal: 'improve_performance', 'increase_distance', 'improve_pace', 'build_endurance'"
    )




# ==================== CUSTOM TOOLS ====================

class GetAthleteProfileTool(Tool[EmptyInput, ToolRunOptions, StringToolOutput]):
    """Tool to get the authenticated athlete's profile."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetAthleteProfile"
        self._description = """Gets the complete profile of the authenticated athlete.
Returns: name, city, weight, FTP, friends, followers.
No parameters required."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return EmptyInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: EmptyInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/athlete",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Build result with Markdown image syntax directly
            result = "Athlete Profile:\n\n"
            
            # Profile photo display disabled for privacy
            # if data.get('profile'):
            #     result += f"![Profile Photo]({data.get('profile')})\n\n"
            # elif data.get('profile_medium'):
            #     result += f"![Profile Photo]({data.get('profile_medium')})\n\n"
            
            result += f"""- Name: {data.get('firstname', '')} {data.get('lastname', '')}
- Username: {data.get('username', 'N/A')}
- ID: {data.get('id')}
- City: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}
- Weight: {data.get('weight', 'N/A')} kg
- FTP: {data.get('ftp', 'N/A')} watts
- Friends: {data.get('friend_count', 0)}
- Followers: {data.get('follower_count', 0)}"""
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error getting profile: {e}")


class GetActivitiesTool(Tool[GetActivitiesInput, ToolRunOptions, StringToolOutput]):
    """Tool to get recent activities."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetActivities"
        self._description = """Gets the most recent activities of the athlete.
Parameters:
- per_page: Number of activities to get (1-200, default: 10)

Returns: list of activities with name, type, distance, time, date, etc."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetActivitiesInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetActivitiesInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            per_page = input.per_page
            
            response = requests.get(
                f"{_auth.base_url}/athlete/activities",
                headers=_auth.get_headers(),
                params={"per_page": min(per_page, 200)},
                timeout=10
            )
            response.raise_for_status()
            activities = response.json()
            
            if not activities:
                return StringToolOutput("No activities found.")
            
            result = f"Last {len(activities)} activities:\n\n"
            
            for i, activity in enumerate(activities, 1):
                distance_km = activity.get('distance', 0) / 1000
                time_min = activity.get('moving_time', 0) / 60
                
                result += f"{i}. {activity.get('name', 'Unnamed')}\n"
                result += f"   - Type: {activity.get('type', 'N/A')}\n"
                result += f"   - Distance: {distance_km:.2f} km\n"
                result += f"   - Time: {time_min:.0f} min\n"
                result += f"   - Date: {activity.get('start_date_local', 'N/A')}\n"
                
                if activity.get('average_heartrate'):
                    result += f"   - Avg HR: {activity.get('average_heartrate'):.0f} bpm\n"
                
                if activity.get('average_speed'):
                    speed_kmh = activity.get('average_speed') * 3.6
                    result += f"   - Speed: {speed_kmh:.1f} km/h\n"
                
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener activities: {e}")


class GetActivityByIdTool(Tool[GetActivityByIdInput, ToolRunOptions, StringToolOutput]):
    """Tool to get details of a specific activity."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetActivityById"
        self._description = """Gets complete details of a specific activity.
Parameters:
- activity_id: Activity ID (get ID with GetActivities)

Returns: detailed information including splits, zones, segments, etc."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetActivityByIdInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetActivityByIdInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            activity_id = input.activity_id
            
            response = requests.get(
                f"{_auth.base_url}/activities/{activity_id}",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            activity = response.json()
            
            distance_km = activity.get('distance', 0) / 1000
            time_min = activity.get('moving_time', 0) / 60
            
            result = f"""Activity Details:

"""
            
            # Add map image if polyline is available and Google Maps key is set
            map_data = activity.get('map', {})
            polyline = map_data.get('polyline', '')
            google_maps_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
            
            if polyline and google_maps_key:
                map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&path=enc:{polyline}&key={google_maps_key}"
                result += f"![Route Map]({map_url})\n\n"
            
            result += f"""- Name: {activity.get('name', 'Unnamed')}
- Type: {activity.get('type', 'N/A')}
- Description: {activity.get('description', 'No description')}
- Distance: {distance_km:.2f} km
- Moving time: {time_min:.0f} min
- Total time: {activity.get('elapsed_time', 0) / 60:.0f} min
- Elevation gain: {activity.get('total_elevation_gain', 0):.0f} m
- Date: {activity.get('start_date_local', 'N/A')}
- Calories: {activity.get('calories', 'N/A')}
- Device: {activity.get('device_name', 'N/A')}"""
            
            if activity.get('average_heartrate'):
                result += f"\n- Avg HR: {activity.get('average_heartrate'):.0f} bpm"
                result += f"\n- Max HR: {activity.get('max_heartrate', 0):.0f} bpm"
            
            if activity.get('average_speed'):
                speed_kmh = activity.get('average_speed') * 3.6
                result += f"\n- Avg speed: {speed_kmh:.1f} km/h"
                result += f"\n- Max speed: {activity.get('max_speed', 0) * 3.6:.1f} km/h"
            
            if activity.get('average_watts'):
                result += f"\n- Avg power: {activity.get('average_watts'):.0f} watts"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error getting activity: {e}")


class GetAthleteStatsTool(Tool[GetAthleteStatsInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener estadísticas del atleta."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetAthleteStats"
        self._description = """Obtiene estadísticas totales y recientes del atleta.
Parameters:
- athlete_id: ID del atleta (obtén el ID con GetAthleteProfile)

Devuelve: estadísticas de carrera y ciclismo (totales y recientes)."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetAthleteStatsInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetAthleteStatsInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            athlete_id = input.athlete_id
            
            response = requests.get(
                f"{_auth.base_url}/athletes/{athlete_id}/stats",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            stats = response.json()
            
            result = "Estadísticas del Atleta:\n\n"
            
            if 'all_run_totals' in stats:
                run = stats['all_run_totals']
                result += "🏃 CARRERA (Total):\n"
                result += f"- Actividades: {run.get('count', 0)}\n"
                result += f"- Distance: {run.get('distance', 0) / 1000:.2f} km\n"
                result += f"- Time: {run.get('moving_time', 0) / 3600:.1f} horas\n"
                result += f"- Elevación: {run.get('elevation_gain', 0):.0f} m\n\n"
            
            if 'recent_run_totals' in stats:
                run = stats['recent_run_totals']
                result += "🏃 CARRERA (Last 4 semanas):\n"
                result += f"- Actividades: {run.get('count', 0)}\n"
                result += f"- Distance: {run.get('distance', 0) / 1000:.2f} km\n"
                result += f"- Time: {run.get('moving_time', 0) / 3600:.1f} horas\n\n"
            
            if 'all_ride_totals' in stats:
                ride = stats['all_ride_totals']
                result += "🚴 CICLISMO (Total):\n"
                result += f"- Actividades: {ride.get('count', 0)}\n"
                result += f"- Distance: {ride.get('distance', 0) / 1000:.2f} km\n"
                result += f"- Time: {ride.get('moving_time', 0) / 3600:.1f} horas\n"
                result += f"- Elevación: {ride.get('elevation_gain', 0):.0f} m\n\n"
            
            if 'recent_ride_totals' in stats:
                ride = stats['recent_ride_totals']
                result += "🚴 CICLISMO (Last 4 semanas):\n"
                result += f"- Actividades: {ride.get('count', 0)}\n"
                result += f"- Distance: {ride.get('distance', 0) / 1000:.2f} km\n"
                result += f"- Time: {ride.get('moving_time', 0) / 3600:.1f} horas\n\n"
            
            result += f"Récords:\n"
            result += f"- Mayor distancia en bici: {stats.get('biggest_ride_distance', 0) / 1000:.2f} km\n"
            result += f"- Mayor elevación: {stats.get('biggest_climb_elevation_gain', 0):.0f} m"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener estadísticas: {e}")


class GetActivityZonesTool(Tool[GetActivityZonesInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener zonas de entrenamiento de una actividad."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetActivityZones"
        self._description = """Obtiene la distribución de zonas de frecuencia cardíaca o potencia de una actividad.
Parameters:
- activity_id: ID de la actividad

Devuelve: tiempo en cada zona de entrenamiento."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetActivityZonesInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetActivityZonesInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/activities/{input.activity_id}/zones",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            zones = response.json()
            
            result = "Zonas de Entrenamiento:\n\n"
            
            for zone_data in zones:
                zone_type = zone_data.get('type', 'unknown')
                result += f"Type: {zone_type.upper()}\n"
                
                if 'distribution_buckets' in zone_data:
                    for bucket in zone_data['distribution_buckets']:
                        min_val = bucket.get('min', 0)
                        max_val = bucket.get('max', 0)
                        time_sec = bucket.get('time', 0)
                        time_min = time_sec / 60
                        result += f"  Zona {min_val}-{max_val}: {time_min:.1f} min\n"
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener zonas: {e}")


class GetActivityLapsTool(Tool[GetActivityLapsInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener vueltas/splits de una actividad."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetActivityLaps"
        self._description = """Obtiene las vueltas o splits de una actividad.
Parameters:
- activity_id: ID de la actividad

Devuelve: información de cada vuelta (distancia, tiempo, velocidad, FC)."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetActivityLapsInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetActivityLapsInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/activities/{input.activity_id}/laps",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            laps = response.json()
            
            if not laps:
                return StringToolOutput("No se encontraron vueltas.")
            
            result = f"Vueltas de la Actividad ({len(laps)} vueltas):\n\n"
            
            for i, lap in enumerate(laps, 1):
                distance_km = lap.get('distance', 0) / 1000
                time_min = lap.get('moving_time', 0) / 60
                speed_kmh = lap.get('average_speed', 0) * 3.6
                
                result += f"Vuelta {i}:\n"
                result += f"  - Distance: {distance_km:.2f} km\n"
                result += f"  - Time: {time_min:.1f} min\n"
                result += f"  - Avg speed: {speed_kmh:.1f} km/h\n"
                
                if lap.get('average_heartrate'):
                    result += f"  - Avg HR: {lap.get('average_heartrate'):.0f} bpm\n"
                
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener vueltas: {e}")


class GetActivityStreamsTool(Tool[GetActivityStreamsInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener datos detallados punto por punto de una actividad."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetActivityStreams"
        self._description = """Obtiene datos detallados punto por punto de una actividad (GPS, FC, potencia, etc.).
Parameters:
- activity_id: ID de la actividad
- keys: Tipos de datos separados por coma (default: time,distance,heartrate,altitude,velocity_smooth)

Devuelve: resumen de los datos disponibles."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetActivityStreamsInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetActivityStreamsInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/activities/{input.activity_id}/streams",
                headers=_auth.get_headers(),
                params={"keys": input.keys, "key_by_type": "true"},
                timeout=10
            )
            response.raise_for_status()
            streams = response.json()
            
            result = "Datos Detallados de la Actividad:\n\n"
            
            for stream_type, stream_data in streams.items():
                data_points = len(stream_data.get('data', []))
                result += f"{stream_type.upper()}:\n"
                result += f"  - Puntos de datos: {data_points}\n"
                
                if data_points > 0:
                    data = stream_data.get('data', [])
                    if stream_type == 'heartrate':
                        result += f"  - Mínimo: {min(data):.0f} bpm\n"
                        result += f"  - Máximo: {max(data):.0f} bpm\n"
                        result += f"  - Promedio: {sum(data)/len(data):.0f} bpm\n"
                    elif stream_type == 'altitude':
                        result += f"  - Mínimo: {min(data):.0f} m\n"
                        result += f"  - Máximo: {max(data):.0f} m\n"
                    elif stream_type == 'velocity_smooth':
                        result += f"  - Max speed: {max(data)*3.6:.1f} km/h\n"
                    elif stream_type == 'watts':
                        result += f"  - Avg power: {sum(data)/len(data):.0f} W\n"
                        result += f"  - Potencia máxima: {max(data):.0f} W\n"
                
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener streams: {e}")


class ExploreSegmentsTool(Tool[ExploreSegmentsInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para explorar segmentos en un área geográfica."""
    
    def __init__(self):
        super().__init__()
        self._name = "ExploreSegments"
        self._description = """Busca segmentos en un área geográfica específica.
Parameters:
- bounds: Coordenadas del área (sw_lat,sw_lng,ne_lat,ne_lng)
- activity_type: 'running' o 'riding' (default: riding)

Devuelve: lista de segmentos en el área."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return ExploreSegmentsInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: ExploreSegmentsInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/segments/explore",
                headers=_auth.get_headers(),
                params={"bounds": input.bounds, "activity_type": input.activity_type},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            segments = data.get('segments', [])
            
            if not segments:
                return StringToolOutput("No se encontraron segmentos en el área.")
            
            result = f"Segmentos encontrados ({len(segments)}):\n\n"
            
            for i, segment in enumerate(segments[:10], 1):
                result += f"{i}. {segment.get('name', 'Unnamed')}\n"
                result += f"   - ID: {segment.get('id')}\n"
                result += f"   - Distance: {segment.get('distance', 0)/1000:.2f} km\n"
                result += f"   - Pendiente promedio: {segment.get('avg_grade', 0):.1f}%\n"
                result += f"   - Elevación: {segment.get('elev_difference', 0):.0f} m\n"
                result += f"   - Categoría: {segment.get('climb_category', 0)}\n"
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al explorar segmentos: {e}")


class GetSegmentByIdTool(Tool[GetSegmentByIdInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener detalles de un segmento."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetSegmentById"
        self._description = """Obtiene detalles completos de un segmento específico.
Parameters:
- segment_id: ID del segmento

Devuelve: información detallada del segmento."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetSegmentByIdInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetSegmentByIdInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/segments/{input.segment_id}",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            segment = response.json()
            
            result = f"""Detalles del Segmento:
- Name: {segment.get('name', 'Unnamed')}
- ID: {segment.get('id')}
- Type: {segment.get('activity_type', 'N/A')}
- Distance: {segment.get('distance', 0)/1000:.2f} km
- Pendiente promedio: {segment.get('average_grade', 0):.1f}%
- Pendiente máxima: {segment.get('maximum_grade', 0):.1f}%
- Elevación alta: {segment.get('elevation_high', 0):.0f} m
- Elevación baja: {segment.get('elevation_low', 0):.0f} m
- Categoría de escalada: {segment.get('climb_category', 0)}
- City: {segment.get('city', 'N/A')}
- País: {segment.get('country', 'N/A')}
- Total de esfuerzos: {segment.get('effort_count', 0)}
- Total de atletas: {segment.get('athlete_count', 0)}"""
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener segmento: {e}")


class GetSegmentLeaderboardTool(Tool[GetSegmentLeaderboardInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener la tabla de clasificación de un segmento."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetSegmentLeaderboard"
        self._description = """Obtiene la tabla de clasificación de un segmento.
Parameters:
- segment_id: ID del segmento
- per_page: Número de entradas (1-200, default: 10)

Devuelve: mejores tiempos en el segmento."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetSegmentLeaderboardInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetSegmentLeaderboardInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/segments/{input.segment_id}/leaderboard",
                headers=_auth.get_headers(),
                params={"per_page": input.per_page},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            entries = data.get('entries', [])
            
            if not entries:
                return StringToolOutput("No hay entradas en la clasificación.")
            
            result = f"Clasificación del Segmento (Top {len(entries)}):\n\n"
            
            for entry in entries:
                rank = entry.get('rank', 0)
                athlete_name = entry.get('athlete_name', 'Desconocido')
                elapsed_time = entry.get('elapsed_time', 0)
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60
                
                result += f"{rank}. {athlete_name}\n"
                result += f"   - Time: {minutes}:{seconds:02d}\n"
                result += f"   - Date: {entry.get('start_date_local', 'N/A')}\n"
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener clasificación: {e}")


class GetAthleteClubsTool(Tool[EmptyInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener clubes del atleta."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetAthleteClubs"
        self._description = """Obtiene los clubes a los que pertenece el atleta autenticado.
No requiere parámetros.

Devuelve: lista de clubes con información básica."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return EmptyInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: EmptyInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/athlete/clubs",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            clubs = response.json()
            
            if not clubs:
                return StringToolOutput("No perteneces a ningún club.")
            
            result = f"Tus Clubes ({len(clubs)}):\n\n"
            
            for i, club in enumerate(clubs, 1):
                result += f"{i}. {club.get('name', 'Unnamed')}\n"
                result += f"   - ID: {club.get('id')}\n"
                result += f"   - Type: {club.get('sport_type', 'N/A')}\n"
                result += f"   - City: {club.get('city', 'N/A')}, {club.get('country', 'N/A')}\n"
                result += f"   - Miembros: {club.get('member_count', 0)}\n"
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener clubes: {e}")


class GetClubByIdTool(Tool[GetClubByIdInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener detalles de un club."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetClubById"
        self._description = """Obtiene detalles completos de un club específico.
Parameters:
- club_id: ID del club

Devuelve: información detallada del club."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetClubByIdInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetClubByIdInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/clubs/{input.club_id}",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            club = response.json()
            
            result = f"""Detalles del Club:
- Name: {club.get('name', 'Unnamed')}
- ID: {club.get('id')}
- Tipo de deporte: {club.get('sport_type', 'N/A')}
- Description: {club.get('description', 'No description')}
- City: {club.get('city', 'N/A')}
- País: {club.get('country', 'N/A')}
- Miembros: {club.get('member_count', 0)}
- Tipo de club: {club.get('club_type', 'N/A')}"""
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener club: {e}")


class GetClubActivitiesTool(Tool[GetClubActivitiesInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener actividades de un club."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetClubActivities"
        self._description = """Obtiene las actividades recientes de los miembros de un club.
Parameters:
- club_id: ID del club
- per_page: Número de actividades (1-200, default: 10)

Devuelve: lista de actividades del club."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetClubActivitiesInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetClubActivitiesInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/clubs/{input.club_id}/activities",
                headers=_auth.get_headers(),
                params={"per_page": input.per_page},
                timeout=10
            )
            response.raise_for_status()
            activities = response.json()
            
            if not activities:
                return StringToolOutput("No hay actividades recientes en el club.")
            
            result = f"Actividades del Club ({len(activities)}):\n\n"
            
            for i, activity in enumerate(activities, 1):
                distance_km = activity.get('distance', 0) / 1000
                result += f"{i}. {activity.get('name', 'Unnamed')}\n"
                result += f"   - Atleta: {activity.get('athlete', {}).get('firstname', 'N/A')} {activity.get('athlete', {}).get('lastname', '')}\n"
                result += f"   - Type: {activity.get('type', 'N/A')}\n"
                result += f"   - Distance: {distance_km:.2f} km\n"
                result += f"   - Date: {activity.get('start_date_local', 'N/A')}\n"
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener actividades del club: {e}")


class GetClubMembersTool(Tool[GetClubMembersInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener miembros de un club."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetClubMembers"
        self._description = """Obtiene la lista de miembros de un club.
Parameters:
- club_id: ID del club
- per_page: Número de miembros (1-200, default: 30)

Devuelve: lista de miembros del club."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetClubMembersInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetClubMembersInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/clubs/{input.club_id}/members",
                headers=_auth.get_headers(),
                params={"per_page": input.per_page},
                timeout=10
            )
            response.raise_for_status()
            members = response.json()
            
            if not members:
                return StringToolOutput("No se encontraron miembros.")
            
            result = f"Miembros del Club ({len(members)}):\n\n"
            
            for i, member in enumerate(members, 1):
                result += f"{i}. {member.get('firstname', 'N/A')} {member.get('lastname', '')}\n"
                result += f"   - Username: {member.get('username', 'N/A')}\n"
                result += f"   - City: {member.get('city', 'N/A')}, {member.get('country', 'N/A')}\n"
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener miembros: {e}")


class GetRouteByIdTool(Tool[GetRouteByIdInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener detalles de una ruta."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetRouteById"
        self._description = """Obtiene detalles completos de una ruta guardada.
Parameters:
- route_id: ID de la ruta

Devuelve: información detallada de la ruta."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetRouteByIdInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetRouteByIdInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/routes/{input.route_id}",
                headers=_auth.get_headers(),
                timeout=10
            )
            response.raise_for_status()
            route = response.json()
            
            result = f"""Detalles de la Ruta:
- Name: {route.get('name', 'Unnamed')}
- ID: {route.get('id')}
- Description: {route.get('description', 'No description')}
- Distance: {route.get('distance', 0)/1000:.2f} km
- Elevation gain: {route.get('elevation_gain', 0):.0f} m
- Type: {route.get('type', 'N/A')}
- Sub-tipo: {route.get('sub_type', 'N/A')}"""
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener ruta: {e}")


class GetAthleteRoutesTool(Tool[GetAthleteRoutesInput, ToolRunOptions, StringToolOutput]):
    """Herramienta para obtener rutas de un atleta."""
    
    def __init__(self):
        super().__init__()
        self._name = "GetAthleteRoutes"
        self._description = """Obtiene las rutas guardadas de un atleta.
Parameters:
- athlete_id: ID del atleta
- per_page: Número de rutas (1-200, default: 10)

Devuelve: lista de rutas del atleta."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return GetAthleteRoutesInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: GetAthleteRoutesInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool."""
        try:
            response = requests.get(
                f"{_auth.base_url}/athletes/{input.athlete_id}/routes",
                headers=_auth.get_headers(),
                params={"per_page": input.per_page},
                timeout=10
            )
            response.raise_for_status()
            routes = response.json()
            
            if not routes:
                return StringToolOutput("No se encontraron rutas.")
            
            result = f"Rutas del Atleta ({len(routes)}):\n\n"
            
            for i, route in enumerate(routes, 1):
                result += f"{i}. {route.get('name', 'Unnamed')}\n"
                result += f"   - ID: {route.get('id')}\n"
                result += f"   - Distance: {route.get('distance', 0)/1000:.2f} km\n"
                result += f"   - Elevación: {route.get('elevation_gain', 0):.0f} m\n"
                result += f"   - Type: {route.get('type', 'N/A')}\n"
                result += "\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error al obtener rutas: {e}")


class CompareRunningSessionsTool(Tool[CompareRunningSessionsInput, ToolRunOptions, StringToolOutput]):
    """Tool to compare running sessions and analyze performance improvements."""
    
    def __init__(self):
        super().__init__()
        self._name = "CompareRunningSessions"
        self._description = """Compares recent running sessions to analyze performance improvements.
Parameters:
- num_sessions: Number of recent running sessions to compare (2-30, default: 5)

Returns: Detailed comparison table with metrics like pace, distance, heart rate, and performance analysis showing if the athlete is improving."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return CompareRunningSessionsInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: CompareRunningSessionsInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool to compare running sessions."""
        try:
            num_sessions = input.num_sessions
            
            # Get recent activities
            response = requests.get(
                f"{_auth.base_url}/athlete/activities",
                headers=_auth.get_headers(),
                params={"per_page": 100},  # Get more to filter runs
                timeout=10
            )
            response.raise_for_status()
            activities = response.json()
            
            # Filter only running activities
            runs = [a for a in activities if a.get('type') == 'Run'][:num_sessions]
            
            if len(runs) < 2:
                return StringToolOutput(f"At least 2 running sessions are needed for comparison. Only {len(runs)} sessions found.")
            
            # Build comparison table
            result = f"## 🏃 Comparison of {len(runs)} Running Sessions\n\n"
            
            # Table header
            result += "| # | Date | Distance (km) | Time (min) | Pace (min/km) | Avg HR | Speed (km/h) |\n"
            result += "|---|------|---------------|------------|---------------|--------|---------------|\n"
            
            # Collect metrics for analysis
            paces = []
            distances = []
            heart_rates = []
            speeds = []
            
            # Table rows
            for i, run in enumerate(runs, 1):
                distance_km = run.get('distance', 0) / 1000
                time_min = run.get('moving_time', 0) / 60
                pace_min_km = (time_min / distance_km) if distance_km > 0 else 0
                avg_hr = run.get('average_heartrate', 0)
                speed_kmh = run.get('average_speed', 0) * 3.6
                date = run.get('start_date_local', 'N/A')[:10]
                
                # Store for analysis
                if pace_min_km > 0:
                    paces.append(pace_min_km)
                if distance_km > 0:
                    distances.append(distance_km)
                if avg_hr > 0:
                    heart_rates.append(avg_hr)
                if speed_kmh > 0:
                    speeds.append(speed_kmh)
                
                # Format pace as min:sec
                pace_minutes = int(pace_min_km)
                pace_seconds = int((pace_min_km - pace_minutes) * 60)
                pace_str = f"{pace_minutes}:{pace_seconds:02d}" if pace_min_km > 0 else "N/A"
                
                hr_str = f"{avg_hr:.0f}" if avg_hr > 0 else "N/A"
                
                result += f"| {i} | {date} | {distance_km:.2f} | {time_min:.0f} | {pace_str} | {hr_str} | {speed_kmh:.1f} |\n"
            
            # Performance Analysis
            result += "\n## 📊 Performance Analysis\n\n"
            
            if len(paces) >= 2:
                # Pace analysis (lower is better)
                recent_pace_avg = sum(paces[:3]) / min(3, len(paces))
                older_pace_avg = sum(paces[-3:]) / min(3, len(paces[-3:]))
                pace_improvement = ((older_pace_avg - recent_pace_avg) / older_pace_avg) * 100
                
                result += f"### 🏃 Pace\n"
                result += f"- **Average last 3 sessions**: {recent_pace_avg:.2f} min/km\n"
                result += f"- **Average previous sessions**: {older_pace_avg:.2f} min/km\n"
                
                if pace_improvement > 2:
                    result += f"- **✅ IMPROVEMENT**: Your pace improved by {pace_improvement:.1f}% 🎉\n"
                elif pace_improvement < -2:
                    result += f"- **⚠️ DECLINE**: Your pace decreased by {abs(pace_improvement):.1f}%\n"
                else:
                    result += f"- **➡️ STABLE**: Your pace remains stable (change: {pace_improvement:.1f}%)\n"
                result += "\n"
            
            if len(distances) >= 2:
                # Distance analysis
                recent_dist_avg = sum(distances[:3]) / min(3, len(distances))
                older_dist_avg = sum(distances[-3:]) / min(3, len(distances[-3:]))
                dist_change = ((recent_dist_avg - older_dist_avg) / older_dist_avg) * 100
                
                result += f"### 📏 Distance\n"
                result += f"- **Average last 3 sessions**: {recent_dist_avg:.2f} km\n"
                result += f"- **Average previous sessions**: {older_dist_avg:.2f} km\n"
                
                if dist_change > 5:
                    result += f"- **✅ INCREASE**: You're running {dist_change:.1f}% more distance 💪\n"
                elif dist_change < -5:
                    result += f"- **⚠️ REDUCTION**: Distance decreased by {abs(dist_change):.1f}%\n"
                else:
                    result += f"- **➡️ STABLE**: Distance remains stable (change: {dist_change:.1f}%)\n"
                result += "\n"
            
            if len(heart_rates) >= 2:
                # Heart rate analysis (lower at same pace is better)
                recent_hr_avg = sum(heart_rates[:3]) / min(3, len(heart_rates))
                older_hr_avg = sum(heart_rates[-3:]) / min(3, len(heart_rates[-3:]))
                hr_change = ((recent_hr_avg - older_hr_avg) / older_hr_avg) * 100
                
                result += f"### ❤️ Heart Rate\n"
                result += f"- **Average last 3 sessions**: {recent_hr_avg:.0f} bpm\n"
                result += f"- **Average previous sessions**: {older_hr_avg:.0f} bpm\n"
                
                if hr_change < -2:
                    result += f"- **✅ IMPROVEMENT**: Your HR decreased by {abs(hr_change):.1f}% (better cardiovascular efficiency) 🫀\n"
                elif hr_change > 2:
                    result += f"- **⚠️ INCREASE**: Your HR increased by {hr_change:.1f}% (possible fatigue or higher effort)\n"
                else:
                    result += f"- **➡️ STABLE**: Your HR remains stable (change: {hr_change:.1f}%)\n"
                result += "\n"
            
            # Overall assessment
            result += "## 🎯 Overall Assessment\n\n"
            
            improvements = 0
            if len(paces) >= 2 and pace_improvement > 2:
                improvements += 1
            if len(distances) >= 2 and dist_change > 5:
                improvements += 1
            if len(heart_rates) >= 2 and hr_change < -2:
                improvements += 1
            
            if improvements >= 2:
                result += "**🌟 EXCELLENT**: Your performance is improving significantly. Keep it up!\n"
            elif improvements == 1:
                result += "**👍 GOOD**: You show improvements in some aspects. Continue working consistently.\n"
            else:
                result += "**💪 STAY CONSISTENT**: Keep training consistently to see improvements.\n"
            
            result += "\n**Recommendation**: Compare similar sessions (same distance/type) for more accurate analysis.\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error comparing running sessions: {e}")

class CompareSpecificRunsTool(Tool[CompareSpecificRunsInput, ToolRunOptions, StringToolOutput]):
    """Tool to compare two specific running sessions by date."""
    
    def __init__(self):
        super().__init__()
        self._name = "CompareSpecificRuns"
        self._description = """Compares two specific running sessions by their dates.
Parameters:
- date1: First date in format YYYY-MM-DD (e.g., 2026-01-18)
- date2: Second date in format YYYY-MM-DD (e.g., 2026-02-01)

Returns: Detailed comparison between the two specific sessions showing improvements or changes in pace, distance, heart rate, and other metrics."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return CompareSpecificRunsInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: CompareSpecificRunsInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool to compare two specific running sessions."""
        try:
            date1 = input.date1
            date2 = input.date2
            
            # Get recent activities (enough to find the dates)
            response = requests.get(
                f"{_auth.base_url}/athlete/activities",
                headers=_auth.get_headers(),
                params={"per_page": 100},
                timeout=10
            )
            response.raise_for_status()
            activities = response.json()
            
            # Filter only running activities
            runs = [a for a in activities if a.get('type') == 'Run']
            
            # Find activities by date
            run1 = None
            run2 = None
            
            for run in runs:
                run_date = run.get('start_date_local', '')[:10]
                if run_date == date1:
                    run1 = run
                if run_date == date2:
                    run2 = run
            
            if not run1:
                return StringToolOutput(f"No running session found on {date1}")
            
            if not run2:
                return StringToolOutput(f"No running session found on {date2}")
            
            # Build comparison
            result = f"## 🏃 Specific Sessions Comparison\n\n"
            result += f"**Session 1**: {date1}\n"
            result += f"**Session 2**: {date2}\n\n"
            
            # Extract metrics for both runs
            def extract_metrics(run):
                distance_km = run.get('distance', 0) / 1000
                time_min = run.get('moving_time', 0) / 60
                pace_min_km = (time_min / distance_km) if distance_km > 0 else 0
                avg_hr = run.get('average_heartrate', 0)
                max_hr = run.get('max_heartrate', 0)
                speed_kmh = run.get('average_speed', 0) * 3.6
                elevation = run.get('total_elevation_gain', 0)
                calories = run.get('calories', 0)
                
                return {
                    'name': run.get('name', 'Sin nombre'),
                    'distance_km': distance_km,
                    'time_min': time_min,
                    'pace_min_km': pace_min_km,
                    'avg_hr': avg_hr,
                    'max_hr': max_hr,
                    'speed_kmh': speed_kmh,
                    'elevation': elevation,
                    'calories': calories
                }
            
            metrics1 = extract_metrics(run1)
            metrics2 = extract_metrics(run2)
            
            # Comparison table
            result += "### 📊 Comparison Table\n\n"
            result += "| Metric | Session 1 ({}) | Session 2 ({}) | Change |\n".format(date1, date2)
            result += "|--------|----------------|----------------|--------|\n"
            
            # Distance
            dist_change = ((metrics2['distance_km'] - metrics1['distance_km']) / metrics1['distance_km'] * 100) if metrics1['distance_km'] > 0 else 0
            dist_indicator = "✅" if dist_change > 0 else "⚠️" if dist_change < 0 else "➡️"
            result += f"| **Distance** | {metrics1['distance_km']:.2f} km | {metrics2['distance_km']:.2f} km | {dist_indicator} {dist_change:+.1f}% |\n"
            
            # Time
            time_change = ((metrics2['time_min'] - metrics1['time_min']) / metrics1['time_min'] * 100) if metrics1['time_min'] > 0 else 0
            result += f"| **Time** | {metrics1['time_min']:.0f} min | {metrics2['time_min']:.0f} min | {time_change:+.1f}% |\n"
            
            # Pace (lower is better)
            if metrics1['pace_min_km'] > 0 and metrics2['pace_min_km'] > 0:
                pace_change = ((metrics1['pace_min_km'] - metrics2['pace_min_km']) / metrics1['pace_min_km'] * 100)
                pace_indicator = "✅" if pace_change > 0 else "⚠️" if pace_change < 0 else "➡️"
                pace1_min = int(metrics1['pace_min_km'])
                pace1_sec = int((metrics1['pace_min_km'] - pace1_min) * 60)
                pace2_min = int(metrics2['pace_min_km'])
                pace2_sec = int((metrics2['pace_min_km'] - pace2_min) * 60)
                result += f"| **Pace** | {pace1_min}:{pace1_sec:02d} min/km | {pace2_min}:{pace2_sec:02d} min/km | {pace_indicator} {pace_change:+.1f}% |\n"
            
            # Speed
            speed_change = ((metrics2['speed_kmh'] - metrics1['speed_kmh']) / metrics1['speed_kmh'] * 100) if metrics1['speed_kmh'] > 0 else 0
            speed_indicator = "✅" if speed_change > 0 else "⚠️" if speed_change < 0 else "➡️"
            result += f"| **Speed** | {metrics1['speed_kmh']:.1f} km/h | {metrics2['speed_kmh']:.1f} km/h | {speed_indicator} {speed_change:+.1f}% |\n"
            
            # Heart Rate
            if metrics1['avg_hr'] > 0 and metrics2['avg_hr'] > 0:
                hr_change = ((metrics2['avg_hr'] - metrics1['avg_hr']) / metrics1['avg_hr'] * 100)
                hr_indicator = "✅" if hr_change < 0 else "⚠️" if hr_change > 0 else "➡️"
                result += f"| **Avg HR** | {metrics1['avg_hr']:.0f} bpm | {metrics2['avg_hr']:.0f} bpm | {hr_indicator} {hr_change:+.1f}% |\n"
            
            if metrics1['max_hr'] > 0 and metrics2['max_hr'] > 0:
                result += f"| **Max HR** | {metrics1['max_hr']:.0f} bpm | {metrics2['max_hr']:.0f} bpm | {((metrics2['max_hr'] - metrics1['max_hr']) / metrics1['max_hr'] * 100):+.1f}% |\n"
            
            # Elevation
            if metrics1['elevation'] > 0 or metrics2['elevation'] > 0:
                elev_change = ((metrics2['elevation'] - metrics1['elevation']) / metrics1['elevation'] * 100) if metrics1['elevation'] > 0 else 0
                result += f"| **Elevation** | {metrics1['elevation']:.0f} m | {metrics2['elevation']:.0f} m | {elev_change:+.1f}% |\n"
            
            # Calories
            if metrics1['calories'] > 0 or metrics2['calories'] > 0:
                result += f"| **Calories** | {metrics1['calories']:.0f} | {metrics2['calories']:.0f} | - |\n"
            
            result += "\n"
            
            # Detailed Analysis
            result += "### 📈 Detailed Analysis\n\n"
            
            improvements = 0
            
            # Pace analysis
            if metrics1['pace_min_km'] > 0 and metrics2['pace_min_km'] > 0:
                result += "**🏃 Pace**\n"
                if pace_change > 2:
                    result += f"- ✅ **IMPROVEMENT**: Your pace improved by {pace_change:.1f}% (ran faster)\n"
                    improvements += 1
                elif pace_change < -2:
                    result += f"- ⚠️ **DECLINE**: Your pace decreased by {abs(pace_change):.1f}% (ran slower)\n"
                else:
                    result += f"- ➡️ **STABLE**: Your pace remained similar (change: {pace_change:.1f}%)\n"
                result += "\n"
            
            # Distance analysis
            result += "**📏 Distance**\n"
            if dist_change > 5:
                result += f"- ✅ **INCREASE**: You ran {dist_change:.1f}% more distance\n"
                improvements += 1
            elif dist_change < -5:
                result += f"- ⚠️ **REDUCTION**: You ran {abs(dist_change):.1f}% less distance\n"
            else:
                result += f"- ➡️ **SIMILAR**: Distance was similar (change: {dist_change:.1f}%)\n"
            result += "\n"
            
            # Heart rate analysis
            if metrics1['avg_hr'] > 0 and metrics2['avg_hr'] > 0:
                result += "**❤️ Heart Rate**\n"
                if hr_change < -2:
                    result += f"- ✅ **IMPROVEMENT**: Your avg HR decreased by {abs(hr_change):.1f}% (better efficiency)\n"
                    improvements += 1
                elif hr_change > 2:
                    result += f"- ⚠️ **INCREASE**: Your avg HR increased by {hr_change:.1f}% (higher effort or fatigue)\n"
                else:
                    result += f"- ➡️ **STABLE**: Your HR remained similar (change: {hr_change:.1f}%)\n"
                result += "\n"
            
            # Overall assessment
            result += "### 🎯 Overall Assessment\n\n"
            
            if improvements >= 2:
                result += "**🌟 EXCELLENT**: You showed significant improvements between these two sessions. Keep it up!\n"
            elif improvements == 1:
                result += "**👍 PROGRESS**: There are improvements in some aspects. Continue working consistently.\n"
            else:
                result += "**💪 CONTINUE**: Maintain consistency in your training to see improvements.\n"
            
            # Context notes
            result += "\n**📝 Notes**:\n"
            result += f"- Session 1: {metrics1['name']}\n"
            result += f"- Session 2: {metrics2['name']}\n"
            
            if abs(metrics2['distance_km'] - metrics1['distance_km']) > 2:
                result += "\n⚠️ Distances are significantly different, which may affect comparison of other metrics.\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error comparing specific sessions: {e}")




# ==================== CREAR HERRAMIENTAS ====================

class RecommendTrainingTool(Tool[RecommendTrainingInput, ToolRunOptions, StringToolOutput]):
    """Tool to recommend personalized training based on performance analysis."""
    
    def __init__(self):
        super().__init__()
        self._name = "RecommendTraining"
        self._description = """Analyzes recent running performance and recommends personalized training workouts.
Parameters:
- num_sessions: Number of recent sessions to analyze (5-30, default: 10)
- goal: Training goal - 'improve_performance', 'increase_distance', 'improve_pace', 'build_endurance'

Returns: Personalized training recommendations with specific workouts, intensity zones, and weekly plan based on current performance level."""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def input_schema(self):
        return RecommendTrainingInput
    
    def _create_emitter(self) -> Emitter:
        return Emitter()
    
    async def _run(self, input: RecommendTrainingInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Executes the tool to recommend training."""
        try:
            num_sessions = input.num_sessions
            goal = input.goal
            
            # Get recent activities
            response = requests.get(
                f"{_auth.base_url}/athlete/activities",
                headers=_auth.get_headers(),
                params={"per_page": 100},
                timeout=10
            )
            response.raise_for_status()
            activities = response.json()
            
            # Filter only running activities
            runs = [a for a in activities if a.get('type') == 'Run'][:num_sessions]
            
            if len(runs) < 5:
                return StringToolOutput(f"At least 5 running sessions are needed to generate recommendations. Only {len(runs)} sessions found.")
            
            # Analyze current performance
            total_distance = 0
            total_time = 0
            paces = []
            distances = []
            heart_rates = []
            weekly_frequency = {}
            
            for run in runs:
                distance_km = run.get('distance', 0) / 1000
                time_min = run.get('moving_time', 0) / 60
                pace_min_km = (time_min / distance_km) if distance_km > 0 else 0
                avg_hr = run.get('average_heartrate', 0)
                date = run.get('start_date_local', '')[:10]
                week = date[:7]  # YYYY-MM format
                
                total_distance += distance_km
                total_time += time_min
                
                if pace_min_km > 0:
                    paces.append(pace_min_km)
                if distance_km > 0:
                    distances.append(distance_km)
                if avg_hr > 0:
                    heart_rates.append(avg_hr)
                
                weekly_frequency[week] = weekly_frequency.get(week, 0) + 1
            
            # Calculate averages
            avg_distance = total_distance / len(runs)
            avg_pace = sum(paces) / len(paces) if paces else 0
            avg_hr = sum(heart_rates) / len(heart_rates) if heart_rates else 0
            avg_weekly_runs = sum(weekly_frequency.values()) / len(weekly_frequency) if weekly_frequency else 0
            max_distance = max(distances) if distances else 0
            
            # Build recommendations
            result = f"## 🎯 Personalized Training Plan\n\n"
            result += f"**Analysis based on**: {len(runs)} recent sessions\n"
            result += f"**Goal**: {self._translate_goal(goal)}\n\n"
            
            # Current performance summary
            result += "### 📊 Your Current Performance\n\n"
            result += f"- **Average distance**: {avg_distance:.2f} km\n"
            result += f"- **Maximum distance**: {max_distance:.2f} km\n"
            
            if avg_pace > 0:
                pace_min = int(avg_pace)
                pace_sec = int((avg_pace - pace_min) * 60)
                result += f"- **Average pace**: {pace_min}:{pace_sec:02d} min/km\n"
            
            if avg_hr > 0:
                result += f"- **Average HR**: {avg_hr:.0f} bpm\n"
            
            result += f"- **Weekly frequency**: {avg_weekly_runs:.1f} runs/week\n\n"
            
            # Determine training level
            if avg_weekly_runs < 2:
                level = "beginner"
            elif avg_weekly_runs < 4:
                level = "intermediate"
            else:
                level = "advanced"
            
            result += f"**Identified level**: {level.upper()}\n\n"
            
            # Goal-specific recommendations
            result += "### 🏃 Weekly Training Plan\n\n"
            
            if goal == "improve_pace":
                result += self._recommend_pace_improvement(avg_distance, avg_pace, level)
            elif goal == "increase_distance":
                result += self._recommend_distance_increase(avg_distance, max_distance, level)
            elif goal == "build_endurance":
                result += self._recommend_endurance(avg_distance, avg_weekly_runs, level)
            else:  # improve_performance (default)
                result += self._recommend_general_improvement(avg_distance, avg_pace, avg_weekly_runs, level)
            
            # Training zones
            if avg_hr > 0:
                result += "\n### ❤️ Recommended Training Zones\n\n"
                result += self._calculate_training_zones(avg_hr)
            
            # Additional tips
            result += "\n### 💡 Additional Tips\n\n"
            result += "1. **Rest**: Include at least 1-2 complete rest days per week\n"
            result += "2. **Progression**: Increase volume or intensity maximum 10% per week\n"
            result += "3. **Variety**: Alternate between different types of workouts\n"
            result += "4. **Listen to your body**: Adjust the plan if you feel excessive fatigue\n"
            result += "5. **Nutrition and hydration**: Essential for recovery\n"
            
            result += "\n### 📅 Next Steps\n\n"
            result += "1. Start with week 1 of the plan\n"
            result += "2. Log all your sessions in Strava\n"
            result += "3. Evaluate your progress every 2-3 weeks\n"
            result += "4. Adjust the plan according to your results\n"
            
            result += "\n**Good luck with your training! 💪🏃‍♂️**\n"
            
            return StringToolOutput(result)
            
        except Exception as e:
            return StringToolOutput(f"Error generating training recommendations: {e}")
    
    def _translate_goal(self, goal: str) -> str:
        """Translate goal to English."""
        goals = {
            "improve_performance": "Improve overall performance",
            "increase_distance": "Increase distance",
            "improve_pace": "Improve pace/speed",
            "build_endurance": "Build endurance"
        }
        return goals.get(goal, "Improve overall performance")
    
    def _recommend_pace_improvement(self, avg_dist: float, avg_pace: float, level: str) -> str:
        """Recommend workouts for pace improvement."""
        result = "**Focus**: Speed and interval training\n\n"
        
        if level == "beginner":
            result += "**Typical week** (3-4 days):\n\n"
            result += "1. **Monday**: Easy run - 3-4 km at comfortable pace\n"
            result += "2. **Wednesday**: Short intervals - 6x400m fast with 2 min recovery\n"
            result += "3. **Friday**: Tempo run - 2 km at moderate-hard pace\n"
            result += "4. **Sunday**: Long run - 5-7 km at easy pace\n"
        elif level == "intermediate":
            result += "**Typical week** (4-5 days):\n\n"
            result += "1. **Monday**: Easy run - 5-6 km\n"
            result += "2. **Tuesday**: Intervals - 8x400m or 5x800m at 5K pace\n"
            result += "3. **Thursday**: Tempo run - 4-5 km at 10K pace\n"
            result += "4. **Saturday**: Fartlek - 6-8 km with pace changes\n"
            result += "5. **Sunday**: Long run - 10-12 km at easy pace\n"
        else:  # advanced
            result += "**Typical week** (5-6 days):\n\n"
            result += "1. **Monday**: Easy run - 8 km\n"
            result += "2. **Tuesday**: Long intervals - 5x1000m at 5K pace\n"
            result += "3. **Wednesday**: Easy run - 6 km\n"
            result += "4. **Thursday**: Tempo run - 6-8 km at threshold pace\n"
            result += "5. **Saturday**: Short intervals - 12x400m at 3K pace\n"
            result += "6. **Sunday**: Long run - 15-18 km at easy pace\n"
        
        return result
    
    def _recommend_distance_increase(self, avg_dist: float, max_dist: float, level: str) -> str:
        """Recommend workouts for distance increase."""
        result = "**Focus**: Gradual volume increase\n\n"
        
        target_long_run = max_dist * 1.2  # 20% increase
        
        if level == "beginner":
            result += "**Typical week** (3-4 days):\n\n"
            result += "1. **Tuesday**: Short run - 3-4 km at comfortable pace\n"
            result += "2. **Thursday**: Medium run - 5-6 km at easy pace\n"
            result += "3. **Saturday**: Short run - 3-4 km at comfortable pace\n"
            result += f"4. **Sunday**: Long run - {target_long_run:.1f} km at very easy pace\n"
        elif level == "intermediate":
            result += "**Typical week** (4-5 days):\n\n"
            result += "1. **Monday**: Easy run - 6 km\n"
            result += "2. **Wednesday**: Medium run - 8-10 km at moderate pace\n"
            result += "3. **Friday**: Easy run - 6 km\n"
            result += "4. **Saturday**: Medium run - 8 km\n"
            result += f"5. **Sunday**: Long run - {target_long_run:.1f} km at easy pace\n"
        else:  # advanced
            result += "**Typical week** (5-6 days):\n\n"
            result += "1. **Monday**: Easy run - 10 km\n"
            result += "2. **Tuesday**: Medium run - 12 km at moderate pace\n"
            result += "3. **Wednesday**: Easy run - 8 km\n"
            result += "4. **Thursday**: Medium run - 10 km\n"
            result += "5. **Saturday**: Medium run - 12 km\n"
            result += f"6. **Sunday**: Long run - {target_long_run:.1f} km at easy pace\n"
        
        result += f"\n**Goal**: Reach {target_long_run:.1f} km in your long run within 4-6 weeks\n"
        
        return result
    
    def _recommend_endurance(self, avg_dist: float, weekly_freq: float, level: str) -> str:
        """Recommend workouts for endurance building."""
        result = "**Focus**: Building aerobic base\n\n"
        
        if level == "beginner":
            result += "**Typical week** (3-4 days):\n\n"
            result += "1. **Tuesday**: Easy run - 4 km (zone 2)\n"
            result += "2. **Thursday**: Easy run - 5 km (zone 2)\n"
            result += "3. **Saturday**: Easy run - 4 km (zone 2)\n"
            result += "4. **Sunday**: Long run - 7-8 km (zone 1-2)\n"
        elif level == "intermediate":
            result += "**Typical week** (4-5 days):\n\n"
            result += "1. **Monday**: Easy run - 6 km (zone 2)\n"
            result += "2. **Wednesday**: Medium run - 8 km (zone 2-3)\n"
            result += "3. **Friday**: Easy run - 6 km (zone 2)\n"
            result += "4. **Saturday**: Medium run - 8 km (zone 2)\n"
            result += "5. **Sunday**: Long run - 12-15 km (zone 2)\n"
        else:  # advanced
            result += "**Typical week** (5-6 days):\n\n"
            result += "1. **Monday**: Easy run - 10 km (zone 2)\n"
            result += "2. **Tuesday**: Medium run - 12 km (zone 2-3)\n"
            result += "3. **Wednesday**: Easy run - 8 km (zone 2)\n"
            result += "4. **Thursday**: Medium run - 10 km (zone 2-3)\n"
            result += "5. **Saturday**: Medium run - 12 km (zone 2)\n"
            result += "6. **Sunday**: Long run - 18-22 km (zone 2)\n"
        
        result += "\n**Key**: 80% of volume in zone 2 (conversational)\n"
        
        return result
    
    def _recommend_general_improvement(self, avg_dist: float, avg_pace: float, weekly_freq: float, level: str) -> str:
        """Recommend balanced training for general improvement."""
        result = "**Focus**: Balanced training (speed + endurance)\n\n"
        
        if level == "beginner":
            result += "**Typical week** (3-4 days):\n\n"
            result += "1. **Tuesday**: Easy run - 4 km\n"
            result += "2. **Thursday**: Easy intervals - 4x2 min fast with 2 min recovery\n"
            result += "3. **Saturday**: Easy run - 5 km\n"
            result += "4. **Sunday**: Long run - 7-8 km at easy pace\n"
        elif level == "intermediate":
            result += "**Typical week** (4-5 days):\n\n"
            result += "1. **Monday**: Easy run - 6 km\n"
            result += "2. **Wednesday**: Intervals - 6x800m at 5K pace\n"
            result += "3. **Friday**: Tempo run - 5 km at 10K pace\n"
            result += "4. **Saturday**: Easy run - 6 km\n"
            result += "5. **Sunday**: Long run - 12-14 km at easy pace\n"
        else:  # advanced
            result += "**Typical week** (5-6 days):\n\n"
            result += "1. **Monday**: Easy run - 10 km\n"
            result += "2. **Tuesday**: Intervals - 8x1000m at 5K pace\n"
            result += "3. **Wednesday**: Easy run - 8 km\n"
            result += "4. **Thursday**: Tempo run - 8 km at threshold pace\n"
            result += "5. **Saturday**: Fartlek - 10 km with pace changes\n"
            result += "6. **Sunday**: Long run - 18-20 km at easy pace\n"
        
        return result
    
    def _calculate_training_zones(self, avg_hr: float) -> str:
        """Calculate training zones based on average HR."""
        # Estimate max HR (220 - age approximation, using avg HR as reference)
        estimated_max_hr = avg_hr * 1.15  # Rough estimate
        
        result = "Based on your average HR, your approximate zones are:\n\n"
        result += f"- **Zone 1 (Recovery)**: {estimated_max_hr * 0.50:.0f}-{estimated_max_hr * 0.60:.0f} bpm - Very easy\n"
        result += f"- **Zone 2 (Aerobic)**: {estimated_max_hr * 0.60:.0f}-{estimated_max_hr * 0.70:.0f} bpm - Conversational\n"
        result += f"- **Zone 3 (Tempo)**: {estimated_max_hr * 0.70:.0f}-{estimated_max_hr * 0.80:.0f} bpm - Moderate-hard\n"
        result += f"- **Zone 4 (Threshold)**: {estimated_max_hr * 0.80:.0f}-{estimated_max_hr * 0.90:.0f} bpm - Hard\n"
        result += f"- **Zone 5 (VO2 Max)**: {estimated_max_hr * 0.90:.0f}-{estimated_max_hr * 1.00:.0f} bpm - Maximum\n"
        
        result += "\n*Note: These are estimates. For precise zones, perform a stress test.*\n"
        
        return result


def create_strava_tools():
    """Crea todas las herramientas de Strava para BeeAI."""
    return [
        # Perfil y estadísticas
        GetAthleteProfileTool(),
        GetAthleteStatsTool(),
        
        # Actividades
        GetActivitiesTool(),
        GetActivityByIdTool(),
        GetActivityZonesTool(),
        GetActivityLapsTool(),
        GetActivityStreamsTool(),
        
        # Análisis y comparación
        CompareRunningSessionsTool(),
        CompareSpecificRunsTool(),
        RecommendTrainingTool(),
        
        # Segmentos
        ExploreSegmentsTool(),
        GetSegmentByIdTool(),
        GetSegmentLeaderboardTool(),
        
        # Clubes
        GetAthleteClubsTool(),
        GetClubByIdTool(),
        GetClubActivitiesTool(),
        GetClubMembersTool(),
        
        # Rutas
        GetRouteByIdTool(),
        GetAthleteRoutesTool(),
    ]


# Made with Bob