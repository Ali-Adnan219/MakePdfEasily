import os
from os import listdir
from PIL import Image
import PyPDF2
from PyPDF2 import PdfMerger


#Create a pdf file using images
def MakePdf(Path,NamePdf):
    try:
        imagenes = []
        images_list = []
        listarImagenes  = listdir(Path)
        for list in listarImagenes:  
            a = Path +"/"+ list
            imagenes.append(a)
        #print(imagenes)
        for f in imagenes:
            try:
                #print(f)
                images_list.append((Image.open(f)).convert('RGB'))
            except IOError as er:
                return er
        images_list[0].save(NamePdf, save_all=True, append_images=images_list[1:])
        return "./"+NamePdf
    except Exception as err:
        return err

#Merge pdf files
def mergerPDf(Path,NamePdf):
    
    try:
        PDFS = []
        listarPDf  = listdir(Path)
        for list in listarPDf:  
            a = Path +"/"+ list
            PDFS .append(a)
        pdfs = PDFS
        merger = PdfMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(NamePdf)
        merger.close()
        return "./"+NamePdf
    except Exception as err:
        return err