# pstack skills（poteto-mode）

来源：https://github.com/cursor/plugins 的 `pstack/skills`（MIT，Lauren Tan），commit ccb5507cec1546dc88135c1139c811e6c59115ba（2026-10-07）。原样复制，未改动内容。
另含 `cursor-team-kit/skills` 中被 poteto-mode 直接引用的 `deslop`、`control-cli`、`control-ui`，以及 `.cursor/agents/poteto-agent.md`（poteto-mode 派子代理时用的 subagent_type）。

未包含（不是文件缺失，而是 Cursor 内置功能）：`create-skill`、`/loop`、Cursor 内置 babysit。
`poteto-help` 里指向 `../../docs/guide/*.md` 的链接未随附（pstack 用户指南，非技能文件）。

唯一的删减：去掉了 `poteto-mode/scripts/` 下 5 个测试文件（`orch/orch.test.ts`、`watch-pr/{cli,github,policy}.test.ts`、`watch-pr/fakes.test-helper.ts`）。它们只用于开发这些脚本本身，而 `orch.test.ts` 会让 `eslint .` 报错（react-hooks/rules-of-hooks），影响仓库的 lint。
