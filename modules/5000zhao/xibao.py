from PIL import Image,ImageFont,ImageDraw

img="./modules/5000zhao/xibao.jpg"
textfont='./modules/5000zhao/fonts/ArialEnUnicodeBold.ttf'
background="./modules/5000zhao/background.jpg"
color='#E4080A'

def xibaodotjpg(text:list):
    
    fontsize=45
    font=ImageFont.truetype(textfont,fontsize)
    
    #w,h=font.getsize(text)

    jpg=Image.open(background)
    draw=ImageDraw.Draw(jpg)
    width,height=jpg.size

    #draw.text((((width-w)/2),height/2),text,fill=color,font=font)
    
    space=28
    h=(fontsize+space)*len(text)
    for i in range(len(text)):
        w=len(text[i])*fontsize
        draw.text(((width-w)/2,(height-h)/2+i*(fontsize+space)),text[i],font=font,fill=color)
    
    
    
    
    
    #jpg.show()
    jpg.save(img)


xibaodotjpg(['1','2','3'])