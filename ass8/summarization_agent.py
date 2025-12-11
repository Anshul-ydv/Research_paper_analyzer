from google.adk.agents.llm_agent import Agent
from typing import List, Dict, Any
from .a2a import A2AMessage, a2a_channel

class SummarizationAgent(Agent):
    def __init__(self):
        super().__init__(
            model='gemini-2.5-flash',
            name='summarization_agent',
            description='An agent that generates concise summaries of academic papers.',
            instruction='''
            You are a summarization agent that can:
            1. Receive academic papers from the research agent
            2. Generate concise, accurate summaries
            3. Highlight key findings and contributions
            4. Return structured summaries via A2A protocol
            '''
        )

    async def handle_message(self, message: A2AMessage):
        """Handle incoming A2A messages."""
        if message.message_type == 'papers_for_summary':
            papers = message.payload.get('papers', [])
            summaries = await self.summarize_papers(papers)
            
            # Send response back through A2A channel
            response = A2AMessage(
                from_agent=self.name,
                to_agent=message.from_agent,
                message_type='summary_response',
                payload={'summaries': summaries},
                correlation_id=message.correlation_id
            )
            await a2a_channel.send(response)

    async def summarize_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate summaries for a list of papers."""
        summaries = []
        for paper in papers:
            summary = await self.generate_summary(paper)
            summaries.append({
                'id': paper['id'],
                'title': paper['title'],
                'summary': summary,
                'url': paper['url']
            })
        return summaries

    async def generate_summary(self, paper: Dict[str, Any]) -> str:
        """Generate a concise summary of a single paper using the LLM."""
        prompt = f"""
        Paper Title: {paper['title']}
        Original Abstract: {paper['summary']}
        
        Generate a concise summary (2-3 sentences) highlighting the main contribution and findings.
        Focus on key innovations and practical implications.
        """
        
        response = await self.generate_content(prompt)
        return response.text

# Initialize the summarization agent
summarization_agent = SummarizationAgent()

# Register message handler with A2A channel
a2a_channel.register_handler('summarization_agent', summarization_agent.handle_message)