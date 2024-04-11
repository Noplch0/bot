from PIL import Image,ImageFont,ImageDraw

img="./modules/5000zhao/xibao.jpg"
textfont='./modules/5000zhao/fonts/ArialEnUnicodeBold.ttf'
background="./modules/5000zhao/background.jpg"
color='#E4080A'

def xibaodotjpg(text:list):

    jpg=Image.open(background)
    draw=ImageDraw.Draw(jpg)
    width,height=jpg.size
    fontsize=40
    font=ImageFont.truetype(font=textfont,size=fontsize)    
    
    space=fontsize
    h=(fontsize+space)*len(text)
    for i in range(len(text)):
        w,h=font.getsize(text[i])
        draw.text(((width-w)/2,(height-h)/2+i*(fontsize+space)),text[i],font=font,fill=color)

    jpg.save(img)


#xibaodotjpg(['有铸币想生成喜报','但是不写内容'])