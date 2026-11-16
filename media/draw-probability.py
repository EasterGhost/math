"""Regenerate the probability chapter's vector figures with TeX Live.

All random records are reproducible teaching simulations, not observed data.
Run with --compile to build the PDFs used by the book.
"""
from pathlib import Path
from math import exp, sqrt, pi, comb
from random import Random
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = Path(__file__).resolve().parent
HEADER = r"""\documentclass[tikz,border=5pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta,positioning}
\definecolor{curveblue}{HTML}{245C86}
\definecolor{accent}{HTML}{A65E2E}
\begin{document}
\begin{tikzpicture}[font=\small,>=Latex,line cap=round,line join=round]
"""
FIGURES = {}

FIGURES['probability-counting-tree'] = r"""
\node (o) at (0,0) {$\bullet$};
\node (a) at (2.8,.9) {$A$};
\node (b) at (2.8,-.9) {$B$};
\node (aa) at (5.6,.9) {$2\cdot4$};
\node (bb) at (5.6,-.9) {$3\cdot5$};
\draw[->,curveblue] (o)--node[above]{$2$}(a);
\draw[->,curveblue] (o)--node[below]{$3$}(b);
\draw[->,curveblue] (a)--node[above]{$4$}(aa);
\draw[->,curveblue] (b)--node[below]{$5$}(bb);
"""


def coord(x, y):
    return f"({x:.5f},{y:.5f})"


def path(points, style="curveblue,thick"):
    return "\\draw["+style+"] plot coordinates {"+" ".join(coord(x,y) for x,y in points)+"};\n"


def curve(fn, a, b, style="curveblue,thick", n=160):
    return path([(a+(b-a)*i/n,fn(a+(b-a)*i/n)) for i in range(n+1)],style)


def node(x, y, label, where="above"):
    return f"\\node[{where}] at {coord(x,y)} {{{label}}};\n"


def axes(xmin, xmax, ymin, ymax, xlabel="x", ylabel="y"):
    vertical = 0 if xmin <= 0 <= xmax else xmin
    return (f"\\draw[->,black!65] {coord(xmin,0)}--{coord(xmax,0)} node[right]{{${xlabel}$}};\n"
            +f"\\draw[->,black!65] {coord(vertical,ymin)}--{coord(vertical,ymax)} node[above]{{${ylabel}$}};\n")


rng = Random(20261114)
total = 0
record = []
for n in range(1,501):
    total += rng.random() < .4
    record.append((n,total/n))
body = "\\begin{scope}[x=.018cm,y=4cm]\n"+axes(0,530,0,1.05,"n","f_n")
body += "\\draw[accent,dashed] (0,.4)--(500,.4);\n"+node(510,.4,"$p=0.4$","right")
body += path(record,"curveblue,thin")
for n in [100,300,500]: body+=node(n,-.025,f"${n}$","below")
body += "\\end{scope}\n"
FIGURES["probability-frequency"] = body

FIGURES["probability-tree"] = r"""
\node (o) at (0,0) {$\Omega$};
\node (a) at (3,.7) {$A$}; \node (b) at (3,-.7) {$B$};
\node (ad) at (6,1.2) {$A\cap D$}; \node (ac) at (6,.25) {$A\cap D^c$};
\node (bd) at (6,-.25) {$B\cap D$}; \node (bc) at (6,-1.2) {$B\cap D^c$};
\draw[->] (o)--node[above]{$0.4$}(a); \draw[->] (o)--node[below]{$0.6$}(b);
\draw[->] (a)--node[above]{$0.02$}(ad); \draw[->] (a)--node[below]{$0.98$}(ac);
\draw[->] (b)--node[above]{$0.05$}(bd); \draw[->] (b)--node[below]{$0.95$}(bc);
"""

body = "\\begin{scope}[x=1.9cm,y=3.2cm]\n"+axes(-.6,3.1,0,1.2,"x","F(x)")
for a,b,y in [(-.5,0,0),(0,1,.25),(1,2,.75),(2,2.8,1)]:
    body+=f"\\draw[curveblue,thick] {coord(a,y)}--{coord(b,y)};\n"
for x,yold,y in [(0,0,.25),(1,.25,.75),(2,.75,1)]:
    body+=f"\\draw[curveblue,fill=white] {coord(x,yold)} circle (1.5pt);\n"
    body+=f"\\fill[curveblue] {coord(x,y)} circle (1.5pt);\n"
for x in [1,2]:body+=node(x,-.03,f"${x}$","below")
for y,label in [(.25,'1/4'),(.75,'3/4'),(1,'1')]:body+=node(-.04,y,f"${label}$","left")
FIGURES['probability-cdf']=body+"\\end{scope}\n"

normal=lambda x:exp(-x*x/2)/sqrt(2*pi)
body="\\begin{scope}[x=1.4cm,y=6cm]\n"+axes(-3.5,3.6,0,.51,"z","\\varphi(z)")
points=[(-1,0)]+[(-1+2*i/100,normal(-1+2*i/100)) for i in range(101)]+[(1,0)]
body+='\\fill[curveblue!15] '+'--'.join(coord(x,y) for x,y in points)+'--cycle;\n'
body+=curve(normal,-3.3,3.3)
for x in [-2,-1,1,2]:body+=node(x,-.012,f"${x}$","below")
body+=node(0,.21,'$P(-1<Z<1)$')
FIGURES['probability-normal']=body+"\\end{scope}\n"

# Ideal Galton board: eight independent left/right decisions. Bin heights are
# exact binomial probabilities, rather than an observed or simulated ball pile.
nrows=8
body=''
for row in range(nrows):
    for k in range(row+1):
        body+=f"\\fill[black!55] {coord(k-row/2,-.48*row)} circle (1.4pt);\n"
board_base=-5.45
for k in range(nrows+2):
    xpos=k-nrows/2-.5
    body+=f"\\draw[black!50] {coord(xpos,board_base)}--{coord(xpos,-4.0)};\n"
for k in range(nrows+1):
    xpos=k-nrows/2
    height=4.4*comb(nrows,k)/2**nrows
    body+=f"\\fill[curveblue!25] {coord(xpos-.36,board_base)} rectangle {coord(xpos+.36,board_base+height)};\n"
    body+=node(xpos,board_base-.04,f'${k}$','below')
body+=f"\\draw[black!50] {coord(-4.5,board_base)}--{coord(4.5,board_base)};\n"
points=[(0,.5),(0,0)];xpos=0
for row,step in enumerate([-1,1,1,-1,1,-1,1,1],1):
    xpos+=step/2
    points.append((xpos,-.48*row))
body+='\\draw[accent,thick,->] '+'--'.join(coord(x,y) for x,y in points)+';\n'
body+='\\fill[accent] (0,.5) circle (2.6pt);\n'
body+=node(0,.8,'$n=8$')+node(4.8,board_base-.07,'$k$','below')
FIGURES['probability-galton']=body

# Bars have width dz and height probability/dz, so their areas are probabilities.
body=''
for panel,nrows in enumerate([8,64]):
    body+=f"\\begin{{scope}}[shift={{(0,{-panel*3.15})}},x=1cm,y=4.3cm]\n"
    body+=axes(-3.55,3.65,0,.51,'z','h')
    dz=2/sqrt(nrows)
    for k in range(nrows+1):
        z=(k-nrows/2)/(sqrt(nrows)/2)
        if abs(z)+dz/2>3.45:continue
        height=comb(nrows,k)/2**nrows/dz
        body+=f"\\draw[curveblue!60,fill=curveblue!13,line width=.3pt] {coord(z-dz/2,0)} rectangle {coord(z+dz/2,height)};\n"
    if panel==1:
        shaded=[(-1,0)]+[(-1+2*i/100,normal(-1+2*i/100)) for i in range(101)]+[(1,0)]
        body+='\\fill[accent!25,opacity=.75] '+'--'.join(coord(x,y) for x,y in shaded)+'--cycle;\n'
        for z in [-1,1]:
            body+=f"\\draw[accent!65,dashed] {coord(z,0)}--{coord(z,normal(z))};\n"
    body+=curve(normal,-3.4,3.4,'accent,thick')
    for z in ([-2,0,2] if panel==0 else [-2,-1,0,1,2]):body+=node(z,-.008,f'${z}$','below')
    body+=node(2.25,.405,f'$n={nrows}$')+'\\end{scope}\n'
FIGURES['probability-normal-limit']=body

body="\\begin{scope}[x=.75cm,y=10cm]\n"+axes(7.5,16.5,0,.23,"x","h")
for a,b,h in [(8,10,3/16),(10,12,3/16),(12,16,1/16)]:
    body+=f"\\draw[fill=curveblue!15,curveblue] {coord(a,0)} rectangle {coord(b,h)};\n"
for x in [8,10,12,16]:body+=node(x,-.006,f"${x}$","below")
body+=node(9,.19,'$3/8$')+node(11,.19,'$3/8$')+node(14,.065,'$2/8$')
FIGURES['probability-histogram']=body+"\\end{scope}\n"

# Heights transcribed from the figure in the 2020 Tianjin paper, question 4.
# The horizontal index j corresponds to diameter 5.31 + 0.02*j millimetres.
diameter_heights=[1.25,3.75,2.5,7.5,10,8.75,6.25,5,5]
body="\\begin{scope}[x=.60cm,y=.17cm,font=\\scriptsize]\n"
body+=axes(-.25,9.65,0,11.7,"d/\\mathrm{mm}","h")
for y in [2.5,5,7.5,10]:
    body+=f"\\draw[black!25,dashed] {coord(0,y)}--{coord(9,y)};\n"
    body+=node(-.25,y,f"${y:g}$","left")
for j,h in enumerate(diameter_heights):
    body+=f"\\draw[fill=curveblue!15,curveblue] {coord(j,0)} rectangle {coord(j+1,h)};\n"
    body+=node(j+.5,h,f"${h:g}$","above")
for j in range(10):
    body+=node(j,-.2,f"${5.31+.02*j:.2f}$","below")
FIGURES['probability-histogram-exam']=body+"\\end{scope}\n"

body="\\begin{scope}[x=.85cm,y=1cm]\n"
body+=r"\draw[black!65,->] (7.5,0)--(16,0) node[right]{$x$};"+'\n'
body+=r"\draw[curveblue] (8,.5)--(8,1.1) (15,.5)--(15,1.1) (8,.8)--(9,.8) (11.5,.8)--(15,.8);"+'\n'
body+=r"\draw[fill=curveblue!12,curveblue] (9,.35) rectangle (11.5,1.25);\draw[curveblue,thick] (10,.35)--(10,1.25);"+'\n'
for x in [8,9,10,11.5,15]:body+=node(x,-.06,f"${x}$","below")
FIGURES['probability-boxplot']=body+"\\end{scope}\n"

body=''
for j,n in enumerate([10,40]):
    body+=f"\\begin{{scope}}[shift={{({j*6.3},0)}},x=5cm,y=9cm]\n"
    body+=axes(-.02,1.08,0,.33,"\\bar X","P")
    for k in range(n+1):
        pr=comb(n,k)*.4**k*.6**(n-k)
        body+=f"\\draw[curveblue] {coord(k/n,0)}--{coord(k/n,pr)};\n"
    body+='\\draw[accent,dashed] (.4,0)--(.4,.29);\n'+node(.6,.29,f"$n={n}$")
    body+=node(.4,-.01,'$0.4$','below')+node(1,-.01,'$1$','below')+'\\end{scope}\n'
FIGURES['probability-sample-means']=body

rng=Random(2)
body="\\begin{scope}[x=4cm,y=.23cm]\n\\draw[accent,dashed] (0,0)--(0,13);\n"
body+=node(0,13,'$\\mu=0$')
for j in range(1,13):
    m=sum(rng.gauss(0,1) for _ in range(25))/25
    color='curveblue' if abs(m)<=1.96/5 else 'accent'
    body+=f"\\draw[{color}] {coord(m-.392,j)}--{coord(m+.392,j)};\\fill[{color}] {coord(m,j)} circle (1.1pt);\n"
body+='\\end{scope}\n'
FIGURES['probability-confidence']=body

xs=[1,2,3,4,5];ys=[20,40,50,40,50]
body="\\begin{scope}[x=.8cm,y=.055cm]\n"+axes(0,6,0,65,"x","y")
body+=path([(0,22),(6,58)])
for x,y in zip(xs,ys):
    body+=f"\\fill[curveblue] {coord(x,y)} circle (1.5pt);\\draw[accent,dashed] {coord(x,y)}--{coord(x,22+6*x)};\n"
body+='\\end{scope}\n\\begin{scope}[shift={(6.6,1.1)},x=.8cm,y=.1cm]\n'+axes(0,6,-12,13,"x","e")
for x,y in zip(xs,ys):body+=f"\\fill[curveblue] {coord(x,y-22-6*x)} circle (1.5pt);\n"
FIGURES['probability-regression']=body+'\\end{scope}\n'

FIGURES['probability-markov']=r"""
\node[draw,circle,minimum size=10mm] (a) at (0,0) {$A$};
\node[draw,circle,minimum size=10mm] (b) at (4,0) {$B$};
\draw[->] (a) to[bend left=25] node[above]{$\alpha$} (b);
\draw[->] (b) to[bend left=25] node[below]{$\beta$} (a);
\draw[->] (a) edge[loop left] node[left]{$1-\alpha$} (a);
\draw[->] (b) edge[loop right] node[right]{$1-\beta$} (b);
"""


def compile_one(name):
    command=[r'F:/texlive/2025/bin/windows/xelatex.exe','-interaction=nonstopmode','-halt-on-error',name+'.tex']
    result=subprocess.run(command,cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    if result.returncode:raise RuntimeError(name+'\n'+result.stdout[-3000:])
    return name


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compile',action='store_true');args=parser.parse_args()
    for name,body in FIGURES.items():
        (HERE/(name+'.tex')).write_text(HEADER+body+'\\end{tikzpicture}\n\\end{document}\n',encoding='utf-8')
    if args.compile:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for name in pool.map(compile_one,FIGURES):print(name)
