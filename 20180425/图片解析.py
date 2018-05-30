from PIL import Image
import pytesseract

# 脚本编写的时候指定tessdata 路径;https://blog.csdn.net/dubinglin/article/details/77519750
tessdata_dir_config = r'--tessdata-dir "E:\Tesseract-OCR\tessdata"'
jpg1 = Image.open('1.png')
#jpg1.show()
text = pytesseract.image_to_string(jpg1,lang='chi_sim',config=tessdata_dir_config)#使用简体中文解析图片
print(text)
# with open('1.txt','w') as f:
#     f.write(str(text))