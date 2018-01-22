# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFilter

im = Image.open("D:/BaiduNetdiskDownload/50-01-B.bmp")


edgenhance = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
edgef = edgenhance.filter(ImageFilter.FIND_EDGES)
edgef.show()


