import os
import asyncio
from dotenv import load_dotenv
from typing import List

# Updated imports from BeeAI SDK for Python (v0.1.68+)
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.adapters.watsonx import WatsonxChatModel
from beeai_framework.backend.types import ChatModelParameters
from beeai_framework.tools import Tool

# Import custom Strava tools
from beeai_agents.strava_custom_tools import create_strava_tools

load_dotenv()


class StravaAgent:
    """
    Complete AI agent to interact with the Strava API using custom tools.
    Provides intelligent analysis of activities, statistics, segments, and more.
    """
    
    def __init__(self, model_id: str = "meta-llama/llama-3-3-70b-instruct"):
        """
        Initialize the Strava agent.
        
        Args:
            model_id: LLM model ID to use (default: meta-llama/llama-3-3-70b-instruct)
        """
        self.agent = None
        self.model_id = model_id
        self.tools: List[Tool] = []
        
    async def initialize(self):
        """
        Initialize the agent with the LLM and custom Strava tools.
        """
        print("🚀 Initializing Strava Agent with custom tools...")
        
        try:
            # 1. Configure the LLM with optimized parameters for ReAct
            print(f"📡 Connecting to model: {self.model_id}")
            
            # Optimized parameters for better adherence to ReAct format
            llm_params = ChatModelParameters(
                temperature=0.0,  # More deterministic to follow format
                max_tokens=2048,
                top_p=0.95,
                top_k=50
            )
            
            llm = WatsonxChatModel(
                model_id=self.model_id,
                parameters=llm_params
            )

            # 2. Create custom Strava tools
            print("🔧 Creating custom Strava tools...")
            self.tools = create_strava_tools()
            print(f"✅ {len(self.tools)} custom tools created")
            
            # 3. Initialize the ReAct Agent with custom tools
            self.agent = ReActAgent(
                llm=llm,
                memory=UnconstrainedMemory(),
                tools=self.tools  # type: ignore
            )
            
            print("✅ Agent initialized successfully\n")
            
        except Exception as e:
            print(f"❌ Error initializing agent: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    async def run(self, query: str) -> str:
        """
        Execute a query on the agent.
        
        Args:
            query: User question or command
            
        Returns:
            str: Agent response
        """
        if not self.agent:
            await self.initialize()
        
        if not self.agent:
            raise RuntimeError("Agent could not be initialized")
        
        print(f"🤖 User: {query}\n")
        print("🤔 Processing...\n")
        
        try:
            response = await self.agent.run(query)
            
            # Extract text from response
            result = ""
            try:
                result = response.last_message.text
            except AttributeError:
                result = str(response)
            
            print("\n🐝 BeeAI Agent responds:")
            print("=" * 80)
            print(result)
            print("=" * 80)
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error processing query: {e}"
            print(error_msg)
            
            # Provide useful error information
            if "LinePrefixParserError" in str(e) or "does not adhere to the schema" in str(e):
                print("\n💡 SUGGESTION: The LLM model is not following the ReAct format correctly.")
                print("   Possible solutions:")
                print("   1. Use a more powerful model (e.g., meta-llama/llama-3-1-70b-instruct)")
                print("   2. Simplify your query to be more direct")
                print("   3. Try a more specific query\n")
            
            import traceback
            traceback.print_exc()
            return error_msg
    
    async def cleanup(self):
        """
        Clean up agent resources.
        """
        print("\n🧹 Cleaning up resources...")
        # Custom tools don't need special cleanup
        print("✅ Resources released")


# --- USAGE EXAMPLES ---
async def example_queries():
    """
    Examples of queries you can make to the agent.
    """
    agent = StravaAgent()
    
    queries = [
        # Activity analysis
        "Show me my last 5 activities with their main statistics",
        
        # Personal statistics
        "What are my total cycling statistics this year?",
        
        # Performance analysis
        "Analyze my progress in the last 10 runs. Have I improved my pace?",
        
        # Profile information
        "What is my current profile?",
        
        # Comparisons
        "Compare my most recent activity with my best time from last month",
    ]
    
    print("📚 EXAMPLE QUERIES YOU CAN MAKE:\n")
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")
    print("\n" + "=" * 80 + "\n")


# --- MAIN FUNCTION ---
async def main():
    """
    Main function that runs the Strava agent.
    """
    print("\n" + "=" * 80)
    print("🏃‍♂️ STRAVA AGENT WITH BEEAI (CUSTOM TOOLS) 🚴‍♀️")
    print("=" * 80 + "\n")
    
    agent = StravaAgent()
    
    try:
        await agent.initialize()
        
        # Example query - you can change it to any other
        user_query = "Compare my last 3 runs and tell me if I'm improving"
        
        await agent.run(user_query)
        
        # Uncomment to see examples of other queries
        # await example_queries()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await agent.cleanup()


def run():
    """
    Entry point for the server script.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 See you later!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run()

# Made with Bob
