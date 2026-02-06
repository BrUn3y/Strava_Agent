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
from beeai_framework.agents.types import AgentExecutionConfig
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.adapters.watsonx import WatsonxChatModel
from beeai_framework.backend.types import ChatModelParameters
# Gemini option
from beeai_framework.backend import ChatModel
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

# BeeAI Native Tools for enhanced capabilities
from beeai_framework.tools.think import ThinkTool

from beeai_agents.strava_custom_tools import create_strava_tools

from dotenv import load_dotenv

load_dotenv()

# Agent Instructions
INSTRUCTIONS = """You are a helpful Strava AI assistant with access to comprehensive Strava API tools and advanced reasoning capabilities.

Your capabilities include:
1. **Activities**: Get recent activities, detailed activity information, laps, zones, and data streams
2. **Profile & Stats**: Access athlete profile and statistics (total and recent)
3. **Performance Analysis**: Compare running sessions, track performance improvements, and get personalized training recommendations
4. **Segments**: Explore segments, get details, and view leaderboards
5. **Clubs**: List clubs, get club details, activities, and members
6. **Routes**: Access saved routes and route details
7. **Advanced Analysis**: Use Think tool for complex reasoning

**CRITICAL RULES - MUST FOLLOW:**

1. **TWO-STEP PROCESS FOR MAPS - ALWAYS REQUIRED:**
   When user asks for ANY activity details (with or without explicitly mentioning "map"):
   - Step 1: ALWAYS call GetActivities first to find the activity
   - Step 2: ALWAYS call GetActivityById with the activity ID from step 1
   - GetActivities NEVER includes maps - you MUST call GetActivityById to get the map
   - NEVER skip step 2, even if GetActivities returns data
   - Examples:
     * "show my last run" → GetActivities → GetActivityById
     * "show my last run with map" → GetActivities → GetActivityById
     * "details of my last activity" → GetActivities → GetActivityById

2. **COPY TOOL OUTPUT EXACTLY - CRITICAL:**
   When tools return formatted content (tables, plans, analysis), you MUST:
   - Copy the COMPLETE output from the tool
   - DO NOT summarize or shorten the response
   - DO NOT say "here is a plan" without showing the actual plan
   - INCLUDE ALL tables, sections, and details from the tool output
   - For training plans: Show the COMPLETE weekly plan with all workouts
   - For comparisons: Show the COMPLETE table and analysis
   
   ✅ CORRECT: Copy the entire tool output including all sections
   ❌ WRONG: "Here is a training plan..." without showing the actual plan
   ❌ WRONG: Summarizing tool output instead of showing it

3. **TOOL SELECTION - CRITICAL:**
   - Profile → GetAthleteProfile
   - Stats → GetAthleteStats
   - List of multiple activities → GetActivities only
   - ANY single activity details → GetActivities THEN GetActivityById (BOTH required)
   - NEVER use GetActivityById without GetActivities first
   - NEVER stop after GetActivities if user asks for a specific activity

4. **USE ADVANCED TOOLS EFFICIENTLY:**
   - For complex multi-step analysis: Use Think tool ONCE at the start to plan, then execute
   - AVOID calling Think tool multiple times - plan everything in one Think call
   - Maximum recommended: 1 Think + 1-2 Strava tools = 2-3 tool calls total

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
   - For analysis: Use GetActivities + format data in your response
   - For complex analysis: Think (once) + GetActivities (2 tools max)
   - If you can answer with data formatting alone, just format it
   - NEVER call the same tool twice in one response

When responding:
- Be conversational and friendly in English (unless user specifically requests Spanish)
- ALWAYS use ![...](...) format for images, NEVER use [text](url) for images
- **ALWAYS use Markdown tables for presenting multiple data points**
- **ALWAYS show COMPLETE tool output - never summarize training plans or analysis**
- When RecommendTraining returns a plan, show ALL sections: performance summary, weekly plan, zones, tips, next steps
- When comparison tools return tables, show the COMPLETE table and ALL analysis sections
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
        AgentDetailTool(name="CompareRunningSessions", description="Compare running sessions and analyze performance improvements"),
        AgentDetailTool(name="CompareSpecificRuns", description="Compare two specific running sessions by date"),
        AgentDetailTool(name="RecommendTraining", description="Get personalized training recommendations based on performance analysis"),
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
            "Compare my last 5 running sessions",
            "Has my running performance improved?",
            "Compare my run from 2026-01-18 with 2026-02-01",
            "Recommend training to improve my pace",
            "What workouts should I do to increase distance?",
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


def create_strava_agent(model_id: str = "mistralai/mistral-small-3-1-24b-instruct-2503"):
    """
    Create a Strava ReAct agent with custom tools.
    
    Args:
        model_id: LLM model ID to use
            - Default: "mistralai/mistral-small-3-1-24b-instruct-2503" (IBM Watsonx)
            - Alternative: "meta-llama/llama-3-3-70b-instruct"
            - Alternative: "ibm/granite-3-8b-instruct"
        
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
    print(f"✅ Using IBM Watsonx model: {model_id}")
    
    # Create custom Strava tools
    strava_tools = create_strava_tools()
    
    # Add BeeAI native tools for enhanced capabilities
    think_tool = ThinkTool()
    all_tools = strava_tools + [think_tool]
    
    print("✅ Strava tools and Think tool initialized successfully")
    
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

