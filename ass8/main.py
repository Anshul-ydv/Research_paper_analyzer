import asyncio
from .agent import research_agent
from .summarization_agent import summarization_agent
from .a2a import a2a_channel

async def main():
    """Run the research agent demo."""
    # Example queries
    queries = [
        "transformer neural networks",
        "quantum computing recent advances"
    ]
    
    for query in queries:
        print(f"\n=== Processing query: {query} ===")
        
        # Step 1: Research agent retrieves papers and sends to summarization agent
        results = await research_agent.process_query(query)
        
        if results['papers']:
            print(f"Found {len(results['papers'])} papers")
            # Wait a bit for summaries to be processed (in real impl, use proper synchronization)
            await asyncio.sleep(2)
        else:
            print("No papers found for the query")

        print("\n---")

if __name__ == "__main__":
    asyncio.run(main())