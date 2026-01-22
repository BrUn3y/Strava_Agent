# 🏃‍♂️ Complete Strava Agent with BeeAI, AgentStack & A2A 🚴‍♀️

## Introduction

The Strava Agent is an advanced conversational AI system designed to interact with the complete Strava API. Built on the BeeAI framework with the AgentStack SDK and A2A protocol support, this agent allows you to analyze your athletic performance, explore segments, manage routes, interact with clubs, and much more through natural conversations or programmatic API calls.

### 🆕 What's New in v0.2.0

- ✅ **A2A Protocol Support**: Full Agent-to-Agent communication protocol
- ✅ **AgentStack Server**: RESTful API endpoints for agent interaction
- ✅ **5 Agent Skills**: Organized capabilities for different use cases
- ✅ **Multi-Agent Ready**: Can be integrated with other A2A-compatible agents
- ✅ **Improved Documentation**: Comprehensive guides for all usage modes

## 🌟 Key Features

### 📊 Activity Analysis
- Query recent activities with advanced filters
- Get complete details of any activity
- Analyze laps/splits and training zones
- View kudos and activity comments
- Update activity information

### 👤 Profile Management
- Query complete athlete profile
- Update weight and other personal data
- View heart rate and power zones
- Get total and recent statistics

### 📈 Statistics and Analysis
- Total statistics by sport (cycling, running, swimming)
- Temporal progress analysis
- Performance comparison
- Personal records identification

### 🗺️ Segments and Routes
- Explore segments in geographic areas
- View leaderboards with advanced filters
- Query specific segment details
- Manage saved routes
- Get elevation and GPS data

### 👥 Clubs and Community
- View clubs you belong to
- Explore club activities
- Query club members
- Detailed club information

### 🚴 Equipment
- Manage bikes and shoes
- View total mileage per equipment
- Query equipment details

### 📡 Advanced Data (Streams)
- Point-by-point GPS data
- Detailed heart rate
- Power and cadence
- Speed and elevation
- Temperature and gradient

## 📋 Requirements

### Minimum Requirements

- **Python:** Version 3.11 or higher
- **Dependency Management:** `uv` to manage Python packages
- **Strava Credentials:** Client ID, Client Secret, and Refresh Token

### Python Dependencies

Project dependencies are managed with `uv` and defined in `pyproject.toml`:

```toml
dependencies = [
    "agentstack-sdk==0.4.0rc1",
    "beeai_framework>=0.1.68",
]
```

### Tools Used

The agent uses the following BeeAI tools:

- **Custom Tools:** Direct implementation of Strava API
- **ReActAgent:** Reasoning and action agent
- **UnconstrainedMemory:** Unrestricted memory for full context
- **WatsonxChatModel:** IBM Granite language model

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd strava_agent
```

### 2. Install Dependencies

Make sure you have `uv` installed. Then run:

```bash
uv sync
```

### 3. Configure Strava Credentials

Create a `.env` file in the project root with your credentials:

```env
# IBM Watsonx (or your LLM provider)
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29

# Strava API
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REFRESH_TOKEN=your_refresh_token
```

#### Get Strava Credentials

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application
3. Get your `Client ID` and `Client Secret`
4. Use the OAuth2 flow to get a `Refresh Token`:

```bash
# Run the helper script
uv run python get_strava_token.py
```

## 🎯 Usage

### Two Ways to Run the Agent

#### 1. Standalone Mode (Original)

Run the agent directly for testing and development:

```bash
uv run server
```

The agent will start and execute an example query. You can modify the query in `src/beeai_agents/agent.py`.

#### 2. A2A Server Mode (New! 🆕)

Run the agent as an A2A-compatible server:

```bash
uv run strava-server
```

The server will start on `http://127.0.0.1:8000` with the following endpoints:

- **A2A Endpoint**: `POST http://127.0.0.1:8000/a2a`
- **Health Check**: `GET http://127.0.0.1:8000/health`
- **Discovery**: `GET http://127.0.0.1:8000/a2a/discover`

**Quick Test:**
```bash
curl -X POST http://127.0.0.1:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{"message": {"role": "user", "content": "Show me my last 5 activities"}}'
```

📖 **For complete A2A documentation, see [A2A_USAGE.md](A2A_USAGE.md)**

## 📝 Example Queries

### 🏃 Activities

**Basic Queries:**
```
"Show me my last 10 activities"
"What were my activities from last week?"
"List my 5 most recent workouts"
```

**Detailed Analysis:**
```
"Give me complete details of activity 12345678"
"Analyze my most recent run in detail"
"Show me the splits and zones for my last cycling activity"
```

**Comparisons:**
```
"Compare my last 3 runs and tell me if I'm improving"
"What's the difference between my fastest and slowest run this month?"
```

**Data Streams:**
```
"Get the GPS and heart rate data from activity 12345678"
"Show me the power data from my last cycling workout"
"What was my heart rate throughout my most recent run?"
```

### 👤 Profile & Statistics

**Profile:**
```
"What's my current profile?"
"Show me my athlete information"
```

**Statistics:**
```
"What are my total running statistics?"
"Show me my cycling stats for this year"
"What's my biggest ride distance?"
```

**Training Zones:**
```
"What are my heart rate zones?"
"Show me my power zones"
"What zones did I train in during my last activity?"
```

### 🗺️ Segments

**Exploration:**
```
"Find cycling segments near coordinates 37.8,-122.4"
"Explore running segments in my area"
```

**Details:**
```
"Give me details about segment 12345"
"What's the elevation profile of segment 67890?"
```

**Leaderboards:**
```
"Show me the leaderboard for segment 12345"
"Who has the fastest time on segment 67890?"
"What's my ranking on this segment?"
```

### 🚴 Routes

```
"Show me my saved routes"
"List all my cycling routes"
"Give me details about route 12345"
"What's the elevation gain on route 67890?"
```

### 👥 Clubs

**Information:**
```
"What clubs do I belong to?"
"Show me details about club 12345"
```

**Activities:**
```
"What are the recent activities in my club?"
"Show me what my club members have been doing"
```

**Members:**
```
"Who are the members of club 12345?"
"Show me the most active members of my club"
```

### 🎯 Complex Analysis

**Performance:**
```
"Analyze my running performance over the last month"
"Am I improving my cycling speed?"
"Compare my heart rate across my recent activities"
```

**Training Insights:**
```
"How much time have I spent in each heart rate zone this month?"
"What's my training volume for the last 4 weeks?"
"Am I training more or less than last month?"
```

**Goal Tracking:**
```
"How close am I to 100km of running this month?"
"What's my total distance this year?"
"Am I on track to reach my monthly distance goal?"
```

### 💡 Tips for Better Queries

- ✅ **Be Specific**: "Show me my last 5 cycling activities with heart rate data"
- ✅ **Use IDs**: "Get details for activity 12345678"
- ✅ **Combine Info**: "Compare my last 3 runs and show me if my pace is improving"
- ✅ **Request Specific Data**: "Get GPS, heart rate, and power streams from activity 12345678"

## 🔧 Strava API - Available Endpoints

### Athlete

| Endpoint | Operation | Description |
|----------|-----------|-------------|
| `GET /athlete` | `getAthleteProfile` | Get complete profile |
| `GET /athlete/zones` | `getAthleteZones` | Training zones |
| `GET /athlete/stats` | `getAthleteStats` | Total statistics |

### Activities

| Endpoint | Operation | Description |
|----------|-----------|-------------|
| `GET /athlete/activities` | `getActivities` | List activities |
| `GET /activities/{id}` | `getActivityById` | Activity details |
| `GET /activities/{id}/zones` | `getActivityZones` | Zone distribution |
| `GET /activities/{id}/laps` | `getActivityLaps` | Laps/splits |
| `GET /activities/{id}/streams` | `getActivityStreams` | Point-by-point data |

### Segments

| Endpoint | Operation | Description |
|----------|-----------|-------------|
| `GET /segments/{id}` | `getSegmentById` | Segment details |
| `GET /segments/{id}/leaderboard` | `getSegmentLeaderboard` | Leaderboard |
| `GET /segments/explore` | `exploreSegments` | Search segments |

### Routes

| Endpoint | Operation | Description |
|----------|-----------|-------------|
| `GET /routes/{id}` | `getRouteById` | Route details |
| `GET /athletes/{id}/routes` | `getAthleteRoutes` | Athlete routes |

### Clubs

| Endpoint | Operation | Description |
|----------|-----------|-------------|
| `GET /athlete/clubs` | `getAthleteClubs` | Athlete clubs |
| `GET /clubs/{id}` | `getClubById` | Club details |
| `GET /clubs/{id}/members` | `getClubMembers` | Club members |
| `GET /clubs/{id}/activities` | `getClubActivities` | Club activities |

## 🏗️ How the Agent Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User / Client                             │
│              (Natural Language Query)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   StravaAgent (Python)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ReActAgent (BeeAI)                      │   │
│  │  - Reasoning and planning                            │   │
│  │  - Tool execution                                    │   │
│  │  - Response generation                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────────┐   │
│  │         WatsonxChatModel (IBM Granite)              │   │
│  │  - Natural language processing                       │   │
│  │  - Text generation                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┴──────────────────────────────┐   │
│  │         Custom Strava Tools (16 tools)              │   │
│  │  - Direct API implementation                         │   │
│  │  - Automatic OAuth2 authentication                  │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Strava API (REST)                           │
│  - Activities, Segments, Routes                             │
│  - Statistics, Clubs, Equipment                             │
│  - GPS/HR/Power data streams                                │
└─────────────────────────────────────────────────────────────┘
```

### Agent Flow

```mermaid
graph TB
    subgraph UI["🖥️ AgentStack UI"]
        A[User Input<br/>Natural Language]
        Z[Display Response<br/>Text + Images + Maps]
    end
    
    subgraph A2A["📡 A2A Protocol"]
        B[POST /a2a<br/>JSON Message]
        Y[HTTP Response<br/>Formatted Content]
    end
    
    subgraph BeeAI["🤖 BeeAI Agent"]
        C[ReAct Agent<br/>Reasoning]
        D[LLM Model<br/>Watsonx/Gemini]
        E{Tool Selection}
    end
    
    subgraph Tools["🔧 16 Custom Tools"]
        F1[GetActivities]
        F2[GetActivityById]
        F3[GetAthleteProfile]
        F4[GetActivityStreams]
        F5[GetSegmentById]
        F6[GetClubById]
        F7[... 10 more]
    end
    
    subgraph Auth["🔐 OAuth2"]
        G[Token Manager]
        H[Auto Refresh]
    end
    
    subgraph Strava["🏃 Strava API"]
        I1[/athlete/activities]
        I2[/activities/:id]
        I3[/athlete]
        I4[/segments/:id]
        I5[/clubs/:id]
    end
    
    subgraph Visual["🖼️ Visual Resources"]
        J1[Profile Photos<br/>Strava CDN]
        J2[Route Maps<br/>Google Maps]
        J3[Club Photos<br/>Strava CDN]
    end
    
    subgraph Format["✨ Response Formatter"]
        K[Visual Formatter<br/>Add Images]
        L[Markdown Generator]
        M[Natural Language]
    end
    
    A -->|1. Query| B
    B -->|2. Parse| C
    C -->|3. Analyze| D
    D -->|4. Select| E
    
    E -->|5a| F1
    E -->|5b| F2
    E -->|5c| F3
    E -->|5d| F4
    E -->|5e| F5
    E -->|5f| F6
    E -->|5g| F7
    
    F1 & F2 & F3 & F4 & F5 & F6 & F7 -->|6. Auth| G
    G -->|7. Token| H
    H -->|8. API Call| I1 & I2 & I3 & I4 & I5
    
    I1 & I2 -->|9. Data| K
    I3 -->|9. Profile + URL| J1
    I4 -->|9. Polyline| J2
    I5 -->|9. Club + URLs| J3
    
    J1 & J2 & J3 -->|10. Enhance| K
    K -->|11. Format| L
    L -->|12. Generate| M
    M -->|13. Response| D
    D -->|14. Return| Y
    Y -->|15. Display| Z
    
    style UI fill:#e1f5ff
    style BeeAI fill:#fff4e1
    style Tools fill:#ffe1e1
    style Strava fill:#e1ffe1
    style Visual fill:#f0e1ff
```

### Processing Steps

1. **Query Reception** - User sends natural language query
2. **Intent Analysis** - LLM analyzes what the user wants
3. **Tool Selection** - Agent selects appropriate Strava tools
4. **API Calls** - Tools make authenticated requests to Strava
5. **Data Processing** - Raw data is formatted and analyzed
6. **Visual Enhancement** - Maps and photos are added if available
7. **Response Generation** - LLM creates natural language response
8. **Delivery** - Formatted response with visuals returned to user

## 🔐 Security and Authentication

The agent implements:

- **OAuth2 with Refresh Token:** Automatic access token renewal
- **Secure credential management:** Environment variables
- **Expiration buffer:** Tokens renewed 5 minutes before expiring
- **Error handling:** Automatic retries on failure

## 📊 Metrics and Analysis

The agent can analyze:

### Running Metrics
- Pace in min/km
- Average and maximum speed
- Heart rate (average, maximum, zones)
- Cadence
- Elevation gain

### Cycling Metrics
- Average and maximum speed
- Power (watts, FTP, zones)
- Heart rate
- Cadence
- Elevation gain
- Kilojoules and calories

### Swimming Metrics
- Pace per 100m
- Total distance
- Moving time

## 🎨 Customization

### Change the LLM Model

The agent uses `meta-llama/llama-3-3-70b-instruct` by default. You can change the model during initialization:

```python
# Default model (recommended)
agent = StravaAgent()  # uses llama-3-3-70b-instruct

# Other compatible models
agent = StravaAgent(model_id="meta-llama/llama-3-1-70b-instruct")
agent = StravaAgent(model_id="ibm/granite-3-8b-instruct")
```

### Modify Queries

Edit the `main()` function in `src/beeai_agents/agent.py`:

```python
async def main():
    agent = StravaAgent()
    await agent.initialize()
    
    # Your custom query
    query = "Your question here"
    await agent.run(query)
    
    await agent.cleanup()
```

## 🐛 Troubleshooting

### Error: "Missing Strava credentials"

Make sure the `.env` file exists and contains all necessary variables.

### Error: "Error refreshing token"

Verify that your `STRAVA_REFRESH_TOKEN` is valid. You may need to generate a new one.

### Error: "Rate limit exceeded"

Strava has rate limits (200 requests/15min, 2000 requests/day). Wait before making more queries.

### The agent doesn't respond correctly

- Verify that the LLM model is available
- Check the logs to see which tools are being called
- Simplify your query to be more specific

### 📖 Complete Troubleshooting Guide

For a detailed troubleshooting guide, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 🚀 Future Improvements

| Feature | Description |
|---------|-------------|
| Trend Analysis | Charts and progress visualizations |
| Training Recommendations | Personalized plans based on data |
| Athlete Comparison | Benchmarking with similar athletes |
| Performance Prediction | ML to predict future times |
| Wearables Integration | Real-time data from devices |
| Alerts and Notifications | Notices of new records or achievements |
| Recovery Analysis | Fatigue and recovery metrics |
| Multi-language Support | Responses in multiple languages |

## 📚 Additional Resources

### Documentation
- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [Strava Getting Started Guide](https://developers.strava.com/docs/getting-started/)
- [API Coverage Analysis](STRAVA_API_COVERAGE.md) - Detailed comparison with official API
- [A2A Usage Guide](A2A_USAGE.md) - Complete A2A protocol documentation
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions

### Visual Resources 🖼️
- [Visual Setup Guide](VISUAL_SETUP_GUIDE.md) - **How to enable maps and photos in UI**
- [Strava Visual Resources](STRAVA_VISUAL_RESOURCES.md) - Available visual resources from API

### Frameworks & Tools
- [BeeAI Framework](https://github.com/i-am-bee/bee-agent-framework)
- [AgentStack SDK](https://github.com/AgentOps-AI/AgentStack)
- [IBM Watsonx](https://www.ibm.com/watsonx)

### Demo & Examples
- [Demo Conversation Guide](demo_conversation.md) - 10-step demo showcasing all capabilities

## 📄 License

This project is under the license specified in the LICENSE file.

## 🤝 Contributions

Contributions are welcome. Please:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This agent is functional for its intended purpose but is under active development. Use of this agent in a production environment is at your own risk. The authors are not responsible for any issues that may arise from its use in production.

## 📞 Support

For questions, issues, or suggestions, please open an issue in the GitHub repository.

---

**Enjoy training with your Strava AI assistant! 🏃‍♂️🚴‍♀️💪**

## 🎯 Implementation Details

### Custom Tools vs OpenAPI

This implementation uses **custom BeeAI tools** instead of OpenAPI tools because:

1. ✅ **Better reliability** - Direct control over API calls
2. ✅ **Easier maintenance** - Simple Python code
3. ✅ **Better performance** - No OpenAPI parsing overhead
4. ✅ **Full control** - Custom error handling and formatting
5. ✅ **Easier to extend** - Add new tools easily

### 16 Custom Tools Implemented

**Profile & Stats (2)**
- GetAthleteProfile
- GetAthleteStats

**Activities (5)**
- GetActivities
- GetActivityById
- GetActivityZones
- GetActivityLaps
- GetActivityStreams

**Segments (3)**
- ExploreSegments
- GetSegmentById
- GetSegmentLeaderboard

**Clubs (4)**
- GetAthleteClubs
- GetClubById
- GetClubActivities
- GetClubMembers

**Routes (2)**
- GetRouteById
- GetAthleteRoutes

### API Coverage

**Implemented:** ~90% of most used Strava endpoints
- ✅ Activities (complete - 5 read endpoints)
- ✅ Profile and statistics (complete - 3 endpoints)
- ✅ Segments (complete - 3 endpoints)
- ✅ Clubs (complete - 4 endpoints)
- ✅ Routes (complete - 2 endpoints)
- ✅ Data streams (complete - included in activities)

**Not implemented (by design):**
- ⚪ Activity uploads/updates (POST/PUT) - Write operations excluded for safety
- ⚪ Kudos and comments (GET/POST) - Social features, not core analytics
- ⚪ Gear management (GET) - Less frequently used
- ⚪ Webhooks - Requires server infrastructure
- ⚪ Segment efforts - Covered by activity streams

📊 **For detailed API coverage analysis, see [STRAVA_API_COVERAGE.md](STRAVA_API_COVERAGE.md)**

This document compares our implementation against the official Strava API documentation at https://developers.strava.com/docs/getting-started/ and explains why certain endpoints are not implemented.

---

Made with ❤️ using BeeAI Framework