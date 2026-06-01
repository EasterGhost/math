\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mathnotes}[2026/06/02 Math notes thesis-style class]

\LoadClass[UTF8,openany]{ctexbook}

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{graphicx}
\RequirePackage{adjustbox}
\RequirePackage{geometry}
\RequirePackage[hidelinks]{hyperref}

\geometry{a4paper,margin=2.5cm}

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
  }
}
