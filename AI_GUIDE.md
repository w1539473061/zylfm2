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
请帮我向 https://github.com/w1539473061/zylfm2 提交一个改进。

## 我要改的内容

<在这里写清楚你想改什么，越具体越好。
 例如：给 CHECKGOLD 那条规则补上说明书依据，先在说明书里核实它到底在哪一章。>

## 背景

这是一个翎风引擎（LF/LFM2/GEEM2）Mir200 服务端脚本的知识库。
说明书在 lf-mir200-knowledge/knowledge_base/（849 章，只读参考）；
耐久规则在 lf-mir200-knowledge/SKILL.md；
按主题的深入笔记在 lf-mir200-knowledge/references/。

## 必须遵守的三条硬约束

1. 只做静态分析：不要编译、启动或运行 Mir200 服务端。
2. 不要提交服务端二进制与运行文件（.exe / .db / .dat / .lic / 日志 / 缓存）。
3. 绝对不要把我自己服务端的任何内容提交上去——包括路径、目录结构、
   脚本名、物品名、NPC 名。

## 最重要的一条：别让私有样本路径泄漏

lf-mir200-knowledge/references/ 下的 mir200-thinking.md 和 mir200-training.md
是由 lf-mir200-knowledge/scripts/lf_kb.py 从「样本Mir200」目录生成的。
样本目录本身被 .gitignore 挡住了，但这两个文件没有。

所以：如果你为了验证而把我的服务端接入为 样本Mir200 并跑过 update，
必须先断开样本、重新跑一次 update，再提交。

提交前务必跑：
  python scripts/check_generated.py
它会拦下私有路径泄漏和手工改动。

## 改哪里

- 新增耐久规则、补充命令/触发/变量/颜色说明 → lf-mir200-knowledge/SKILL.md
- 某个主题的深入笔记（如死循环排查、Envir 配置）→ lf-mir200-knowledge/references/ 下对应文件
- 索引/检索/学习工具的行为 → lf-mir200-knowledge/scripts/lf_kb.py
- 仓库级工具 → scripts/
- 使用说明 → README.md
- 不要手工编辑 mir200-thinking.md 与 mir200-training.md（会被守卫拦下）

## 写作要求

- 文档和注释用中文；代码本身（变量名、函数名、关键字）保持英文。
- 先检查这条规则是否已经存在。已存在的话就补依据、改措辞，不要新增重复条目。
- 新增规则要写明适用范围：这是引擎级规则（任何 LF/LFM2 服务端都成立），
  还是某个服务端的特定做法？后者请标明来源，不要写成通用事实。
- 引用命令语法时注明依据的说明章节路径，例如
  knowledge_base/chapters/629-传奇脚本命令详解.md。
- 不要凭记忆写命令，也不要相信我给的章节号。先在说明书里检索确认，
  检索不到就说明「未收录」。我可能记错，以你的检索结果为准。

## 提交前必须跑这四项，全过才算完成

  python -m unittest discover -s tests
  python scripts/check_generated.py
  python scripts/validate_knowledge_base.py
  python lf-mir200-knowledge/scripts/lf_kb.py --root lf-mir200-knowledge validate

## Git 流程

1. 在 GitHub 上 fork 这个仓库到我的账号
2. clone 我的 fork，并加 upstream 指向原仓库：
     git remote add upstream https://github.com/w1539473061/zylfm2.git
3. 开一个说明改动的分支，例如 fix/checkgold-rule
4. 改动、跑上面四项验证、commit
5. push 到我的 fork
6. 向原仓库的 main 开 Pull Request

如果本机没有 gh CLI，push 之后 GitHub 会提示 Compare & pull request，
或者直接用这个链接（把占位符换掉）：
  https://github.com/w1539473061/zylfm2/compare/main...<我的用户名>:<分支名>?expand=1

## PR 描述

按 .github/PULL_REQUEST_TEMPLATE.md 填，逐条勾选自查清单。
特别要如实说明：这条改动是引擎级规则，还是我自己服务端的经验。

## 最后

把四项检查的实际输出贴给我看，不要只说「通过了」。
如果某一项没过，先修好再继续，不要带着失败的检查开 PR。
```

---

## 你需要补上的信息

提示词里只有一处占位符要填——「我要改的内容」。写得越具体，AI 越不容易跑偏。

好的写法：

> 我想给 `CHECKGOLD` 那条规则补上说明书依据。它现在在 SKILL.md 的「变量与语法」一节，
> 但没有标章节。请先在说明书里检索确认它到底在哪一章、原始定义怎么写，
> 再补进那条规则里。顺便确认一下 `CHECKITEM` 是不是测物品的，免得写成「CHECKITEM 金币」。

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

常见的四种情况：

**AI 说找不到 `样本Mir200`**——正常，这个目录不随仓库分发。你的 AI 不需要它也能
改 SKILL.md 和 references/，那些是纯文本改动。

**AI 想跑 `update` 来「验证」**——可以，但要提醒它：跑完必须断开样本重跑一次，
否则会把你的服务端路径写进生成文件。这就是守卫存在的原因。

**AI 改了 `mir200-thinking.md` 或 `mir200-training.md`**——让它撤销这两个文件的改动。
想影响它们的内容，应该改 `SKILL.md` 里的耐久规则，或改 `lf_kb.py` 里的生成逻辑。

**AI 说它要提交的内容「已经存在」**——相信它，让它改成补充依据或修正措辞。
规则重复比规则缺失更麻烦：两条措辞不同的同类规则，将来改动时容易只改一条。

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
