"""Regenerate the existing function and vector illustrations as standalone TikZ.

Run from any directory. Use --compile to build the corresponding PDF figures.
Only the Python standard library and XeLaTeX from PATH are required.
"""
from pathlib import Path
from math import sin, cos, tan, pi, exp, atan, sqrt
from concurrent.futures import ThreadPoolExecutor
import argparse
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
HEADER = r"""\documentclass[tikz,border=3pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta,calc}
\definecolor{curveblue}{HTML}{245C86}
\definecolor{accent}{HTML}{A65E2E}
\definecolor{curveteal}{HTML}{287B6D}
\definecolor{curveviolet}{HTML}{76578B}
\begin{document}
\begin{tikzpicture}[font=\small,>=Latex,line cap=round,line join=round]
"""
FIGURES = {}


def pt(x, y):
    return f"({x:.6f},{y:.6f})"


def graph(fn, lo, hi, style="curveblue,thick", samples=240):
    pts = [pt(lo + (hi-lo)*i/samples, fn(lo + (hi-lo)*i/samples))
           for i in range(samples+1)]
    return "\\draw[" + style + "] plot coordinates {" + " ".join(pts) + "};\n"


def label(x, y, text, anchor="above"):
    return f"\\node[{anchor}] at {pt(x,y)} {{${text}$}};\n"


def axes(xlo, xhi, ylo, yhi, xname="x", yname="y"):
    return (f"\\draw[->,black!65] {pt(xlo,0)}--{pt(xhi,0)} node[right]{{${xname}$}};\n"
            f"\\draw[->,black!65] {pt(0,ylo)}--{pt(0,yhi)} node[above]{{${yname}$}};\n")


FIGURES["function-composition"] = r"""
\node (x) at (0,0) {$x\in A$};
\node (u) at (7,0) {$u=g(x)\in B$};
\node (y) at (15,0) {$y=f(u)\in C$};
\draw[->,curveblue,thick] (x)--node[above]{$g$}(u);
\draw[->,accent,thick] (u)--node[above]{$f$}(y);
"""

body = ""
for k in range(3):
    body += f"\\begin{{scope}}[shift={{({k*4.7},0)}},x=1.05cm,y=.65cm]\n"
    body += axes(-1.65, 1.8, -1.35, 1.55)
    if k == 0:
        body += r"\draw[curveblue,thick] (-1.5,-1)--(0,-1) (0,1)--(1.5,1);"+"\n"
        body += r"\draw[curveblue,fill=white] (0,-1) circle (2pt) (0,1) circle (2pt);"+"\n"
        body += r"\fill[accent] (0,0) circle (2pt);"+"\n"
        body += label(-.08, -1, "-1", "below left") + label(-.08, 1, "1", "above left")
    elif k == 1:
        body += r"\draw[curveblue,thick] (-1.5,1)--(1.5,1);"+"\n"
        body += r"\draw[curveblue,fill=white] (0,1) circle (2pt);\fill[accent] (0,0) circle (2pt);"+"\n"
        body += label(-.08, 1, "1", "above left")
    else:
        body += r"\draw[curveblue,thick] (-1.5,1)--(1.5,1);\fill[curveblue] (0,1) circle (2pt);"+"\n"
        body += label(-.08, 1, "1", "above left") + label(-.05, 0, "O", "below left")
    body += "\\end{scope}\n"
FIGURES["function-continuity"] = body

FIGURES["trig-unit-circle"] = r"""
\begin{scope}[scale=1.7]
\draw[curveblue,thick] (0,0) circle (1);
\draw[accent,very thick] (1,0) arc[start angle=0,end angle=40,radius=1];
\draw[->,black!65] (-1.2,0)--(1.4,0) node[right]{$x$};
\draw[->,black!65] (0,-1.18)--(0,1.3) node[above]{$y$};
\coordinate (A) at ({cos(40)},{sin(40)});
\draw[black!50,dashed] (A)--({cos(40)},0) (A)--(0,{sin(40)});
\draw[->,curveblue,thick] (0,0)--(A);
\draw[accent,->] (.28,0) arc[start angle=0,end angle=40,radius=.28];
\node at (.43,.15) {$\theta$};
\node[above left] at (.38,.32) {$1$};
\node[below] at ({cos(40)},0) {$\cos\theta$};
\node[left] at (0,{sin(40)}) {$\sin\theta$};
\node[below left] at (0,0) {$O$};
\node[above right] at (A) {$A$};
\fill[curveblue] (A) circle (1.1pt);
\end{scope}
"""

body = "\\begin{scope}[x=1.04cm,y=.70cm]\n"
body += axes(-2*pi-.15, 2*pi+.3, -1.3, 1.4)
body += graph(sin, -2*pi, 2*pi) + graph(cos, -2*pi, 2*pi, "accent,dashed,thick")
for x, text in [(-2*pi, "-2\\pi"), (-pi, "-\\pi"), (pi, "\\pi"), (2*pi, "2\\pi")]:
    body += f"\\draw[black!60] {pt(x,-.08)}--{pt(x,.08)};\n" + label(x, -.09, text, "below")
for y in [-1, 1]:
    body += f"\\draw[black!60] (-.05,{y})--(.05,{y});\n" + label(-.07, y, str(y), "left")
body += label(-.05, 0, "O", "below left")
body += r"\draw[curveblue,thick] (-5.6,1.65)--(-4.9,1.65) node[right,black]{$y=\sin x$};"+"\n"
body += r"\draw[accent,dashed,thick] (2.3,1.65)--(3,1.65) node[right,black]{$y=\cos x$};"+"\n"
FIGURES["trig-sine-cosine"] = body + "\\end{scope}\n"

body = "\\begin{scope}[x=1.04cm,y=.54cm]\n"
body += axes(-2*pi-.15, 2*pi+.3, -3.35, 3.55)
for j in [-3, -1, 1, 3]:
    x = j*pi/2
    body += f"\\draw[black!45,dashed] {pt(x,-3.2)}--{pt(x,3.2)};\n"
    text = { -3:r"-\frac{3\pi}{2}", -1:r"-\frac\pi2", 1:r"\frac\pi2", 3:r"\frac{3\pi}{2}"}[j]
    body += label(x, -3.3, text, "below")
for j in range(-2, 3):
    lo, hi = max(-2*pi, j*pi-atan(3.2)), min(2*pi, j*pi+atan(3.2))
    body += graph(tan, lo, hi, samples=150)
for x, text in [(-2*pi, "-2\\pi"), (-pi, "-\\pi"), (pi, "\\pi"), (2*pi, "2\\pi")]:
    body += label(x, -.08, text, "below")
for y in [-3,-2,-1,1,2,3]:
    body += f"\\draw[black!60] (-.05,{y})--(.05,{y});\n" + label(-.06,y,str(y),"left")
body += label(-.05, 0, "O", "below left") + label(3.7, 2.8, r"y=\tan x")
FIGURES["trig-tangent"] = body + "\\end{scope}\n"

body = "\\begin{scope}[x=1.55cm,y=.19cm]\n"
body += axes(-2.1, 2.15, -.6, 26)
for x in [-2,-1,1,2]:
    body += f"\\draw[black!60] {pt(x,-.3)}--{pt(x,.3)};\n" + label(x,-.4,str(x),"below")
for y in [5,10,15,20,25]:
    body += f"\\draw[black!60] {pt(-.025,y)}--{pt(.025,y)};\n" + label(-.045,y,str(y),"left")
body += label(-.025,-.35,"O","below left")
specs=[(.2,"accent",r"(0.2)^x"),(.5,"curveviolet,dashed",r"(0.5)^x"),
       (2,"curveteal,dashed",r"2^x"),(exp(1),"black!65,dash dot",r"e^x"),(5,"curveblue",r"5^x")]
for a,style,text in specs:
    body += graph(lambda x,a=a:a**x,-2,2,style+",thick")
for j,(_,style,text) in enumerate(specs):
    y=23.5-j*2.8
    body += f"\\draw[{style},thick] {pt(.28,y)}--{pt(.68,y)};\n"+label(.73,y,text,"right")
body += "\\fill[curveblue] (0,1) circle (1.4pt);\n"+label(-.06,1,"1","left")
FIGURES["function-exponentials"] = body + "\\end{scope}\n"

FIGURES["vector-addition"] = r"""
\coordinate (O) at (0,0); \coordinate (A) at (2.55,.25);
\coordinate (C) at (.8,1.5); \coordinate (B) at (3.35,1.75);
\draw[->,curveblue,thick] (O)--node[below]{$\vec a$}(A);
\draw[->,curveblue,thick] (C)--node[above]{$\vec a$}(B);
\draw[->,accent,thick] (O)--node[left]{$\vec b$}(C);
\draw[->,accent,thick] (A)--node[right]{$\vec b$}(B);
\draw[->,black!75] (O)--(B);
\node[below left] at (O) {$O$};\node[below right] at (A) {$A$};
\node[above left] at (C) {$C$};\node[above right] at (B) {$B$};
"""

FIGURES["vector-decomposition"] = r"""
\coordinate (O) at (0,0); \coordinate (D) at (2.34,.36);
\coordinate (E) at (.60,1.50); \coordinate (P) at (2.94,1.86);
\draw[->,curveblue,thick] (O)--node[below,sloped]{$x\vec e_1$}(D);
\draw[->,accent,thick] (O)--node[left]{$y\vec e_2$}(E);
\draw[black!45,dashed] (E)--(P)--(D);
\draw[->,black!80,thick] (O)--node[above,sloped]{$\vec a$}(P);
\node[below left] at (O) {$O$};\node[below right] at (D) {$D$};
\node[above left] at (E) {$E$};\node[above right] at (P) {$P$};
\fill[black!75] (P) circle (1.2pt);
"""

FIGURES["vector-cube"] = r"""
\coordinate (A) at (0,0); \coordinate (B) at (2.35,0);
\coordinate (C) at (3.2,.85); \coordinate (D) at (.85,.85);
\coordinate (Ap) at (0,2.35); \coordinate (Bp) at (2.35,2.35);
\coordinate (Cp) at (3.2,3.2); \coordinate (Dp) at (.85,3.2);
\draw[black!70] (A)--(B)--(C)--(Cp)--(Dp)--(Ap)--cycle
    (Ap)--(Bp)--(Cp) (B)--(Bp);
\draw[black!45,dashed] (A)--(D)--(C) (D)--(Dp);
\draw[accent] (Ap)--(B);
\draw[accent,dashed] (Ap)--(D)--(B);
\node[below left] at (A) {$A$};\node[below right] at (B) {$B$};
\node[right] at (C) {$C$};\node[below left] at (D) {$D$};
\node[left] at (Ap) {$A'$};\node[above right] at (Bp) {$B'$};
\node[above right] at (Cp) {$C'$};\node[above left] at (Dp) {$D'$};
"""

FIGURES["complex-plane"] = r"""
\begin{scope}[scale=1.15]
\draw[->,black!65] (-.55,0)--(3.5,0) node[right]{$\operatorname{Re}z$};
\draw[->,black!65] (0,-1.55)--(0,1.7) node[above]{$\operatorname{Im}z$};
\coordinate (Z) at (2,1.1);\coordinate (Zbar) at (2,-1.1);
\draw[black!40,dashed] (0,1.1)--(Z)--(Zbar)--(0,-1.1);
\draw[->,curveblue,thick] (0,0)--node[above,sloped]{$r$}(Z);
\draw[->,accent,thick] (0,0)--(Zbar);
\draw[accent,->] (.54,0) arc[start angle=0,end angle=28.8108,radius=.54];
\node at (.8,.18) {$\theta$};
\fill[curveblue] (Z) circle (1.4pt);\fill[accent] (Zbar) circle (1.4pt);
\node[above right] at (Z) {$z=a+bi$};
\node[below right] at (Zbar) {$\overline z=a-bi$};
\node[below left] at (0,0) {$O$};\node[above left] at (2,0) {$a$};
\node[left] at (0,1.1) {$b$};\node[left] at (0,-1.1) {$-b$};
\end{scope}
"""

body = "\\begin{scope}[scale=1.8]\n"+axes(-1.35,1.6,-1.23,1.25,r"\operatorname{Re}z",r"\operatorname{Im}z")
body += "\\draw[curveblue,thick] (0,0) circle (1);\n"
vertices=[pt(cos(k*pi/3),sin(k*pi/3)) for k in range(6)]
body += "\\draw[black!35] "+"--".join(vertices)+"--cycle;\n"
body += r"\draw[accent,thick] (1,0)--(.5,.866025);\draw[black!45,dashed] (0,0)--(.5,.866025);"+"\n"
body += r"\draw[accent,->] (.28,0) arc[start angle=0,end angle=60,radius=.28];\node at (.43,.23) {$\frac\pi3$};"+"\n"
for k in range(6):
    x,y=cos(k*pi/3),sin(k*pi/3)
    body += f"\\fill[curveblue] {pt(x,y)} circle (1.1pt);\n"
    anchor=["above right","above right","above left","above left","below left","below right"][k]
    text={0:r"z_0=1",3:r"z_3=-1"}.get(k,f"z_{k}")
    body += label(x,y,text,anchor)
body += label(-.03,0,"O","below left")+"\\end{scope}\n"
FIGURES["complex-roots"] = body


def compile_one(name):
    exe=shutil.which("xelatex")
    if not exe:
        raise RuntimeError("XeLaTeX was not found on PATH.")
    result=subprocess.run([exe,"-interaction=nonstopmode","-halt-on-error",name+".tex"],
                          cwd=HERE,capture_output=True,text=True,encoding="utf-8",errors="replace")
    if result.returncode or "Missing character:" in result.stdout:
        raise RuntimeError(name+"\n"+result.stdout[-3500:])
    return name


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--compile",action="store_true")
    args=parser.parse_args()
    for name,body in FIGURES.items():
        (HERE/(name+".tex")).write_text(HEADER+body+"\\end{tikzpicture}\n\\end{document}\n",encoding="utf-8")
    if args.compile:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for name in pool.map(compile_one,FIGURES):
                print("Compiled "+name)
