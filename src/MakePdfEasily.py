import os
from os import listdir
from PIL import Image
import PyPDF2
from PyPDF2 import PdfMerger


#Create a pdf file using images
def MakePdf(Path, NamePdf):
    try:
        imagenes = [os.path.join(Path, filename) for filename in os.listdir(Path)]
        sorted_imagenes = sorted(imagenes, key=lambda x: os.path.basename(x))
        images_list = []
        for f in sorted_imagenes:
            try:
                images_list.append((Image.open(f)).convert('RGB'))
            except IOError as er:
                print(er)
                return er
        images_list[0].save(NamePdf, save_all=True, append_images=images_list[1:])
        return "./" + NamePdf
    except Exception as err:
        print(err)
        return err

#Merge pdf files
def mergerPDf(Path,NamePdf):
    try:
        PDFS = [os.path.join(Path, f) for f in sorted(os.listdir(Path), key=os.path.basename)]
        merger = PdfMerger()
        [merger.append(pdf) for pdf in PDFS]
        merger.write(NamePdf); merger.close()
        return "./"+NamePdf
    except Exception as err:
        print(err)
        return err