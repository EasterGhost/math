\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mathnotes}[2026/06/02 Math notes thesis-style class]

\LoadClass[UTF8,openany]{ctexbook}

\ifdefined\setCJKfamilyfont
  \setCJKfamilyfont{mathnoteskai}[AutoFakeBold=2]{KaiTi}
  \providecommand{\kaiti}{}
  \renewcommand{\kaiti}{\upshape\CJKfamily{mathnoteskai}}
  \renewcommand{\kaishu}{\kaiti}

  % 黑体同理：中文没有斜体字形，强制正体，免得在斜体环境（如定理环境）
  % 里去要 SimHei 的 it 字形而触发 “Font shape ... undefined” 警告
  \setCJKfamilyfont{mathnoteshei}[AutoFakeBold=2]{SimHei}
  \renewcommand{\heiti}{\upshape\CJKfamily{mathnoteshei}}
\else
  \providecommand{\kaiti}{\kaishu}
\fi

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{graphicx}
\RequirePackage{adjustbox}
\RequirePackage{wrapfig}
\RequirePackage{geometry}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{amsthm}

% ---- 定理环境 ----
\theoremstyle{definition}
\newtheorem{definition}{定义}[chapter]      % 按章编号：定义 1.1, 1.2...
\newtheorem{example}{例}[chapter]
\newtheorem{exercise}{习题}[chapter]

\theoremstyle{plain}
\newtheorem{theorem}{定理}[chapter]
\newtheorem{lemma}{引理}[chapter]
\newtheorem{proposition}{命题}[chapter]
\newtheorem{corollary}{推论}[chapter]

\theoremstyle{remark}
\newtheorem{remark}{注}[chapter]

% 证明环境（amsthm 自带，但用中文标签）
\renewcommand{\proofname}{\textbf{证明}}

\geometry{a4paper,margin=2.5cm}

\raggedbottom
\tolerance=1000
\emergencystretch=1em

\AtBeginDocument{
  \linespread{1}\songti\fontsize{12pt}{22pt}\selectfont
  \setlength{\abovedisplayskip}{12pt}
  \setlength{\belowdisplayskip}{12pt}
  \setlength{\abovedisplayshortskip}{6pt}
  \setlength{\belowdisplayshortskip}{6pt}
}
\setlength{\parindent}{2em}
\setlength{\parskip}{6pt}
\newcommand{\rightparen}{\mathclose{)}}

\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}

% ctex 的 \paragraph 是小标题，默认会往目录里写条目；本类目录只到 subsection，
% 所以在 \AtBeginDocument 里把 paragraph 级的目录项屏蔽掉
% （放在 AtBeginDocument 是为了捕获 hyperref 包装之后的最终版本）。
\AtBeginDocument{%
  \makeatletter
  \let\mathnotes@addcontentsline\addcontentsline
  \renewcommand\addcontentsline[3]{%
    \def\mathnotes@tempa{#2}\def\mathnotes@tempb{paragraph}%
    \ifx\mathnotes@tempa\mathnotes@tempb\else\mathnotes@addcontentsline{#1}{#2}{#3}\fi}%
  \makeatother
}

\makeatletter
\renewcommand*\l@chapter{\@dottedtocline{0}{0em}{1.8em}}
\renewcommand*\l@section{\@dottedtocline{1}{1.8em}{2.4em}}
\renewcommand*\l@subsection{\@dottedtocline{2}{4.2em}{3.2em}}
\makeatother

\ctexset{
  chapter = {
    name = {},
    number = \arabic{chapter},
    beforeskip = 12bp,
    afterskip = 0bp,
    format = \centering\heiti\fontsize{16pt}{22pt}\selectfont,
    nameformat = \heiti\fontsize{16pt}{22pt}\selectfont,
    numberformat = \heiti\fontsize{16pt}{22pt}\selectfont,
    titleformat = \heiti\fontsize{16pt}{22pt}\selectfont,
    aftername = \hspace{1em}
  },
  section = {
    beforeskip = 6bp,
    afterskip = 0bp,
    format = \heiti\fontsize{14pt}{22pt}\selectfont,
    numberformat = \heiti\fontsize{14pt}{22pt}\selectfont,
    titleformat = \heiti\fontsize{14pt}{22pt}\selectfont
  },
  subsection = {
    beforeskip = 6bp,
    afterskip = 0bp,
    format = \heiti\fontsize{12pt}{22pt}\selectfont,
    numberformat = \heiti\fontsize{12pt}{22pt}\selectfont,
    titleformat = \heiti\fontsize{12pt}{22pt}\selectfont
  },
  subsubsection = {
    beforeskip = 6bp,
    afterskip = 0bp,
    format = \songti\fontsize{12pt}{22pt}\selectfont,
    numberformat = \songti\fontsize{12pt}{22pt}\selectfont,
    titleformat = \songti\fontsize{12pt}{22pt}\selectfont
  },
  % 段落级小标题：与 subsection 同款字体字号（12pt 黑体），保留首行缩进。
  % 行内式（正文紧接在后面）:  \paragraph{1°连续性} 正文……
  % 独占一行式（标题单独占行）: \paragraph{1°多项式函数} \mbox{}  然后空一行再写正文
  %   注意：独占式不要用 \linebreak —— 那会把标题按两端对齐拉伸（"多 项 式 函 数"），
  %   而且会丢掉下一行的首行缩进；\mbox{} + 空行才是干净的写法。
  paragraph = {
    beforeskip = 0bp,     % 段落间距由 parskip 负责，这里再加会变成双倍
    afterskip = 1em,
    indent = 2em,
    aftername = \quad,
    format = \heiti\fontsize{12pt}{22pt}\selectfont
  }
}
