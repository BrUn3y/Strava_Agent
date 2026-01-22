"""
Strava Agent with AgentStack and A2A support
Provides conversational access to Strava API through A2A protocol
"""

import os
import asyncio
from collections.abc import AsyncGenerator

from a2a.types import AgentSkill, Message
from a2a.utils.message import get_message_text
from agentstack_sdk.server import Server
from agentstack_sdk.server.context import RunContext
from agentstack_sdk.a2a.types import AgentMessage
from agentstack_sdk.a2a.extensions import AgentDetail, AgentDetailTool
from agentstack_sdk.server.store.platform_context_store import PlatformContextStore

from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.adapters.watsonx import WatsonxChatModel
from beeai_framework.backend.types import ChatModelParameters
# Gemini option (quota exceeded)
# from beeai_framework.backend import ChatModel
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

# BeeAI Native Tools for enhanced capabilities
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.code.python import PythonTool

from beeai_agents.strava_custom_tools import create_strava_tools

from dotenv import load_dotenv

load_dotenv()

# Agent Instructions
INSTRUCTIONS = """You are a helpful Strava AI assistant with access to comprehensive Strava API tools, advanced reasoning, and data analysis capabilities.

Your capabilities include:
1. **Activities**: Get recent activities, detailed activity information, laps, zones, and data streams
2. **Profile & Stats**: Access athlete profile and statistics (total and recent)
3. **Segments**: Explore segments, get details, and view leaderboards
4. **Clubs**: List clubs, get club details, activities, and members
5. **Routes**: Access saved routes and route details
6. **Advanced Analysis**: Use Think tool for complex reasoning and Python tool for data analysis & visualizations

**CRITICAL RULES - MUST FOLLOW:**

1. **ONLY call tools that match the user's request:**
   - User asks for "profile" → use GetAthleteProfile
   - User asks for "activity", "run", "workout", "route", "map" → use GetActivityById or GetActivities
   - User asks for "stats" → use GetAthleteStats
   - DO NOT call GetAthleteProfile when user asks about activities

2. **MARKDOWN IMAGE FORMAT - EXTREMELY IMPORTANT:**
   When a tool returns a map URL or image URL, you MUST format it as Markdown image:
   
   ✅ CORRECT FORMAT:
   ![Route Map](https://maps.googleapis.com/maps/api/staticmap?...)
   
   ❌ WRONG - DO NOT DO THIS:
   The map is available [here](https://maps.googleapis.com/...)
   
   ✅ CORRECT EXAMPLE:
   "Tu medio maratón del 2 de noviembre:
   
   ![Route Map](https://maps.googleapis.com/maps/api/staticmap?size=600x400&path=enc:q{d}Bn|bvR...&key=...)
   
   - Distancia: 31.02 km
   - Tiempo: 174 minutos"
   
   The ![...](...) syntax makes the image render in the UI. Links [here](...) do NOT render images.

3. **PRESERVE TOOL OUTPUT IMAGES:**
   If a tool returns ![Photo](URL) or ![Map](URL), copy it EXACTLY to your response.
   DO NOT convert it to a link or plain text.

4. **USE ADVANCED TOOLS EFFICIENTLY:**
   - For complex multi-step analysis: Use Think tool ONCE at the start to plan, then execute
   - For data analysis: Get data first with Strava tools, THEN use Python tool once
   - AVOID calling Think tool multiple times - plan everything in one Think call
   - Examples:
     * "Analyze my training trend" → Think (plan) → GetActivities → Python (analyze)
     * "Create a chart" → GetActivities → Python (create chart)
     * "Compare activities" → GetActivities → Python (compare)
   - Maximum recommended: 1 Think + 1-2 Strava tools + 1 Python = 3-4 tool calls total

5. **ALWAYS USE MARKDOWN TABLES FOR DATA - EXTREMELY IMPORTANT:**
   When presenting multiple data points, activities, or comparisons, ALWAYS use Markdown tables.
   
   ✅ CORRECT FORMAT:
   | Date | Distance (km) | Time (min) | Pace (min/km) |
   |------|--------------|------------|---------------|
   | 2025-01-15 | 10.5 | 52 | 4:57 |
   | 2025-01-18 | 8.2 | 38 | 4:38 |
   
   ❌ WRONG - DO NOT USE BULLET LISTS FOR TABULAR DATA:
   - Activity 1: 10.5 km, 52 min
   - Activity 2: 8.2 km, 38 min
   
   Use tables for:
   - Multiple activities comparison
   - Statistics over time
   - Leaderboards
   - Lap/split data
   - Any data with 3+ comparable items

6. **EFFICIENCY RULES - CRITICAL:**
   - For simple queries (1-5 activities): Just use GetActivities and format as table
   - For analysis without charts: Use GetActivities + format data in your response
   - For charts/graphs: Use GetActivities + Python tool (2 tools max)
   - For complex analysis: Think (once) + GetActivities + Python (3 tools max)
   - If you can answer with data formatting alone, DON'T use Python tool
   - NEVER call the same tool twice in one response

When responding:
- Be conversational and friendly in Spanish
- ALWAYS use ![...](...) format for images, NEVER use [text](url) for images
- **ALWAYS use Markdown tables for presenting multiple data points**
- Provide clear, structured information
- Use emojis (🏃, 🚴, 📊, 🗺️)
- Format numbers appropriately (km, minutes, etc.)
- ONLY show images relevant to the user's question
- Be efficient: Use minimum tools necessary
- Think once, act once, respond once

Remember: ![Image](url) renders an image, [link](url) does not!"""

# Agent Detail for A2A
AGENT_DETAIL = AgentDetail(
    interaction_mode="multi-turn",
    user_greeting="Hello! I'm your Strava AI assistant. I can help you analyze your activities, explore segments, check your stats, and much more! 🏃‍♂️🚴‍♀️",
    version="1.0.0",
    framework="BeeAI",
    author={"name": "Edgar Bruney"},
    tools=[
        AgentDetailTool(name="GetAthleteProfile", description="Get authenticated athlete's complete profile"),
        AgentDetailTool(name="GetActivities", description="Get recent activities with filters"),
        AgentDetailTool(name="GetActivityById", description="Get complete details of a specific activity"),
        AgentDetailTool(name="GetAthleteStats", description="Get total and recent athlete statistics"),
        AgentDetailTool(name="GetActivityZones", description="Get heart rate or power zone distribution"),
        AgentDetailTool(name="GetActivityLaps", description="Get laps/splits of an activity"),
        AgentDetailTool(name="GetActivityStreams", description="Get point-by-point GPS, HR, power data"),
        AgentDetailTool(name="ExploreSegments", description="Find segments in a geographic area"),
        AgentDetailTool(name="GetSegmentById", description="Get detailed segment information"),
        AgentDetailTool(name="GetSegmentLeaderboard", description="Get segment leaderboard rankings"),
        AgentDetailTool(name="GetAthleteClubs", description="Get clubs the athlete belongs to"),
        AgentDetailTool(name="GetClubById", description="Get detailed club information"),
        AgentDetailTool(name="GetClubActivities", description="Get recent club activities"),
        AgentDetailTool(name="GetClubMembers", description="Get club member list"),
        AgentDetailTool(name="GetRouteById", description="Get detailed route information"),
        AgentDetailTool(name="GetAthleteRoutes", description="Get athlete's saved routes"),
        AgentDetailTool(name="Think", description="Break down complex problems into steps for better reasoning"),
        AgentDetailTool(name="Python", description="Execute Python code for data analysis and visualizations"),
    ],
)

# Agent Skills for A2A
AGENT_SKILLS = [
    AgentSkill(
        id="strava-activities",
        name="Activity Analysis",
        description="Analyze your Strava activities, get detailed stats, compare performances, and track progress",
        tags=["Activities", "Stats", "Analysis"],
        examples=[
            "Show me my last 10 activities",
            "Get details of activity 12345678",
            "What were my activities from last week?",
            "Compare my last 3 runs",
        ]
    ),
    AgentSkill(
        id="strava-segments",
        name="Segment Explorer",
        description="Explore segments, view leaderboards, and find challenging routes in your area",
        tags=["Segments", "Leaderboards", "Exploration"],
        examples=[
            "Find cycling segments near coordinates 37.8,-122.4",
            "Show me the leaderboard for segment 12345",
            "What segments are popular in my area?",
        ]
    ),
    AgentSkill(
        id="strava-stats",
        name="Statistics & Profile",
        description="Access your profile, training zones, and comprehensive statistics",
        tags=["Profile", "Statistics", "Zones"],
        examples=[
            "What's my current profile?",
            "Show me my total cycling statistics",
            "What are my heart rate zones?",
        ]
    ),
    AgentSkill(
        id="strava-clubs",
        name="Club Management",
        description="View your clubs, club activities, and member information",
        tags=["Clubs", "Community", "Social"],
        examples=[
            "What clubs do I belong to?",
            "Show me recent activities from my club",
            "Who are the members of club 12345?",
        ]
    ),
    AgentSkill(
        id="strava-routes",
        name="Route Planning",
        description="Access and analyze your saved routes",
        tags=["Routes", "Planning", "Navigation"],
        examples=[
            "Show me my saved routes",
            "Get details about route 67890",
            "What's the elevation profile of my favorite route?",
        ]
    ),
]

# Initialize AgentStack server
server = Server()


def create_strava_agent(model_id: str = "meta-llama/llama-3-3-70b-instruct"):
    """
    Create a Strava ReAct agent with custom tools.
    
    Args:
        model_id: LLM model ID to use
            - Default: "meta-llama/llama-3-3-70b-instruct" (IBM Watsonx - Active)
            - Alternative: "ibm/granite-3-8b-instruct", "meta-llama/llama-3-1-70b-instruct"
            - Gemini (quota exceeded): "gemini:gemini-2.0-flash-exp"
        
    Returns:
        Configured ReActAgent instance
    """
    # Configure LLM with optimized parameters
    llm_params = ChatModelParameters(
        temperature=0.0,  # More deterministic for better tool usage
        max_tokens=2048,
        top_p=0.95,
        top_k=50
    )
    
    # Option 1: IBM Watsonx (Active)
    # Requires: WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL in .env
    llm = WatsonxChatModel(
        model_id=model_id,
        parameters=llm_params
    )
    
    # Option 2: Google Gemini (Quota exceeded - commented out)
    # Requires: GEMINI_API_KEY in .env
    # from beeai_framework.backend import ChatModel
    # llm = ChatModel.from_name(
    #     "gemini:gemini-2.0-flash-exp",
    #     parameters=llm_params
    # )
    
    # Create custom Strava tools
    strava_tools = create_strava_tools()
    
    # Add BeeAI native tools for enhanced capabilities
    think_tool = ThinkTool()
    
    # Python tool - requires code interpreter setup
    # Check if code interpreter URL is configured
    code_interpreter_url = os.getenv("CODE_INTERPRETER_URL")
    
    if code_interpreter_url:
        try:
            from beeai_framework.tools.code.storage import LocalPythonStorage
            
            # Setup storage directories
            local_dir = os.getenv("CODE_STORAGE_PATH", "./code_storage")
            interpreter_dir = os.getenv("CODE_INTERPRETER_DIR", "/tmp/code_storage")
            
            # Create local directory if it doesn't exist
            os.makedirs(local_dir, exist_ok=True)
            
            storage = LocalPythonStorage(
                local_working_dir=local_dir,
                interpreter_working_dir=interpreter_dir
            )
            python_tool = PythonTool(
                code_interpreter_url=code_interpreter_url,
                storage=storage
            )
            all_tools = strava_tools + [think_tool, python_tool]
            print("✅ Python tool initialized successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize Python tool: {e}")
            print("   Continuing with Think tool only...")
            all_tools = strava_tools + [think_tool]
    else:
        print("ℹ️  Python tool not configured (CODE_INTERPRETER_URL not set)")
        print("   To enable Python tool, set CODE_INTERPRETER_URL in .env")
        print("   Continuing with Think tool only...")
        all_tools = strava_tools + [think_tool]
    
    # Initialize ReAct agent
    agent = ReActAgent(
        llm=llm,
        memory=UnconstrainedMemory(),
        tools=all_tools  # type: ignore
    )
    
    return agent


@server.agent(
    name="Strava Agent",
    default_input_modes=["text"],
    default_output_modes=["text"],
    detail=AGENT_DETAIL,
    skills=AGENT_SKILLS
)
async def strava_a2a_agent(input: Message, context: RunContext) -> AsyncGenerator[AgentMessage, None]:
    """
    A2A-compatible Strava agent endpoint with session history support.
    
    Analyzes Strava activities, explores segments, views statistics, manages clubs, and plans routes.
    Maintains conversation context across multiple turns.
    
    Args:
        input: A2A Message from user
        context: Run context from AgentStack (includes session history)
        
    Yields:
        AgentMessage responses
    """
    # Store incoming message in session history
    await context.store(input)
    
    # Extract user query from A2A message
    user_query = get_message_text(input)
    print(f"🏃 Strava Agent received query: '{user_query}'")
    
    # Load conversation history for context
    # This allows the agent to reference previous messages
    history = [msg async for msg in context.load_history() if isinstance(msg, Message)]
    print(f"📚 Loaded {len(history)} messages from history")
    
    # Create agent instance
    agent = create_strava_agent()
    
    try:
        # Run agent with the current query
        # The agent can use its own memory for tool usage context
        response = await agent.run(user_query)
        
        print("✅ Strava Agent finished processing")
        
        # Extract final answer
        try:
            final_answer = response.last_message.text
        except AttributeError:
            final_answer = str(response)
        
        # Extract images from tool outputs and add them to the response
        # This ensures images are preserved even if the LLM removes them
        import re
        tool_outputs = []
        if hasattr(response, 'iterations'):
            for iteration in response.iterations:
                if hasattr(iteration, 'state') and hasattr(iteration.state, 'tool_output'):
                    if iteration.state.tool_output:
                        tool_outputs.append(str(iteration.state.tool_output))
        
        # Find all Markdown images in tool outputs
        images_found = []
        for output in tool_outputs:
            images = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', output)
            images_found.extend(images)
        
        # If images were found in tools but not in final answer, prepend them
        if images_found and '![' not in final_answer:
            print(f"📸 Found {len(images_found)} images in tool outputs, adding to response")
            image_markdown = '\n'.join([f'![{alt}]({url})' for alt, url in images_found])
            final_answer = f"{image_markdown}\n\n{final_answer}"
        
        # Create response message
        agent_msg = AgentMessage(text=final_answer)
        
        # Yield response to user
        yield agent_msg
        
        # Store agent response in session history
        await context.store(agent_msg)
        
    except Exception as e:
        error_message = f"❌ Error processing Strava query: {str(e)}\n\nPlease try rephrasing your question or check if you have valid Strava credentials configured."
        print(f"Error details: {e}")
        import traceback
        traceback.print_exc()
        
        # Create and store error message
        error_msg = AgentMessage(text=error_message)
        yield error_msg
        await context.store(error_msg)


def run():
    """
    Start the AgentStack server with Strava agent.
    """
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "=" * 80)
    print("🏃‍♂️ STRAVA AGENT WITH AGENTSTACK & A2A 🚴‍♀️")
    print("=" * 80)
    print(f"\n🚀 Starting server on {host}:{port}")
    print(f"📡 A2A endpoint: http://{host}:{port}/a2a")
    print(f"📊 Health check: http://{host}:{port}/health")
    print("\n💡 Available skills:")
    for skill in AGENT_SKILLS:
        print(f"   • {skill.name}: {skill.description}")
    print("\n" + "=" * 80 + "\n")
    
    try:
        server.run(host=host, port=port, context_store=PlatformContextStore())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()

# Made with Bob

