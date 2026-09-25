# 用 AI 接入你自己的服务端

这份文档给「已经拿到这个技能、想让它读懂我自己服务端」的人用。

技能自带 849 章说明书，**不接入服务端也能查命令语法**。但如果你想让它回答
「我这个服里 XX 功能是怎么实现的」，就需要把服务端脚本接进来让它检索。

把下面那段提示词复制给你的 AI，填上你的服务端路径即可。

## 提示词

```text
请帮我把这个翎风引擎知识库技能接入我自己的 Mir200 服务端，然后带我学一遍。

## 技能位置

<填技能目录的绝对路径，例如 D:\skills\lf-mir200-knowledge>

如果这个目录不存在，请先从 https://github.com/w1539473061/zylfm2 取下来：
  git clone https://github.com/w1539473061/zylfm2.git
然后技能在 zylfm2/lf-mir200-knowledge/。

## 我的服务端

<填包含 Envir 的那一层目录的绝对路径，例如 D:\MirServer\Mir200>
注意：要的是 Mir200 目录本身（里面能看到 Envir 文件夹），不是服务端根目录。

## 第一步：自检

先确认技能可用：

  python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" validate

## 第二步：把服务端接进来

推荐用目录联接，这样服务端更新后索引跟着更新，不用重复拷贝：

  cmd /c mklink /J "<技能目录>\样本Mir200" "<我的 Mir200 路径>"

目录联接（/J）普通权限就能建，不需要管理员。如果系统不允许，改用复制，
但之后服务端改动了要重新拷贝一次。

接好后重建索引：

  python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" update

## 第三步：确认接入成功

  python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" validate

看输出里的 sample_index_records，应该是个大于 0 的数字（我的服务端脚本数量）。
如果还是 0，说明 样本Mir200 没接对，请排查。

## 第四步：带我学

1. 先读 "<技能目录>\references\mir200-training.md"，那是课程顺序。
2. 再读 "<技能目录>\references\mir200-thinking.md"，那是脚本思维摘要。
3. 然后按课程逐课来，每课都去检索我服务端里的真实脚本。

## 之后我问你问题时的规矩

- 回答前先检索说明书确认语法，再检索我的服务端脚本看实际写法。
- 区分「说明书官方行为」和「从我的脚本推断出的结论」，后者要标明。
- 引用要落到具体文件路径。
- 我的服务端脚本通常是 GBK/ANSI 编码，改动时要保持原编码与换行。

## 硬约束

1. 只做静态分析：不要编译、启动或运行 Mir200 服务端。
2. 不要修改服务端二进制、数据库、授权文件与运行日志
   （.exe / .db / .dat / .lic / Log 目录下的东西）。
3. 不要把我的服务端内容传到网上或提交到任何公开仓库。

## 最后

把第二步和第三步的实际输出贴给我看，确认 sample_index_records 真的大于 0。
```

---

## 你需要补上的信息

提示词里有两处占位符：

| 占位符 | 填什么 | 怎么确认填对了 |
| --- | --- | --- |
| 技能位置 | 技能目录的绝对路径 | 该目录下能看到 `SKILL.md` 和 `knowledge_base` 文件夹 |
| 我的服务端 | 包含 `Envir` 的那一层 | 该目录下能看到 `Envir` 文件夹，且 `Envir` 里有 `MapInfo.txt` |

第二处最容易填错。`Mir200` 的典型结构是：

```
D:\MirServer\              <- 服务端根目录，不是这个
  Mir200\                  <- 是这一层
    Envir\
      MapInfo.txt
      Market_def\
      QuestDiary\
    ...
  DBServer\
  LoginSrv\
```

所以要填 `D:\MirServer\Mir200`，不是 `D:\MirServer`。

## 接入之后能做什么

接入前后，技能能回答的问题不一样：

| 问题类型 | 接入前 | 接入后 |
| --- | --- | --- |
| 「`CHECKITEM` 怎么用？」 | 能答（查说明书） | 能答 |
| 「我这服的装备回收 NPC 在哪？」 | 答不了 | 能答（检索你的脚本） |
| 「给我看下我这服转生脚本怎么写的」 | 答不了 | 能答，还能用 `learn-script` 深挖 |
| 「我这张地图怎么去下一张？」 | 答不了 | 能答（解析你的 `MapInfo.txt`） |

常用的三条命令：

```powershell
# 在说明书里查命令语法
python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" search "CHECKITEM" --source docs

# 在你自己的脚本里查功能实现
python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" search "装备回收" --source sample

# 深挖某个脚本：标签、调用、标识、定时器、变量、相关说明章节
# 路径换成你自己服务端里真实存在的文件（相对 样本Mir200 的路径）
python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" learn-script "样本Mir200/Envir/QuestDiary/系统功能/装备转移.txt"
```

不知道有哪些脚本时，先用 `search --source sample` 搜关键词，命中结果里会带路径。

## 索引会跳过什么

技能不会把你的运行日志和备份塞进索引，这是有意设计的：

- **运行产物与二进制**：`Log`、`ConLog`、`Map`、`M2Data`、`Castle`、`GuildBase`、
  `Notice`、`Share`、`ShareV`、`Sort`、`PlugClient`、`Market_Saved`、`Market_Prices`、
  `MasterNo`、`MonIcons`、`NpcIcons`。
- **备份副本**：路径中任何一段含 `备份` 的文件，以及文件名以 ` - 副本`、` - 原版`、
  ` - 备用` 结尾的文件。

不排除的话，每日运行日志会撑爆索引体积并污染检索排名；而带日期的备份是**旧值副本**，
命中它比没命中更糟——它会把项目已经修好的值重新当成现状。

如果你搜某个功能返回空、但明明记得文件在，先确认它是不是命中了上面的规则。

## 一个必须知道的坑

`references/` 下的 `mir200-thinking.md` 和 `mir200-training.md` 是**由脚本生成的**，
生成来源就是你的 `样本Mir200`。

**你接入服务端后跑 `update`，你自己服务端的脚本路径会被写进这两个文件。**

这对本地使用**没有影响**，是正常行为，你不用管它。

但如果你之后想把改进**提交回上游仓库**，就必须先处理掉——否则等于把你的服务端
目录结构和脚本名公开出去。具体做法见 [AI_GUIDE.md](AI_GUIDE.md)。

## 用完了想断开

把 `样本Mir200` 联接删掉，再跑一次 `update` 清空索引：

```powershell
# 删联接（注意：不要用 Remove-Item -Recurse，那会删掉真实服务端内容）
[System.IO.Directory]::Delete("<技能目录>\样本Mir200", $false)

python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" update
```

删联接那条命令**务必用上面这种写法**。用 `Remove-Item -Recurse` 删联接有删穿到
真实目录的风险，那会毁掉你的服务端。
