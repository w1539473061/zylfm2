# 贡献指南

感谢愿意一起完善这个知识库。因为本仓库要公开分发，而 Mir200 脚本往往涉及各自的私服，
所以下面有几条**硬规则**，请先读完再动手。

> **用 AI 帮忙提交？** 直接用 [AI_GUIDE.md](AI_GUIDE.md) 里那段提示词，
> 它已经把这些规则都写进去了。

## 最重要的一条：不要把私有服务端内容提交上来

本仓库是**通用**知识库。`样本Mir200` 是你自己的服务端，它已被 `.gitignore` 排除，
不会被提交——但有两个例外需要你手动注意：

`lf-mir200-knowledge/references/` 下的这两个文件是**由脚本生成的**：

- `mir200-thinking.md`
- `mir200-training.md`

它们由 `lf_kb.py update` 从 `样本Mir200` 重新生成。**你只要接入自己的服务端跑过一次
`update`，自己服务端的脚本路径就会被写进这两个文件**，而它们是被 git 追踪的。
样本目录本身有 `.gitignore` 挡着，这两个文件没有。

所以提交前请务必：

```powershell
# 断开样本（或确认 --root 指向的目录里没有 样本Mir200），然后重建
python lf-mir200-knowledge\scripts\lf_kb.py --root lf-mir200-knowledge update

# 逐行检查将要提交的内容，确认没有自己服务端的路径
git diff --cached

# 跑守卫，它会替你确认这两个文件是无样本状态的产物
python scripts\check_generated.py
```

`check_generated.py` 会在干净副本上重新生成这两个文件并与仓库版本比对，
所以**私有路径泄漏**和**手工改动**都会被它拦下。

## 提交流程

1. **Fork** 本仓库。
2. 从 `main` 开一个分支，名字说明你要改什么，例如 `fix/merchant-path-rule`。
3. 改动并本地验证（见下）。
4. 推送到你的 fork，然后向本仓库 `main` 提 **Pull Request**。
5. 我会审阅。**所有改动都由我审核后才合并**，不会自动进 `main`。

## 本地验证

提交前请在仓库根目录跑完整套：

```powershell
# 回归测试（31 项；缺 bs4 时 CHM 转换相关项会自动跳过）
python -m unittest discover -s tests

# 生成文件守卫（防止私有样本路径泄漏 / 手工改动生成物）
python scripts\check_generated.py

# 说明书完整性：链接可达性与乱码
python scripts\validate_knowledge_base.py

# 技能自检（先 update 建索引，再带 --strict 校验）
python lf-mir200-knowledge\scripts\lf_kb.py --root lf-mir200-knowledge update
python lf-mir200-knowledge\scripts\lf_kb.py --root lf-mir200-knowledge validate --strict
```

四项全过再提 PR。

**顺序很重要**：`check_generated.py` 要排在 `update` **之前**跑。
`update` 会按当前状态重新生成那两个文件，如果先生成了，被污染的版本就被覆盖成干净版，
守卫就抓不到了。CI 里也是这个顺序。

## 改哪里

| 你想改什么 | 该改哪个文件 |
| --- | --- |
| 新增一条耐久规则、补充触发/变量/颜色说明 | `lf-mir200-knowledge/SKILL.md` |
| 某个主题的深入笔记（如死循环排查、Envir 配置） | `lf-mir200-knowledge/references/` 下对应文件 |
| 索引/检索/学习工具的行为 | `lf-mir200-knowledge/scripts/lf_kb.py` |
| 仓库级工具（安装器、校验、CHM 转换） | `scripts/` |
| 测试 | `tests/` |
| 使用说明 | `README.md` |

**不要手工编辑** `mir200-thinking.md` 与 `mir200-training.md`——它们由脚本生成，会被守卫拦下。
想影响它们的内容，请改 `SKILL.md` 里的耐久规则，或改 `lf_kb.py` 里的生成逻辑。

说明书正文（`knowledge_base/chapters/`）是翎风引擎原作者的资料，由 CHM 转换而来。
除非是转换错误（乱码、链接失效、内容缺失），否则不要改动它。

## 写作约定

- **文档与注释用中文**，代码本身（变量名、函数名、关键字）保持英文。
- 动手前先检索：**这条规则是不是已经存在？** 已存在就补依据、改措辞，
  不要新增重复条目——两条措辞不同的同类规则，将来改动时容易只改一条。
- 新增规则要写清**适用范围**：这是引擎级规则（任何 LF/LFM2 服务端都成立），
  还是某个服务端的特定做法？后者请标明来源，别写成通用事实。
- 引用命令语法时，注明依据的说明章节路径，例如 `knowledge_base/chapters/629-传奇脚本命令详解.md`。
- 不要凭记忆写命令，也不要照抄别人给的章节号——先在说明书里检索确认，
  检索不到就说明「未收录」。章节号很容易记错：`CHECKGOLD` 常被误引为 628 章，
  但 628 章（程序变量说明）讲的是 `P0-P999` 变量族，实测 0 次提及 `CHECKGOLD`，
  真正的定义在 629 章。

## 三条硬约束

1. **只做静态分析与静态验证**：不编译、不启动、不运行 Mir200 服务端。
2. **不提交**服务端二进制与运行文件（`.exe`、`.db`、`.dat`、`.lic`、日志、缓存）。
3. **不提交**任何私有服务端的脚本、路径、物品名、NPC 名、账号信息。

第 3 条不只看 `样本Mir200`——提 PR 时请通读一遍自己的 diff，
确认没有把自己服务端的设计细节混进通用规则里。

## 关于 Pull Request 的内容

PR 描述里请说明：

- 你改了什么、为什么改。
- 依据是什么（说明书哪一章、或哪个可公开的样本）。
- 本地四项验证的结果。

如果改动来自你自己的服务端经验，说明「这是 X 类服务端的常见做法」即可，
不需要附上你的服务端文件。
