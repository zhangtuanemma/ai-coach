#!/usr/bin/env python3
 # -*- coding: utf-8 -*-
AI 问题处理教练 - Web 版
"""

import streamlit as st
from anthropic import Anthropic
import os

# 从原有文件导入 coaching_framework
from ai_coach_flexible import FlexibleCoach

# 页面配置
st.set_page_config(
    page_title="AI 问题处理教练",
    page_icon="💡",
    layout="centered"
)

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False

# 标题
st.title("💡 AI 问题处理教练")
st.markdown("我会像朋友一样和你聊聊，帮你理清思路")

# API Key 输入（侧边栏）
with st.sidebar:
    api_key = st.text_input("Anthropic API Key", type="password", value=os.environ.get("ANTHROPIC_API_KEY", ""))
    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key
    st.markdown("---")
    if st.button("清空对话"):
        st.session_state.messages = []
        st.session_state.started = False
        st.rerun()

# 显示对话历史
for msg in st.session_state.messages:
    role = "你" if msg["role"] == "user" else "教练"
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.write(f"**{role}：**{msg['content']}")

# 开始对话
if not st.session_state.started:
    st.info("说说看，遇到什么事了？")

# 用户输入
if prompt := st.chat_input("输入你的问题..."):
    if not api_key:
        st.error("请在侧边栏输入 API Key")
        st.stop()

    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.started = True

    with st.chat_message("user"):
        st.write(f"**你：**{prompt}")

    # 调用 API
    try:
        coach = FlexibleCoach()
        client = Anthropic(api_key=api_key)

        # 构建消息
        messages = st.session_state.messages.copy()

        # 检查是否需要改变策略
        question_count = sum(1 for m in st.session_state.messages if m["role"] == "assistant" and "?" in m["content"])
        if question_count >= 4:
            messages.append({
                "role": "user",
                "content": "[系统提示：已经连续提问4次以上，不要再追问了。现在给出对比方案让对方感受差别，或者直接亮出你的建议]"
            })

        # 调用 API
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            system=coach.coaching_framework,
            messages=messages
        )

        assistant_message = response.content[0].text

        # 添加助手消息
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        with st.chat_message("assistant"):
            st.write(f"**教练：**{assistant_message}")

        st.rerun()

    except Exception as e:
        st.error(f"错误：{e}")
