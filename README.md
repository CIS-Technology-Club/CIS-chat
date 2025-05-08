# CIS Web AI 应用

这是一个基于Flask和Google Gemini API的Web应用，为Cebu International School (CIS)提供智能问答服务。

## 功能

- 使用Google Gemini API处理用户问题
- 基于预先加载的知识库(database.md)回答关于CIS的问题
- 提供易用的Web界面与AI助手交互

## 环境要求

- Python 3.9或更高版本
- Google Gemini API密钥

## 安装

1. 克隆此仓库：
   ```
   git clone [repository-url]
   cd CIS_web_AI
   ```

2. 创建并激活虚拟环境：
   ```
   python -m venv .venv
   source .venv/bin/activate  # 在Windows上使用 .venv\Scripts\activate
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
   注：如果requirements.txt不存在，可运行：
   ```
   pip install flask flask-cors google-generativeai
   ```

## 配置

在运行应用前，需要设置Gemini API密钥：

```
export GEMINI_API_KEY=您的API密钥
```

Windows系统使用：
```
set GEMINI_API_KEY=您的API密钥
```

## 运行应用

1. 启动Flask服务器：
   ```
   python server.py
   ```

2. 打开浏览器访问：
   ```
   http://127.0.0.1:8042
   ```

## 项目结构

- `server.py`: Flask服务器代码，处理Web请求并与Gemini API交互
- `index.html`: 前端界面，提供用户交互
- `database.md`: 知识库文件，包含关于CIS的信息
- `gemini.py`: 直接使用Gemini API的示例代码

## 使用说明

1. 在网页界面的输入框中输入关于CIS的问题
2. 点击"发送"按钮或按Enter键提交问题
3. 等待AI助手根据知识库生成回答
