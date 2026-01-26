"""
Dynamic tool builder for agentic workflows.
Completely configuration-driven with no hardcoding.

All tool behavior is defined in the workflow JSON through the _meta.executor configuration.
"""
from typing import Dict, Any, Callable, Optional
from langchain_core.tools import StructuredTool
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field, create_model
import json
import importlib


def _map_json_type_to_python(json_type: str) -> type:
    """Map JSON schema types to Python types"""
    type_mapping = {
        "string": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "object": dict,
        "array": list
    }
    return type_mapping.get(json_type, str)


def _create_dynamic_schema(name: str, properties: Dict[str, Any], required: list) -> type:
    """
    Create a dynamic Pydantic model from JSON schema properties.

    Args:
        name: Name for the schema
        properties: JSON schema properties
        required: List of required field names

    Returns:
        Dynamically created Pydantic model
    """
    fields = {}

    for prop_name, prop_schema in properties.items():
        field_type = _map_json_type_to_python(prop_schema.get("type", "string"))
        field_description = prop_schema.get("description", "")

        # Set as optional if not in required list
        if prop_name in required:
            fields[prop_name] = (field_type, Field(description=field_description))
        else:
            fields[prop_name] = (field_type, Field(default=None, description=field_description))

    # Create dynamic Pydantic model
    if fields:
        return create_model(f"{name}Input", **fields)
    else:
        return create_model(f"{name}Input")


def _load_executor(executor_config: Dict[str, Any]) -> Optional[Callable]:
    """
    Dynamically load an executor function based on configuration.

    Configuration format:
    {
        "module": "path.to.module",           # Python module path
        "function": "function_name",           # Function to call
        "wrapper": "optional_wrapper_arg"      # Optional argument to pass
    }

    Args:
        executor_config: Executor configuration from JSON

    Returns:
        Callable function or None if loading fails
    """
    if not executor_config:
        return None

    try:
        module_path = executor_config.get("module")
        function_name = executor_config.get("function")

        if not module_path or not function_name:
            return None

        # Dynamically import the module
        module = importlib.import_module(module_path)

        # Get the function from the module
        executor_func = getattr(module, function_name, None)

        return executor_func

    except (ImportError, AttributeError):
        # Module or function not found - silently return None
        return None
    except Exception as e:
        return None


def build_ssf_call_tool(tool_config: Dict[str, Any]) -> Optional[StructuredTool]:
    """
    Build a server-side function (SSF) tool dynamically from configuration.

    The tool behavior is completely defined by the JSON configuration.
    No hardcoding - all execution logic is loaded dynamically.

    Configuration structure in _meta:
    {
        "functionId": "...",               # Function identifier
        "moduleId": "...",                 # Module identifier
        "type": "ssf-call",                # Tool type
        "executor": {                      # Optional: custom executor
            "module": "BL.module.path",    # Module to import
            "function": "executor_function", # Function to call
            "wrapper": "wrapper_arg"        # Optional: wrapper argument
        }
    }

    Args:
        tool_config: Complete tool configuration from JSON

    Returns:
        StructuredTool or None if build fails
    """
    try:
        name = tool_config["name"]
        description = tool_config.get("description", "SSF call tool")
        schema = tool_config.get("config", {}).get("schema", {})
        meta = tool_config.get("config", {}).get("_meta", {})

        # Extract schema properties
        properties = schema.get("properties", {})
        required = schema.get("required", [])

        # Create dynamic Pydantic model from schema
        InputSchema = _create_dynamic_schema(name, properties, required)

        # Extract metadata
        function_id = meta.get("functionId", "unknown")
        module_id = meta.get("moduleId", "unknown")
        tool_type = meta.get("type", "ssf-call")

        # Load custom executor if configured
        executor_config = meta.get("executor")
        custom_executor = _load_executor(executor_config) if executor_config else None

        def _execute(**kwargs):
            """Execute the SSF call dynamically based on configuration"""

            # If custom executor is configured, use it
            if custom_executor:
                try:
                    # Get wrapper argument if specified
                    wrapper_arg = executor_config.get("wrapper")

                    # Prepare execution data
                    data = kwargs.get("data", kwargs)

                    # Execute with wrapper if specified, otherwise pass data directly
                    if wrapper_arg:
                        result = custom_executor(wrapper_arg, data)
                    else:
                        result = custom_executor(data)

                    # Return JSON string for consistency
                    return json.dumps(result) if isinstance(result, dict) else str(result)

                except Exception as e:
                    return json.dumps({
                        "status": "error",
                        "tool": name,
                        "executor_config": executor_config,
                        "error": str(e),
                        "message": f"Error executing custom executor for {name}"
                    })

            # Default: Placeholder for actual SSF implementation
            return json.dumps({
                "status": "pending_implementation",
                "function_id": function_id,
                "module_id": module_id,
                "tool_name": name,
                "tool_type": tool_type,
                "input": kwargs,
                "message": f"SSF call to {name} - awaiting production implementation"
            })

        return StructuredTool(
            name=name,
            description=description,
            func=_execute,
            args_schema=InputSchema,
        )

    except Exception as e:
        print(f"Error building SSF tool '{tool_config.get('name', 'unknown')}': {e}")
        return None


def build_partial_view_tool(tool_config: Dict[str, Any]) -> Optional[StructuredTool]:
    """
    Build a partial view rendering tool dynamically from configuration.

    Configuration structure in _meta:
    {
        "type": "partial-view",
        "uiView": "{...}",                 # JSON string of UI configuration
        "executor": {                       # Optional: custom renderer
            "module": "path.to.renderer",
            "function": "render_function"
        }
    }

    Args:
        tool_config: Complete tool configuration from JSON

    Returns:
        StructuredTool or None if build fails
    """
    try:
        name = tool_config["name"]
        description = tool_config.get("description", "Partial view tool")
        schema = tool_config.get("config", {}).get("schema", {})
        meta = tool_config.get("config", {}).get("_meta", {})

        # Extract UI view configuration
        ui_view_json = meta.get("uiView", "{}")
        try:
            ui_view = json.loads(ui_view_json)
        except:
            ui_view = {}

        # Extract schema properties
        properties = schema.get("properties", {})
        required = schema.get("required", [])

        # Create dynamic Pydantic model
        InputSchema = _create_dynamic_schema(name, properties, required)

        # Load custom executor if configured
        executor_config = meta.get("executor")
        custom_executor = _load_executor(executor_config) if executor_config else None

        def _render(**kwargs):
            """Render partial view dynamically based on configuration"""

            # If custom executor is configured, use it
            if custom_executor:
                try:
                    render_data = {
                        "view_config": ui_view,
                        "input": kwargs
                    }
                    result = custom_executor(render_data)
                    return json.dumps(result) if isinstance(result, dict) else str(result)

                except Exception as e:
                    return json.dumps({
                        "status": "error",
                        "tool": name,
                        "error": str(e),
                        "message": f"Error rendering partial view {name}"
                    })

            # Default: Placeholder for actual partial view rendering
            view_id = ui_view.get("ViewUniqueId", "unknown")
            view_name = ui_view.get("Name", name)
            instruction = ui_view.get("Instruction", "")

            return json.dumps({
                "status": "pending_implementation",
                "RenderingId": view_id,
                "ContentType": "partial_view",
                "ViewName": view_name,
                "Template": f"<Placeholder UI Template for {view_name}>",
                "TemplateDescription": instruction,
                "OverridesApplied": kwargs,
                "message": f"Partial view {name} - awaiting production implementation. Reference as [partial_view: {view_id}]"
            })

        return StructuredTool(
            name=name,
            description=description,
            func=_render,
            args_schema=InputSchema,
        )

    except Exception as e:
        return None


def build_agent_tool(name: str, description: str, agent_graph) -> Optional[StructuredTool]:
    """
    Build an agent-as-a-tool dynamically.

    This creates a tool that delegates to a sub-agent graph.
    The sub-agent is invoked with the provided input and returns its result.

    Args:
        name: Tool name
        description: Tool description
        agent_graph: Compiled sub-agent graph to invoke

    Returns:
        StructuredTool or None if build fails
    """
    try:
        class AgentInput(BaseModel):
            input: str = Field(description="Input message or task for the sub-agent")

        def _invoke_agent(input: str):
            """Invoke the sub-agent graph"""
            try:
                # Invoke the sub-agent with the input
                result = agent_graph.invoke({
                    "messages": [HumanMessage(content=input)],
                    "iteration_count": 0
                })

                # Extract the final message from the result
                messages = result.get("messages", [])
                if messages:
                    last_message = messages[-1]
                    if hasattr(last_message, "content"):
                        return last_message.content
                    return str(last_message)

                return f"Sub-agent {name} executed successfully"

            except Exception as e:
                return f"Error executing sub-agent {name}: {str(e)}"

        return StructuredTool(
            name=name,
            description=description,
            func=_invoke_agent,
            args_schema=AgentInput,
        )

    except Exception as e:
        return None
