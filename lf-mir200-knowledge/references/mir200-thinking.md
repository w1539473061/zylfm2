# Mir200 Script Thinking

This package includes the manual knowledge base; add local `样本Mir200` scripts to regenerate sample-derived patterns.

## Principles

- 先找入口，再看条件，再看动作，最后确认状态回写。
- NPC 脚本常把问答、跳转、奖励和退出放在同一条线里处理。
- 任务脚本常把 UI 交互、背包检测、物品流转和反馈消息绑定在一起。
- 地图事件与自动化脚本常靠定时器、全局变量和场景条件驱动。
- MapInfo 中的 `源地图 源X,源Y -> 目标地图 目标X,目标Y` 是地图链接；玩家踩到源坐标后进入目标坐标。
- `QMission-0.txt` 这类任务页展示脚本不要用 `GOTO @标签` 做当前进度页分发；菜单用 `<文本/@标签>` 直连，进度页把 `#IF / #SAY / #ACT BREAK` 直接写在目标标签里。

## Patterns


## Dominant Categories


## Reading Discipline

- Treat the manual as syntax authority and `样本Mir200` as practical usage authority when local samples are available.
- The public package does not include `样本Mir200`; do not present sample-derived behavior as verified until a local sample root is supplied.
- For any script, write down: entry, guards, actions, state writeback, failure path.
- If a pattern appears in multiple examples, prefer the repeated local style over a one-off shortcut.

## Update Loop

1. Refresh `docs.json` and `sample.json`.
2. Rebuild this summary from the current sample scripts.
3. Rebuild `mir200-training.md` so the learning course follows current examples.
4. Read this file before answering new Mir200 questions.

Source root: `lf-mir200-knowledge`
