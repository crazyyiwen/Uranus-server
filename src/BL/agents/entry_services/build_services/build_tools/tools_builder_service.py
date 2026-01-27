

from BL.agents.entry_services.build_services.build_tools.deep_agent_tools_service import DeepTools
from BL.agents.entry_services.build_services.build_tools.react_tools_service import ReactTools


class CommonReactTools:
    """
    Common React Tools Builder
    """
    def build_dynamic_tools(self):
        """
        
        Build and return the tools for Common React.
        Returns:
            list: A list of tools for Common React.
        """
        # Implementation for building Common React tools goes here
        return ReactTools()
    
    def build_dynamic_tools_with_mcp(self):
        """
        Build and return the tools for Common React.
        Returns:
            list: A list of tools for Common React.
        """
        # Implementation for building Common React tools goes here
        return ["Tool1", "Tool2", "Tool3"]
    
class DeepAgentTools:
    """
    Common React Tools Builder
    """
    def build_dynamic_tools(self):
        """
        Build and return the tools for Common React.
        Returns:
            list: A list of tools for Common React.
        """
        # Implementation for building Common React tools goes here
        return DeepTools()
    
    def build_dynamic_tools_with_mcp(self):
        """
        Build and return the tools for Common React.
        Returns:
            list: A list of tools for Common React.
        """
        # Implementation for building Common React tools goes here
        return ["Tool1", "Tool2", "Tool3"]