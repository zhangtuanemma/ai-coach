# AI 问题处理教练 - 部署说明

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
streamlit run streamlit_app.py
```

3. 浏览器会自动打开 `http://localhost:8501`

## 部署到 Streamlit Cloud（免费）

### 步骤：

1. **上传到 GitHub**
   - 创建一个 GitHub 仓库
   - 上传这三个文件：
     - `streamlit_app.py`
     - `ai_coach_flexible.py`
     - `requirements.txt`

2. **部署到 Streamlit Cloud**
   - 访问 https://share.streamlit.io/
   - 用 GitHub 账号登录
   - 点击 "New app"
   - 选择你的仓库和 `streamlit_app.py`
   - 点击 "Deploy"

3. **设置 API Key（重要）**
   - 在 Streamlit Cloud 的 App settings 中
   - 添加 Secret：`ANTHROPIC_API_KEY = "你的API密钥"`
   - 或者让用户在侧边栏输入自己的 API Key

4. **分享链接**
   - 部署完成后会得到一个链接，如：`https://你的用户名-ai-coach.streamlit.app`
   - 把这个链接分享给别人就可以了

## 使用说明

- 用户打开网页后，在侧边栏输入 API Key（如果你没有在 Streamlit Cloud 设置）
- 在输入框输入问题，开始对话
- 点击"清空对话"可以重新开始

## 注意事项

- API Key 可以设置在 Streamlit Cloud 的 Secrets 中（推荐）
- 也可以让每个用户输入自己的 API Key
- 免费版 Streamlit Cloud 有使用限制，但对小团队够用
