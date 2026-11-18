# 从数字到数学

> It is not designed for everyone, but for the one who finds his place.

《从数字到数学》是一份面向高中生的数学讲义，服务于日常学习，也为复习和进一步探索提供材料。在具备相应先修知识的基础上，可以配合讲授用于首次学习，也可以在已有经验之后重新阅读。

讲义依照定义和推理的依赖组织内容，关注一个结论怎样得到、一种方法为什么适用，以及已有知识如何支持新的认识。各章围绕自己的研究对象形成完整的结构，前面建立的概念与工具也在后文继续发挥作用。不应试，但不反应试。

## 内容

| 章节 | 内容 |
| --- | --- |
| 第一章：分析引论 | 从数列进入极限、数项级数与迭代，建立研究无限过程的基础。 |
| 第二章：函数专题 | 从函数概念出发，研究连续性，整理初等函数的性质及常用公式。 |
| 第三章：向量代数 | 从几何向量进入线性空间、线性变换与复数。 |
| 第四章：二次曲线 | 组织方程、几何关系及多种表示方法，并通过仿射、射影等观点深化认识。 |
| 第五章：微积分初步 | 从变化率与累积量分别建立微分、积分，证明二者的联系，研究应用并以微分方程收束。 |
| 第六章：概率论与数理统计 | 从计数原理建立概率模型，由随机变量的分布走向抽样、估计、检验和回归。 |
| 附录 | 汇集常用记号、不等式及公式，供学习时查阅。 |

## 阅读方式

- 主线可独立完成相应专题的基本学习，读者可以跳过全部星号内容。
- 星号标记选讲范围和认识层次，通常围绕主线中的同一对象深化解释。可根据基础穿插阅读，也可完成主线后再集中学习。
- 例题保留题面，供课堂展开与独立思考。节内习题落实相应内容；章末综合习题覆盖全章，单题可以考察一个知识点，也可以联合多个知识点。
- 配套习题解另册编排，内容与构建说明见[习题解目录](solutions/README.md)。本仓库收录讲义及解答册的源码和构建文件。

各章的先修知识与更具体的使用说明见[前言](chapters/preface.tex)。

## 源码结构

| 路径 | 用途 |
| --- | --- |
| `main.tex` | 讲义编译入口。 |
| `solutions.tex` | 例题与习题解编译入口。 |
| `solutions/` | 按章分文件夹、按节组织的题面与解答源码。 |
| `mathnotes.cls` | 排版类，定义字体、标题、定理及习题等格式。 |
| `chapters/` | 正文、前后记及附录；较长章节按节拆分为独立文件。 |
| `media/` | 插图、独立TikZ文稿及部分插图的Python生成脚本。 |

## 编译

当前排版使用TeX Live与XeLaTeX，并调用Windows中文字体，包括宋体、黑体和楷体。其他系统需相应配置字体；字体变化可能影响分页。

以下命令在仓库根目录的PowerShell中执行，需确保`xelatex`与`latexmk`已加入`PATH`。

### 首次构建插图

插图PDF属于编译产物，不随源码提交。首次构建时，先编译`media/`中的独立TeX插图：

```powershell
Get-ChildItem -LiteralPath media -Filter *.tex | ForEach-Object {
    xelatex -interaction=nonstopmode -halt-on-error -output-directory=media $_.FullName
    if ($LASTEXITCODE -ne 0) {
        throw "插图编译失败：$($_.Name)"
    }
}
```

已收录生成后的TikZ源码，普通构建无需运行Python生成脚本。修改插图后，重新编译相应的TeX文件即可。

### 构建正文

```powershell
latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

输出为仓库根目录下的`main.pdf`。`latexmk`会按需重复编译，更新目录与交叉引用。

### 构建习题解

完成插图构建后，直接编译另册：

```powershell
latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error solutions.tex
```

输出为`solutions.pdf`。题面与解答保存在同一节源码中，编译无需运行Python脚本。PDF与其他编译产物不提交。

## 勘误

欢迎通过[Issues](https://github.com/EasterGhost/math/issues)反馈数学错误、表述疑问及排版问题。请注明所用提交版本、章节或题号，并尽量附上具体位置、问题说明或推导依据。页码可能随版本变化。

## 版权

Copyright (c) 2026 Andrew Elizabeth / EasterGhost.

除另有标注外，本项目中作者享有著作权与类似权利的内容采用[CC BY-NC-ND 4.0（署名—非商业性使用—禁止演绎）](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh-hans)许可协议。您可以按协议要求署名并为非商业目的复制、分享；协议不授予商业使用或分享演绎作品的权限。

引用的试题及其他第三方材料依其各自的权利状态处理，不包含在上述授权中。完整授权说明与协议全文见[LICENSE](LICENSE)；如需协议未授予的权限，可通过仓库[Issues](https://github.com/EasterGhost/math/issues)联系作者。
