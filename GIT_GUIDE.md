# 📤 Git 上传指南

## 快速上传到 GitHub

### 1️⃣ 初始化 Git 仓库

```bash
cd /Users/keyvanzhuo/Documents/CodeProjects/ConnetOnion/file-assistant
git init
```

### 2️⃣ 添加文件到暂存区

```bash
# 添加所有文件（.gitignore 会自动忽略不需要的文件）
git add .

# 查看将要提交的文件
git status
```

### 3️⃣ 创建第一次提交

```bash
git commit -m "🎉 Initial commit: File Assistant with Ollama support"
```

### 4️⃣ 创建 GitHub 仓库

1. 访问 [GitHub](https://github.com/new)
2. 创建新仓库（例如：`file-assistant`）
3. **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

### 5️⃣ 连接远程仓库并推送

```bash
# 添加远程仓库（替换为你的 GitHub 用户名和仓库名）
git remote add origin https://github.com/YOUR_USERNAME/file-assistant.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 🔍 验证上传的文件

以下文件会被上传到 Git：

```
✅ agent.py              # 主程序
✅ prompt.md             # 系统提示词
✅ requirements.txt      # 依赖列表
✅ env.example          # 配置模板
✅ README.md            # 项目文档
✅ CHANGELOG.md         # 更新日志
✅ GIT_GUIDE.md         # 本指南
✅ .gitignore           # Git 忽略规则
✅ test_files/          # 测试文件
✅ test_ollama.py       # Ollama 测试脚本
```

以下文件会被 **忽略**（不会上传）：

```
❌ __pycache__/         # Python 缓存
❌ test_dir/            # 大型测试数据
❌ .env                 # 私密环境变量
❌ *.pyc                # 编译文件
❌ .DS_Store            # Mac 系统文件
```

## 📝 后续更新

当你修改代码后：

```bash
# 查看修改
git status

# 添加修改的文件
git add .

# 提交
git commit -m "描述你的修改"

# 推送到 GitHub
git push
```

## 🎨 提交信息规范

建议使用语义化提交信息：

```bash
git commit -m "✨ feat: 添加新功能"
git commit -m "🐛 fix: 修复 bug"
git commit -m "📝 docs: 更新文档"
git commit -m "♻️ refactor: 重构代码"
git commit -m "⚡ perf: 性能优化"
git commit -m "✅ test: 添加测试"
```

## 🔐 保护隐私

**重要提醒：**
- ✅ `.env` 文件已在 `.gitignore` 中，不会上传
- ✅ 永远不要将 API Key 提交到 Git
- ✅ 使用 `env.example` 作为配置模板

## 💡 常见问题

### Q: 如何删除已经提交的敏感文件？

```bash
# 从 Git 历史中删除文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push origin --force --all
```

### Q: 如何撤销最后一次提交？

```bash
# 保留修改，撤销提交
git reset --soft HEAD~1

# 放弃修改，撤销提交
git reset --hard HEAD~1
```

---

**🎉 现在你的项目已经准备好上传到 GitHub 了！**

