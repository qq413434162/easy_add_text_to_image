# easy_add_text_to_image
<div align=center>

[![PyPI version](https://img.shields.io/pypi/v/dankcli.svg?label=PyPI)](https://pypi.org/project/dankcli/)
[![Python Version](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
</div>

`easy_add_text_to_image` is a CLI Tool or Package Generator which automatically 
adds white space and text to the bottom of your image.

# Features
- rich annotations
- simple and easy to use
- convenient development CLI tool provide


# Requirement
```shell
Pillow==8.4.0
```

turns this

![xxEfmt.png](https://s1.ax1x.com/2022/11/08/xxEfmt.png)

to this

![xxEh0P.png](https://s1.ax1x.com/2022/11/08/xxEh0P.png)

# How to use it
- bash
```bash
python main.py --src "./example/test.png" --out "./example/test_after.png" --text "photo-1546992743-6baeb1d6b07d"
```
- Code
```python
out_img_path = ""
src_img_path = "./example/test.png"
config = Config(
        src=src_img_path,
        text="",
        out=out_img_path,
        font="./fonts/PingFang.ttc",
        text_auto_split=True,
)
final_path = EasyAddTextToImage(config).add_text("photo-1546992743-6baeb1d6b07d").save_to()
```