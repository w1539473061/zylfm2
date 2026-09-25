# 用 AI 接入你自己的服务端

这份文档给「已经拿到这个技能、想让它读懂我自己服务端」的人用。

技能自带 849 章说明书，**不接入服务端也能查命令语法**。但如果你想让它回答
「我这个服里 XX 功能是怎么实现的」，就需要把服务端脚本接进来让它检索。

下面两段提示词，按需要复制给 AI（Claude Code / Codex / ZCode / Cursor 都能用）。
**复制前先把里面的路径改成你自己的。**

## 一、接入技能

技能装到本机技能目录后，AI 客户端会自动认到它，以后开新会话也能用。

```text
我搞了个翎风引擎（LF/LFM2/GEEM2）Mir200 脚本的知识库技能，想让你接入本机，
以后我写脚本的时候你直接帮我查。

仓库我放在：D:\zcode\zylfm2
（要是这个目录还没有，你帮我克隆下来：
  git clone https://github.com/w1539473061/zylfm2.git D:\zcode\zylfm2 ）

技能在仓库里的 lf-mir200-knowledge 文件夹。你帮我装到本机技能目录：

  cd /d D:\zcode\zylfm2
  python scripts\install_skill.py --target zcode

装的时候会跳过生成的索引，所以装完你建一次：

  python "%USERPROFILE%\.zcode\skills\lf-mir200-knowledge\scripts\lf_kb.py" --root "%USERPROFILE%\.zcode\skills\lf-mir200-knowledge" update

然后确认技能是好的：

  python "%USERPROFILE%\.zcode\skills\lf-mir200-knowledge\scripts\lf_kb.py" --root "%USERPROFILE%\.zcode\skills\lf-mir200-knowledge" validate

以后我让你查命令、写脚本，你先去技能自带的 849 章说明书里检索，
把依据的章节路径写出来。说明书里查不到的就直说没收录，不要凭记忆编。
```

用 Codex 的话把 `--target zcode` 换成 `--target codex`，路径里的 `.zcode` 换成 `.codex`。

## 二、接入你自己的服务端

这一步做完，技能就能检索你服务端里的真实脚本了。

```text
我有个翎风引擎的 Mir200 服务端，想让你接上知识库技能，这样你能看懂我自己服里的脚本。

技能我装在：%USERPROFILE%\.zcode\skills\lf-mir200-knowledge
（没装技能的话，就用仓库里的 D:\zcode\zylfm2\lf-mir200-knowledge）

我的服务端在：D:\MirServer\Mir200
注意是 Mir200 那一层，里面能看到 Envir 文件夹，不是 D:\MirServer 这个根目录。

你分两步弄。

第一步先把技能本身跑通，这步跟我的服务端没关系。先看技能完不完整：

  python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" validate

如果提示索引不存在，就先建一次：

  python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" update

第二步把我服务端接进去：

  cmd /c mklink /J "<技能目录>\样本Mir200" "D:\MirServer\Mir200"

这是目录联接，普通权限就能建，不用管理员。要是系统不让建，就直接复制一份过去，
但记得我服务端改了之后要重新拷。

接好再跑一次 update，然后 validate，看输出里 sample_index_records 这个数字，
大于 0 才算接上了。还是 0 就是没接对，你排查一下。

接上之后带我学一遍：
先看 references\mir200-training.md 里的课程顺序，再对着 mir200-thinking.md 看脚本思路，
然后一课一课来，每课都去我服务端里找真实脚本对着看。

以后我问你问题的时候：
- 说清楚哪些是说明书的官方说法、哪些是你从我脚本里推断出来的，别混着说
- 引用要指到具体文件
- 我的脚本是 GBK 编码，你要改就保持原编码和换行

三条底线，别碰：
1. 只做静态分析，不要编译、不要启动服务端
2. 不要动 .exe / .db / .dat / .lic 和 Log 目录里的东西
3. 我服务端的内容不要传到网上，也不要提交到任何公开仓库

弄完把 validate 的实际输出贴给我，我要看到那个数字。
```

## 你需要补上的信息

两段提示词里要改的地方：

| 要改的 | 改成什么 | 怎么确认改对了 |
| --- | --- | --- |
| 技能仓库路径 | 你放仓库的地方 | 该目录下能看到 `lf-mir200-knowledge` 文件夹 |
| 技能目录 | 装好后的技能位置 | 该目录下能看到 `SKILL.md` 和 `knowledge_base` 文件夹 |
| 我的服务端 | 包含 `Envir` 的那一层 | 该目录下能看到 `Envir` 文件夹，且 `Envir` 里有 `MapInfo.txt` |

最后一处最容易填错。`Mir200` 的典型结构是：

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

不是含糊其辞的「可能」，是实测确认的。我拿一个假服务端试过，跑完 `update` 后
这两个文件里出现了这样的整行内容：

```
- `样本Mir200/Envir/QuestDiary/我的专属系统/装备回收_老王定制版.txt` ([@main], @main)
- `样本Mir200/Envir/Market_def/比奇省/老王杂货商-0.txt` (#SAY)
```

连我随手编的「老王」这种名字都原样带出去了。换成你的服务端，出去的就是你的
真实目录名和脚本名。

**这对本地使用没有影响，是正常行为，你不用管它。** 它只是让技能知道
「这个功能在你服的哪个文件里」，不跑 `update` 反而检索不到你自己的脚本。

但如果你之后想把改进**提交回上游仓库**，就必须先处理掉——否则等于把你的服务端
目录结构和脚本名公开出去。具体做法见 [AI_GUIDE.md](AI_GUIDE.md)，
那里的守卫脚本会直接告诉你哪个文件第几行泄漏了什么。

## 用完了想断开

把 `样本Mir200` 联接删掉，再跑一次 `update` 清空索引：

```powershell
# 删联接（注意：不要用 Remove-Item -Recurse，那会删掉真实服务端内容）
[System.IO.Directory]::Delete("<技能目录>\样本Mir200", $false)

python "<技能目录>\scripts\lf_kb.py" --root "<技能目录>" update
```

删联接那条命令**务必用上面这种写法**。用 `Remove-Item -Recurse` 删联接有删穿到
真实目录的风险，那会毁掉你的服务端。
