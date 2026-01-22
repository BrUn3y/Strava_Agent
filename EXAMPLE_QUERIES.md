# 📝 Example Queries for Strava Agent

Based on the available Strava API tools, here are useful example queries you can ask the agent:

## 🏃 Activities

### Basic Activity Queries
```
"Show me my last 10 activities"
"What were my activities from last week?"
"List my 5 most recent workouts"
"Show me all my activities from this month"
```

### Detailed Activity Analysis
```
"Give me complete details of activity 12345678"
"Analyze my most recent run in detail"
"Show me the splits and zones for my last cycling activity"
"What were the laps in my most recent activity?"
```

### Activity Comparisons
```
"Compare my last 3 runs and tell me if I'm improving"
"What's the difference between my fastest and slowest run this month?"
"Show me my progress in the last 10 cycling activities"
```

### Activity Data Streams
```
"Get the GPS and heart rate data from activity 12345678"
"Show me the power data from my last cycling workout"
"What was my heart rate throughout my most recent run?"
"Get altitude and speed data from my last activity"
```

## 👤 Profile & Statistics

### Profile Information
```
"What's my current profile?"
"Show me my athlete information"
"What are my FTP and weight settings?"
```

### Statistics
```
"What are my total running statistics?"
"Show me my cycling stats for this year"
"What are my statistics from the last 4 weeks?"
"What's my biggest ride distance?"
"What's my highest elevation gain?"
```

### Training Zones
```
"What are my heart rate zones?"
"Show me my power zones"
"What zones did I train in during my last activity?"
```

## 🗺️ Segments

### Segment Exploration
```
"Find cycling segments near coordinates 37.8,-122.4"
"Explore running segments in my area"
"What segments are available around [coordinates]?"
```

### Segment Details
```
"Give me details about segment 12345"
"What's the elevation profile of segment 67890?"
"Show me information about the Hawk Hill segment"
```

### Leaderboards
```
"Show me the leaderboard for segment 12345"
"Who has the fastest time on segment 67890?"
"What's my ranking on segment [id]?"
"Show me the top 20 times for this segment"
```

## 🚴 Routes

### Route Queries
```
"Show me my saved routes"
"List all my cycling routes"
"Give me details about route 12345"
"What routes do I have saved?"
```

### Route Analysis
```
"What's the elevation gain on route 67890?"
"Show me the distance and profile of my favorite route"
"Compare the difficulty of my saved routes"
```

## 👥 Clubs

### Club Information
```
"What clubs do I belong to?"
"Show me details about club 12345"
"List all my clubs"
```

### Club Activities
```
"What are the recent activities in my club?"
"Show me what my club members have been doing"
"List the last 20 activities from club 12345"
```

### Club Members
```
"Who are the members of club 12345?"
"Show me the most active members of my club"
"List all members of my cycling club"
```

## 🎯 Complex Analysis Queries

### Performance Analysis
```
"Analyze my running performance over the last month"
"Am I improving my cycling speed?"
"What's my average pace trend in the last 10 runs?"
"Compare my heart rate across my recent activities"
```

### Training Insights
```
"How much time have I spent in each heart rate zone this month?"
"What's my training volume for the last 4 weeks?"
"Show me my elevation gain trend"
"Am I training more or less than last month?"
```

### Goal Tracking
```
"How close am I to 100km of running this month?"
"What's my total distance this year?"
"How many activities have I completed this week?"
"Am I on track to reach my monthly distance goal?"
```

### Segment Hunting
```
"Find challenging climbing segments near my last ride"
"What are the most popular segments in my area?"
"Show me segments I haven't attempted yet"
```

## 💡 Tips for Better Queries

### Be Specific
- ✅ "Show me my last 5 cycling activities with heart rate data"
- ❌ "Show me stuff"

### Use Activity IDs
- ✅ "Get details for activity 12345678"
- ❌ "Show me that activity from yesterday"

### Combine Information
- ✅ "Compare my last 3 runs and show me if my pace is improving"
- ❌ "Show runs" (too vague)

### Request Specific Data
- ✅ "Get GPS, heart rate, and power streams from activity 12345678"
- ❌ "Get data" (unclear what data)

## 🔍 Advanced Query Examples

### Multi-Step Analysis
```
"First show me my profile, then get my last 5 activities, and analyze if I'm improving"
"Get my cycling statistics and compare them with my last month's performance"
"Show me my clubs, then get the recent activities from my main club"
```

### Contextual Queries
```
"Based on my recent activities, what segments should I try?"
"Looking at my statistics, am I training enough?"
"Considering my last 10 runs, what's my average pace?"
```

### Comparative Analysis
```
"Compare my performance on segment 12345 with the leaderboard"
"How do my statistics compare to last year?"
"What's the difference between my running and cycling volume?"
```

## 📊 Data Visualization Queries

While the agent returns text, you can ask for structured data:

```
"Give me a summary table of my last 10 activities"
"List my activities with distance, time, and pace in a structured format"
"Show me my monthly statistics organized by sport type"
```

## 🎓 Learning Queries

```
"Explain what my heart rate zones mean"
"What does FTP stand for and what's mine?"
"How is average pace calculated?"
"What's the difference between moving time and elapsed time?"
```

---

## 🚀 Getting Started

1. **Start Simple**: Begin with basic queries like "Show me my last 5 activities"
2. **Get IDs**: Use activity/segment/club IDs from initial queries for detailed analysis
3. **Build Complexity**: Combine multiple queries for deeper insights
4. **Experiment**: Try different phrasings to see what works best

## 📝 Note

The agent has access to 16 custom tools covering:
- ✅ Profile & Statistics (2 tools)
- ✅ Activities (5 tools)
- ✅ Segments (3 tools)
- ✅ Clubs (4 tools)
- ✅ Routes (2 tools)

All queries are processed through natural language, so feel free to ask in your own words!