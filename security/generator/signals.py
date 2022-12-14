from PIL import Image, ImageDraw
import qrcode

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from io import BytesIO
from django.core.files import File
from django.conf import settings
import os
from .models import Student


@receiver(pre_save,sender=Student)
def create_qr(sender,instance,*args,**kwargs):
    """
    Take class instance

    Return the qr code matrix 
    """
    qr = qrcode.QRCode(version=1, box_size = 6, border=5)

    data = instance.reg_no +" "+ instance.gadget_serial 
    qr.add_data(data)
    qr.make(fit=True)
    # qrcode_img = qrcode.make(data)
    qrcode_img=qr.make_image(fill_color = 'black', back_color = 'white')
    canvas = Image.new("RGB",(220,220),"white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qrcode_img)
    new_name = instance.reg_no.replace("/","-")
    fname = f"qrcode-{new_name}.png"
    buffer = BytesIO()
    canvas.save(buffer,"Png")
    instance.qr_code.save(fname,File(buffer),save=False)
    canvas.close()

@receiver(post_save,sender=Student)
def text_generator(sender,instance,created,**kwargs):
    if created:
        with open(os.path.join(settings.MEDIA_ROOT,"db_data.txt"),"a",encoding="utf-8") as f:
            data = f.write(str(instance.reg_no)+"\n")

# Importing library
#import qrcode

# # Data to encode
# data = "GeeksforGeeks"

# # Creating an instance of QRCode class
# qr = qrcode.QRCode(version = 1,
# 				box_size = 10,
# 				border = 5)

# # Adding data to the instance 'qr'
# qr.add_data(data)

# qr.make(fit = True)
# img = qr.make_image(fill_color = 'red',
# 					back_color = 'white')

# img.save('MyQRCode2.png')

