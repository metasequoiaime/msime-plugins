# msime-plugins

水杉输入法（Metasequoia IME）的社区扩展包合集：音效包、音乐包、指令表、特效包、辅助码表、符号集、短语表和单词本。

扩展包是纯数据：一个 `plugin.toml` 加上音频或数据文件，不能带任何可执行内容，也不能申请权限。同一个包在 macOS、Windows、Linux 和鸿蒙电脑（2in1）上通用，不需要按平台分别制作。

## 扩展包列表

| 目录 | 类型 | 名称 | 说明 |
| --- | --- | --- | --- |
| [`packs/mech-blue-switch`](packs/mech-blue-switch) | 音效包 | 机械青轴 | 清脆的段落轴，空格和回车带卫星轴回响 |
| [`packs/soft-thock`](packs/soft-thock) | 音效包 | 静音线性轴 | 低沉的“咚”，没有咔嗒声，适合安静场合 |
| [`packs/kalimba`](packs/kalimba) | 音效包 | 拇指琴 | 五声音阶拇指琴，上屏时扫一个和弦 |
| [`packs/jasmine-flower`](packs/jasmine-flower) | 音效包·旋律 | 茉莉花 | 古筝音色，每按一个键弹一个音 |
| [`packs/fur-elise`](packs/fur-elise) | 音效包·旋律 | 致爱丽丝 | 钢琴音色，每按一个键弹一个音 |
| [`packs/two-tigers`](packs/two-tigers) | 音效包·旋律 | 两只老虎 | 玩具木琴音色，每次上屏弹一个音 |
| [`packs/rain-ambience`](packs/rain-ambience) | 音乐包 | 窗外小雨 | 约 38 秒无缝循环的雨声 |
| [`packs/kaomoji`](packs/kaomoji) | 指令表 | 颜文字 | `/kx` 开心、`/fp` 掀桌等 18 个颜文字 |
| [`packs/date-formats`](packs/date-formats) | 指令表 | 日期时间格式 | `/rq`、`/iso`、`/sjc` 等 13 种日期时间写法 |
| [`packs/symbols`](packs/symbols) | 指令表 | 常用符号 | `/ssd` ℃、`/dg` ✓、`/jt` → 等 31 个符号 |
| [`packs/neon`](packs/neon) | 特效包 | 霓虹 | 粉、青、紫三色火花，短促明亮 |
| [`packs/sakura`](packs/sakura) | 特效包 | 樱花 | 几片淡粉色花瓣慢慢飘散 |
| [`packs/fireworks`](packs/fireworks) | 特效包 | 烟花 | 金红烟花，连击越高越猛烈 |
| [`packs/soft-glow`](packs/soft-glow) | 特效包 | 微光 | 候选框淡淡亮一下，青绿色 |
| [`packs/math-symbols`](packs/math-symbols) | 符号集 | 数学符号 | 运算、关系、集合、逻辑、希腊字母等八组符号，外加一组颜文字 |
| [`packs/polite-phrases`](packs/polite-phrases) | 短语表 | 客套话 | K 模式下 `xx` 谢谢！、`xk` 辛苦了！、`qsd` 请稍等。等 51 条 |
| [`packs/cs-basic-words`](packs/cs-basic-words) | 单词本 | 计算机基础词汇 | 281 个计算机基础英语单词和短语，附简短中文释义 |

本仓库自带的这些包由维护者制作，特效包只是参数，指令表、符号集、短语表的内容和单词本的中文释义由维护者自己编写，同样以 CC0-1.0 发布。音频全部由 [`scripts/generate_seed_packs.py`](scripts/generate_seed_packs.py) 现场合成，没有任何录音或第三方素材，以 CC0-1.0 放入公有领域；旋律包演奏的乐曲均为传统民歌或早已进入公有领域的作品。

## 安装

在输入法设置的「插件」页，点「导入文件夹」选中 `packs/` 下的某个包目录，或点「导入 .zip」选中发布页下载的压缩包。导入时输入法会按与本仓库 CI 相同的规则再校验一遍，不合格的包不会被安装。

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
| `kind` | `sound`（音效包，含旋律）、`music`（音乐包）、`command_table`（指令表）、`effect`（特效包）、`helpcode`（辅助码表）、`symbol_set`（符号集）、`phrase_table`（短语表）、`wordbook`（单词本） |
| `id` | 小写字母、数字、`.`、`-`、`_`，以字母或数字开头，最长 64；本仓库内唯一，且与目录名一致 |
| `name` / `version` | 必填，分别最长 80 和 32 个字节 |
| `license` | 必填，SPDX 许可证表达式，覆盖目录里的全部文件，如 `CC0-1.0`、`CC-BY-4.0` |
| `author` / `description` | 选填，最长 120 和 500 个字节 |
| `permissions` | 必须为空数组 `[]` |

未列出的键会被拒绝。

### 音效包（`kind = "sound"`）

`mode = "keys"` 时在 `[sounds]` 里为按键分类指定采样：`default`（必填）、`space`、`enter`、`backspace`、`commit`、`achievement`，未指定的分类使用 `default`。`mode = "sequence"` 时在 `[sequence]` 里给一个采样 `sample` 和一串半音偏移 `semitones`（最多 128 个），每按一个键（`advance = "key"`）或每次上屏（`advance = "commit"`）弹下一个音，停顿三秒后从头开始。

采样只接受 WAV（PCM），单个不超过 1.5 秒、512 KiB，最多 8 个，整包不超过 4 MiB。Ogg 只用于背景音乐：短采样在各平台都要整段解码后播放，WAV 的时长能在播放前核实，Ogg 不能。

### 音乐包（`kind = "music"`）

`[music]` 的 `tracks` 列出最多 8 首曲目（WAV 或 Ogg Vorbis），单首不超过 15 分钟、16 MiB。输入法处于激活状态且开启背景音乐时循环播放，焦点在密码框时暂停。

### 指令表（`kind = "command_table"`）

`[[commands]]` 每项是 `trigger`（小写 ASCII 字母，最长 32）、`title`（候选旁显示的说明，最长 48 个字节）和 `template`。模板只能是文字加 `{date}`、`{date:格式}`、`{time}`、`{time:格式}`、`{weekday}` 这几个占位符，格式为 strftime 写法；不能含换行或制表符，展开后不超过 199 个 UTF-16 单元。每个包最多 256 条。

### 特效包（`kind = "effect"`）

特效包不带任何文件，只在 `[effect]` 里选用输入法内置的一种打字特效并调整参数：`style`（必填，`flash`、`sparks` 或 `power_mode`）、`intensity`（0 到 100，默认 50）、`colors`（1 到 4 个 `#RRGGBB` 颜色）、`duration_ms`（60 到 1500）、`particles`（每次按键的火花数，0 到 64）。目录里除了 `plugin.toml` 只能放 `.txt` / `.md` 说明。

在输入法设置「插件 → 我的插件」里打开特效包，选「使用此特效包」。macOS 用全部参数；Windows 和鸿蒙电脑只闪烁候选卡片，取强度、时长和第一个颜色；Linux 只显示连击计数，特效包没有可见效果。

### 辅助码表（`kind = "helpcode"`）

辅助码表替换全拼或双拼的辅助码方案。`[helpcode]` 只有 `table` 一个键，点名包里的一个 `.txt` 码表文件：

```
# 注释
好=nz
明=ry
```

- 文件 1 字节到 1 MiB，UTF-8（可以带 BOM），LF 或 CRLF 换行。
- 每行是空行、`#` 开头的注释，或者 `字=码`，等号两边不能有空格：字恰好是一个非 ASCII、非空白的 Unicode 字符，码是 1 到 2 个小写字母。
- 1 到 30000 条，同一个字只能出现一次。任何一行不合规，整个包被拒绝，不会跳过坏行。

在输入法设置「输入 → 辅助码」的方案下拉框里选「名称（插件）」，或在「插件 → 我的插件」里打开「用于全拼」或「用于双拼」，每个方案最多用一个辅助码表；选中的表被删除或无法载入时退回该方案原来的辅助码。macOS、Windows、Linux 桌面和鸿蒙电脑可用。

本仓库只提供 [`templates/helpcode`](templates/helpcode) 和一张几个字的演示表，不收录成熟的辅助码方案，投稿要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 符号集（`kind = "symbol_set"`）

符号集给符号面板追加符号组或颜文字组，全部写在清单里，没有数据文件。每个 `[[groups]]` 只有四个键：

| 键 | 说明 |
| --- | --- |
| `tab` | 必填，`symbols`（符号页，以包名作为一个分类）或 `kaomoji`（颜文字页，排在「All」之后） |
| `title` | 必填，组名，不能为空白，最长 48 个字节 |
| `keywords` | 选填，供搜索的关键词，写了就不能为空白，最长 256 个字节 |
| `items` | 必填，1 到 512 个字符串；每个 1 到 64 个 UTF-16 单元，不能为空白、不能含控制字符，同组内不能重复 |

每个包 1 到 32 组，合计最多 2048 项。不需要选用：导入后就出现在符号面板里，删除后消失，不与内置符号去重。显示插件符号集的是 Windows 和 Linux 的符号面板、macOS 的表情与符号面板，以及鸿蒙电脑的键盘符号选择器。

### 短语表（`kind = "phrase_table"`）

短语表给 K 模式（中文模式下按 Shift+K）添加短语，全部写在清单里，没有数据文件。`[[phrases]]` 每项只有 `key`（1 到 32 个小写字母）和 `text`（不能为空白，最长 199 个 UTF-16 单元，不能含换行、制表符等控制字符）。同一个 `key` 可以对应多段文字，但同一对 `key` 和 `text` 不能重复。每个包 1 到 2000 条。

在输入法设置「插件 → 我的插件」里打开短语表的「启用」，最多同时启用 16 个，按启用顺序排列。K 模式先列词库里的短语，再列编码以输入开头的插件短语。「输入 → 快捷模式」里关掉快捷短语时短语表不起作用。短语不写进词库，删除短语表后直接消失。macOS、Windows、Linux 桌面和鸿蒙电脑可用。

### 单词本（`kind = "wordbook"`）

单词本是背单词里的一本词书。`[wordbook]` 只有 `file` 一个键，点名包里的一个 `.tsv` 词表文件：

```
# 注释
algorithm	/ˈælɡərɪðəm/	n. 算法
compiler	n. 编译器
```

- 文件 1 字节到 4 MiB，UTF-8（可以带 BOM），LF 或 CRLF 换行；空行和 `#` 开头的行跳过。
- 每行是 `单词<TAB>释义` 或 `单词<TAB>音标<TAB>释义`，不支持引号转义。单词 1 到 64 个字符，音标不超过 64 个字符（可以留空），释义 1 到 256 个字符，都不能含控制字符。
- 1 到 20000 个单词，同一个单词只能出现一次。任何一行不合规，整个包被拒绝。
- `id` 除了通用规则，还只能用小写字母、数字和 `-`，首尾不能是 `-`，最长 59；`name` 最长 64 个字符。

导入后这本书出现在背单词的词书列表里，排在内置词书之后，标着「插件」；插件书不能在背单词里删除，要在插件页删除，删除后复习进度仍然保留。macOS、Windows、Linux 桌面和鸿蒙电脑可用。

完整的带注释示例见 [`templates/`](templates/)。

## 授权说明

本仓库的脚本与文档以 [GNU General Public License v3.0](LICENSE) 开源。每个扩展包的素材以其 `plugin.toml` 中 `license` 声明的许可证为准。

只接受作者本人原创、或明确处于公有领域、或以允许再分发的许可证发布的素材。翻录的商业音效、受版权保护的乐曲及其改编版本不会被合并，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。
