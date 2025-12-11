from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json
import asyncio
from queue import Queue

@dataclass
class A2AMessage:
    from_agent: str
    to_agent: str
    message_type: str
    payload: Dict[str, Any]
    correlation_id: str
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_json(self) -> str:
        return json.dumps({
            'from': self.from_agent,
            'to': self.to_agent,
            'type': self.message_type,
            'payload': self.payload,
            'correlationId': self.correlation_id,
            'timestamp': self.timestamp
        })

class A2AChannel:
    """Simple A2A communication channel using a message queue."""
    
    def __init__(self):
        self.message_queue = Queue()
        self.handlers = {}

    async def send(self, message: A2AMessage):
        """Send a message to another agent."""
        self.message_queue.put(message)
        # Process message asynchronously
        await self._process_message(message)

    async def _process_message(self, message: A2AMessage):
        """Process an incoming message."""
        if message.to_agent in self.handlers:
            await self.handlers[message.to_agent](message)

    def register_handler(self, agent_name: str, handler):
        """Register a message handler for an agent."""
        self.handlers[agent_name] = handler

# Initialize the A2A channel
a2a_channel = A2AChannel()