# 🔧 Troubleshooting Guide - Strava Agent

## Common Issues and Solutions

### 1. LinePrefixParserError: "Transition from 'thought' to 'tool_input' does not exist"

**Error Message:**
```
beeai_framework.parsers.line_prefix.LinePrefixParserError: The generated output does not adhere to the schema.
Transition from 'thought' to 'tool_input' does not exist!
```

**Cause:**
This error occurs when the LLM model doesn't properly follow the ReAct (Reasoning + Acting) pattern format required by the BeeAI framework. The model is generating output that doesn't match the expected schema transitions.

**Solutions:**

#### Solution 1: Use a More Capable Model (Recommended)
The default model has been changed to `meta-llama/llama-3-1-70b-instruct` which has better instruction-following capabilities:

```python
agent = StravaAgent()  # Uses llama-3-1-70b-instruct by default
```

Or explicitly specify a model:
```python
agent = StravaAgent(model_id="meta-llama/llama-3-1-70b-instruct")
```

**Recommended Models (in order of reliability):**
1. `meta-llama/llama-3-1-70b-instruct` ✅ (Best for ReAct)
2. `meta-llama/llama-3-1-8b-instruct` (Faster, less reliable)
3. `ibm/granite-3-8b-instruct` (Alternative)

**Not Recommended:**
- `openai/gpt-oss-120b` ❌ (Known to have schema adherence issues)

#### Solution 2: Simplify Your Queries
Instead of complex multi-part queries, use simpler, more direct questions:

**❌ Complex (may fail):**
```python
query = """
Analiza mis últimas 10 actividades. Dame un resumen con: distancia total, 
tiempo total, actividad más larga, y mi frecuencia cardíaca promedio. 
También dame una recomendación de entrenamiento.
"""
```

**✅ Simple (more reliable):**
```python
query = "Muéstrame mis últimas 5 actividades"
```

#### Solution 3: Reduce Tool Complexity
If you're still experiencing issues, consider creating a simplified version of the OpenAPI schema with fewer endpoints:

```python
# In strava-tool.yaml, comment out less-used endpoints
# Keep only essential ones like:
# - /athlete
# - /athlete/activities
# - /activities/{id}
```

#### Solution 4: Adjust LLM Parameters
The agent now uses optimized parameters:
- `temperature=0.0` - More deterministic output
- `max_tokens=2048` - Sufficient for responses
- `top_p=0.95` - Balanced creativity
- `top_k=50` - Focused token selection

These are already configured in the latest version.

---

### 2. Authentication Errors

**Error Message:**
```
❌ Faltan credenciales de Strava
```

**Solution:**
Ensure your `.env` file contains all required credentials:

```bash
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REFRESH_TOKEN=your_refresh_token
```

To get these credentials:
1. Go to https://www.strava.com/settings/api
2. Create an application
3. Use the authorization flow to get a refresh token

---

### 3. Token Refresh Issues

**Error Message:**
```
Error al refrescar token de Strava
```

**Solutions:**
1. Verify your refresh token is still valid
2. Check that your Strava app has the correct permissions
3. Ensure your client_id and client_secret are correct
4. Try generating a new refresh token

---

### 4. API Rate Limiting

**Error Message:**
```
429 Too Many Requests
```

**Solution:**
Strava has rate limits:
- 100 requests per 15 minutes
- 1000 requests per day

Wait before making more requests or implement request throttling.

---

### 5. Empty or Incomplete Responses

**Possible Causes:**
1. No activities in your Strava account
2. API permissions not granted
3. Network connectivity issues

**Solutions:**
1. Verify you have activities in your Strava account
2. Check that your app has read permissions
3. Test direct API access using `test_agent.py`

---

## Testing Your Setup

### Quick Test
Run the test script to verify API connectivity:

```bash
python test_agent.py
```

This will:
- ✅ Test authentication
- ✅ Fetch your profile
- ✅ Retrieve recent activities
- ✅ Verify the API is working

### Full Agent Test
Run the agent with a simple query:

```bash
python -m src.beeai_agents.agent
```

Or programmatically:

```python
import asyncio
from src.beeai_agents.agent import StravaAgent

async def test():
    agent = StravaAgent()
    await agent.initialize()
    result = await agent.run("Muéstrame mi perfil")
    print(result)

asyncio.run(test())
```

---

## Debug Mode

To get more detailed error information, the agent now provides helpful suggestions when schema errors occur:

```
💡 SUGERENCIA: El modelo LLM no está siguiendo el formato ReAct correctamente.
   Posibles soluciones:
   1. Usa un modelo más potente (ej: meta-llama/llama-3-1-70b-instruct)
   2. Simplifica tu consulta para que sea más directa
   3. Reduce el número de herramientas disponibles
   4. Intenta con una consulta más específica
```

---

## Getting Help

If you continue to experience issues:

1. **Check the logs** - The agent provides detailed output
2. **Test the API directly** - Use `test_agent.py` to isolate issues
3. **Verify your model** - Ensure you're using a recommended model
4. **Simplify your query** - Start with basic questions
5. **Check your credentials** - Verify all environment variables are set

---

## Version Information

- **BeeAI Framework**: >=0.1.68
- **Python**: >=3.11,<4.0
- **Recommended Model**: meta-llama/llama-3-1-70b-instruct

---

## Additional Resources

- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [BeeAI Framework Documentation](https://github.com/i-am-bee/bee-agent-framework)
- [OAuth2 Flow Guide](https://developers.strava.com/docs/authentication/)