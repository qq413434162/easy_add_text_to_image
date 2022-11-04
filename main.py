from collections import defaultdict

from PIL import Image, \
    ImageFont, \
    ImageDraw
import os
import argparse

import logging

logger = logging.getLogger(__name__)

TOP_PADDING = 10
BOTTOM_PADDING = 10
WIDTH_PADDING = 80
WHITE_COLOR = "rgb(255, 255, 255)"
BLACK_COLOR = "rgb(0, 0, 0)"
TEXT_ALIGN = "center"
FONT_SIZE = 26
TEXT_AUTO_SPLIT_NUM = 13
FONT = "./fonts/PingFang.ttc"


class Config(object):
    # 针对的图片
    src_image: str
    # 输出的图片
    out_image: str
    # 输出的图片是否是jpg
    src_image_is_jpeg: bool
    # 打印文字
    text: str
    # 字体路径
    font: str
    # 字体大小pt单位
    font_size: int
    
    @classmethod
    def parser(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--src",
                            help="source file name",
                            required=True,
                            type=str)
        parser.add_argument("--text",
                            help="text for append to image",
                            required=True,
                            type=str)
        parser.add_argument("--out",
                            help="output file name",
                            default="",
                            type=str)
        parser.add_argument("--font",
                            help="font full path",
                            default=FONT,
                            type=str)
        parser.add_argument("--font_size",
                            help="font size use pt unit",
                            default=FONT_SIZE,
                            type=int)
        parser.add_argument("--text_top_padding",
                            help="text top padding",
                            default=TOP_PADDING,
                            type=int)
        parser.add_argument("--text_bottom_padding",
                            help="text bottom padding",
                            default=BOTTOM_PADDING,
                            type=int)
        parser.add_argument("--text_width_padding",
                            help="text width padding",
                            default=WIDTH_PADDING,
                            type=int)
        parser.add_argument("--text_color",
                            help="text color",
                            default=BLACK_COLOR,
                            type=str)
        parser.add_argument("--text_background_color",
                            help="text background color",
                            default=WHITE_COLOR,
                            type=str)
        parser.add_argument("--text_align",
                            help="text align",
                            default=TEXT_ALIGN,
                            type=str)
        parser.add_argument("--text_auto_split",
                            help="text align",
                            default=False,
                            type=bool)
        parser.add_argument("--text_auto_split_num",
                            help="text align",
                            default=TEXT_AUTO_SPLIT_NUM,
                            type=int)
        args = parser.parse_args()
        logger.debug(args.__dict__)
        return cls(
                **args.__dict__
        )
    
    def handle_path(self, path: str) -> str:
        """
        针对linux的~转换绝对正式路径
        :param path:
        :type path:
        :return:
        :rtype:
        """
        return os.path.expanduser(path)
    
    def __init__(self,
                 src: str,
                 text: str,
                 out: str = "",
                 font: str = FONT,
                 font_size: int = FONT_SIZE,
                 text_top_padding: int = TOP_PADDING,
                 text_bottom_padding: int = BOTTOM_PADDING,
                 text_width_padding: int = WIDTH_PADDING,
                 text_color: str = BLACK_COLOR,
                 text_background_color: str = WHITE_COLOR,
                 text_align: str = TEXT_ALIGN,
                 text_auto_split: bool = False,
                 text_auto_split_num: int = TEXT_AUTO_SPLIT_NUM,
                 ):
        self.src_image = self.handle_path(src)
        self.out_image = self.handle_path(out)
        self.src_image_is_jpeg = True if (
                ".jpg" in self.src_image or ".jpeg" in self.src_image) else False
        self.text = text
        self.font = font
        self.font_size = font_size
        self.text_top_padding = text_top_padding
        self.text_bottom_padding = text_bottom_padding
        self.text_width_padding = text_width_padding
        self.text_color = text_color
        self.text_background_color = text_background_color
        self.text_align = text_align
        self.text_auto_split = text_auto_split
        self.text_auto_split_num = text_auto_split_num


class EasyAddTextToImage(object):
    _config: Config
    # 来源图像的属性
    _src_img_object: Image
    _src_img_width: int
    _src_img_height: int
    
    # 字体对象
    _font_object: ImageFont
    
    # 文字行
    _text: str
    
    # 新增的文字图像
    _text_image: Image
    
    # 是否jpeg格式
    _is_jpeg: bool
    
    def __init__(self, config: Config):
        self._text = config.text
        self._config = config
        self._load_image()
        self._load_font()
    
    def _load_image(self, ):
        self._src_img_object = Image.open(self._config.src_image)
        self._src_img_width, self._src_img_height = self._src_img_object.size
        self._is_jpeg = True if (".jpg" in self._config.src_image or ".jpeg" in
                                 self._config.src_image) else False
    
    def _load_font(self, ):
        self._font_object = ImageFont.truetype(self._config.font,
                                               size=self._config.font_size)
    
    def _get_height(self, lines: str, font: ImageFont) -> int:
        """
        根据文字计算追加的高度
        :param lines:
        :type lines:
        :param font:
        :type font:
        :return:
        :rtype:
        """
        line_num = len(lines.split('\n'))
        height_per_line = font.getsize(lines.split('\n')[0])[1]
        return height_per_line * line_num + TOP_PADDING + BOTTOM_PADDING
    
    def _text_wrap(self, text: str, font: ImageFont, max_width: int) -> str:
        """
        根据文字内容和大小自动增加回车
        :param text: 文字内容
        :type text: string
        :param font: 字体对象
        :type font:
        :param max_width: 图片宽度
        :type max_width: int
        :return: 自动增加回车的文字
        :rtype: string
        """
        lines = []
        
        if font.getsize(text)[0] < max_width:
            lines.append(text)
        else:
            i = 0
            line = ""
            while i < len(text):
                if font.getsize(line + text[i])[0] < (max_width - WIDTH_PADDING):
                    line = line + text[i]
                else:
                    lines.append(line)
                    line = ""
                i += 1
            # 补最后一行
            if line:
                lines.append(line)
        return '\n'.join(lines)
    
    def _get_draw_x(self, draw, lines, font, img):
        """
        得到开始在画布上写文字的x轴
        :param draw:
        :type draw:
        :param lines:
        :type lines:
        :param font:
        :type font:
        :param img:
        :type img:
        :return:
        :rtype:
        """
        line = max(lines.split('\n'), key=lambda x: font.getsize(x)[0])
        w = draw.textsize(line, font=font)[0]
        W = img.size[0]
        return (W - w) / 2
    
    def add_text(self, text: str):
        """
        添加写入的文字
        :param text: 写入的文字
        :type text: string
        :return:
        :rtype:
        """
        self._text += text
        return self
    
    def _count_text(self) -> str:
        """
        计算写入的文字
        :return:
        :rtype:
        """
        new_text = self._text
            
        line = new_text.replace("\\n", "\n")
        if "\n" in line:
            lines_list = []
            intentional_new_lines = line.split("\n")
            for intentionalNewLine in intentional_new_lines:
                lines_list.append(self._text_wrap(intentionalNewLine,
                                                  self._font_object,
                                                  self._src_img_width))
            lines = "\n".join(lines_list)
        else:
            lines = self._text_wrap(line,
                                    self._font_object,
                                    self._src_img_width)
        return lines
    
    def draw_text(self, text: str):
        """
        追加文字在原有图片上
        :return:
        :rtype:
        """
        image_with_white_space = Image.new("RGBA", (self._src_img_width,
                                                    self._src_img_height +
                                                    self._get_height(
                                                            text,
                                                            self._font_object,
                                                    )), self._config.text_background_color)
        image_with_white_space.paste(self._src_img_object, (0, 0))
        draw = ImageDraw.Draw(image_with_white_space)
        
        draw.text((self._get_draw_x(
                draw,
                text,
                self._font_object,
                image_with_white_space,
        ),
                   self._src_img_height - TOP_PADDING - 10),
                text,
                fill=self._config.text_color,
                font=self._font_object,
                align=self._config.text_align,
        )
        self._text_image = image_with_white_space
    
    def save_to(self, save_path: str = None) -> str:
        """
        
        :param save_path: 保存路径
        :type save_path: string
        :return: 保存路径
        :rtype: string
        """
        if not save_path:
            save_path = self._config.out_image
        
        # 不指定保存路径则保存在当前路径下
        if not save_path:
            name, ext = os.path.splitext(self._config.src_image)
            save_path = f"{name}-after{ext}"

        text = self._count_text()
        self.draw_text(text)
        # 保存
        logger.debug("Saved as " + save_path)
        
        if self._is_jpeg:
            rgb_image = self._text_image.convert("RGB")
            rgb_image.save(save_path)
        else:
            self._text_image.save(save_path)
        return save_path


if __name__ == '__main__':
    config = Config.parser()
    EasyAddTextToImage(config).save_to()
