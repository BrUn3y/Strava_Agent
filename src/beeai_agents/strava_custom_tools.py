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
            
            # Add profile photo as Markdown image if available
            if data.get('profile'):
                result += f"![Profile Photo]({data.get('profile')})\n\n"
            elif data.get('profile_medium'):
                result += f"![Profile Photo]({data.get('profile_medium')})\n\n"
            
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
                result += f"   - ID: {activity.get('id')}\n"
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


# ==================== CREAR HERRAMIENTAS ====================

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