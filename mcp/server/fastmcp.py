
class FastMCP:
    def __init__(self, name="test"): 
        self.name = name
    def tool(self, name=None, description=None):
        def decorator(func): return func
        return decorator
    def run(self, transport="stdio"): pass
