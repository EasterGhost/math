"""Exact axial sections of Dandelin spheres; angles are measured in degrees."""
from pathlib import Path
from math import sin,cos,tan,radians,hypot
here=Path(__file__).resolve().parent
alpha=radians(30);h=.6;k=tan(alpha)
lines=[r'\documentclass[tikz,border=3pt]{standalone}',r'\usepackage[UTF8,fontset=windows]{ctex}',r'\usepackage{amsmath}',r'\definecolor{sectionblue}{HTML}{245C86}',r'\begin{document}',r'\begin{tikzpicture}[line cap=round,line join=round,font=\small]']
def co(x,z):return f'({x:.5f},{z:.5f})'
for index,(name,beta_deg,zmin,zmax) in enumerate([('椭圆',20,-.2,2.6),('抛物线',60,-.2,2.6),('双曲线',80,-3,2)]):
 beta=radians(beta_deg);scale=4/(zmax-zmin)
 # Fit cone in a common-width rectangular viewing window.
 xmax=1.65/scale
 lines += [f'\\begin{{scope}}[shift={{({index*4.4:.3f},0)}}]',f'\\begin{{scope}}[scale={scale:.5f},shift={{(0,{-zmin:.5f})}}]','% Geometry is bounded explicitly; leave labels unclipped.']
 lines += [f'\\draw[gray!75] {co(-k*zmin,zmin)}--{co(-k*zmax,zmax)};',f'\\draw[gray!75] {co(k*zmin,zmin)}--{co(k*zmax,zmax)};',f'\\draw[dashed,gray!60] {co(0,zmin)}--{co(0,zmax)};']
 # Intersect the plane's axial line with the drawing box.
 candidates=[]
 for x in [-xmax,xmax]:
  z=tan(beta)*x+h/cos(beta)
  if zmin<=z<=zmax:candidates.append((x,z))
 for z in [zmin,zmax]:
  x=(z*cos(beta)-h)/sin(beta)
  if -xmax<=x<=xmax:candidates.append((x,z))
 assert len(candidates)==2
 lines.append(f'\\draw[sectionblue,thick] {co(*candidates[0])}--{co(*candidates[1])};')
 centers=[h/(cos(beta)+sin(alpha))]
 if abs(cos(beta)-sin(alpha))>1e-9:centers.append(h/(cos(beta)-sin(alpha)))
 for n,c in enumerate(centers,1):
  rho=abs(c)*sin(alpha);delta=h-c*cos(beta);fx=-delta*sin(beta);fz=c+delta*cos(beta)
  assert abs(hypot(fx,fz-c)-rho)<1e-9
  zt=c*cos(alpha)**2;xt=abs(c)*sin(alpha)*cos(alpha)
  labelpos=('below left' if n==1 else 'below right') if index==0 else 'above left'
  lines += [f'\\draw[fill=sectionblue!7,draw=black!65] {co(0,c)} circle[radius={rho:.5f}];',f'\\draw[dotted,gray!70] {co(-xt,zt)}--{co(xt,zt)};',f'\\draw[gray!60] {co(0,c)}--{co(fx,fz)};',f'\\fill[sectionblue] {co(fx,fz)} circle[radius={1.5/scale:.5f}pt] node[{labelpos}] {{$F_{{{n}}}$}};']
 lines += [r'\fill (0,0) circle[radius=1pt] node[below right] {$O$};',r'\end{scope}',f'\\node at (0,-.45) {{{name}}};',r'\end{scope}']
lines += [r'\end{tikzpicture}',r'\end{document}']
(here/'dandelin-axial.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Sphere tangencies verified in all three axial sections.')
