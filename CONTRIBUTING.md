# 贡献扩展包

1. 从 [`templates/`](templates/) 复制最接近的模板到 `packs/<你的 id>/`，目录名与 `plugin.toml` 里的 `id` 保持一致。
2. 修改 `plugin.toml` 的 `id`、`name`、`author`、`description`，替换为你自己的素材。
3. 在输入法设置的「扩展」页用「导入文件夹」导入这个目录，确认能正常导入、听起来符合预期。
4. 在 README 的扩展包列表里加一行，然后提交 PR。

CI 会用输入法导入时的同一套规则校验每个包，校验不过的 PR 不会被合并。想在提交前自己检查，可以在 [metasequoiaime/msime](https://github.com/metasequoiaime/msime) 里执行 `cargo build -p msime-pack-tool --bin msime-pack` 编出校验工具，再在本仓库运行 `scripts/check-packs.sh <msime-pack 的路径>`。

合并到 main 后，CI 会把每个包打成 `<id>-<version>.zip` 发到 [Packs 发布页](https://github.com/metasequoiaime/msime-plugins/releases/tag/packs)。

## 素材要求

- 素材必须是你本人原创、明确处于公有领域，或以允许再分发的许可证发布；`license` 字段要覆盖目录里的每个文件。素材有出处时，在 PR 描述里写明来源链接。
- 乐曲要注意：古典作品本身处于公有领域，但别人的录音与编曲通常不是。请使用自己的演奏、合成，或许可证明确允许再分发的录音。
- 不接受从商业产品（其他输入法、游戏、键盘厂商等）里提取的音效。
- 音量适中，开头结尾不要有爆音。按键音应短促，避免在快速打字时互相叠成噪声。
- 一个 PR 只提交一个包，或同一作者的一组相关包。

## 更新已有的包

修改素材或指令时提高 `version`。不要修改已发布包的 `id`，否则已经导入的用户会把它当成另一个包。
