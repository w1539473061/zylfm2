# Mir200 Training Course

This package has no public `样本Mir200`; provide a local sample root before sample-based training.

- Method: 按真实脚本信号抽样，从简单入口到组合系统逐层学习。
- Lessons: 8
- Example files: 0
- Sample records considered: 0

## How To Train

1. Start with lesson 1 and inspect each listed sample file.
2. For each file, trace entry, guards, actions, state writeback, and failure path.
3. Compare the sample against the manual before copying command syntax.
4. Add new reusable observations to `mir200-thinking.md`, then run `update` to refresh generated summaries.

## Lessons

### 入口与分发

- ID: `lesson-01-entry-dispatch`
- Goal: 先定位玩家从哪个 NPC 标签进入，再追踪 GOTO 和按钮链接如何把流程分出去。
- Signals: [@main], @main, GOTO
- Thinking focus:
  - 入口不是业务本身，入口负责把玩家动作分派到真正的处理标签。
  - 读脚本时先画标签流，再判断每个分支的条件和副作用。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。

### 对话与界面组织

- ID: `lesson-02-dialog-ui`
- Goal: 学习 #SAY、按钮链接、大对话框、ITEMBOX、Text/Img 等 UI 如何承载业务输入。
- Signals: #SAY, OPENMERCHANTBIGDLG, ITEMBOX, Text:, Img:, MESSAGEBOX
- Thinking focus:
  - UI 标签既展示说明，也把玩家选择绑定到后续标签。
  - ITEMBOX 这类控件要顺着 boxitem 变量继续查真正的状态读写。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。

### 条件守门与成本检查

- ID: `lesson-03-guards-costs`
- Goal: 提炼 CHECK、COMPARE、RANDOM、货币/背包/地图检查如何阻止非法执行。
- Signals: #IF, CHECKITEM, CHECKGOLD, CHECKGAMEGOLD, COMPARETEXT, RANDOM, CHECKBAGSIZE, small , large , equal 
- Thinking focus:
  - 先检查资格，再扣成本，再执行奖励或传送。
  - 有 #ELSEACT 或 BREAK 的地方通常是失败路径，不要只读成功路径。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。

### 动作、奖励与惩罚

- ID: `lesson-04-actions-rewards`
- Goal: 学习 GIVE、TAKE、GAMEGOLD、MAPMOVE、MonGen、SENDMSG 等动作如何改变玩家、地图和背包。
- Signals: #ACT, GIVE , TAKE , GAMEGOLD, MAPMOVE, MonGen, SENDMSG, MESSAGEBOX
- Thinking focus:
  - 动作块是副作用集中区，要把每个 TAKE/GIVE/MAPMOVE 当成状态变化记录。
  - 扣费与奖励最好成对审查，确认失败路径不会误扣或漏还。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。

### 变量、物品状态与回写

- ID: `lesson-05-state-writeback`
- Goal: 学习 MOV、SET、物品属性读写、文本列表、UpdateItem/ReturnBoxItem 如何保存业务结果。
- Signals: MOV , SET , GetCustomItemText, GETITEMADDVALUE, CHANGEITEMADDVALUE, SetNewItemValue, UpdateItem, ReturnBoxItem, AddTextListEx, DelTextListLine
- Thinking focus:
  - 变量只是中间账本，真正结果常落在物品、列表文件、称号、计时器或角色状态上。
  - 遇到 boxitem 和自定义属性时，必须同时检查读取、清零、写入、刷新和归还。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。

### 定时器、机器人与全局流程

- ID: `lesson-06-timers-automation`
- Goal: 学习 SetOnTimer、OnTimer、Robot_def、AutoRunRobot 和 QManage 如何驱动后台流程。
- Signals: SetOnTimer, OnTimer, AutoRunRobot, Robot, Gmexecute, @Startup, @Login
- Thinking focus:
  - 自动化脚本不靠玩家点击触发，入口常在 Startup/Login/OnTimer。
  - 读定时器要把启动位置、间隔、终止条件和重复副作用连起来看。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。

### 地图、怪物与商人配置

- ID: `lesson-07-world-config`
- Goal: 学习 MapInfo、MapEvent、MonGen、MerChant、Npcs 等配置文件如何把脚本挂到世界上，特别是 MapInfo 的地图链接行。
- Signals: MapInfo, MapEvent, MonGen, MerChant, Npcs, NoRecall, SAFE, Mongen, ->
- Thinking focus:
  - 功能脚本往往不是孤立文件，要从地图/NPC/刷怪配置找到它的挂载点。
  - MapInfo 链接行表示玩家走到源地图源坐标时，被传送到目标地图目标坐标。
  - 排查问题时同时看脚本内容和配置入口，确认玩家是否真的能触发。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。

### 组合系统拆解

- ID: `lesson-08-combined-systems`
- Goal: 练习把复杂系统拆成入口、UI、守门、动作、状态回写、后台触发六个面向再逐项检查。
- Signals: OPENMERCHANTBIGDLG, ITEMBOX, SetOnTimer, GOTO, RANDOM, UpdateItem, ReturnBoxItem, MAPMOVE
- Thinking focus:
  - 复杂脚本不要从头读到尾硬啃，先按职责切块。
  - 每次改动前写出输入、条件、成本、成功副作用、失败副作用和恢复路径。
- Examples:
  - No strong matching sample yet; search manually before answering this topic.
- Practice:
  - 先用 search 查同类关键词，再 inspect 最相关的样本。
  - 写出入口、条件、动作、状态回写、失败路径五项笔记。
  - 把可复用经验补进 mir200-thinking.md 或重新运行 update 生成。


Source root: `lf-mir200-knowledge`
