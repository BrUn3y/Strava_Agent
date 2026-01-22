#!/usr/bin/env python3
"""
Demo script to showcase visual resources in Strava Agent
This script demonstrates how the agent displays maps, profile photos, and club logos
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def demo_visual_resources():
    """Display examples of visual resources available in Strava Agent"""
    
    print("=" * 80)
    print("🎨 STRAVA AGENT - VISUAL RESOURCES DEMO")
    print("=" * 80)
    print()
    
    # Check if Google Maps API key is configured
    google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if google_maps_key:
        print("✅ Google Maps API Key: Configured")
    else:
        print("❌ Google Maps API Key: NOT configured")
        print("   → Set GOOGLE_MAPS_API_KEY in .env file")
    
    print()
    print("-" * 80)
    print("📊 AVAILABLE VISUAL RESOURCES")
    print("-" * 80)
    print()
    
    # 1. Route Maps
    print("1️⃣  ROUTE MAPS 🗺️")
    print("   Description: Static maps showing activity routes")
    print("   Source: Google Maps Static API + Strava polylines")
    print("   Format: ![Route Map](https://maps.googleapis.com/...)")
    print("   Size: 600x400 pixels")
    print("   Example query: 'Muéstrame mi última actividad con el mapa'")
    print()
    
    # Example polyline (encoded GPS data)
    example_polyline = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
    if google_maps_key:
        example_map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=600x400&path=enc:{example_polyline}&key={google_maps_key}"
        print(f"   Example URL: {example_map_url[:80]}...")
    print()
    
    # 2. Profile Photos
    print("2️⃣  PROFILE PHOTOS 👤")
    print("   Description: Athlete profile pictures from Strava")
    print("   Source: Strava CDN (dgalywyr863hv.cloudfront.net)")
    print("   Format: ![Profile Photo](https://dgalywyr863hv.cloudfront.net/...)")
    print("   Example query: 'Muéstrame mi perfil de Strava'")
    print()
    
    # 3. Club Logos
    print("3️⃣  CLUB LOGOS 🏆")
    print("   Description: Logos of clubs the athlete belongs to")
    print("   Source: Strava CDN (dgalywyr863hv.cloudfront.net)")
    print("   Format: ![Club Logo](https://dgalywyr863hv.cloudfront.net/...)")
    print("   Example query: '¿A qué clubes pertenezco?'")
    print()
    
    print("-" * 80)
    print("💡 HOW IT WORKS")
    print("-" * 80)
    print()
    print("1. User asks a question (e.g., 'Show my last activity')")
    print("2. Agent calls Strava API to get activity data")
    print("3. Agent extracts polyline (GPS data) from activity")
    print("4. Agent generates Google Maps URL with polyline")
    print("5. Agent formats response with Markdown image syntax")
    print("6. AgentStack UI renders the image automatically")
    print()
    
    print("-" * 80)
    print("📝 EXAMPLE RESPONSES")
    print("-" * 80)
    print()
    
    # Example 1: Activity with map
    print("Example 1: Activity with Route Map")
    print("-" * 40)
    print("User: 'Muéstrame mi actividad más reciente'")
    print()
    print("Agent Response:")
    print("```markdown")
    print("🏃 **Morning Run**")
    print("📅 Date: 2024-01-15")
    print("⏱️ Duration: 45:23")
    print("📏 Distance: 8.5 km")
    print("⚡ Average Speed: 11.2 km/h")
    print()
    print("![Route Map](https://maps.googleapis.com/maps/api/staticmap?...)")
    print("```")
    print()
    
    # Example 2: Profile with photo
    print("Example 2: Profile with Photo")
    print("-" * 40)
    print("User: 'Muéstrame mi perfil completo'")
    print()
    print("Agent Response:")
    print("```markdown")
    print("👤 **John Doe**")
    print()
    print("![Profile Photo](https://dgalywyr863hv.cloudfront.net/pictures/athletes/12345/large.jpg)")
    print()
    print("📍 Location: San Francisco, CA")
    print("🏃 Activities: 156")
    print("👥 Followers: 234")
    print("```")
    print()
    
    # Example 3: Clubs with logos
    print("Example 3: Clubs with Logos")
    print("-" * 40)
    print("User: '¿A qué clubes pertenezco?'")
    print()
    print("Agent Response:")
    print("```markdown")
    print("🏆 **Your Clubs:**")
    print()
    print("1. **Running Club SF**")
    print("   ![Club Logo](https://dgalywyr863hv.cloudfront.net/pictures/clubs/67890/large.jpg)")
    print("   👥 Members: 450")
    print()
    print("2. **Bay Area Cyclists**")
    print("   ![Club Logo](https://dgalywyr863hv.cloudfront.net/pictures/clubs/12345/large.jpg)")
    print("   👥 Members: 320")
    print("```")
    print()
    
    print("-" * 80)
    print("⚠️  LIMITATIONS")
    print("-" * 80)
    print()
    print("• Indoor activities (treadmill, stationary bike) have NO maps")
    print("  → They don't have GPS data (empty polyline)")
    print()
    print("• Google Maps Static API has usage limits")
    print("  → Free tier: 25,000 map loads per day")
    print()
    print("• Strava API has rate limits")
    print("  → 100 requests per 15 minutes")
    print("  → 1,000 requests per day")
    print()
    
    print("-" * 80)
    print("🚀 NEXT STEPS")
    print("-" * 80)
    print()
    print("1. Open the AgentStack UI: http://localhost:8333")
    print("2. Select 'Strava Agent' from the menu")
    print("3. Try these queries:")
    print("   • 'Muéstrame mi última actividad'")
    print("   • 'Muéstrame mi perfil'")
    print("   • '¿A qué clubes pertenezco?'")
    print()
    print("4. See the images render automatically in the UI!")
    print()
    
    print("=" * 80)
    print("📚 For more information, see: VISUAL_RESOURCES_DEMO.md")
    print("=" * 80)
    print()

if __name__ == "__main__":
    demo_visual_resources()

# Made with Bob
