# EXAMPLE PLUGIN
METADATA = {
    "name": "arithmetic",
    "version": "1.0.0",
    "author": "开发者",
    "description": "arithmetic operations",
    "tools": [
        {
            "name": "add",
            "description": "Add two numbers",
            "entryPoint": "add",
            "schema": {
                "title": "add",
                "description": "add two numbers.",
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer"
                    },
                    "b": {
                        "type": "integer"
                    }
                },
                "required": [
                    "a",
                    "b"
                ]
            }
	    },
        {
            "name": "subtract",
            "description": "subtract two numbers.",
            "entryPoint": "subtract",
            "schema": {
                "title": "subtract",
                "description": "subtract two numbers.",
                "type": "object",
                "properties": {
                    "a": {
                        "description": "subtractee",
                        "type": "integer"
                    },
                    "b": {
                        "description": "subtractor",
                        "type": "integer"
                    }
                },
                "required": [
                    "a",
                    "b"
                ]
            }
	    },
        {
            "name": "multiply",
            "description": "multiply two numbers.",
            "entryPoint": "multiply",
            "schema": {
                "title": "multiply",
                "description": "multiply two numbers.",
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer"
                    },
                    "b": {
                        "type": "integer"
                    }
                },
                "required": [
                    "a",
                    "b"
                ]
            }
	    },
        {
            "name": "divide",
            "description": "divide two numbers",
            "entryPoint": "divide",
            "schema": {
                "title": "divide",
                "description": "divide two numbers.",
                "type": "object",
                "properties": {
                    "a": {
                        "description": "dividend",
                        "type": "integer"
                    },
                    "b": {
                        "description": "divisor",
                        "type": "integer"
                    }
                },
                "required": [
                    "a",
                    "b"
                ]
            }
	    }
    ]
}

def add(a: int, b:int) -> int:
    """加法函数
    
    Args:
        a (int): 加数
        b (int): 加数
        
    Returns:
        int: 加法结果
    """
    return a+b

def subtract(a: int, b:int) -> int:
    """减法函数
    
    Args:
        a (int): 被减数
        b (int): 减数
        
    Returns:
        int: 减法结果
    """
    return a-b

def multiply(a: int, b:int) -> int:
    """乘法函数
    
    Args:
        a (int): 乘数
        b (int): 乘数
        
    Returns:
        int: 乘法结果
    """
    return a*b

def divide(a: int, b:int) -> int:
    """除法函数
    
    Args:
        a (int): 被除数
        b (int): 除数
        
    Returns:
        int: 除法结果
    """
    return a/b

# 以下代码可供本地测试
if __name__ == "__main__":
    a = 240
    b = 3
    print("a+b=", add(a, b))
    print("a-b=", subtract(a, b))
    print("a*b=", multiply(a, b))
    print("a/b=", divide(a, b))