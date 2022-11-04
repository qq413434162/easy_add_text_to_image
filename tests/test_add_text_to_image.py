import logging
import os
import unittest

from main import Config, \
    EasyAddTextToImage

logger = logging.getLogger(__name__)


class Try(unittest.TestCase):
    def setUp(self):
        super(Try, self).setUp()
    
    def tearDown(self):
        super(Try, self).tearDown()
    
    def test_create(self):
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
        self.assertTrue(os.path.exists(final_path))
