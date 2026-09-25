## 改了什么

<!-- 简要说明这次改动的内容 -->

## 为什么改

<!-- 解决了什么问题，或补上了哪条缺失的规则 -->

## 依据

<!-- 说明书哪一章？还是某个服务端的实践经验？ -->
<!-- 如果是实践经验，说明是「哪一类服务端的常见做法」即可，不要附私有服务端文件 -->

## 自检清单

- [ ] 已跑 `python -m unittest discover -s tests`，全部通过
- [ ] 已跑 `python scripts\check_generated.py`，守卫通过
- [ ] 已跑 `python scripts\validate_knowledge_base.py`，无缺失链接与乱码
- [ ] 已跑 `python lf-mir200-knowledge\scripts\lf_kb.py --root lf-mir200-knowledge validate`，`ok: true`
- [ ] **已通读自己的 diff，确认不含任何私有服务端的路径、脚本名、物品名、NPC 名**
- [ ] 没有手工编辑 `references/mir200-thinking.md` 或 `references/mir200-training.md`

## 补充说明

<!-- 可选：需要审阅者特别注意的地方 -->
