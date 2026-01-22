# 🌐 Strava Agent with A2A Protocol

This document explains how to use the Strava Agent with AgentStack and the A2A (Agent-to-Agent) protocol.

## 📋 Table of Contents

- [What is A2A?](#what-is-a2a)
- [Installation](#installation)
- [Running the A2A Server](#running-the-a2a-server)
- [API Endpoints](#api-endpoints)
- [Using the Agent](#using-the-agent)
- [Agent Skills](#agent-skills)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## 🤔 What is A2A?

A2A (Agent-to-Agent) is a protocol that enables standardized communication between AI agents. It allows:

- **Interoperability**: Different agents can communicate using a common protocol
- **Discoverability**: Agents can advertise their capabilities (skills)
- **Composability**: Agents can be chained together to solve complex tasks
- **Standardization**: Consistent API across different agent implementations

## 📦 Installation

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file contains:

```env
# IBM Watsonx (or your LLM provider)
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29

# Strava API
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REFRESH_TOKEN=your_refresh_token

# Server Configuration (optional)
HOST=127.0.0.1
PORT=8000
```

## 🚀 Running the A2A Server

### Start the Server

```bash
# Using the script command
uv run strava-server

# Or directly with Python
uv run python -m beeai_agents.strava_a2a_agent
```

The server will start on `http://127.0.0.1:8000` by default.

### Server Output

```
================================================================================
🏃‍♂️ STRAVA AGENT WITH AGENTSTACK & A2A 🚴‍♀️
================================================================================

🚀 Starting server on 127.0.0.1:8000
📡 A2A endpoint: http://127.0.0.1:8000/a2a
📊 Health check: http://127.0.0.1:8000/health

💡 Available skills:
   • Activity Analysis: Analyze your Strava activities...
   • Segment Explorer: Explore segments, view leaderboards...
   • Statistics & Profile: Access your profile, training zones...
   • Club Management: View your clubs, club activities...
   • Route Planning: Access and analyze your saved routes

================================================================================
```

## 🔌 API Endpoints

### Health Check

```bash
GET http://127.0.0.1:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.2.0"
}
```

### A2A Endpoint

```bash
POST http://127.0.0.1:8000/a2a
Content-Type: application/json

{
  "message": {
    "role": "user",
    "content": "Show me my last 5 activities"
  }
}
```

### Agent Discovery

```bash
GET http://127.0.0.1:8000/a2a/discover
```

Returns agent capabilities, skills, and available tools.

## 💬 Using the Agent

### Using curl

```bash
# Simple query
curl -X POST http://127.0.0.1:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "role": "user",
      "content": "What are my total cycling statistics?"
    }
  }'

# Activity details
curl -X POST http://127.0.0.1:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "role": "user",
      "content": "Get details of activity 12345678"
    }
  }'
```

### Using Python

```python
import requests

url = "http://127.0.0.1:8000/a2a"
headers = {"Content-Type": "application/json"}

# Query the agent
data = {
    "message": {
        "role": "user",
        "content": "Show me my last 10 activities"
    }
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(result["message"]["content"])
```

### Using JavaScript/TypeScript

```typescript
const url = "http://127.0.0.1:8000/a2a";

const query = {
  message: {
    role: "user",
    content: "What clubs do I belong to?"
  }
};

const response = await fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(query)
});

const result = await response.json();
console.log(result.message.content);
```

## 🎯 Agent Skills

The Strava Agent exposes 5 main skills through A2A:

### 1. Activity Analysis (`strava-activities`)

Analyze activities, get detailed stats, compare performances.

**Examples:**
- "Show me my last 10 activities"
- "Get details of activity 12345678"
- "Compare my last 3 runs"

### 2. Segment Explorer (`strava-segments`)

Explore segments, view leaderboards, find routes.

**Examples:**
- "Find cycling segments near coordinates 37.8,-122.4"
- "Show me the leaderboard for segment 12345"

### 3. Statistics & Profile (`strava-stats`)

Access profile, training zones, and statistics.

**Examples:**
- "What's my current profile?"
- "Show me my total cycling statistics"
- "What are my heart rate zones?"

### 4. Club Management (`strava-clubs`)

View clubs, activities, and members.

**Examples:**
- "What clubs do I belong to?"
- "Show me recent activities from my club"

### 5. Route Planning (`strava-routes`)

Access and analyze saved routes.

**Examples:**
- "Show me my saved routes"
- "Get details about route 67890"

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `WATSONX_API_KEY` | IBM Watsonx API key | Yes | - |
| `WATSONX_PROJECT_ID` | IBM Watsonx project ID | Yes | - |
| `WATSONX_URL` | Watsonx API endpoint | Yes | - |
| `STRAVA_CLIENT_ID` | Strava application client ID | Yes | - |
| `STRAVA_CLIENT_SECRET` | Strava application secret | Yes | - |
| `STRAVA_REFRESH_TOKEN` | Strava OAuth refresh token | Yes | - |
| `HOST` | Server host address | No | 127.0.0.1 |
| `PORT` | Server port | No | 8000 |

### LLM Model Configuration

By default, the agent uses `meta-llama/llama-3-3-70b-instruct`. To change the model, modify `strava_a2a_agent.py`:

```python
def create_strava_agent(model_id: str = "your-model-id"):
    # ...
```

## 📝 Examples

### Complete Workflow Example

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/a2a"

def query_agent(message: str):
    """Send a query to the Strava agent"""
    response = requests.post(
        BASE_URL,
        json={"message": {"role": "user", "content": message}},
        headers={"Content-Type": "application/json"}
    )
    return response.json()["message"]["content"]

# 1. Get profile
print("=== My Profile ===")
profile = query_agent("What's my current profile?")
print(profile)

# 2. Get recent activities
print("\n=== Recent Activities ===")
activities = query_agent("Show me my last 5 activities")
print(activities)

# 3. Get statistics
print("\n=== Statistics ===")
stats = query_agent("What are my total running statistics?")
print(stats)

# 4. Analyze performance
print("\n=== Performance Analysis ===")
analysis = query_agent("Compare my last 3 runs and tell me if I'm improving")
print(analysis)
```

### Multi-Agent Conversation

```python
# Maintain conversation context
conversation = []

def chat(message: str):
    conversation.append({"role": "user", "content": message})
    response = requests.post(
        BASE_URL,
        json={"message": conversation[-1]},
        headers={"Content-Type": "application/json"}
    )
    result = response.json()["message"]["content"]
    conversation.append({"role": "assistant", "content": result})
    return result

# Start conversation
print(chat("Show me my last activity"))
print(chat("Now get the detailed zones for that activity"))
print(chat("What does this tell me about my training?"))
```

## 🐛 Troubleshooting

### Server Won't Start

**Problem**: Server fails to start with import errors

**Solution**:
```bash
# Reinstall dependencies
uv sync --reinstall

# Check Python version (must be 3.11+)
python --version
```

### Authentication Errors

**Problem**: "Missing Strava credentials" or "Error refreshing token"

**Solution**:
1. Verify `.env` file exists and contains all required variables
2. Run `uv run python get_strava_token.py` to get a fresh token
3. Make sure token has correct scopes: `read,activity:read_all,profile:read_all`

### Agent Not Responding

**Problem**: Agent returns errors or doesn't use tools

**Solution**:
1. Check server logs for detailed error messages
2. Verify LLM credentials (Watsonx API key)
3. Try a simpler query first: "Show me my profile"
4. Check if Strava API is accessible

### Rate Limiting

**Problem**: "Rate limit exceeded" errors

**Solution**:
- Strava has rate limits: 200 requests/15min, 2000 requests/day
- Wait before making more requests
- Batch queries when possible

### Connection Refused

**Problem**: Cannot connect to server

**Solution**:
```bash
# Check if server is running
curl http://127.0.0.1:8000/health

# Check if port is in use
lsof -i :8000

# Try different port
PORT=8080 uv run strava-server
```

## 🔗 Related Documentation

- [README.md](README.md) - Main project documentation
- [EXAMPLE_QUERIES.md](EXAMPLE_QUERIES.md) - Query examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed troubleshooting guide
- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [AgentStack Documentation](https://docs.agentstack.sh/)
- [A2A Protocol Specification](https://github.com/a2a-protocol/spec)

## 🤝 Contributing

To add new features or skills:

1. Add new tools in `strava_custom_tools.py`
2. Update `AGENT_SKILLS` in `strava_a2a_agent.py`
3. Update `AGENT_DETAIL.tools` list
4. Test with A2A protocol
5. Update documentation

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Made with ❤️ using BeeAI Framework, AgentStack, and A2A Protocol**