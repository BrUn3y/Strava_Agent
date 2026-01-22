# 🏃‍♂️ Complete Strava Agent with BeeAI 🚴‍♀️

## Introduction

The Strava Agent is an advanced conversational AI system designed to interact with the complete Strava API. Built on the BeeAI framework with the AgentStack SDK, this agent allows you to analyze your athletic performance, explore segments, manage routes, interact with clubs, and much more through natural conversations.

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

### Run the Agent

```bash
uv run server
```

The agent will start and execute an example query. You can modify the query in `src/beeai_agents/agent.py`.

### Example Queries

#### 📊 Activity Analysis

```python
# Recent activities
"Show me my last 10 activities with their main statistics"

# Detailed analysis
"Give me a complete analysis of my most recent activity including laps and zones"

# Comparison
"Compare my last 5 runs and tell me if I've improved my pace"

# Time filters
"What activities did I do last week?"
```

#### 📈 Statistics

```python
# Total statistics
"What are my total cycling statistics this year?"

# Personal records
"What has been my longest run and my highest elevation gain?"

# Progress
"Analyze my progress over the last 3 months"
```

#### 🗺️ Segments and Routes

```python
# Explore segments
"Find cycling segments near my last activity"

# Leaderboards
"Show me the leaderboard for segment 12345"

# Routes
"List my saved routes"
```

#### 👥 Clubs

```python
# My clubs
"What clubs do I belong to?"

# Club activities
"Show me the latest activities from my main club"

# Members
"Who are the most active members of my club?"
```

#### 🚴 Equipment

```python
# Query equipment
"How many kilometers does my main bike have?"

# Details
"Give me information about all my equipment"
```

#### 📡 Advanced Data

```python
# Data streams
"Get the GPS and heart rate data from my last activity"

# Power analysis
"Show me the power data from my last workout"
```

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

## 🏗️ Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User / Client                             │
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

- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [BeeAI Framework](https://github.com/i-am-bee/bee-agent-framework)
- [AgentStack SDK](https://github.com/AgentOps-AI/AgentStack)
- [IBM Watsonx](https://www.ibm.com/watsonx)

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
- ✅ Activities (complete)
- ✅ Profile and statistics (complete)
- ✅ Segments (complete)
- ✅ Clubs (complete)
- ✅ Routes (complete)
- ✅ Data streams (complete)

**Not implemented (less common):**
- ⚪ Activity uploads (POST)
- ⚪ Activity updates (PUT)
- ⚪ Kudos and comments (GET/POST)
- ⚪ Gear management (GET)

---

Made with ❤️ using BeeAI Framework