#!/usr/bin/env python3
"""
测试 Ollama 集成

这个脚本帮助你验证 Ollama 是否正确配置并可以与 ConnectOnion 一起工作。
"""

import sys
import requests
from connectonion import Agent


def check_ollama_service():
    """检查 Ollama 服务是否运行"""
    print("🔍 检查 Ollama 服务...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("✅ Ollama 服务正在运行")
            print(f"📦 已安装的模型: {len(models)} 个")
            for model in models:
                print(f"   - {model.get('name', 'unknown')}")
            return True, models
        else:
            print("❌ Ollama 服务响应异常")
            return False, []
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 Ollama 服务")
        print("💡 请运行: ollama serve")
        return False, []
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False, []


def test_basic_tool(model_name: str):
    """测试基本工具调用"""
    print(f"\n🧪 测试基本工具调用 (使用模型: {model_name})...")
    print("="*60)
    
    import os
    
    def greet(name: str) -> str:
        """向某人打招呼"""
        return f"你好，{name}！很高兴见到你。"
    
    try:
        # 设置环境变量以使用 Ollama
        os.environ["OPENAI_API_KEY"] = "ollama"
        os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
        
        # 创建测试 Agent
        agent = Agent(
            name="test_agent",
            system_prompt="你是一个友好的助手，擅长使用工具。当需要打招呼时，使用 greet 工具。",
            tools=[greet],
            model=model_name,  # 使用实际安装的模型
            max_iterations=3
        )
        
        # 测试查询
        test_query = "请向 '小明' 打个招呼"
        print(f"👤 测试问题: {test_query}")
        print("⏳ 等待响应...\n")
        
        response = agent.input(test_query)
        
        print(f"🤖 Agent 回复:")
        print(f"{response}")
        print("\n✅ 测试成功！Ollama 集成正常工作。")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n💡 排查建议:")
        print("1. 确认 Ollama 服务正在运行: ollama serve")
        print("2. 确认已下载模型: ollama run llama3.2")
        print("3. 检查模型名称是否正确")
        print("4. 尝试重启 Ollama 服务")
        return False


def print_recommendations():
    """打印使用建议"""
    print("\n" + "="*60)
    print("📚 推荐的 Ollama 模型")
    print("="*60)
    print("""
🇨🇳 中文友好：
  ollama run qwen2.5:7b        # 千问 7B（推荐中文使用）
  ollama run chatglm3          # ChatGLM3

⚡ 快速轻量：
  ollama run llama3.2          # Llama 3.2 1B
  ollama run llama3.2:3b       # Llama 3.2 3B（平衡）

🎯 高质量：
  ollama run mistral:7b        # Mistral 7B
  ollama run deepseek-r1:7b    # DeepSeek R1

📊 使用建议：
  - 开发测试: llama3.2 或 llama3.2:3b
  - 中文任务: qwen2.5:7b
  - 生产环境: 根据硬件选择更大模型
    """)


def main():
    """主函数"""
    print("🦙 Ollama + ConnectOnion 集成测试")
    print("="*60)
    
    # 检查服务
    service_ok, models = check_ollama_service()
    
    if not service_ok:
        print("\n❌ Ollama 服务未运行或配置不正确")
        print("\n📝 快速开始指南:")
        print("1. 安装 Ollama:")
        print("   macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh")
        print("   Windows: 访问 https://ollama.com/download")
        print("\n2. 下载模型:")
        print("   ollama run llama3.2")
        print("\n3. 启动服务:")
        print("   ollama serve")
        print("\n4. 重新运行此脚本:")
        print("   python test_ollama.py")
        return
    
    # 检查是否有可用模型
    if not models:
        print("\n⚠️  没有找到已安装的模型")
        print("💡 请先下载一个模型: ollama run llama3.2")
        return
    
    # 选择测试模型
    test_model = None
    
    # 优先使用 llama3.2
    for model in models:
        model_name = model.get("name", "")
        if "llama3.2" in model_name:
            test_model = model_name
            break
    
    # 如果没有 llama3.2，使用第一个可用模型
    if not test_model and models:
        test_model = models[0].get("name")
        print(f"\n⚠️  未找到 llama3.2 模型")
        print(f"💡 当前已安装: {[m.get('name') for m in models]}")
        print(f"💡 将使用 {test_model} 进行测试")
        print(f"💡 建议下载: ollama run llama3.2")
        print()
    
    if not test_model:
        print("\n❌ 没有可用的模型")
        return
    
    # 运行测试
    success = test_basic_tool(test_model)
    
    if success:
        print_recommendations()
        print("\n🎉 恭喜！你可以开始使用 Ollama 了！")
        print("\n📝 下一步:")
        print("1. 运行你的 Agent: python agent.py")
        print("2. 在 agent.py 中设置: USE_OLLAMA = True")
        print("3. 查看完整文档: cat OLLAMA-SETUP.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 测试中断")
        sys.exit(0)

