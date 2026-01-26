"""
Visual Formatter for Strava Agent
Formats responses with images and visual resources for AgentStack UI
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class StravaVisualFormatter:
    """Formats Strava data with visual resources for UI display."""
    
    def __init__(self):
        # Google Maps API key (optional, for map rendering)
        self.google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        # Mapbox token (alternative to Google Maps)
        self.mapbox_token = os.getenv("MAPBOX_ACCESS_TOKEN", "")
    
    def format_profile_with_photo(self, profile: Dict[str, Any]) -> str:
        """Format athlete profile without photo (privacy setting)."""
        # Note: Photo display disabled for privacy
        
        response = f"""## 👤 Your Strava Profile

"""
        
        # Photo display disabled for privacy
        # photo_url = profile.get('profile', '')
        # if photo_url:
        #     response += f"![Profile Photo]({photo_url})\n\n"
        
        response += f"""**Name:** {profile.get('firstname', '')} {profile.get('lastname', '')}
**Username:** @{profile.get('username', 'N/A')}
**Location:** {profile.get('city', 'N/A')}, {profile.get('country', 'N/A')}
"""
        
        if profile.get('weight'):
            response += f"**Weight:** {profile.get('weight')} kg\n"
        
        response += f"""
**Friends:** {profile.get('friend_count', 0)}
**Followers:** {profile.get('follower_count', 0)}
"""
        
        return response
    
    def format_activity_with_map(self, activity: Dict[str, Any]) -> str:
        """Format activity with route map."""
        response = f"""## 🏃 {activity.get('name', 'Activity')}

"""
        
        # Add map if polyline is available
        map_data = activity.get('map', {})
        polyline = map_data.get('polyline', '')
        
        if polyline:
            map_url = self._generate_map_url(polyline)
            if map_url:
                response += f"![Route Map]({map_url})\n\n"
        
        # Activity metrics
        distance_km = activity.get('distance', 0) / 1000
        moving_time_min = activity.get('moving_time', 0) / 60
        elevation = activity.get('total_elevation_gain', 0)
        
        response += f"""### 📊 Main Metrics
- **Type:** {activity.get('type', 'N/A')}
- **Distance:** {distance_km:.2f} km
- **Time:** {moving_time_min:.0f} min ({moving_time_min/60:.1f} hours)
- **Elevation Gain:** {elevation:.0f} m
"""
        
        # Speed/Pace
        avg_speed = activity.get('average_speed', 0)
        if avg_speed > 0:
            speed_kmh = avg_speed * 3.6
            response += f"- **Average Speed:** {speed_kmh:.1f} km/h\n"
            
            # Add pace for running
            if activity.get('type') == 'Run':
                pace_min_km = 60 / speed_kmh if speed_kmh > 0 else 0
                pace_min = int(pace_min_km)
                pace_sec = int((pace_min_km - pace_min) * 60)
                response += f"- **Average Pace:** {pace_min}:{pace_sec:02d} min/km\n"
        
        # Heart rate
        if activity.get('average_heartrate'):
            response += f"- **Average HR:** {activity.get('average_heartrate'):.0f} bpm\n"
        if activity.get('max_heartrate'):
            response += f"- **Max HR:** {activity.get('max_heartrate'):.0f} bpm\n"
        
        # Power (cycling)
        if activity.get('average_watts'):
            response += f"- **Average Power:** {activity.get('average_watts'):.0f} W\n"
        if activity.get('weighted_average_watts'):
            response += f"- **Normalized Power:** {activity.get('weighted_average_watts'):.0f} W\n"
        
        # Cadence
        if activity.get('average_cadence'):
            response += f"- **Average Cadence:** {activity.get('average_cadence'):.0f} rpm\n"
        
        # Calories
        if activity.get('calories'):
            response += f"- **Calories:** {activity.get('calories'):.0f} kcal\n"
        
        return response
    
    def format_club_with_photo(self, club: Dict[str, Any]) -> str:
        """Format club information with photos."""
        response = f"""## 🏆 {club.get('name', 'Club')}

"""
        
        # Add club profile photo
        profile_url = club.get('profile', '')
        if profile_url:
            response += f"![Club Logo]({profile_url})\n\n"
        
        # Add cover photo if available
        cover_url = club.get('cover_photo', '')
        if cover_url:
            response += f"![Club Cover]({cover_url})\n\n"
        
        response += f"""**Type:** {club.get('sport_type', 'N/A')}
**Location:** {club.get('city', 'N/A')}, {club.get('state', 'N/A')}, {club.get('country', 'N/A')}
**Members:** {club.get('member_count', 0)}
"""
        
        if club.get('description'):
            response += f"\n**Description:** {club.get('description')}\n"
        
        return response
    
    def format_segment_with_map(self, segment: Dict[str, Any]) -> str:
        """Format segment with map."""
        response = f"""## 🎯 {segment.get('name', 'Segment')}

"""
        
        # Add map if polyline is available
        map_data = segment.get('map', {})
        polyline = map_data.get('polyline', '')
        
        if polyline:
            map_url = self._generate_map_url(polyline)
            if map_url:
                response += f"![Segment Map]({map_url})\n\n"
        
        distance_km = segment.get('distance', 0) / 1000
        elevation = segment.get('total_elevation_gain', 0)
        avg_grade = segment.get('average_grade', 0)
        
        response += f"""### 📊 Segment Details
- **Distance:** {distance_km:.2f} km
- **Elevation Gain:** {elevation:.0f} m
- **Average Grade:** {avg_grade:.1f}%
- **Max Grade:** {segment.get('maximum_grade', 0):.1f}%
- **Activity Type:** {segment.get('activity_type', 'N/A')}
"""
        
        # Effort counts
        if segment.get('effort_count'):
            response += f"- **Total Efforts:** {segment.get('effort_count'):,}\n"
        if segment.get('athlete_count'):
            response += f"- **Athletes:** {segment.get('athlete_count'):,}\n"
        
        return response
    
    def _generate_map_url(self, polyline: str, size: str = "600x400") -> Optional[str]:
        """Generate static map URL from polyline."""
        if not polyline:
            return None
        
        # Try Google Maps first
        if self.google_maps_key:
            return (
                f"https://maps.googleapis.com/maps/api/staticmap"
                f"?size={size}"
                f"&path=enc:{polyline}"
                f"&key={self.google_maps_key}"
            )
        
        # Try Mapbox as alternative
        if self.mapbox_token:
            # Mapbox requires decoded coordinates, which is more complex
            # For now, return None if no Google Maps key
            return None
        
        # No map service available
        return None
    
    def format_activities_list(self, activities: list) -> str:
        """Format list of activities with thumbnails."""
        if not activities:
            return "No activities found."
        
        response = f"## 📊 Your Recent Activities ({len(activities)} activities)\n\n"
        
        for i, activity in enumerate(activities, 1):
            distance_km = activity.get('distance', 0) / 1000
            moving_time_min = activity.get('moving_time', 0) / 60
            
            response += f"""### {i}. {activity.get('name', 'Activity')}
- **Type:** {activity.get('type', 'N/A')} | **Distance:** {distance_km:.2f} km | **Time:** {moving_time_min:.0f} min
"""
            
            # Add small map thumbnail if available
            map_data = activity.get('map', {})
            summary_polyline = map_data.get('summary_polyline', '')
            if summary_polyline and (self.google_maps_key or self.mapbox_token):
                map_url = self._generate_map_url(summary_polyline, size="300x200")
                if map_url:
                    response += f"![Map]({map_url})\n"
            
            response += "\n"
        
        return response


# Global formatter instance
_formatter = StravaVisualFormatter()


def get_formatter() -> StravaVisualFormatter:
    """Get the global visual formatter instance."""
    return _formatter

# Made with Bob
