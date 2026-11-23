import sys, numpy as np, glob, subprocess, os, tempfile
from PIL import Image
src,out=sys.argv[1],sys.argv[2]
td=tempfile.mkdtemp()
subprocess.run(['ffmpeg','-v','error','-i',src,'-vf','fps=3',f'{td}/m%03d.png'],check=True)
x0=1e9;x1=0;y0=1e9;y1=0
for f in glob.glob(f'{td}/m*.png'):
    g=np.array(Image.open(f).convert('L')); ys,xs=np.where(g>45)
    x0=min(x0,xs.min());x1=max(x1,xs.max());y0=min(y0,ys.min());y1=max(y1,ys.max())
S=Image.open(glob.glob(f'{td}/m*.png')[0]).size[0]
z=min(1080*0.94/(x1-x0), 1920*0.9/(y1-y0), 1920/S)
sz=int(S*z)//2*2; cx=int(((x0+x1)/2)*z); l=min(max(cx-540,0),sz-1080)
im=Image.open(glob.glob(f'{td}/m*.png')[0]).convert('RGB')
center=im.getpixel((S//2,S//20)); edge=im.getpixel((3,3))
# background: radial gradient 1080x1920 + feather mask
y,x=np.mgrid[0:1920,0:1080]; r=np.clip(np.sqrt(((x-540)/540)**2+((y-960)/960)**2)/1.414,0,1)[...,None]
bg=(np.array(center)*(1-r)+np.array(edge)*r).astype('uint8'); Image.fromarray(bg).save(f'{td}/bg.png')
top=(1920-sz)//2; f=min(150,max(top,1))
a=np.full((sz,1080),255.0)
if top>0:
    for i in range(f): a[i,:]*=i/f; a[sz-1-i,:]*=i/f
Image.fromarray(a.astype('uint8')).save(f'{td}/mask.png')
fc=(f"[0:v]scale={sz}:{sz},crop=1080:{sz}:{l}:0[v];[2:v]format=gray[m];[v][m]alphamerge[vm];"
    f"[1:v][vm]overlay=0:{top}:shortest=1,format=yuv420p")
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-loop','1','-i',f'{td}/bg.png','-loop','1','-i',f'{td}/mask.png',
  '-filter_complex',fc,'-t',subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip(),'-c:v','libx264','-crf','18','-r','30','-movflags','+faststart','-an',out],check=True)
