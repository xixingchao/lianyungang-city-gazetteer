# 连云港市志 第五十九卷《方言》全新重做项目

本项目用于从原始材料重新制作《连云港市志》第五十九卷《方言》。本轮重做不依托旧 OCR、旧重排文本、旧双审台账或旧交付结论。

## 原则

- 原始 PDF/CEB/JPG/XML 为最高证据层。
- 新 OCR、新页图、新台账全部在本项目内重新生成。
- 旧项目 `lianyungang-city-gazetteer-volume59-redo` 仅作为历史废案，不作为本轮依据。
- 旧 GitHub 维护包中的第59卷文本仅可在后续人工阶段作为差异参考；默认不纳入本轮起步流程。
- 方言、音标、声韵调表、同音字汇、方言词汇必须按 `gazetteer-digitization` skill 的 dialect/dictionary 模式单独分流。

## 目录

```text
config/
input/source/
workbench/page_images/original/
workbench/page_images/cropped/
workbench/ocr/raw/
workbench/layout/
workbench/dialect/
workbench/manual_transcription/
workbench/review/
workbench/qa/
scripts/
output/reports/
output/reader/
output/package/
```

## 当前源文件

原件目录：`E:\codex_Learing\17_project_数字化工作站\连云港志原件`

预计源 PDF：`连云港志下_2.pdf`

第59卷初步页段按历史证据定位为源 PDF 第 295-342 页；本轮会重新渲染页图并生成新的 `page_mapping.csv`，后续再由人工/版面检查确认卷边界。
