# 连云港市志工作站脚本

规则：不修改原始 `连云港市志(上|中|下)` 目录中的 CEB/JPG/XML；用户导出的 PDF 也作为只读输入处理。

- `parse_xml_metadata.ps1`：读取七个 GB2312 XML，生成源文件清单和 XML 目录初提取报告。
- `run_pdf_ocr.py`：读取已导出的上册 PDF，生成页图、逐页 OCR 文本/JSON、分册汇总和 OCR 统计。

## OCR 续跑命令

先跑样本：

```powershell
python .\连云港市志_workstation\scripts\run_pdf_ocr.py --sample --engine rapidocr --dpi 180
```

样本通过后跑上册 3 个 PDF 全量：

```powershell
python .\连云港市志_workstation\scripts\run_pdf_ocr.py --parts all --engine rapidocr --dpi 180
```
