# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-01-10 08:15:53
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-01-20 08:41:22
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

import base64



def base64_to_image(base64_str: str) -> Image.Image:
    """
    功能：base64文本格式转换为图片对象
    base64_str: str
    return: Image.Image
    """
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img

def image_to_base64(image: Image.Image, fmt="png") -> str:
    """
    功能：base64文本格式转换为图片对象
    image: Image.Image
    fmt: 图片格式
    return: str
    """
    output_buffer = BytesIO()
    image.save(output_buffer, format=fmt)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode("utf-8")
    return f"data:image/{fmt};base64," + base64_str

def draw_grid_transverse_line(draw, pos_list, fill, width, gap):
    """
    绘制横向虚线
    """
    x_begin, y_begin = pos_list[0]
    x_end, y_end = pos_list[1]
    for x in range(x_begin, x_end, gap):
        draw.line([(x, y_begin), (x + gap / 2, y_begin)], fill=fill, width=width)



class ImageExample:
    
    def create_one(self, pms):
        # 创建一个白色的图片
        image = Image.new(mode="RGB", size=(750, 860), color="white")
        # 创建一个画笔
        draw = ImageDraw.Draw(image)
        # 创建一个字体
        font = ImageFont.truetype(font='PingFang.ttc', size=16)
        
        # 写入文字
        draw.text((40, 30), "we are the champions!", font=font, fill="#999999")
        
        # 绘制横向实线
        draw.line((30, 60, 720, 60), width=1, fill=0)
        
        # 绘制横向虚线
        y_pos_list = [(10, 180), (750, 180)]
        draw_grid_transverse_line(draw, y_pos_list, fill="#E7E7E7", width=1, gap=5)
        image.show()


    

def main():
    ImageExample().create_one(None)
    print("Hello, World!")


if __name__ == "__main__":
    main()
