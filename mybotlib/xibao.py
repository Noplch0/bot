from PIL import Image,ImageFont,ImageDraw

img="./mybotlib/utils/xibao.jpg"
textfont='./mybotlib/utils/fonts/ArialEnUnicodeBold.ttf'
background="./mybotlib/utils/background.jpg"
color='#E4080A'


def setsize(text:list):
    maxlength=0
    for i in range(len(text)):
        maxlength=(len(text[i]) if maxlength<len(text[i]) else maxlength)
    
    size=40*9/maxlength
    
    return int(size)

def xibaodotjpg(text:list):

    jpg=Image.open(background)
    draw=ImageDraw.Draw(jpg)
    width,height=jpg.size
    fontsize=setsize(text)
    font=ImageFont.truetype(font=textfont,size=fontsize)    
    
    space=fontsize
    h=(fontsize+space)*len(text)
    for i in range(len(text)):
        w,h=font.getsize(text[i])
        draw.text(((width-w)/2,(height-h)/2+i*(fontsize+space)),text[i],font=font,fill=color)

    jpg.save(img)


#xibaodotjpg(['有铸币想生成喜报','但是不写内容'])