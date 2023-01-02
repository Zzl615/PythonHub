# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-01-02 15:01:08
# @Descp: 创建处方图片
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-01-02 17:41:32

from pydantic import BaseModel, Field

from typing import List

from PIL import Image, ImageDraw, ImageFont

from io import BytesIO
import base64
import re


class PrescriptionDiagnostic(BaseModel):  
    name: str = Field("", description="姓名")
    gender: str = Field("", description="性别")
    age: str = Field("", description="年龄") 
    department: str = Field("", description="科室")
    name: str = Field("", description="开具时间")
    create_time: str = Field("", description="开具时间")
    diagnostic: str = Field("", description="诊断")

class Prescription(BaseModel):
    drug: str = Field("", description="药品")
    dosage: str = Field("", description="用法用量")
    standard: str = Field("", description="规格")
    total: str = Field("", description="总数")


class SignInfo(BaseModel):
    doctor_sign: str = Field("", description="医生签字")
    pharmacist_sign: str = Field("", description="药师签字")


class ImageConfig(BaseModel):
    width: int = Field(750, description="图片宽度")
    length: int = Field(860, description="图片长度")
    order_no: str = Field("", description="处方单号")
    presc_limit: int = Field(5, description="处方数量")
    header: PrescriptionDiagnostic = Field(default_factory=PrescriptionDiagnostic, description="处方标题")
    prescription_list: List[Prescription] =  Field(default_factory=Prescription, description="处方列表")
    sign: SignInfo = Field(default_factory=SignInfo, description="签字信息")



class CreatePrescriptionImage:

    def _base64_to_image(self, base64_str: str) -> Image.Image:
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        return img

    
    def _draw_underlined_text(self, draw, pos, text, font, **options):
        draw.text(pos, text, font=font, **options)
    
    def _prescription(self, draw, pms: ImageConfig, font, font_01):
        self._draw_underlined_text(draw, (63, 314), 'Rp.', font, fill=0)
        row_01 = 63
        row_02 = 414
        row_03 = 655
        row_mid = 68
        num = 0
        for item in pms.prescription_list[0:5]:
            self._draw_underlined_text(draw, (row_01, 350 + num*row_mid), item.drug, font, fill=0)
            self._draw_underlined_text(draw, (row_01, 384 + num*row_mid), item.dosage, font_01, fill=0)
            self._draw_underlined_text(draw, (row_02, 366 + num*row_mid), item.standard, font, fill=0)
            self._draw_underlined_text(draw, (row_03, 366 + num*row_mid), item.total, font, fill=0)
            num +=1

        
        if len(pms.prescription_list) < pms.presc_limit:
            start = 350 + num*row_mid
            end = 720
            mid = (end - start)/2 + start - 10
            draw.line((30, start, 720, start), width=1, fill=0)
            self._draw_underlined_text(draw, (300, mid), "以下空白，修改无效", font, fill=0)
    

    def _header(self, draw, pms: ImageConfig, font_01, font_02):
        self._draw_underlined_text(draw, (40, 30), f"处方编号：{pms.order_no}", font_01, fill=0)
        self._draw_underlined_text(draw, (230, 93), '互联网医院处方笺', font_02, fill=0)

        
    def _diagnostic(self, draw, pms: ImageConfig):
        font = ImageFont.truetype(font='PingFang.ttc', size=15)
        self._draw_underlined_text(draw, (63, 169), f"姓名：{pms.header.name}", font, fill=0)
        self._draw_underlined_text(draw, (305, 169), f"性别：{pms.header.gender}", font, fill=0)
        self._draw_underlined_text(draw, (514, 169), f"年龄：{pms.header.age}", font, fill=0)
        self._draw_underlined_text(draw, (63, 207),  f"科室：{pms.header.department}", font, fill=0)
        self._draw_underlined_text(draw, (514, 211), f"开具时间：{pms.header.department}", font, fill=0)
        self._draw_underlined_text(draw, (63, 245), f"诊断：{pms.header.diagnostic}", font, fill=0)
    

    def _tail(self, draw, font):
        line_high = 730
        self._draw_underlined_text(draw, (63, line_high),  "医师：", font, fill=0)
        self._draw_underlined_text(draw, (250, line_high), "药师：", font, fill=0)
        self._draw_underlined_text(draw, (410, line_high), "调配：", font, fill=0)
        self._draw_underlined_text(draw, (530, line_high), "核对/发药：", font, fill=0)
    


    def _tail_notice(self, draw, font_01):
        line_01 = 790
        line_02 = 813
        self._draw_underlined_text(draw, (63, line_01), '注：', font_01, fill=0)
        self._draw_underlined_text(draw, (100, line_01), '本处方72小时内有效。', font_01, fill=0)
        self._draw_underlined_text(draw, (100, line_02), '互联网医院在线开具的处方必须有医师的电子签名，经药师审核后生效，个人自行下载不具备效力', font_01, fill=0)


    def run(self, pms: ImageConfig):
        image = Image.new(mode="RGB", size=(pms.width, pms.length), color="white")
        # 添加文字
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font='PingFang.ttc', size=16)
        font_01 = ImageFont.truetype(font='PingFang.ttc', size=14)
        font_02 = ImageFont.truetype(font='PingFang.ttc', size=22)
        self._header(draw, pms=pms, font_01=font_01, font_02=font_02)
        draw.line((10, 145, 750, 145), width=5, fill="#F9F9F9")
        self._diagnostic(draw, pms=pms)
        draw.line((10, 287, 750, 287), width=5, fill="#F9F9F9")
        self._prescription(draw, pms=pms, font=font, font_01=font_01)
        draw.line((10, 720, 750, 720), width=5, fill="#F9F9F9")
        self._tail(draw, font=font)
        self._tail_notice(draw, font_01=font_01)
        # company_img = Image.open("src/resource/company.png")
        # image.paste(company_img, (530, 627),  mask=company_img)
        doctor_sign_img = self._base64_to_image(pms.sign.doctor_sign)
        image.paste(doctor_sign_img, (62, 695),  mask=doctor_sign_img)
        # pharmacist_sign_img = self._base64_to_image(pms.sign.pharmacist_sign)
        # image.paste(pharmacist_sign_img, (245, 695),  mask=pharmacist_sign_img)
        draw.rectangle(xy=(0, 0, 750, 860), fill=None, outline="#F9F9F9", width=20)
        image.show()




if __name__ == "__main__":
        
    params  ={
        'width': 750,
        'length': 860,
        'order_no': '123344455',
        'header': {
            'name': '张小星',
            'gender': '女',
            'age': '31岁',
            'department': '呼吸科',
            'create_time': '2022-12-29',
            'diagnostic': '上呼吸道感染',
        },
        "prescription_list" : [
            {'drug': '布洛芬缓释胶囊', 'dosage': '用法用量: 口服，每天1次，每次2粒', 'standard': '0.1%×10g', 'total': 'x1盒'},
            {'drug': '酚咖片', 'dosage': '用法用量: 口服，每天1次，每次2粒', 'standard': '0.2%×10g', 'total': 'x5盒'},
            {'drug': '甘草片', 'dosage': '用法用量: 口服，每天1次，每次2粒', 'standard': '0.4%×10g', 'total': 'x3盒'},
            {'drug': '板蓝根', 'dosage': '用法用量: 口服，每天1次，每次2粒', 'standard': '0.8%×10g', 'total': 'x4盒'},
            {'drug': '阿莫西林', 'dosage': '用法用量: 口服，每天1次，每次2粒', 'standard': '0.1%×10g', 'total': 'x8盒'},
        ],
        "sign": {
            "doctor_sign" : "iVBORw0KGgoAAAANSUhEUgAAAMgAAABQCAYAAABcbTqwAAABuElEQVR42u3aS67CMAwF0Ox/03lT9ATEbvOjOUdiRCVa5JvYgVIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgpb68WtfA2+IQECERhA9F8K04qoBwWjj+F0IrIE8oHC0WzUBkA1InBqR1jyMDUoPvo8UavnvUxKtMDsjMwPLjARldqLMLL9JCCoWAhOaMFYVbJz571T7RWim/Fc/Molk94zjZEojwELqiIFa1cp8WBa2WlmqrlbL3Z0eKPHNaJyACkjrFqZsHJNNatmYwARGQ8Kq702wwKiBFQM4NSKTnLmXuap5pg0bOYe8CMnsnZZMhvXXUudMp1t37+LYoZEMrIA8OR3QQ7VWYvQNy5X5azx/dPYXh4QG5ulLv8kPhlYDUROhb1wnIg0Nyt5WZ0U6M+LEuGvgqIPQKSF0UkJIc2u/ukk6wBCRVpKND0vtI90rLaTgnHJBoMY06ULhapNk2LfIcK//EyYYByV5TBwag50re6ySMA4f0EbvDbi1K9LOrcJy7a8wKx6/tnuXQ74TgkH1CIWSeTzgODsnd4nlSy9krUHD8/AYAAAAAAAAAAAAAAAAAAAAAwGV/7ct4pKe7ZqYAAAAASUVORK5CYII=",
            "pharmacist_sign" : "iVBORw0KGgoAAAANSUhEUgAAAMgAAABQCAYAAABcbTqwAAABuElEQVR42u3aS67CMAwF0Ox/03lT9ATEbvOjOUdiRCVa5JvYgVIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgpb68WtfA2+IQECERhA9F8K04qoBwWjj+F0IrIE8oHC0WzUBkA1InBqR1jyMDUoPvo8UavnvUxKtMDsjMwPLjARldqLMLL9JCCoWAhOaMFYVbJz571T7RWim/Fc/Molk94zjZEojwELqiIFa1cp8WBa2WlmqrlbL3Z0eKPHNaJyACkjrFqZsHJNNatmYwARGQ8Kq702wwKiBFQM4NSKTnLmXuap5pg0bOYe8CMnsnZZMhvXXUudMp1t37+LYoZEMrIA8OR3QQ7VWYvQNy5X5azx/dPYXh4QG5ulLv8kPhlYDUROhb1wnIg0Nyt5WZ0U6M+LEuGvgqIPQKSF0UkJIc2u/ukk6wBCRVpKND0vtI90rLaTgnHJBoMY06ULhapNk2LfIcK//EyYYByV5TBwag50re6ySMA4f0EbvDbi1K9LOrcJy7a8wKx6/tnuXQ74TgkH1CIWSeTzgODsnd4nlSy9krUHD8/AYAAAAAAAAAAAAAAAAAAAAAwGV/7ct4pKe7ZqYAAAAASUVORK5CYII=",
        }
    }
    input_dto = ImageConfig.parse_obj(params)
    obj = CreatePrescriptionImage()
    obj.run(input_dto)



