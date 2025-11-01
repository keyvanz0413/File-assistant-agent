#!/usr/bin/env python3
"""
文件助手 Agent - 使用 ConnectOnion 框架构建

这是一个智能文件管理助手，可以：
- 列出目录文件
- 读取文件内容
- 搜索关键字
- 统计文件数量
- AI 总结文件内容

支持本地 Ollama 模型和 OpenAI API。
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
from connectonion import Agent, llm_do

# 加载 .env 环境变量
load_dotenv()

def list_files(directory: str, extension: Optional[str] = None, recursive: bool = False) -> str:
    """
    列出输入路径下的所有文件

    参数:
        directory: 要列出的目录路径
        extension: 要列出的文件扩展名，可选（如 '.py', '.txt'）
        recursive: 是否递归搜索子目录，默认 False

    返回:
        一个字符串，包含所有文件的名称，每个文件占一行
    """
    try:
        path = Path(directory)

        if not path.exists():
            return f"目录 {directory} 不存在"

        if not path.is_dir():
            return f"路径 {directory} 不是一个目录"

        files = []
        
        if recursive:
            # 递归搜索所有子目录
            for file in path.rglob("*"):
                if file.is_file():
                    if extension is None or file.suffix == extension:
                        # 显示相对路径，让用户知道文件在哪个子目录
                        files.append(str(file.relative_to(path)))
        else:
            # 只搜索当前目录
            for file in path.iterdir():
                if file.is_file():
                    if extension is None or file.suffix == extension:
                        files.append(file.name)

        if not files:
            recursive_msg = "（包括子目录）" if recursive else ""
            ext_msg = f"（扩展名: {extension}）" if extension else ""
            return f"在目录 {directory} 下没有找到任何文件{recursive_msg}{ext_msg}"

        recursive_msg = "（包括子目录）" if recursive else ""
        total_count = len(files)
        
        # 智能截断：文件太多时，只返回摘要和前几个示例
        MAX_FILES_TO_SHOW = 50  # 最多显示 50 个文件
        
        if total_count > MAX_FILES_TO_SHOW:
            # 文件太多，返回统计信息和文件类型分布
            sorted_files = sorted(files)
            sample_files = sorted_files[:MAX_FILES_TO_SHOW]
            
            # 统计文件类型
            from collections import Counter
            extensions = [Path(f).suffix or '(无扩展名)' for f in files]
            ext_counts = Counter(extensions)
            
            result = f"在目录 {directory} 下找到 {total_count} 个文件{recursive_msg}\n\n"
            result += "📊 文件类型统计:\n"
            for ext, count in ext_counts.most_common():
                percentage = (count / total_count) * 100
                result += f"  {ext}: {count} 个 ({percentage:.1f}%)\n"
            
            result += f"\n📝 前 {MAX_FILES_TO_SHOW} 个文件示例:\n"
            result += "\n".join(f"  - {f}" for f in sample_files)
            result += f"\n\n💡 提示: 文件过多，仅显示前 {MAX_FILES_TO_SHOW} 个。如需查看特定类型，请使用 extension 参数过滤。"
            return result
        else:
            # 文件数量合理，返回完整列表
            result = f"在目录 {directory} 下找到 {total_count} 个文件{recursive_msg}:\n"
            result += "\n".join(f"  - {f}" for f in sorted(files))
            return result

    except Exception as e:
        return f"获取文件列表时出错: {str(e)}"


def read_file(file_path: str) -> str:
    """
    读取文件内容

    参数:
        file_path: 要读取的文件路径

    返回:
       一个字符串，包含文件的内容
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"文件 {file_path} 不存在"
        if not path.is_file():
            return f"路径 {file_path} 不是一个文件"
        content = path.read_text(encoding="utf-8")

        if len(content) > 5000:
            preview = content[:5000]
            return f"文件 {file_path} 的内容过长，显示前5000字符:\n{preview}...\n(总字符数: {len(content)})"
        
        return f"文件 {file_path} 的内容:\n{content}"

    except UnicodeDecodeError:
        return f"错误：无法读取文件 '{file_path}'（可能是二进制文件）"
    except PermissionError:
        return f"错误：没有权限读取文件 '{file_path}'"  
    except Exception as e:
        return f"读取文件时出错: {str(e)}"


def search_files(directory: str, keyword: str, recursive: bool = False) -> str:
    """
    在输入路径下搜索包含关键字的文件

    参数:
        directory: 要搜索的目录路径
        keyword: 要搜索的关键字
        recursive: 是否递归搜索子目录，默认 False

    返回:
       一个字符串，包含所有包含关键字的文件的名称
    """
    try:
        path = Path(directory)
        if not path.exists():
            return f"目录 {directory} 不存在"
        if not path.is_dir():
            return f"路径 {directory} 不是一个目录"
        
        files = []
        
        # 选择遍历方式
        file_iterator = path.rglob("*") if recursive else path.iterdir()
        
        for file in file_iterator:
            if file.is_file():
                try:
                    content = file.read_text(encoding="utf-8")
                    if keyword.lower() in content.lower():
                        # 显示相对路径
                        relative_path = str(file.relative_to(path)) if recursive else file.name
                        files.append(relative_path)
                except:
                    # 跳过无法读取的文件（二进制文件、权限问题等）
                    continue
        
        if not files:
            recursive_msg = "（包括子目录）" if recursive else ""
            return f"在目录 {directory} 下没有找到包含关键字 '{keyword}' 的文件{recursive_msg}"
        
        recursive_msg = "（包括子目录）" if recursive else ""
        total_count = len(files)
        
        # 智能截断
        MAX_FILES_TO_SHOW = 50
        
        if total_count > MAX_FILES_TO_SHOW:
            sorted_files = sorted(files)
            sample_files = sorted_files[:MAX_FILES_TO_SHOW]
            
            result = f"在目录 {directory} 下找到 {total_count} 个包含关键字 '{keyword}' 的文件{recursive_msg}\n\n"
            result += f"📝 前 {MAX_FILES_TO_SHOW} 个匹配文件:\n"
            result += "\n".join(f"  - {f}" for f in sample_files)
            result += f"\n\n💡 共找到 {total_count} 个匹配文件，仅显示前 {MAX_FILES_TO_SHOW} 个。"
            return result
        else:
            result = f"在目录 {directory} 下找到 {total_count} 个包含关键字 '{keyword}' 的文件{recursive_msg}:\n"
            result += "\n".join(f"  - {f}" for f in sorted(files))
            return result
    
    except Exception as e:
        return f"搜索文件时出错: {str(e)}"


def count_files(directory: str, extension: Optional[str] = None, recursive: bool = False) -> str:
    """
    统计输入路径下的文件数量

    参数:
        directory: 要统计的目录路径
        extension: 文件扩展名过滤（可选）
        recursive: 是否递归统计子目录，默认 False

    返回:
       一个字符串，包含目录下的文件数量
    """
    try:
        path = Path(directory)
        if not path.exists():
            return f"目录 {directory} 不存在"
        if not path.is_dir():
            return f"路径 {directory} 不是一个目录"
        
        # 选择遍历方式
        if recursive:
            files = [f for f in path.rglob("*") if f.is_file()]
        else:
            files = [f for f in path.iterdir() if f.is_file()]
        
        if extension:
            files = [f for f in files if f.suffix == extension]
        
        recursive_msg = "（包括子目录）" if recursive else ""
        ext_msg = f"（{extension} 文件）" if extension else ""
        return f"目录 '{directory}' 下共有 {len(files)} 个文件{ext_msg}{recursive_msg}"
        
    except Exception as e:
        return f"错误：{str(e)}"


def summarize_file(file_path: str, max_chars: int = 10000) -> str:
    """
    使用 LLM 智能总结文件内容

    参数:
        file_path: 要总结的文件路径
        max_chars: 发送给 LLM 的最大字符数，默认 10000（避免超过上下文限制）

    返回:
       一个字符串，包含 LLM 生成的文件内容摘要
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"文件 {file_path} 不存在"
        if not path.is_file():
            return f"路径 {file_path} 不是一个文件"
        
        content = path.read_text(encoding="utf-8")
        
        # 如果文件内容很短，直接返回
        if len(content) < 100:
            return f"文件内容较短：{content}"
        
        # 如果文件太长，截断后再总结
        content_to_summarize = content
        is_truncated = False
        if len(content) > max_chars:
            content_to_summarize = content[:max_chars]
            is_truncated = True
        
        # 使用 LLM 进行智能总结
        prompt = f"""请总结以下文件的主要内容，用 3-5 句话概括：

文件路径：{file_path}
文件大小：{len(content)} 字符

内容：
{content_to_summarize}
"""
        
        if is_truncated:
            prompt += f"\n（注意：文件内容过长，仅显示前 {max_chars} 字符）"
        
        summary = llm_do(prompt)
        
        result = f"📄 文件总结 ({file_path}):\n{summary}"
        if is_truncated:
            result += f"\n\n💡 提示：文件总长度为 {len(content)} 字符，总结基于前 {max_chars} 字符"
        
        return result
    
    except UnicodeDecodeError:
        return f"错误：无法读取文件 '{file_path}'（可能是二进制文件）"
    except Exception as e:
        return f"总结文件时出错: {str(e)}"


if __name__ == "__main__":
    # ========== 工具定义 ==========
    tools = [
        list_files,
        read_file,
        search_files,
        count_files,
        summarize_file
    ]

    # ========== 模型配置 ==========
    # 选择使用的模型类型
    USE_OLLAMA = True  # True: 使用本地 Ollama, False: 使用 OpenAI API
    
    if USE_OLLAMA:
        # 配置 Ollama 本地模型
        # 确保 Ollama 服务正在运行: ollama serve
        # 确保已下载模型: ollama run llama3.2
        os.environ["OPENAI_API_KEY"] = "ollama"
        os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
        
        agent = Agent(
            name="file_assistant",
            system_prompt="prompt.md",
            tools=tools,
            max_iterations=10,
            model="llama3.2"  # 推荐: llama3.2, llama3.2:3b, qwen2.5:7b
        )
        print("🦙 使用 Ollama 本地模型: llama3.2")
    else:
        # 配置 OpenAI API
        # 需要在 .env 文件中设置 OPENAI_API_KEY
        agent = Agent(
            name="file_assistant",
            system_prompt="prompt.md",
            tools=tools,
            max_iterations=10,
            model="gpt-4o-mini"  # 可选: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
        )
        print("🤖 使用 OpenAI API: gpt-4o-mini")

    # ========== 交互循环 ==========
    print("\n文件助手已启动！输入 'exit', 'quit' 或 '退出' 来结束对话。\n")
    
    while True:
        user_input = input("👤 你: ")
        
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("👋 再见！")
            break
        
        if not user_input.strip():
            continue
        
        try:
            # 调用 Agent 处理用户输入
            response = agent.input(user_input)
            print(f"🤖 助手: {response}\n")
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")
            print("💡 提示: 请检查模型配置是否正确\n")