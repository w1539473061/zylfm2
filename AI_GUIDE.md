# 用 AI 提交改进

这份文档给「想用 AI 帮我改这个知识库」的人用。

把下面那段提示词复制给你的 AI（Claude Code / Codex / ZCode / Cursor 等），
补上你想改什么，AI 就会按正确流程走完并开好 Pull Request。

## 为什么需要专门的提示词

这个仓库有两个坑，AI 不知道就会踩：

**第一个坑（严重）**：`lf-mir200-knowledge/references/` 下的 `mir200-thinking.md`
与 `mir200-training.md` 是**由脚本生成的**，生成来源是 `样本Mir200` 目录。
样本目录本身被 `.gitignore` 挡住了，但这两个文件没有。所以——

> 如果 AI 为了验证而把你的服务端接入为 `样本Mir200` 并跑过 `update`，
> 你自己服务端的**脚本路径、目录结构、脚本名**就会被写进这两个文件，
> 然后跟着 PR 一起交上来。你多半不会注意到。

**第二个坑**：那两个文件手工改了也没用，下次 `update` 会把改动冲掉，
而且仓库的守卫会拦下你的 PR。

所以下面的提示词里，这两条是重点。

---

## 复制这段给你的 AI

```text
我在用你这个翎风引擎（LF/LFM2/GEEM2）Mir200 脚本的知识库技能，用着用着发现有地方
可以补充、有地方不对，也可能我自己服务端里摸出了一些值得写进去的经验。
你帮我把它提交回原仓库。

## 我想改什么

<在这里写清楚，越具体越好。三种常见情况：

 1. 补规则/改错：我在说明书里翻到 XX 命令的写法跟技能里说的不一样，
    或者技能里某条规则我找不到依据，你帮我核实并修正。

 2. 加经验：我在自己服务端里折腾 XX 功能的时候摸出了一些门道，
    想把它写进技能，以后别人也用得上。

 3. 改工具：lf_kb.py 或仓库脚本本身有 bug / 能改进的地方。
    （这种直接描述现象和你期望的行为，别只丢一句「优化一下」。）>

## 这个仓库是什么

翎风引擎 Mir200 服务端脚本的知识库。说明书在
lf-mir200-knowledge/knowledge_base/（849 章，只读参考，别改它）；
耐久规则在 lf-mir200-knowledge/SKILL.md；
按主题的深入笔记在 lf-mir200-knowledge/references/；
检索工具是 lf-mir200-knowledge/scripts/lf_kb.py。

## 三条底线

1. 只做静态分析：不要编译、不要启动、不要运行 Mir200 服务端。
2. 不要提交服务端二进制和运行文件（.exe / .db / .dat / .lic / 日志 / 缓存）。
3. 绝对不要把我自己服务端的内容提交上去——包括路径、目录结构、脚本名、
   物品名、NPC 名。

## 提交前最要紧的一件事

lf-mir200-knowledge/references/ 下的 mir200-thinking.md 和 mir200-training.md
是 lf_kb.py 从「样本Mir200」目录生成出来的。样本目录本身被 .gitignore 挡住了，
但这两个文件没有，它们是跟着仓库走的。

所以如果你为了验证而把我的服务端接成 样本Mir200 跑过 update，
提交前必须先断开样本、重新跑一次 update，再提交。

这不是理论风险。实测过：接一个假服务端进去跑 update，这两个文件里就被写进了
形如 `样本Mir200/Envir/QuestDiary/我的专属系统/装备回收_老王定制版.txt` 的整行路径——
连我瞎编的「老王」这种名字都原样带出去了。你服务端里的真实目录名和脚本名会一样出去。

每次提交前都跑一遍这个，它会拦下私有路径泄漏和手工改动：

  python scripts/check_generated.py

它会直接告诉你哪个文件第几行泄漏了什么，照着提示改就行。

## 改哪里

- 新增耐久规则、补充命令/触发/变量/颜色说明 → lf-mir200-knowledge/SKILL.md
- 某个主题的深入笔记（死循环排查、Envir 配置之类）→ lf-mir200-knowledge/references/ 下对应文件
- 索引/检索/学习工具的行为 → lf-mir200-knowledge/scripts/lf_kb.py
- 仓库级工具 → scripts/
- 使用说明 → README.md
- 千万别手工编辑 mir200-thinking.md 和 mir200-training.md，守卫会拦你

## 写规则的要求

- 文档和注释用中文，代码本身（变量名、函数名、关键字）保持英文。
- 先搜一遍这条规则是不是已经有了。已经有了就补依据、改措辞，别新增重复条目。
  两条措辞不同的同类规则，将来改的时候很容易只改一条。
- 最重要的一条：分清楚这是「引擎级规则」还是「我这个服的特定做法」。
  引擎级的（任何 LF/LFM2 服务端都成立）才能写成通用规则；
  你自己服里的做法必须标明来源和适用范围，别写成像官方行为一样。
  这条最容易被忽略——你摸出来的门道很可能只在你的服务端上成立。
- 引用命令语法时注明依据的章节路径，比如
  knowledge_base/chapters/629-传奇脚本命令详解.md。
- 不要凭记忆写命令，也不要相信我给的章节号。我可能记错。
  先在说明书里检索确认，检索不到就老实写「未收录」。
  （举个例子：我曾经以为 CHECKGOLD 在 628 章，实际 628 章讲的是 P0-P999 变量族，
  根本没提 CHECKGOLD；真正的定义在 629 章。所以以你检索到的为准。）

## 提交前必须跑这五项，全过才算完成

  python -m unittest discover -s tests
  python scripts/check_generated.py
  python scripts/validate_knowledge_base.py
  python lf-mir200-knowledge/scripts/lf_kb.py --root lf-mir200-knowledge update
  python lf-mir200-knowledge/scripts/lf_kb.py --root lf-mir200-knowledge validate --strict

注意三件事：
- 顺序不能乱，check_generated.py 要排在 update 前面。update 会重新生成那两个文件，
  先生成的话被污染的版本就被覆盖成干净版了，守卫就抓不到。
- --root 必须写在子命令前面（lf_kb.py --root X update），写成 update --root X 会报错。
- validate 不带 --strict 时索引缺失也返回 0，所以必须带 --strict。

## Git 流程

1. 在 GitHub 上 fork 这个仓库到我的账号
2. clone 我的 fork，加 upstream 指向原仓库：
     git remote add upstream https://github.com/w1539473061/zylfm2.git
3. 开一个说明改动的分支，比如 fix/checkgold-rule
4. 改动、跑上面四项验证、commit
5. push 到我的 fork
6. 向原仓库的 main 开 Pull Request

本机没有 gh CLI 的话，push 之后 GitHub 会提示 Compare & pull request，
或者直接用这个链接（把占位符换掉）：
  https://github.com/w1539473061/zylfm2/compare/main...<我的用户名>:<分支名>?expand=1

## PR 描述

按 .github/PULL_REQUEST_TEMPLATE.md 填，逐条勾选自查清单。
特别要如实说明：这条改动是引擎级规则，还是我自己服务端的经验。

## 最后

把四项检查的实际输出贴给我看，不要只说「通过了」。
哪项没过就先修好，别带着失败的检查开 PR。
```

---

## 你需要补上的信息

提示词里只有一处占位符要填——「我想改什么」。写得越具体，AI 越不容易跑偏。

好的写法：

> 我在自己服里配复活点的时候，发现说明书对 `CHANGEMAP` 和 `MAPMOVE` 的区别
> 讲得含糊，我试出来是 XX 不一样。你帮我在说明书里核实一下到底是不是这样，
> 是的话就补进 SKILL.md，并标明这是我实测的、不是说明书原文。

不好的写法：

> 帮我优化一下这个知识库。

**注意上面「好的写法」里我故意没写章节号。** 因为我自己就记错过一次——
我曾以为 `CHECKGOLD` 在 628 章，实际 628 章（程序变量说明）讲的是 `P0-P999` 这类变量族，
压根没提 `CHECKGOLD`（实测出现 0 次）；真正的定义在 629 章：
`checkgold 数值 ;拥有金币数>=数值为1否则为0`。所以让 AI 自己去查，
比给它一个可能错的答案更可靠。

## 提交之后

PR 会自动触发 GitHub Actions，跑那四项检查。维护者会看检查结果和你的 diff，
**通过审核后才合并**，不会自动进 `main`。

如果 CI 报了「生成文件守卫未通过」，说明你的改动里带了私有样本路径。
按提示断开 `样本Mir200` 重跑 `update` 即可，具体命令守卫会打印出来。

## 如果 AI 卡住了

常见的五种情况：

**AI 说找不到 `样本Mir200`**——正常，这个目录不随仓库分发。你的 AI 不需要它也能
改 SKILL.md 和 references/，那些是纯文本改动。

**AI 想跑 `update` 来「验证」**——可以，但要提醒它：跑完必须断开样本重跑一次，
否则会把你的服务端路径写进生成文件。这就是守卫存在的原因。

**AI 改了 `mir200-thinking.md` 或 `mir200-training.md`**——让它撤销这两个文件的改动。
想影响它们的内容，应该改 `SKILL.md` 里的耐久规则，或改 `lf_kb.py` 里的生成逻辑。

**AI 说它要提交的内容「已经存在」**——相信它，让它改成补充依据或修正措辞。
规则重复比规则缺失更麻烦：两条措辞不同的同类规则，将来改动时容易只改一条。

**AI 把自己服务端的做法写成通用规则**——这是最需要你盯的一条。让它标清楚
适用范围和来源，或者改成「某服务端经验」而不是「引擎行为」。

## 如果 AI 没有 GitHub 权限

AI 跑不了 fork、push、开 PR 这几步（需要你的账号凭据）。这时让它：

1. 在本地把改动做完、四项检查跑过、commit 好。
2. 把改动导成补丁给你：

```powershell
git format-patch main --stdout > 我的改动.patch
```

3. 你自己在 GitHub 网页上 fork、开分支，然后把这个 `.patch` 文件
   拖到 GitHub 的网页上传界面，或者用 GitHub Desktop 导入。

**不要**让 AI 拿着你的 GitHub token 去操作——除非你清楚它会把什么推上去。
