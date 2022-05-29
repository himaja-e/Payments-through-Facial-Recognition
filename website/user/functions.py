import face_recognition
from django.shortcuts import render
import cv2
import numpy as np
import os
import glob


def handle_uploaded_file(uname,f):


    if('.jpg' in f.name or '.png' in f.name or '.jpeg' in f.name or '.JPG' in f.name or '.PNG' in f.name or '.JPEG' in f.name):
        namestr=""
        l = (f.name).split('.')
        l = l[:-1]
        for i in l:
            namestr=namestr+i
        if uname!=namestr or namestr=='abcd':
            return "a"      # validate whether the image is named with username


        fi = open('user/images/' + f.name,'wb+')
        with fi as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            dirname = os.path.dirname(__file__)
            path = os.path.join(dirname, 'images')
            globals()['image_{}'.format(0)] = face_recognition.load_image_file(path+'\\'+f.name)
            if(len(face_recognition.face_encodings(face_recognition.load_image_file(path+'\\'+f.name)))==0):
                fi.close()
                os.remove(path+'\\'+f.name)    # an image with duplicate name is removed
                q=path+'\\'+f.name
                return q
    return ""
    
