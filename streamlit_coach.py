#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题处理 AI 教练 - Streamlit版本
可以一键部署到 Streamlit Cloud，让别人直接访问
"""

import streamlit as st
import os
import sys
from anthropic import Anthropic

# 确保UTF-8编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# 页面配置
st.set_page_config(
    page_title="问题处理 AI 教练",
    page_icon="💬",
    layout="centered"
)

# 教练框架
COACHING_FRAMEWORK = """
你是一位经验丰富的总裁，帮助站长在处理问题时做出正确的决策和判断。

【好慷的使命和核心价值观】
使命：让服务者和被服务者都感到幸福
核心价值观：
- 以家人之心对待员工和客户 - 人是目的不是工具
- 做好服务是最本分的事
- 不要因为短期得失，牺牲长期利益
- 服务要120%满意
- 复利（长期积累，持续增长）

【决策判断标准：公平、客观、利他】
遇到问题时，问自己：
- 公平吗？对客户公平、对员工公平
- 客观吗？事实是什么就是什么，不找借口
- 利他吗？先想对方怎么样，而不是先想自己怎么省事
- 以家人之心吗？如果是你的家人，你会怎么做？
- 为了长期还是短期？不要因为短期得失，牺牲长期利益

【核心认知】
1. 当"老板"是不怕问题的
   - 你是老板，不是打工的。你就是公司，不是传话筒
   - 问题不是麻烦，是机会。挑剔的客户是磨刀石，客户身边都是客户
   - 你能做到别人做不到的，这就是你的本事

2. 要正确理解好慷的价值观，别怕吃亏
   - 不占别人便宜（包括客户和员工）
   - 方案要客观、公平、以对方利益为出发点
   - 人的一生中要做一些亏钱的生意。吃别人吃不下的亏，才能挣别人挣不了的钱

3. 不害怕不逃避，坦诚是最好的话术
   - 不坦诚是因为心里没底，心里没底是因为不明白公司为什么这么做
   - 事实是什么就是什么，该承认的错误就承认
   - 哪怕公司错了，诚信永远是对的

【问题处理四步法】
1. 听 - 先倾听，不打断
2. 认 - 认可对方的感受
3. 问 - 引导思考
4. 做 - 给方法，做闭环

【你的角色】
- 你是总裁，不是教练。重点帮站长做出正确的决策判断
- 直接指出问题：这个决策符合"公平、客观、利他"吗？是以家人之心吗？
- 引导思考：如果是你的家人，你会怎么做？这是为了长期还是短期？
- 帮助理解：好慷为什么要这么做？背后是什么价值观？

【对话要求】
- 一次只问一个问题
- 用简单、直接的话（中学生能听懂）
- 重点在决策和判断，不要过多指导沟通细节和话术
- 每次回复3-5句话
- 当用户理解了核心认知、做出了决策，适时结束
- 多用例子，少讲道理

【对话策略】（重要）
- 不要连续追问超过5次，对方会疲惫
- 在第4-5次对话时，改变策略：
  * 给出对比方案，让对方感受差别（"如果这样做会怎样？如果那样做会怎样？"）
  * 或者直接亮出建议（"我建议你这样做，因为..."）
- 避免一直问问题不给答案
"""

# 初始化session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# 标题
st.title("💬 问题处理 AI 教练")
st.caption("帮助你更好地处理客户和员工问题")

# 侧边栏 - API密钥设置
with st.sidebar:
    st.header("⚙️ 设置")

    # API密钥输入
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
        help="输入你的Anthropic API密钥"
    )

    if not api_key:
        st.warning("请输入API密钥才能开始对话")

    st.divider()

    # 重新开始按钮
    if st.button("🔄 重新开始", use_container_width=True):
        st.session_state.messages = []
        st.session_state.turn_count = 0
        st.session_state.question_count = 0
        st.rerun()

    # 导出对话按钮
    if st.session_state.messages and st.button("📥 导出对话", use_container_width=True):
        # 生成对话记录文本
        export_text = "="*60 + "\n"
        export_text += "问题处理教练对话记录\n"
        export_text += "="*60 + "\n\n"

        for msg in st.session_state.messages:
            role = "你" if msg["role"] == "user" else "教练"
            export_text += f"{role}：{msg['content']}\n\n"

        export_text += "="*60 + "\n"

        st.download_button(
            label="下载对话记录",
            data=export_text,
            file_name="对话记录.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()
    st.caption("基于 Claude AI 驱动")

# 显示欢迎消息
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("欢迎使用问题处理教练！")
        st.write("我会像朋友一样和你聊聊，帮你理清思路。")
        st.write("说说看，遇到什么事了？")

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 用户输入
if prompt := st.chat_input("输入你的消息..."):
    if not api_key:
        st.error("请先在侧边栏输入API密钥")
        st.stop()

    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.turn_count += 1

    # 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)

    # 检查是否是回答问题
    if st.session_state.messages and len(st.session_state.messages) >= 2:
        last_assistant_msg = st.session_state.messages[-2]["content"]
        if '?' in last_assistant_msg:
            st.session_state.question_count += 1
        else:
            st.session_state.question_count = 0

    # 构建消息
    messages = st.session_state.messages.copy()

    # 在第4-5轮时提示教练改变策略
    if st.session_state.question_count >= 4:
        messages.append({
            "role": "user",
            "content": "[系统提示：已经连续提问4次以上，不要再追问了。现在给出对比方案让对方感受差别，或者直接亮出你的建议]"
        })

    # 调用Claude API
    try:
        client = Anthropic(api_key=api_key)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # 流式输出
            with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=500,
                system=COACHING_FRAMEWORK,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    message_placeholder.write(full_response + "▌")

            message_placeholder.write(full_response)

        # 添加助手消息到历史
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"错误：{str(e)}")
        st.info("请检查API密钥是否正确")
