"""Rebuild the calculus chapter's vector diagrams (run from any directory).

Python generates standalone TikZ sources; TeX Live renders the PDF figures.
Use --compile to compile all figures, or omit it to regenerate sources only.
"""
from pathlib import Path
from math import exp, sin, cos, pi, sqrt
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = Path(__file__).resolve().parent
FIGURES = {}
HEADER = r"""\documentclass[tikz,border=5pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta}
\definecolor{curveblue}{HTML}{245C86}
\definecolor{accent}{HTML}{A65E2E}
\begin{document}
\begin{tikzpicture}[font=\small,>=Latex,line cap=round,line join=round]
"""


def coord(x, y):
    return f'({x:.5f},{y:.5f})'


def curve(fn, a, b, style='curveblue,thick', n=150):
    points = [coord(a+(b-a)*i/n, fn(a+(b-a)*i/n)) for i in range(n+1)]
    return '\\draw['+style+'] plot[smooth] coordinates {'+' '.join(points)+'};\n'


def line(x, y, u, v, style='gray'):
    return f'\\draw[{style}] {coord(x,y)}--{coord(u,v)};\n'


def node(x, y, text, pos='above'):
    return f'\\node[{pos}] at {coord(x,y)} {{{text}}};\n'


def dot(x, y, label='', pos='above'):
    return f'\\fill[curveblue] {coord(x,y)} circle (1.2pt);\n'+(node(x,y,label,pos) if label else '')


def axes(xmax, ymax, xmin=-.15, ymin=-.15, xlabel='x', ylabel='y'):
    return line(xmin,0,xmax,0,'->,black!65')+node(xmax,0,'$'+xlabel+'$','right')+line(0,ymin,0,ymax,'->,black!65')+node(0,ymax,'$'+ylabel+'$')


def panel(body, x=0, y=0, sx=1, sy=1):
    return f'\\begin{{scope}}[shift={{{coord(x,y)}}},xscale={sx},yscale={sy}]\n'+body+'\\end{scope}\n'


def fill_under(fn, a, b, base=0, style='curveblue!12', n=80):
    pts = [coord(a,base)]+[coord(a+(b-a)*i/n,fn(a+(b-a)*i/n)) for i in range(n+1)]+[coord(b,base)]
    return '\\fill['+style+'] '+'--'.join(pts)+'--cycle;\n'


# 5.1: the same parabola and a fixed point, with moving secants.
f=lambda x: .55*x*x+.3
b=axes(3.2,4.65)+curve(f,0,2.72)
a=1
for h,style in [(1.3,'accent'),(.65,'accent,dashed'),(.25,'accent,dotted')]:
    slope=(f(a+h)-f(a))/h
    b+=curve(lambda x,m=slope:f(a)+m*(x-a),.45,2.65,style)
    b+=dot(a+h,f(a+h))
b+=curve(lambda x:f(a)+1.1*(x-a),.35,2.75,'black,dashed')
b+=dot(a,f(a),r'$P$','above left')+node(2.55,f(2.55),r'$y=f(x)$','above left')
b+=node(2.5,2.5,r'$\ell$','below')
FIGURES['secants']=panel(b,sx=1.25,sy=.7)

f=lambda x: .45*x*x+.45
a,h=1,.95
b=axes(2.8,3.35)+curve(f,0,2.5)
b+=curve(lambda x:f(a)+.9*(x-a),.45,2.5,'black,dashed')
b+=line(a,f(a),a+h,f(a),'gray,dotted')+line(a+h,0,a+h,f(a+h),'gray,dotted')
b+=line(a,0,a,f(a),'gray,dotted')+dot(a,f(a),r'$P$','above left')
b+=line(a+h+.14,f(a),a+h+.14,f(a)+.9*h,'<->,black')+node(a+h+.14,f(a)+.45*h,r'$dy$','right')
b+=line(a+h+.68,f(a),a+h+.68,f(a+h),'<->,accent')+node(a+h+.68,(f(a)+f(a+h))/2,r'$\Delta y$','right')
b+=line(a, .12,a+h,.12,'<->,gray')+node(a+h/2,.12,r'$dx=h$','above')
b+=node(a+h,f(a+h),r'$Q$','above left')+node(2.3,2.9,r'$\Delta y-dy=r(h)$')
FIGURES['differential']=panel(b,sx=1.6,sy=1)

# 5.2: reflected graphs and reflected tangent directions, with equal units.
b=axes(3.6,3.6)+line(0,0,3.3,3.3,'gray,dotted')
b+=curve(lambda x:x*x,0,1.8)+curve(sqrt,0,3.25,'accent,thick')
b+=curve(lambda x:1+2*(x-1),.55,1.65,'curveblue,dashed')
b+=curve(lambda x:1+.5*(x-1),.2,2.8,'accent,dashed')
b+=dot(1,1,r'$(1,1)$','below right')+node(0,2.7,r'$f(x)=x^2$','left')
b+=node(3.15,sqrt(3.15),r'$f^{-1}(x)=\sqrt{x}$')
b+=node(2.9,2.9,r'$y=x$','right')
FIGURES['inverse']=b

# 5.3: Rolle and Lagrange on two exactly related graphs.
b=axes(3.5,2.05)+curve(lambda x:1.6*sin(pi*x/3),0,3)
b+=line(.6,1.6,2.4,1.6,'accent,dashed')+dot(1.5,1.6,r'$f^{\prime}(\xi)=0$')
b+=node(0,0,r'$a$','below')+node(3,0,r'$b$','below')+node(1.5,-.52,r'$f(a)=f(b)$','below')
c=axes(3.5,3.05)+curve(lambda x:.35*x+1.6*sin(pi*x/3),0,3)
c+=line(0,0,3,1.05,'black,dashed')+line(.5,1.775,2.5,2.475,'accent,dashed')
c+=dot(1.5,2.125,r'$f^{\prime}(\xi)=\dfrac{f(b)-f(a)}{b-a}$','above')
c+=node(0,0,r'$a$','below')+node(3,0,r'$b$','below')
FIGURES['mean-value']=panel(b,sy=.9)+panel(c,x=5.4,sy=.9)

# 5.4: a function and its derivative share the stationary abscissae.
b=axes(2.25,1.7,xmin=-2.25,ymin=-1.7)+curve(lambda x:(x**3-3*x)/2,-2.05,2.05)
for x in [-1,1]:b+=line(x,-1.55,x,1.55,'gray,dotted')+dot(x,(x**3-3*x)/2)
b+=node(1.6,-1.2,r'$f(x)=\frac{x^3-3x}{2}$','below')
c=axes(2.25,2.35,xmin=-2.25,ymin=-1.1)+curve(lambda x:1.5*(x*x-1),-1.53,1.53)
for x in [-1,1]:c+=dot(x,0,f'${x}$','above')
c+=node(0,-1.5,r'$f^{\prime}<0$','below')+node(-1.65,1.4,r'$f^{\prime}>0$')+node(1.65,1.4,r'$f^{\prime}>0$')
FIGURES['monotonicity']=panel(b)+panel(c,x=6)

# 5.5: tangent and chord bounds; higher polynomial approximation is separate.
f=lambda x:.55*x*x+.35
b=axes(3.25,4)+curve(f,0,2.5)
b+=line(.4,f(.4),2.2,f(2.2),'accent,thick')
b+=curve(lambda x:f(1.3)+1.43*(x-1.3),.15,2.65,'black,dashed')
for x in [.4,1.3,2.2]:b+=dot(x,f(x))
b+=node(1.55,2.7,r'$s$')+node(2.6,2.6,r'$\ell$','right')
FIGURES['convexity']=panel(b,sx=1.35,sy=.8)
b=axes(1.55,4.35,xmin=-1.3,ymin=-.1)+curve(exp,-1.1,1.35)
for n,style in [(1,'black,dotted'),(2,'accent,dashed'),(3,'black,dashed')]:
    def poly(x,n=n):
        term,total=1,1
        for k in range(1,n+1):term*=x/k;total+=term
        return total
    label_y={1:2.1,2:3.0,3:4.05}[n]
    b+=curve(poly,-1.1,1.35,style)+line(1.35,poly(1.35),1.6,label_y,'gray')+node(1.6,label_y,f'$T_{n}$','right')
b+=dot(0,1)+node(.8,exp(.8),r'$e^x$','above left')
FIGURES['taylor']=panel(b,sx=1.9,sy=.75)

# 5.6 and 5.7: Riemann samples and Darboux upper/lower sums.
f=lambda x:.35+.16*x*x
def rectangles(n, upper=False):
    body=axes(3.5,2.2)
    for i in range(n):
        l,r=3*i/n,3*(i+1)/n
        h=f(r if upper else (l+r)/2)
        body+=f'\\filldraw[fill=curveblue!10,draw=black!45] {coord(l,0)} rectangle {coord(r,h)};\n'
        if not upper:body+=dot((l+r)/2,h)
    return body+curve(f,0,3)+node(1.5,-.4,f'$n={n}$','below')
FIGURES['riemann-sums']=panel(rectangles(4),sx=1.35)+panel(rectangles(12),x=6,sx=1.35)
b=axes(3.6,2.2)
for i in range(6):
    l,r=i*.5,(i+1)*.5
    b+=f'\\filldraw[fill=curveblue!10,draw=black!40] {coord(l,0)} rectangle {coord(r,f(l))};\n'
    b+=f'\\filldraw[fill=accent!25,draw=accent!65] {coord(l,f(l))} rectangle {coord(r,f(r))};\n'
b+=curve(f,0,3)+node(2,2.1,r'$U(f;P)-L(f;P)$')
FIGURES['darboux']=panel(b,sx=1.65,sy=1.2)

# 5.8: an increment of an accumulation function, and its derivative.
f=lambda x:x-1
b=axes(2.45,1.45,ymin=-1.25,xlabel='t')
b+=fill_under(f,0,1,style='black!8')+fill_under(f,1,2,style='curveblue!12')
b+=fill_under(f,1.5,1.9,style='accent!30')+curve(f,0,2.2)
for x,lab in [(1,'1'),(1.5,'x'),(1.9,'x+h')]:b+=node(x,0,'$'+lab+'$','below')
b+=node(.3,-.7,r'$-$')+node(1.2,.65,r'$+$')+node(.6,1.2,r'$f(t)=t-1$')
c=axes(2.45,.9,ymin=-.85)+curve(lambda x:x*x/2-x,0,2.2)
for x in [1.5,1.9]:c+=dot(x,x*x/2-x)+line(x,0,x,x*x/2-x,'gray,dotted')
c+=node(1,.2,r'$A(x)=\int_0^x f(t)\,dt$')+node(1,-.75,r'$A^{\prime}(1)=0$','below')
FIGURES['accumulation']=panel(b,sx=1.55)+panel(c,x=5.7,sx=1.55)

# 5.9: midpoint rectangles below a convex graph, chords above it.
f=lambda x: .3+.2*x*x
b=axes(3.4,2.55)
c=axes(3.4,2.55)
for i in range(3):
    l,r=i,i+1;m=(l+r)/2
    b+=f'\\filldraw[fill=curveblue!10,draw=black!40] {coord(l,0)} rectangle {coord(r,f(m))};\n'
    b+=curve(lambda x,m=m:f(m)+.4*m*(x-m),l,r,'accent,dashed')
    c+=f'\\filldraw[fill=accent!12,draw=accent] {coord(l,0)}--{coord(l,f(l))}--{coord(r,f(r))}--{coord(r,0)}--cycle;\n'
b+=curve(f,0,3)+node(1.5,-.4,r'$M_n\le\int_a^b f$','below')
c+=curve(f,0,3)+node(1.5,-.4,r'$\int_a^b f\le T_n$','below')
FIGURES['quadrature']=panel(b,sx=1.2)+panel(c,x=5.8,sx=1.2)

# 5.10: pointwise and uniform convergence; then instability under differentiation.
b=axes(3.3,2.4)
for n,style in [(1,'gray'),(4,'black,dashed'),(16,'accent,dashed'),(64,'curveblue,thick')]:
    b+=curve(lambda x,n=n:2*(x/3)**n,0,3,style)
b+=node(1.5,2.5,r'$n=1,4,16,64$')
b+=node(0,2,r'$1$','left')
b+=line(0,0,3,0,'black,thick')+r'\draw[fill=white] (3,0) circle (2pt);'+dot(3,2)
b+=node(1.5,-.4,r'$f_n(x)=x^n,\quad 0\le x\le1$','below')
b+=node(3,0,r'$1$','below')
c=axes(3.3,2.4)
c+=node(0,2,r'$1$','left')
for n,style in [(1,'gray'),(4,'black,dashed'),(16,'accent,dashed')]:c+=curve(lambda x,n=n:2*x/(3*(n+1)),0,3,style)
c+=f'\\fill[curveblue!8] (0,0) rectangle (3,{2/5});\n'
c+=line(0,2/5,3,2/5,'curveblue,dotted')+node(1.5,1.7,r'$\|f_n\|_\infty=\dfrac1{n+1}$')
c+=node(1.5,-.4,r'$f_n(x)=\dfrac{x}{n+1}$','below')+node(3,0,r'$1$','below')
FIGURES['convergence']=panel(b,sx=1.25)+panel(c,x=6,sx=1.25)
b=axes(1.17,.42,xmin=-1.1,ymin=-.42)
c=axes(1.17,1.4,xmin=-1.1,ymin=-1.4)
for n,style in [(5,'gray'),(12,'curveblue,thick')]:
    b+=curve(lambda x,n=n:sin(n*x)/n,-1,1,style,n=240)
    c+=curve(lambda x,n=n:cos(n*x),-1,1,style,n=240)
for body_name in ['b','c']:
    if body_name=='b':b+=node(-1,0,r'$-1$','below')+node(1,0,r'$1$','below')
    else:c+=node(-1,0,r'$-1$','below')+node(1,0,r'$1$','below')
b+=node(0,.88,r'$f_n(x)=\sin(nx)/n$')
c+=node(0,2.15,r'$f_n^{\prime}(x)=\cos(nx)$')
FIGURES['derivative-error']=panel(b,sx=2.2,sy=2)+panel(c,x=6,sx=2.2,sy=.8)

# 5.11: vertical and horizontal slices for the same bounded region.
b=axes(2.6,2.6)
b+=fill_under(lambda x:2-x*x,0,1,style='curveblue!10')
# Region between y=x^2 and y=2-x^2, -1<=x<=1 (shift axes only for layout).
b=axes(1.65,2.45,xmin=-1.5)
pts=[coord(-1+2*i/100,(-1+2*i/100)**2) for i in range(101)]
pts += [coord(1-2*i/100,2-(1-2*i/100)**2) for i in range(101)]
b+='\\fill[curveblue!10] '+'--'.join(pts)+'--cycle;\n'
b+=curve(lambda x:x*x,-1.3,1.3)+curve(lambda x:2-x*x,-1.3,1.3,'accent,thick')
b+=f'\\filldraw[fill=accent!22,draw=accent] (.4,.16) rectangle (.53,1.7191);\n'
b+=line(.465,.16,.465,1.7838,'<->,black')+node(.56,1.04,r'$f(x)-g(x)$','right')
b+=node(-.95,2.3,r'$f(x)=2-x^2$')+node(0,-.32,r'$g(x)=x^2$','below')
FIGURES['area-slices']=panel(b,sx=1.75,sy=1.05)

# A side view of disks, and shells in the meridian plane.
b=axes(3.6,1.8,ymin=-1.7)
b+=curve(lambda x:.35+.35*x,.2,3)+curve(lambda x:-.35-.35*x,.2,3)
b+=r'\draw[gray] (.2,0) ellipse (.12 and .42);\draw[gray] (3,0) ellipse (.25 and 1.4);'
b+=r'\filldraw[fill=curveblue!15,draw=curveblue] (1.5,0) ellipse (.20 and .875);'
b+=line(1.5,0,1.5,.875,'<->,black')+node(1.56,.44,r'$f(x)$','right')
b+=node(1.7,-1.9,r'$dV=\pi f(x)^2\,dx$','below')
c=axes(3.5,2.8)
c+=curve(lambda x:2.4-.3*x*x,0,2.5)
c+=r'\filldraw[fill=accent!18,draw=accent] (1.4,0) rectangle (1.6,1.632);'
c+=line(0,-.25,1.5,-.25,'<->,black')+node(.75,-.25,r'$x$','below')
c+=node(1.6,1.0,r'$f(x)$','right')+node(1.7,-1.0,r'$dV=2\pi x f(x)\,dx$','below')
FIGURES['rotation']=panel(b,sy=.8)+panel(c,x=5.8,y=-.8,sy=.8)

# Polygonal approximation to an arc; the local frustum is shown separately.
f=lambda x:.2+.2*x*x
b=axes(3.5,2.5)+curve(f,0,3)
for i in range(5):
    l,r=3*i/5,3*(i+1)/5
    b+=line(l,f(l),r,f(r),'accent,thick')+dot(l,f(l))
b+=dot(3,f(3))+node(1.3,2.15,r'$\sum_i|r(t_i)-r(t_{i-1})|$')
c=axes(3.4,2.5)
c+=curve(f,.2,3)
l,r=1,2.6
c+=line(l,f(l),r,f(l),'gray,dashed')+line(r,f(l),r,f(r),'gray,dashed')+line(l,f(l),r,f(r),'accent,thick')
c+=node(1.8,.3,r'$\Delta x$','below')+node(r,1.0,r'$\Delta y$','right')
c+=node(1.6,2.25,r'$\Delta s\approx\sqrt{\Delta x^2+\Delta y^2}$')
FIGURES['arc-length']=panel(b,sx=1.25)+panel(c,x=5.8,sx=1.25)
b=axes(3.9,2.2,ymin=-2.0)
for sign in [-1,1]:b+=line(.6,sign*.65,3,sign*1.45,'curveblue,thick')
b+=r'\draw[curveblue] (.6,0) ellipse (.23 and .65);\draw[curveblue] (3,0) ellipse (.35 and 1.45);'
b+=line(.6,.65,3,1.45,'accent,very thick')+node(1.8,1.23,r'$\Delta s$')
b+=line(.6,0,.6,.65,'gray,dashed')+node(.4,.3,r'$r_1$','left')
b+=line(3,0,3,1.45,'gray,dashed')+node(3,.65,r'$r_2$','right')
b+=node(1.8,-1.9,r'$\Delta S=\pi(r_1+r_2)\Delta s$','below')
FIGURES['surface-frustum']=panel(b,sx=1.25,sy=.8)

b=axes(3.45,2.5)
lo,hi=.42,.65
sample_radius=1.7+.7*cos((lo+hi)/2)
pts=[coord(0,0)]+[coord(sample_radius*cos(lo+(hi-lo)*i/30),sample_radius*sin(lo+(hi-lo)*i/30)) for i in range(31)]
b+='\\fill[accent!22] '+'--'.join(pts)+'--cycle;\n'
b+=r'\draw[curveblue,thick] plot[domain=0:110,samples=90] ({(1.7+.7*cos(\x))*cos(\x)},{(1.7+.7*cos(\x))*sin(\x)});'
for ang in [lo,hi]:b+=line(0,0,2.4*cos(ang),2.4*sin(ang),'gray,dashed')
b+=f'\\draw[accent] ({.85*cos(lo)},{.85*sin(lo)}) arc[start angle={lo*180/pi},end angle={hi*180/pi},radius=.85];'
b+=node(1.05,.55,r'$\Delta\theta$','right')+node(2.2,1.7,r'$r=r(\theta)$')
b+=node(1.5,-.4,r'$\Delta S\approx\tfrac12r^2\Delta\theta$','below')
FIGURES['polar-area']=panel(b,sx=1.5,sy=1.1)

# 5.12: an infinite tail and a finite-endpoint singularity.
b=axes(4.7,1.45)
b+=fill_under(lambda x:exp(-x),0,2.2)+fill_under(lambda x:exp(-x),2.2,4.4,style='accent!25')
b+=curve(lambda x:exp(-x),0,4.4)+line(2.2,0,2.2,exp(-2.2),'accent,dashed')
b+=node(2.2,0,r'$R$','below')+node(1,1.05,r'$e^{-x}$')+node(3.3,.4,r'$\int_R^\infty f$')
c=axes(1.18,3.3,xmin=-.05)
c+=fill_under(lambda x:1/sqrt(x),.12,1,style='curveblue!12')+curve(lambda x:1/sqrt(x),.1,1)
c+=line(.12,0,.12,1/sqrt(.12),'accent,dashed')+node(.12,0,r'$\varepsilon$','below')
c+=node(1,0,r'$1$','below')+node(.65,1.95,r'$x^{-1/2}$')
FIGURES['improper']=panel(b,sy=2.2)+panel(c,x=6,sx=3,sy=.9)

# A conic and its osculating circle agree to second order at the marked point.
b=axes(2.65,1.7,xmin=-2.35,ymin=-1.4)
b+=r'\draw[curveblue,thick] (0,0) ellipse (2 and 1);'
b+=r'\draw[accent,thick,dashed] (1.5,0) circle (.5);'
b+=line(1.5,0,2,0,'accent,thick')
b+=dot(2,0,r'$P$','above right')+dot(1.5,0,r'$C$','below left')
b+=node(1.65,.55,r'$\rho=\tfrac12$')+node(-.6,2.1,r'$\dfrac{x^2}{4}+y^2=1$')
c=axes(2.6,1.8,xmin=-.35,ymin=-1.65)
pts=[coord(.5*t*t,t) for t in [-1.55+3.1*i/160 for i in range(161)]]
c+='\\draw[curveblue,thick] plot[smooth] coordinates {'+' '.join(pts)+'};\n'
c+=r'\draw[accent,thick,dashed] (1,0) circle (1);'
c+=line(0,0,1,0,'accent,thick')+dot(0,0,r'$P$','below left')+dot(1,0,r'$C$','below')
c+=node(.5,.15,r'$\rho=1$')+node(1.45,1.4,r'$y^2=2x$')
FIGURES['curvature']=panel(b)+panel(c,x=7)


def compile_one(name):
    exe=Path('F:/texlive/2025/bin/windows/xelatex.exe')
    result=subprocess.run([str(exe),'-interaction=nonstopmode','-halt-on-error',
                           '-output-directory='+str(HERE),str(HERE/f'calculus-{name}.tex')],
                          capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:
        raise RuntimeError(name+'\n'+result.stdout[-2500:])
    log=(HERE/f'calculus-{name}.log').read_text(encoding='utf-8',errors='replace')
    if 'Missing character:' in log:
        raise RuntimeError(name+': missing glyph')
    return name


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--compile',action='store_true')
    args=parser.parse_args()
    for name,body in FIGURES.items():
        (HERE/f'calculus-{name}.tex').write_text(HEADER+body+'\\end{tikzpicture}\n\\end{document}\n',encoding='utf-8')
    print(f'Generated {len(FIGURES)} TikZ diagrams.')
    if args.compile:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for name in pool.map(compile_one,FIGURES):print('Compiled '+name)
