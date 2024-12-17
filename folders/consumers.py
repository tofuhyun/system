import json
from channels.generic.websocket import AsyncWebsocketConsumer


class FolderUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection."""
        self.group_name = 'folder_updates'

        # Add the WebSocket to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Remove the WebSocket from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive data from the WebSocket.
        Expected payload:
        {
            "message": "<your_message>"
        }
        """
        try:
            # Parse the incoming JSON data
            data = json.loads(text_data)
            message = data.get('message', '')

            # Broadcast the message to the group
            if message:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'folder_message',  # Event type handled by `folder_message`
                        'message': message
                    }
                )
        except json.JSONDecodeError:
            # Handle invalid JSON error
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON payload'
            }))

    async def folder_message(self, event):
        """
        Handle messages sent to the group.
        Expected `event` structure:
        {
            "type": "folder_message",
            "message": "<your_message>"
        }
        """
        message = event.get('message', '')

        # Send the message back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
