from typing import Any, Dict, List, Callable
import inspect
import json

class ConverseToolManager:
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
    
    def register_tool(self, name: str, func: Callable, description: str, input_schema: Dict):
        """
        Register a new tool with the system
        """
        self._tools[name] = {
            'function': func,
            'description': description,
            'input_schema': input_schema
        }

    def get_tools(self) -> Dict[str, List[Dict]]:
        """
        Generate the tools specification for the Bedrock Runtime API
        """
        tool_specs = []
        for name, tool in self._tools.items():
            tool_specs.append({
                'toolSpec': {
                    'name': name,
                    'description': tool['description'],
                    'inputSchema': tool['input_schema']
                }
            })
        
        return {'tools': tool_specs}

    def execute_tool(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool based on the agent's request
        
        Args:
            payload: Dict containing toolUseId, name, and input
        
        Returns:
            Dict containing toolUseId and the tool's output
        """
        tool_use_id = payload['toolUseId']
        tool_name = payload['name']
        tool_input = payload['input']

        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        try:
            tool_func = self._tools[tool_name]['function']
            result = tool_func(**tool_input)
            
            return {
                'toolUseId': tool_use_id,
                'content': [{
                    'text': str(result)
                }],
                'status': 'success'
            }
        except Exception as e:
            return {
                'toolUseId': tool_use_id,
                'content': [{
                    'text': str(e)
                }],
                'status': 'error'
            }

    def clear_tools(self):
        """Clear all registered tools"""
        self._tools.clear()
    