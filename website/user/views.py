from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector as sql
import face_recognition
import cv2
import numpy as np
import os
import time
import glob
import dlib
import MySQLdb as sql
from .forms import upload
from user.forms import *
from user.functions import handle_uploaded_file
from user import *



# Create your views here.
def formsubmission(request):
   
    form = upload()
    p=""
    username=""
    emailid=""
        
    if request.method == "POST":
        form = upload(request.POST,request.FILES)
        username = request.POST['name']
        passwd = request.POST['password']
        if form.is_valid():
            f=request.FILES['file']
            p=handle_uploaded_file(username,f)   # save the image in the user directory

                #Check the number of faces in the uploaded image. Since, it is a payment system, there can't be more than one face and if more than 1 face is found
    #error page is returned
            detector = dlib.get_frontal_face_detector()
            frame =cv2.imread("user/images/" + (f).name)
            gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            for count,face in enumerate(faces):
                if(count>1):
                    return render(request,'error.html')
                    
        else:
            form = upload()

            
            
        if(username!="abcd" and password!="12345"):

            m=sql.connect(host="localhost",user="root",passwd="himaja",database='website')
            cursor=m.cursor()
            c="select * from users where user_name='{}' and password='{}'".format(username,passwd)
            cursor.execute(c)
            t=tuple(cursor.fetchall())
            if(p!="" or t==()):
                return render(request,"error.html")
        
        
        return render(request,'home.html',{'form':form})

        



def validation(request):
    return render(request,'validate.html')




def facereco(request):
    t1=time.time()
    capture = cv2.VideoCapture(0)

    #array of pictures with encodings
    known_face_encodings = []
    known_face_names = []
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'images')
    image_list=[]


    #array of all the saved files' paths
    for image in os.listdir(path):
        image_list.append(path+'\\'+image)

    
    number = len(image_list)     #number of known faces

    names = image_list.copy()

    for i in range(number):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(image_list[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        known_face_encodings.append(globals()['image_encoding_{}'.format(i)])

        # array of known names
        names[i] = names[i].replace("known_people/", "")  
        known_face_names.append(names[i])

    # Initializing some variables
    locations = []
    encodings = []
    face_names = []
    process_this_frame = True
    name="Unknown"

    while True:
            # Capture frame
        ret, frame = capture.read()

            # Resize frame of video to 1/4 of its size
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
        if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
            locations = face_recognition.face_locations(rgb_small_frame)
            encodings = face_recognition.face_encodings(rgb_small_frame, locations)

            face_names = []
            for encoding in encodings:
                    # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, encoding)
                name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                distances = face_recognition.face_distance(known_face_encodings, encoding)
                best_match_index = np.argmin(distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


            # Display the results
        for (top, right, bottom, left), name in zip(locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

                # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
        cv2.imshow('Video', frame)
        key=cv2.waitKey(1)

        t2=time.time()
        if(t2-t1>100):
            break
        if(name!="Unknown"):
            break
            

        # Release handle to the webcam
    capture.release()
    cv2.destroyAllWindows()
    if(name!="Unknown"):
        return render(request,"success.html")
    




def findnumber(request):
    t1=time.time()
    cap = cv2.VideoCapture(0)
 
 
    # Detect the coordinates
    detector = dlib.get_frontal_face_detector()
    
    
    # Capture frames continuously
    while True:
    
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
    
        # RGB to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
    
        # Iterator to count faces
        i = 0
        for face in faces:
    
            # Get the coordinates of faces
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
    
            # Increment iterator for each face in faces
            i = i+1
            
            # Display the box and faces
            cv2.putText(frame, 'face num'+str(i), (x-10, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
    
        # Display the resulting frame
        cv2.imshow('frame', frame)

        t2=time.time()
        name=str(i)
        # This command let's us quit with the "q" button on a keyboard.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    
    # Release capture
    cap.release()
    cv2.destroyAllWindows()
    return render(request,"people.html", {"findnumber":name})
        
