# msime-plugins

水杉输入法（Metasequoia IME）的社区扩展包合集：按键音效、旋律、背景音乐、`/` 指令表等。

扩展包是纯数据：一个 `plugin.toml` 加上音频或模板，不能带任何可执行内容，也不能申请权限。同一个包在 macOS、Windows、Linux 和鸿蒙电脑（2in1）上通用，不需要按平台分别制作。

## 扩展包列表

| 目录 | 类型 | 名称 | 说明 |
| --- | --- | --- | --- |

## 安装

在输入法设置的「扩展」页，点「导入文件夹」选中 `packs/` 下的某个包目录，或点「导入 .zip」选中发布页下载的压缩包。导入时输入法会按与本仓库 CI 相同的规则再校验一遍，不合格的包不会被安装。

导入后的包保存在各平台的状态目录下的 `plugins/`：

| 平台 | 位置 |
| --- | --- |
| macOS | `~/Library/Application Support/app.msime.macos/plugins/` |
| Windows | 数据目录下的 `plugins\`（默认 `%LOCALAPPDATA%\MSIME-Client\plugins\`） |
| Linux | `$XDG_CONFIG_HOME/msime-client/plugins/`（默认 `~/.config/msime-client/plugins/`） |
| 鸿蒙电脑 | 应用状态目录下的 `plugins/` |

不建议手动往这些目录里复制文件，用设置页导入才会校验。

## 扩展包结构

每个包是 `packs/` 下的一个目录，目录名与 `id` 一致，至少包含一个 `plugin.toml`，其余文件与它放在同一层（不支持子目录）：

```
packs/my-keys/
├── plugin.toml
├── key.wav
└── commit.wav
```

### 通用字段

| 键 | 说明 |
| --- | --- |
| `schema_version` | 格式版本，目前为 `1` |
| `kind` | `sound`（按键音效或旋律）、`music`（背景音乐）、`command_table`（`/` 指令表） |
| `id` | 小写字母、数字、`.`、`-`、`_`，以字母或数字开头，最长 64；本仓库内唯一，且与目录名一致 |
| `name` / `version` | 必填，分别最长 80 和 32 个字节 |
| `license` | 必填，SPDX 许可证表达式，覆盖目录里的全部文件，如 `CC0-1.0`、`CC-BY-4.0` |
| `author` / `description` | 选填，最长 120 和 500 个字节 |
| `permissions` | 必须为空数组 `[]` |

未列出的键会被拒绝。

### `kind = "sound"`

`mode = "keys"` 时在 `[sounds]` 里为按键分类指定采样：`default`（必填）、`space`、`enter`、`backspace`、`commit`、`achievement`，未指定的分类使用 `default`。`mode = "sequence"` 时在 `[sequence]` 里给一个采样 `sample` 和一串半音偏移 `semitones`（最多 128 个），每按一个键（`advance = "key"`）或每次上屏（`advance = "commit"`）弹下一个音，停顿三秒后从头开始。

采样只接受 WAV（PCM），单个不超过 1.5 秒、512 KiB，最多 8 个，整包不超过 4 MiB。Ogg 只用于背景音乐：短采样在各平台都要整段解码后播放，WAV 的时长能在播放前核实，Ogg 不能。

### `kind = "music"`

`[music]` 的 `tracks` 列出最多 8 首曲目（WAV 或 Ogg Vorbis），单首不超过 15 分钟、16 MiB。输入法处于激活状态且开启背景音乐时循环播放，焦点在密码框时暂停。

### `kind = "command_table"`

`[[commands]]` 每项是 `trigger`（小写 ASCII 字母，最长 32）、`title`（候选旁显示的说明，最长 48 个字节）和 `template`。模板只能是文字加 `{date}`、`{date:格式}`、`{time}`、`{time:格式}`、`{weekday}` 这几个占位符，格式为 strftime 写法；不能含换行或制表符，展开后不超过 199 个 UTF-16 单元。每个包最多 256 条。

完整的带注释示例见 [`templates/`](templates/)。

## 授权说明

本仓库的脚本与文档以 [GNU General Public License v3.0](LICENSE) 开源。每个扩展包的素材以其 `plugin.toml` 中 `license` 声明的许可证为准。

只接受作者本人原创、或明确处于公有领域、或以允许再分发的许可证发布的素材。翻录的商业音效、受版权保护的乐曲及其改编版本不会被合并，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。
