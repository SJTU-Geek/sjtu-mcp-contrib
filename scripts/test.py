# scripts/example_plugin.py
METADATA = {
    "name": "示例插件",
    "version": "1.0.0",
    "author": "开发者",
    "description": "示例插件说明",
    "entry_point": "execute"  # 推荐显式声明入口函数
}

def execute(input_data: dict) -> dict:
    """业务逻辑入口函数
    
    Args:
        input_data (dict): 输入的字典参数
        
    Returns:
        dict: 包含处理结果的字典
    """
    result = {
        "original_data": input_data,
        "processed": f"Processed by {METADATA['name']}",
        "success": True
    }
    return result

# 以下代码在模块导入时不会执行（最佳实践）
if __name__ == "__main__":
    # 本地测试代码
    print("本地测试结果:", execute({"test": True}))