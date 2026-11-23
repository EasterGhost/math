# 从数字到数学·例题与习题解

本册为《从数字到数学》的配套解答，与讲义同为 1.0 候选版（RC2，2026年11月24日）。各章按讲义题号收录例题、习题及部分思考任务，保留完整题面、各小问和选做标记。

| 章节 | 文件夹 | 解答单元 |
| --- | --- | ---: |
| 第一章：分析引论 | `chapters/analysis/` | 67 |
| 第二章：函数 | `chapters/functions/` | 53 |
| 第三章：向量代数 | `chapters/vector/` | 91 |
| 第四章：二次曲线 | `chapters/quadratic/` | 523 |
| 第五章：微积分 | `chapters/calculus/` | 436 |
| 第六章：概率论与数理统计 | `chapters/probability/` | 156 |
| 附录 A：集合与常用逻辑用语 | `chapters/appendices/` | 12 |
| 合计 | | 1338 |

解答首先采用讲义已经建立的目标方法，有价值的其他解法并列说明。正文已完整解答的迭代引入例子不重复收录；1.3未单列例题或习题，仅保留位置说明。第三章习题3.2的两小问共用图形，合为一个解答单元。

## 源码结构

`solutions.tex`是根目录的编译入口。`chapters/`下六个章入口分别引入各章文件夹中的节文件；题号、题面和解答在同一节文件内维护。`solutions-style.tex`定义解答册的排版，`media/`保存解答册单独使用的插图源码。修订时直接修改相应节文件。

## 编译

使用与正文相同的TeX Live、XeLaTeX和字体环境。在仓库根目录执行：

```powershell
latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error solutions.tex
```

输出为根目录下的`solutions.pdf`。无需Python整合步骤，也不依赖本地编写记录。

第三章复用`media/vector-cube.pdf`，第六章复用`media/probability-histogram-exam.pdf`。首次构建前，按仓库根目录README的说明编译插图，或分别用XeLaTeX编译这两个同名`.tex`文件。其他解答图形随解答册一并编译。

编写任务、交接记录、审查材料及内部脚本留在本地，不纳入正式源码。PDF与中间编译产物也不提交。
