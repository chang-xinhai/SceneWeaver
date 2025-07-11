# Socket Communication with generate_indoors_mcp.py

This modified version of `generate_indoors_mcp.py` allows you to control Blender scene generation through socket communication, making the Blender UI interactive between actions.

## Features

- **Socket Server**: Listens on `localhost:12345` for JSON commands
- **Interactive Blender**: UI remains responsive between actions
- **Command Queue**: Actions are queued and processed sequentially
- **Real-time Response**: Immediate feedback for status commands

## Usage

### 1. Start Blender with the Modified Script

```bash
blender --python infinigen_examples/generate_indoors_mcp.py -- --save_dir debug/
```

The script will:
- Start a socket server on `localhost:12345`
- Register a Blender timer to process incoming commands
- Keep the Blender UI interactive
- Display usage information in the console

### 2. Send Commands via Socket

You can send commands using the provided client script or any socket client.

#### Using the Example Client

```bash
# Check if server is running
python infinigen_examples/socket_client_example.py --action ping

# Get server status
python infinigen_examples/socket_client_example.py --action status

# Initialize physics scene
python infinigen_examples/socket_client_example.py --action init_physcene --iter 0 --save_dir debug/

# Initialize metascene
python infinigen_examples/socket_client_example.py --action init_metascene --iter 1 --save_dir debug/

# Stop the server
python infinigen_examples/socket_client_example.py --action stop_server
```

### 3. Command Format

Commands are sent as JSON objects with the following structure:

```json
{
    "action": "init_physcene",
    "iter": 0,
    "description": "",
    "save_dir": "debug/",
    "json_name": "",
    "inplace": ""
}
```

#### Available Actions

- **Special Commands** (processed immediately):
  - `ping`: Check if server is running
  - `status`: Get server status and queue information
  - `stop_server`: Stop the socket server

- **Scene Generation Commands** (queued for processing):
  - `init_physcene`: Initialize physics scene
  - `init_metascene`: Initialize metascene  
  - `init_gpt`: Initialize GPT
  - Other actions from the original script...

#### Command Parameters

- `action` (required): The action to perform
- `iter` (optional): Iteration number (default: 0)
- `description` (optional): Description for the action
- `save_dir` (optional): Directory to save results (default: "debug/")
- `json_name` (optional): JSON filename
- `inplace` (optional): Inplace flag

### 4. Manual Socket Communication

You can also send commands manually using any socket client:

```python
import socket
import json

# Connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12345))

# Send command
command = {"action": "ping"}
s.send(json.dumps(command).encode('utf-8'))

# Receive response
response = s.recv(1024)
print(json.loads(response.decode('utf-8')))

s.close()
```

## How It Works

1. **Socket Server**: Runs in a separate thread, listening for connections
2. **Command Queue**: Thread-safe queue stores incoming commands
3. **Blender Timer**: Registered timer function checks for queued commands every 0.1 seconds
4. **Action Processing**: Commands are processed using the original scene generation logic
5. **UI Updates**: Blender UI is refreshed after each action completes

## Benefits

- **Interactive Development**: Blender UI remains usable while waiting for commands
- **Remote Control**: Send commands from external scripts or applications
- **Batch Processing**: Queue multiple commands for sequential execution
- **Real-time Feedback**: Get immediate status updates and error messages
- **Flexible Integration**: Easy to integrate with other tools and workflows

## Error Handling

- Invalid JSON commands return error responses
- Exceptions during action processing are logged and returned
- Server can be gracefully stopped with the `stop_server` command
- Cleanup function ensures proper resource management

## Notes

- The socket server only accepts connections from localhost for security
- Commands are processed sequentially in the order they are received
- Large operations may take time; the UI remains responsive during processing
- The server automatically handles client disconnections and reconnections 