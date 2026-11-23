import sys, numpy as np
from PIL import Image, ImageFilter
W,H=1080,1350
def bg(w,h,center,edge):
    y,x=np.mgrid[0:h,0:w]; r=np.sqrt(((x-w/2)/(w/2))**2+((y-h/2)/(h/2))**2)/1.414
    r=np.clip(r,0,1)[...,None]; c=np.array(center)*(1-r)+np.array(edge)*r
    return Image.fromarray(c.astype('uint8'))
def to45(path, out):
    im=Image.open(path).convert('RGB'); S=im.size[0]
    g=np.array(im.convert('L')); ys,xs=np.where(g>45)
    x0,x1=xs.min(),xs.max(); cw=int(S*0.8)
    if x1-x0 < cw-60 or ys.max()>S-20:
        cx=(x0+x1)//2; l=min(max(cx-cw//2,0),S-cw)
        im.crop((l,0,l+cw,S)).resize((W,H),Image.LANCZOS).save(out,quality=95); return
    center=im.getpixel((S//2,S//20)); edge=im.getpixel((5,5))
    b=bg(W,H,center,edge); sq=im.resize((W,W),Image.LANCZOS)
    m=Image.new('L',(W,W),255); a=np.array(m,float); f=120
    for i in range(f): a[i,:]*=i/f; a[W-1-i,:]*=i/f
    b.paste(sq,(0,(H-W)//2),Image.fromarray(a.astype('uint8'))); b.save(out,quality=95)
if __name__=='__main__': to45(sys.argv[1],sys.argv[2])
