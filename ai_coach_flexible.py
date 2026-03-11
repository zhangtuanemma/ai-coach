#!/usr/bin/env python3                                                                                                                                              
  # -*- coding: utf-8 -*-
  """                                                                                                                                                                 
  灵活的问题处理 AI 教练                                                                                                                                            
  使用 Claude API 实现自然对话式教练
  """

  import os
  import sys
  import io

  # 强制设置 UTF-8 编码
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
  sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

  from anthropic import Anthropic

  class FlexibleCoach:
      """灵活的对话式教练"""

      def __init__(self):
          # 从环境变量获取 API key
          api_key = os.environ.get("ANTHROPIC_API_KEY")
          if not api_key:
              print("错误：请设置 ANTHROPIC_API_KEY 环境变量")
              print("在终端运行：export ANTHROPIC_API_KEY='你的API密钥'")
              sys.exit(1)

          self.client = Anthropic(api_key=api_key)
          self.conversation_history = []
          self.turn_count = 0  # 跟踪对话轮次
          self.question_count = 0  # 跟踪连续提问次数

          # 核心理念和方法
          self.coaching_framework = """
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

  【核心处理原则】（基于真实案例）
  | 维度 | 核心原则 |
  |---|---|
  | 对员工 | 以家人之心，坦诚沟通，不回避问题。讲清出发点，让员工明白你是为他好 |
  | 对客户 | 不争对错，主动承担，不让客户吃亏。挑剔的客户是磨刀石 |
  | 对规则 | 立场坚定，法归法，情归情。规则必须执行，但人情可以另行弥补 |
  | 对责任 | 不逃避，不少赔，有担当才能走得远 |
  | 对沟通 | 讲清出发点，用类比打动人，不怕投诉曝光 |

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

  【真实案例】
  1. 员工疑似盗窃（以家人之心）：
     错误：找理由让员工默默离职。
     正确：坦诚跟员工聊，问家里有没有困难。即使不承认，也能帮他以后不再犯错。然后对客户负责，该赔的赔（80%可能是我们的问题）。
     启示：不让任何一方吃亏，有担当的企业才能走得远。

  2. 老员工不戴头盔被辞退（法归法，情归情）：
     立场坚定：不戴头盔+有事故记录，依规开除，发公告警示。
     情理兼顾：帮员工介绍新工作，从其老公处购买绿植（大几千元）实质性帮扶。
     启示：规则必须执行，但人情可以另行弥补。

  3. 员工不理解摔伤扣分（讲清出发点）：
     用"打孩子"类比：妈妈打孩子两巴掌，是疼在孩子身上、痛在妈妈心里，目的是让孩子下次不再摔。
     启示：只要出发点是为员工好，就要把这个出发点讲清楚。

  4. 成都李女士投诉（不要急于处理）：
     错误：王凤带情绪、意气用事，把客户当麻烦，想赶紧赔钱了事。
     正确：挑剔客户是"磨刀石"，服务好了能带来更多客户。不要急于处理难搞事件，想好策略再行动。记住自己"服务者"身份。
     启示：态度决定结果。心态够好，事情就不复杂。

  5. 客户投诉员工拖地后摔跤（不争对错）：
     不争对错：开门做生意就要有承担灰度责任的准备，不能在客户面前争谁对谁错。
     法情分离：公司层面用"法"处理（该赔赔），个人层面用"情"打动人。
     启示：不怕投诉/曝光，诚信就是最大的底气。

  6. 玻璃擦坏客户要1000（杭州站长案例）：
     公司评估赔500，客户要1000。站长直接说"好的，我加你微信转给你"。
     客户愣住了："你们权限这么大吗？"站长："在客户满意度上我们权限比较大。"
     结果：年底客户原价购买春节保姆，没要优惠。
     启示：能做到别人做不到的，客户会记住你。

  【问题处理四步法】
  1. 听 - 先倾听，不打断
     - 让员工把话说完，包括抱怨和情绪
     - 了解整个服务过程，找到真正的问题点
     - 不要急着反驳或解释

  2. 认 - 认可对方的感受
     - 理解员工的委屈或困难
     - 站在中立角度，既维护员工也维护客户
     - 让员工感受到被理解

  3. 问 - 引导思考
     - 分析：这个地方为什么会出问题？
     - 反问：如果换一种方式会不会更好？
     - 让员工自己意识到问题，而不是你告诉他

  4. 做 - 给方法，做闭环
     - 给出具体的改进方法
     - 全员共识：把案例分享给所有人避雷
     - 跟踪反馈：后续关注员工表现和客户评价

  【优秀站长的实战方法】

  张文华（北京广安门站）- 投诉处理专家：
  核心做法：
  - 第一时间了解投诉原因（先问客户，再问员工）
  - 倾听员工完整表达，包括抱怨和情绪
  - 如果客户同意，上门113看实际情况，拍照取证
  - 分析透彻后再沟通，用事实说话，让员工心服口服
  - 做闭环：每周质量会上讲案例，全员避雷
  关键点：自己技能要过硬，113跟单发现问题，才有说服力。现在员工投诉后都很痛快回来复训。

  李花（苏州站）- 规范流程守底线：
  核心做法：
  - 遇到问题（如客户家东西丢了）立即报备公司，留记录
  - 安抚员工：清者自清，配合调查，公司相信你
  - 讲现实：年龄大了工作不好找，要珍惜这份工作
  - 规避风险：按规范流程做，提醒客户收好贵重物品
  - 有投诉必复训：出现事件就停单一天复训，没有例外
  关键点：规范流程保护员工也保护客户，让员工认知到做正确的事。

  林瑞娜（南京栖霞站）- 建立信任带队伍：
  核心做法：
  - 及时回复员工消息（除了睡觉随时在线），经理教的方法
  - 能解决就解决，解决不了也要反馈进度，让员工知道你在处理
  - 带他们挣钱（最重要）：引导出远单，做家访，帮助提升
  - 先问企业认同度，再讲现实情况（年龄、附近没客户），最后问需要什么帮助
  - 不听的先放一边，等他主动要单时再引导
  关键点：挣到钱是物质，情绪价值是精神，但挣钱更重要。

  王海燕（苏州站）- 政策宣导有方法：
  核心做法：
  - 自己先理解政策，才能有底气宣导（源头很重要）
  - 站会宣导后，观察员工反应，识别不理解的人
  - 单独沟通：理性反馈可以，但不能用情绪煽动
  - 讲生活中的例子，让大家更能理解
  关键点：自己要坚定，员工才会信任你。不理解当中去执行，执行着就理解了。

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

      def start(self):
          """开始教练对话"""
          print("\n" + "="*60)
          print("欢迎使用 AI 问题处理教练")
          print("我会像朋友一样和你聊聊，帮你理清思路")
          print("="*60 + "\n")

          # 获取问题描述
          print("说说看，遇到什么事了？")
          problem = input("\n你：").strip()

          if not problem:
              print("没事的话我们下次再聊～")
              return

          # 开始对话
          self.chat(problem)

      def chat(self, user_message):
          """进行对话"""
          # 增加轮次计数
          self.turn_count += 1

          # 检查用户回复是否是回答问题（简单判断）
          if '?' not in self.conversation_history[-1]['content'] if self.conversation_history else False:
              self.question_count = 0  # 重置提问计数
          else:
              self.question_count += 1  # 增加提问计数

          # 添加用户消息到历史
          self.conversation_history.append({
              "role": "user",
              "content": user_message
          })

          # 构建消息
          messages = self.conversation_history.copy()

          # 在第4-5轮时提示教练改变策略
          if self.question_count >= 4:
              messages.append({
                  "role": "user",
                  "content": "[系统提示：已经连续提问4次以上，不要再追问了。现在给出对比方案让对方感受差别，或者直接亮出你的建议]"
              })

          # 调用 Claude API
          try:
              response = self.client.messages.create(
                  model="claude-sonnet-4-6",
                  max_tokens=500,  # 适度限制回复长度，保持深度
                  system=self.coaching_framework,
                  messages=messages
              )

              # 获取回复
              assistant_message = response.content[0].text

              # 添加助手消息到历史（不包含系统提示）
              self.conversation_history.append({
                  "role": "assistant",
                  "content": assistant_message
              })

              # 显示回复
              print(f"\n教练：{assistant_message}\n")

              # 检查是否应该结束
              if self.should_end(user_message, assistant_message):
                  print("对话记录已自动保存。\n")
                  self.save_conversation()
                  return

              # 继续对话
              self.continue_conversation()

          except Exception as e:
              print(f"\n错误：{e}")
              print("对话出现问题，请检查网络连接或 API 配置")

      def should_end(self, user_message, assistant_message):
          """判断是否应该结束对话"""
          # 用户明确表示理解并有决定
          understanding_keywords = ['明白了', '懂了', '知道怎么做', '清楚了', '理解了', '我会', '我去']
          if any(keyword in user_message for keyword in understanding_keywords):
              return True

          # 教练主动结束（确认用户理解后）
          ending_keywords = ['加油', '去试试', '去做', '行动起来', '就这样']
          if any(keyword in assistant_message for keyword in ending_keywords):
              return True

          return False

      def continue_conversation(self):
          """继续对话"""
          while True:
              user_input = input("你：").strip()

              if not user_input:
                  continue

              # 检查是否结束对话
              if user_input.lower() in ['退出', 'quit', 'exit', '再见', 'bye']:
                  print("\n教练：好的，有问题随时来找我聊！加油💪\n")
                  self.save_conversation()
                  break

              # 继续对话
              self.chat(user_input)
              break

      def save_conversation(self):
          """保存对话记录"""
          filename = "对话记录.txt"

          with open(filename, 'a', encoding='utf-8') as f:
              f.write("\n" + "="*60 + "\n")
              f.write("对话记录\n")
              f.write("="*60 + "\n\n")

              for msg in self.conversation_history:
                  role = "你" if msg["role"] == "user" else "教练"
                  f.write(f"{role}：{msg['content']}\n\n")

              f.write("="*60 + "\n")

          print(f"对话记录已保存到：{filename}")

  def main():
      """主函数"""
      coach = FlexibleCoach()
      coach.start()

  if __name__ == "__main__":
      main()
