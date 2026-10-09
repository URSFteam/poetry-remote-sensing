# 《诗词遥感》电子版

本仓库用于在 Read the Docs 托管《诗词遥感》电子版。

Read the Docs 根据 `.readthedocs.yaml` 合并 `site.zip.part-*`，再用 `site-pages.zip` 覆盖更新后的页面，并将静态 HTML 发布为网站。

## 本地重新生成

将以下两份 Word 稿件放在本仓库的上一级目录：

- `诗词遥感-草稿 - 小修版-诗词楷体版.docx`
- `诗词遥感-序言-陈镜明.docx`

在已安装 `python-docx` 的 Python 环境中运行：

```powershell
python generate_site.py
python package_pages.py
```

生成过程不会改动 Word 源文件。

仅更新文字时，把新的 `site-pages.zip` 上传到 GitHub 仓库根目录，替换同名文件并提交。Read the Docs 构建后即可显示新版本；如没有自动构建，在项目的 Builds 页面手动构建 `latest`。

本次序言更新还需一并提交 `.readthedocs.yaml`、`generate_site.py`、`package_pages.py` 和本说明。以后仅改文字时只需更新 `site-pages.zip`。

若更换或增加正文插图，则还需重新打包包含 `site/` 的 `site.zip`，按 8 MiB 切分并以连续编号 `site.zip.part-01`、`site.zip.part-02` 等替换全部旧分卷。
