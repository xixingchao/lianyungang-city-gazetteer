param(
  [string]$ProjectRoot = "E:\codex_Learing\09_project_东辛农场",
  [string]$WorkstationRoot = "E:\codex_Learing\09_project_东辛农场\连云港市志_workstation"
)

$ErrorActionPreference = "Stop"

function Get-TextValue($node, [string]$name) {
  $item = $node.SelectSingleNode($name)
  if ($null -eq $item) { return "" }
  return ($item.InnerText -replace "\s+", " ").Trim()
}

function Collect-CatalogRows($node, [int]$level, [string]$parent) {
  $rows = @()
  foreach ($child in $node.ChildNodes) {
    if ($child.Name -ne "catalogRow") { continue }
    $name = $child.GetAttribute("chapterName")
    $page = $child.GetAttribute("ebookPageNum")
    $path = if ([string]::IsNullOrWhiteSpace($parent)) { $name } else { "$parent / $name" }
    $rows += [pscustomobject]@{
      Level = $level
      Name = $name
      EbookPageNum = $page
      Path = $path
    }
    $rows += Collect-CatalogRows -node $child -level ($level + 1) -parent $path
  }
  return $rows
}

$sources = @(
  @{ Volume = "上"; Part = "part01"; Base = "连云港市志(上).1"; Dir = Join-Path $ProjectRoot "连云港市志(上)" },
  @{ Volume = "上"; Part = "part02"; Base = "连云港市志(上).2"; Dir = Join-Path $ProjectRoot "连云港市志(上)" },
  @{ Volume = "上"; Part = "part03"; Base = "连云港市志(上).3"; Dir = Join-Path $ProjectRoot "连云港市志(上)" },
  @{ Volume = "中"; Part = "part01"; Base = "连云港市志(中).1"; Dir = Join-Path $ProjectRoot "连云港市志(中)" },
  @{ Volume = "中"; Part = "part02"; Base = "连云港市志(中).2"; Dir = Join-Path $ProjectRoot "连云港市志(中)" },
  @{ Volume = "下"; Part = "part01"; Base = "连云港市志(下).1"; Dir = Join-Path $ProjectRoot "连云港市志(下)" },
  @{ Volume = "下"; Part = "part02"; Base = "连云港市志(下).2"; Dir = Join-Path $ProjectRoot "连云港市志(下)" }
)

$gb2312 = [System.Text.Encoding]::GetEncoding("GB2312")
$summary = @()
$catalogReport = New-Object System.Collections.Generic.List[string]
$manifestReport = New-Object System.Collections.Generic.List[string]

$catalogReport.Add("# 连云港市志 XML 目录初提取") | Out-Null
$catalogReport.Add("") | Out-Null
$catalogReport.Add("生成时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')") | Out-Null
$catalogReport.Add("") | Out-Null
$catalogReport.Add("说明：本报告来自 CEB 同目录 XML 的 `Catalog`，只作为目录初稿；后续必须与源页目录核对。") | Out-Null
$catalogReport.Add("") | Out-Null

$manifestReport.Add("# 连云港市志源文件清单") | Out-Null
$manifestReport.Add("") | Out-Null
$manifestReport.Add("生成时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')") | Out-Null
$manifestReport.Add("") | Out-Null
$manifestReport.Add("原始源文件只登记，不改名、不覆盖。") | Out-Null
$manifestReport.Add("") | Out-Null
$manifestReport.Add("| 卷 | 分册 | 类型 | 路径 | 大小 | 修改时间 |") | Out-Null
$manifestReport.Add("| --- | --- | --- | --- | ---: | --- |") | Out-Null

foreach ($src in $sources) {
  $ceb = Join-Path $src.Dir ($src.Base + ".ceb")
  $jpg = Join-Path $src.Dir ($src.Base + ".jpg")
  $xmlPath = Join-Path $src.Dir ($src.Base + ".xml")

  foreach ($kind in @(@("CEB", $ceb), @("JPG", $jpg), @("XML", $xmlPath))) {
    $file = Get-Item -LiteralPath $kind[1]
    $manifestReport.Add("| $($src.Volume) | $($src.Part) | $($kind[0]) | ``$($file.FullName)`` | $($file.Length) | $($file.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')) |") | Out-Null
  }

  $text = $gb2312.GetString([System.IO.File]::ReadAllBytes($xmlPath))
  [xml]$xml = $text
  $root = $xml.SelectSingleNode("/book-metadata")
  $bib = $xml.SelectSingleNode("/book-metadata/bib-metadata")
  $catalog = $xml.SelectSingleNode("/book-metadata/bib-metadata/Catalog")
  $rows = if ($null -eq $catalog) { @() } else { Collect-CatalogRows -node $catalog -level 1 -parent "" }
  $topRows = @($rows | Where-Object { $_.Level -eq 1 })
  $maxLevel = if (@($rows).Count -eq 0) { 0 } else { (@($rows | Measure-Object -Property Level -Maximum).Maximum) }

  $bookName = Get-TextValue $root "BookName"
  $title = if ($null -eq $bib) { "" } else { Get-TextValue $bib "Title" }
  $creator = if ($null -eq $bib) { "" } else { Get-TextValue $bib "Creator" }
  $publisher = if ($null -eq $bib) { "" } else { ($bib.Publisher.InnerText -replace "\s+", " ").Trim() }
  $publishDate = Get-TextValue $root "PublishDate"
  $isbn = Get-TextValue $root "BookID"

  $summary += [pscustomobject]@{
    Volume = $src.Volume
    Part = $src.Part
    BaseName = $src.Base
    BookName = $bookName
    Title = $title
    Creator = $creator
    Publisher = $publisher
    PublishDate = $publishDate
    ISBN = $isbn
    CebBytes = (Get-Item -LiteralPath $ceb).Length
    CatalogRows = @($rows).Count
    TopCatalogRows = @($topRows).Count
    MaxCatalogLevel = $maxLevel
  }

  $catalogReport.Add("## $($src.Volume) $($src.Part) $($src.Base)") | Out-Null
  $catalogReport.Add("") | Out-Null
  $catalogReport.Add("- 书名：$bookName") | Out-Null
  $catalogReport.Add("- 标题：$title") | Out-Null
  $catalogReport.Add("- 编者/作者：$creator") | Out-Null
  $catalogReport.Add("- 出版者：$publisher") | Out-Null
  $catalogReport.Add("- 出版日期：$publishDate") | Out-Null
  $catalogReport.Add("- ISBN/BookID：$isbn") | Out-Null
  $catalogReport.Add("- 目录条目数：$(@($rows).Count)，顶层条目：$(@($topRows).Count)，最大层级：$maxLevel") | Out-Null
  $catalogReport.Add("") | Out-Null
  $catalogReport.Add("| 层级 | 电子页 | 目录路径 |") | Out-Null
  $catalogReport.Add("| ---: | ---: | --- |") | Out-Null
  foreach ($row in $rows) {
    $catalogReport.Add("| $($row.Level) | $($row.EbookPageNum) | $($row.Path) |") | Out-Null
  }
  $catalogReport.Add("") | Out-Null
}

$summaryPath = Join-Path $WorkstationRoot "workbench\indexes\连云港市志_XML元数据摘要.csv"
$manifestPath = Join-Path $WorkstationRoot "workbench\indexes\连云港市志_源文件清单.md"
$catalogPath = Join-Path $WorkstationRoot "workbench\indexes\连云港市志_XML目录初提取.md"

$summary | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath $summaryPath
[System.IO.File]::WriteAllLines($manifestPath, $manifestReport, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllLines($catalogPath, $catalogReport, [System.Text.Encoding]::UTF8)

Write-Host "生成完成:"
Write-Host "- $summaryPath"
Write-Host "- $manifestPath"
Write-Host "- $catalogPath"
