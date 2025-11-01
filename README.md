# 🗂️ File Assistant

一个基于 [ConnectOnion](https://github.com/wanghaisheng/ConnectOnion) 框架构建的智能文件管理助手，支持本地 Ollama 模型和 OpenAI API。

## ✨ 功能特性

- 📁 **列出文件** - 浏览目录，支持扩展名过滤和递归搜索
- 📖 **读取内容** - 智能读取文件，自动处理长文件
- 🔍 **关键字搜索** - 在文件中搜索特定关键字
- 📊 **统计分析** - 统计文件数量和类型分布
- 🤖 **AI 总结** - 使用 LLM 智能总结文件内容
- 🦙 **本地运行** - 支持 Ollama 本地模型，完全免费

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置模型

#### 方案 A：使用本地 Ollama（推荐）

**优势：** 完全免费、数据隐私、可离线使用

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 下载模型
ollama run llama3.2

# 3. 验证服务
curl http://localhost:11434/api/tags
```

在 `agent.py` 中设置：
```python
USE_OLLAMA = True  # 使用 Ollama
```

#### 方案 B：使用 OpenAI API

创建 `.env` 文件：
```bash
cp env.example .env
```

编辑 `.env`：
```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

在 `agent.py` 中设置：
```python
USE_OLLAMA = False  # 使用 OpenAI API
```

### 3. 运行助手

```bash
python agent.py
```

## 💬 使用示例

```
👤 你: 列出 test_files 目录下的所有文件

🤖 助手: 在目录 test_files 下找到 2 个文件:
  - README.md
  - demo.txt

👤 你: 读取 demo.txt 的内容

🤖 助手: 文件 demo.txt 的内容:
Hello, this is a demo file!

👤 你: 总结一下 README.md

🤖 助手: 📄 文件总结 (test_files/README.md):
这是一个测试文件夹，包含用于演示文件助手功能的示例文件。
主要用于测试文件列表、读取和搜索等功能。
```

## 🛠️ 可用工具

| 工具 | 说明 | 参数 |
|------|------|------|
| `list_files` | 列出目录文件 | `directory`, `extension`, `recursive` |
| `read_file` | 读取文件内容 | `file_path` |
| `search_files` | 搜索关键字 | `directory`, `keyword`, `recursive` |
| `count_files` | 统计文件数量 | `directory`, `extension`, `recursive` |
| `summarize_file` | AI 总结内容 | `file_path`, `max_chars` |

## 🦙 Ollama 模型推荐

| 模型 | 大小 | 特点 | 命令 |
|------|------|------|------|
| **llama3.2** | 2GB | 快速轻量 ⚡ | `ollama run llama3.2` |
| **llama3.2:3b** | 2GB | 平衡性能 ⚖️ | `ollama run llama3.2:3b` |
| **qwen2.5:7b** | 4.7GB | 中文优化 🇨🇳 | `ollama run qwen2.5:7b` |
| **mistral:7b** | 4GB | 高质量输出 ⭐ | `ollama run mistral:7b` |

更多模型请访问：https://ollama.com/library

## 📁 项目结构

```
file-assistant/
├── agent.py              # 主程序
├── prompt.md             # 系统提示词
├── requirements.txt      # Python 依赖
├── env.example          # 环境变量模板
├── test_files/          # 测试文件
│   ├── demo.txt
│   └── README.md
├── test_ollama.py       # Ollama 集成测试
└── README.md            # 项目文档
```

## 🧪 测试 Ollama 配置

如果你想测试 Ollama 是否正确配置：

```bash
python test_ollama.py
```

这个脚本会：
- ✅ 检查 Ollama 服务状态
- ✅ 列出已安装的模型
- ✅ 测试基本工具调用
- ✅ 提供配置建议

## 🔧 常见问题

### 问题 1：Ollama 连接失败

```
ValueError: Unknown model 'llama3.2'
```

**解决方案：**
```bash
# 确保 Ollama 服务正在运行
ollama serve

# 确保模型已下载
ollama run llama3.2
```

### 问题 2：OpenAI API 错误

```
Error: Invalid API key
```

**解决方案：**
- 检查 `.env` 文件中的 `OPENAI_API_KEY` 是否正确
- 确保 API key 有效且有余额

### 问题 3：文件过大无法处理

**解决方案：**
- 工具会自动截断超长内容
- `read_file` 限制为 5000 字符
- `summarize_file` 限制为 10000 字符
- 可以在函数参数中调整 `max_chars`

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [ConnectOnion 文档](https://github.com/wanghaisheng/ConnectOnion)
- [Ollama 官网](https://ollama.com/)
- [OpenAI API](https://platform.openai.com/)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
