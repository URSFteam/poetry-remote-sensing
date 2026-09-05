# 《诗词遥感》电子版

本仓库用于在 Read the Docs 托管《诗词遥感》电子版。

Read the Docs 根据 `.readthedocs.yaml` 合并 `site.zip.part-*`，并将其中的静态 HTML 发布为网站。

## 本地重新生成

将 Word 稿件放在本仓库的上一级目录，然后运行：

```powershell
python generate_site.py
```

生成过程不会改动 Word 源文件。

生成 `site/` 后，将其压缩为 `site.zip` 并按小于 25 MB 的大小切分为 `site.zip.part-*`，即可更新托管版本。
