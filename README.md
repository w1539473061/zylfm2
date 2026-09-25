# zylfm2

翎风专用。

本仓库提供一个面向 **LF / LFM2 / 翎风引擎 / GEEM2 的 Mir200 服务端脚本**的知识库技能（skill），
内含完整的引擎说明书检索工具、从真实脚本提炼的耐久规则，以及一套可持续自我升级的训练流程。

## 内容

```
lf-mir200-knowledge/
  SKILL.md                    # 技能主说明：工作流 + 耐久规则
  knowledge_base/             # 849 章翎风引擎说明书（由原始 CHM 转换）
    index.md
    chapters/*.md
    assets/                   # 说明书里的配图
    manifest.json
  references/                 # 按主题提炼的规则与深挖记录，按需读取
  scripts/lf_kb.py            # 索引、检索、查看、学习工具（只用 Python 标准库）
  .lfmir-kb/indexes/          # 生成的索引（可重建，不必提交）

scripts/                      # 仓库级工具
  install_skill.py            # 安装技能到本机技能目录
  validate_knowledge_base.py  # 校验说明书链接与乱码
  check_generated.py          # 守卫：生成文件不得含私有样本路径或被手工改动
  convert_chm_to_md.py        # 原始 CHM → Markdown 转换（可选，需第三方库）

tests/                        # 回归测试（28 项）
.github/                      # CI 与 PR 模板
```

## 快速开始

需要 Python 3.10+，核心工具无第三方依赖。

```powershell
$KB = "lf-mir200-knowledge"

# 1. 自检
python "$KB\scripts\lf_kb.py" --root "$KB" validate

# 2. 检索说明书
python "$KB\scripts\lf_kb.py" --root "$KB" search "CHECKITEM GIVE 装备回收" --source docs --limit 8

# 3. 读取某一章
python "$KB\scripts\lf_kb.py" --root "$KB" inspect "knowledge_base/chapters/643-扩展GIVE命令.md"
```

## 安装到本机技能目录

`knowledge_base` 是技能的必要组成，不能只复制 `SKILL.md`。用仓库自带安装器整体安装：

```powershell
# 装到 ZCode（默认）
python scripts\install_skill.py --target zcode

# 装到 Codex
python scripts\install_skill.py --target codex

# 装到自定义位置
python scripts\install_skill.py --dest "D:\skills\lf-mir200-knowledge"
```

目标目录已存在时需加 `--force` 才会替换。安装会跳过生成的索引（首次使用跑一次 `update` 即可重建）。

## 接入自己的服务端样本（可选但强烈推荐）

本仓库**不包含**任何服务端样本——说明书是通用资料，而样本可能涉及私有服务端文件。

想让技能基于**你自己的**服务端脚本作答，把服务端根目录接入为 `样本Mir200` 即可。
推荐用目录联接，这样服务端更新后索引跟着更新，不必重复拷贝：

```powershell
# Windows（管理员或开发者模式）
cmd /c mklink /J "lf-mir200-knowledge\样本Mir200" "D:\你的服务端\Mir200"
```

然后重建索引：

```powershell
python "lf-mir200-knowledge\scripts\lf_kb.py" --root "lf-mir200-knowledge" update
```

`样本Mir200` 里应当是包含 `Envir` 的那一层（即 `Mir200` 目录本身）。

接入后，`search --source sample` 会检索你的真实脚本，`learn-script` 可以深挖单个脚本：

```powershell
python "$KB\scripts\lf_kb.py" --root "$KB" learn-script "样本Mir200/Envir/QuestDiary/系统功能/装备转移.txt"
```

`learn-script` 一次给出标签、调用、标识、输入控件、物品框、定时器、变量与匹配的说明书章节。

## 检索来源

| `--source` | 检索范围 |
| --- | --- |
| `docs` | 849 章引擎说明书 |
| `sample` | 接入的 `样本Mir200` 脚本 |
| `mapinfo` | `MapInfo.txt` 的地图链接（按方向解析） |
| `all` | 以上全部（默认） |

## 排除规则

接入实机服务端后，索引会**有意跳过**两类内容：

- **运行产物与二进制**：`Log`、`ConLog`、`Map`、`M2Data`、`Castle`、`GuildBase`、`Notice`、`Share`、`ShareV`、`Sort`、`PlugClient`、`Market_Saved`、`Market_Prices`、`MasterNo`、`MonIcons`、`NpcIcons`。
- **备份副本**：路径中任何一段含 `备份` 的文件，以及文件名以 ` - 副本`、` - 原版`、` - 备用` 结尾的文件。

不排除的话，每日运行日志会撑爆索引体积并污染检索排名，而带日期的备份是**旧值副本**——
命中它比没命中更糟，会把项目已经修好的值重新当成现状。

注意这里只排除人为复制命名，**不排除**引擎意义上的「副本地图」相关脚本，所以正常功能脚本不会被误伤。

## 自我升级

服务端脚本结构变动后（新增目录、新增 NPC、编辑 `MapInfo.txt` 等）重建索引：

```powershell
python "lf-mir200-knowledge\scripts\lf_kb.py" --root "lf-mir200-knowledge" update
```

重建 849 章说明书索引约需一秒。

技能本身也可持续训练：`references/mir200-training.md` 是一份按课程顺序排列的样本阅读路线，
`references/mir200-thinking.md` 是当前从真实脚本提炼出的脚本思维摘要。

## 开发验证

```powershell
# 回归测试（28 项；CHM 转换相关测试在缺第三方库时自动跳过）
python -m unittest discover -s tests

# 生成文件守卫：防止私有样本路径被写进 references 下的生成文件
python scripts\check_generated.py

# 说明书完整性：链接可达性与乱码检查
python scripts\validate_knowledge_base.py

# 技能自检
python "lf-mir200-knowledge\scripts\lf_kb.py" --root "lf-mir200-knowledge" validate
```

## 一起完善这个知识库

欢迎提交改进，但请先读 [CONTRIBUTING.md](CONTRIBUTING.md)。

有一条需要特别注意：`references/mir200-thinking.md` 与 `references/mir200-training.md`
是 `lf_kb.py update` 从 `样本Mir200` **生成**的。你接入自己的服务端跑过 `update` 之后，
自己服务端的脚本路径会被写进这两个被 git 追踪的文件。提交前请断开样本重跑 `update`，
并运行 `python scripts\check_generated.py` 确认。

流程是标准的 fork → 分支 → PR，**所有改动都由仓库维护者审核后才合并**。
PR 会自动触发 GitHub Actions 跑上面四项检查，作为审阅的客观依据。

## 约束

**只做静态分析与静态验证：不编译、不启动、不运行 Mir200 服务端。**
不修改服务端二进制、数据库、授权文件与运行日志。

## 许可

说明书版权归翎风引擎原作者所有，此处仅作格式转换以便检索。
