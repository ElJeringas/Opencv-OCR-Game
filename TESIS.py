# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:43:49 2019

@author: Santiago
"""

#Librerias-------------------------------------------------------------------------------------------------------------
import numpy as np
import cv2
from PIL import Image
import pytesseract
import re
import pyttsx3
#-----------------------------------------------------------------------------------------------------------------------
#Saludo de bienvenida--------------------------------------------------------------------------------------------------
print('Bienvenido')
print('Juego de operaciones matemáticas.')
engine = pyttsx3.init()
engine.say('Bienvenido')
engine.say('Juego de operaciones matemáticas.')
engine.runAndWait()
#----------------------------------------------------------------------------------------------------------------------
#ROI N°1---------------------------------------------------------------------------------------------------------------
x1=130
y1=162
x2=680
y2=478
#----------------------------------------------------------------------------------------------------------------------

cap = cv2.VideoCapture(0)
#---------------------------------------------------------------------------------------------------------------------

#Procesamiento de imagen + OCR-----------------------------------------------------------------------------------------
def proc(img):
    i=0

    #Tesseract v 4.0
    #------------------------------------------------------------------------------------------------------------------
    #OCR options:
    config = ("-l eng --psm 6 --oem 1")     #--PRIMER NUMERO
    config2 = ("-l eng --psm 6 --oem 1")    #--SEGUNDO NUEMRO
    config3 = ("-l eng --psm 6 --oem 1")    #--TERCER NUMERO

    #lenguaje=default, psm=6:Assume a single uniform block of text., OEM=1: Neural nets LSTM engine only.--------------
    #------------------------------------------------------------------------------------------------------------------

    img = cv2.imread('capture.jpg', -1)  # abre imagen
    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 11)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None ,alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
  #  result_norm = cv2.merge(result_norm_planes)

    cv2.imwrite('shadows_out.png', result)
    #cv2.imwrite('shadows_out.png', result_norm)
########################################################################################################################
########################################################################################################################

    ROI_1 = cv2.imread("shadows_out.png")    
    #------------------------------------------------------------------------------------------------------------------
    #Escala de grises de ROI 1-----------------------------------------------------------------------------------------
    gray = cv2.cvtColor(ROI_1, cv2.COLOR_BGR2GRAY)
    #------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------
    #ROI 2: PRIMER NUMERO------------------------------------------------------------------------------------------------
    x3=89
    y3=7
    x4=523
    y4=73
    #-------------------------------------------------------------------------------------------------------------------
    #ROI 3 SEGUNDO NUMERO-----------------------------------------------------------------------------------------------
    x5=8
    y5=125
    x6=523
    y6=188
    #-------------------------------------------------------------------------------------------------------------------
    #ROI 4 RESULTADO----------------------------------------------------------------------------------------------------
    x7=2
    y7=240
    x8=526
    y8=300
    #-------------------------------------------------------------------------------------------------------------------
    #ROI 2: PROCESAMIENTO DE IMAGEN SOBRE PRIMER NUMERO-----------------------------------------------------------------
    ROI_2=gray[y3:y4,x3:x4]
    blur = cv2.medianBlur(ROI_2,5)
    cv2.imwrite("blur.jpg", blur)    
    _,th = cv2.threshold(blur,0,230,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite("bin.jpg", th)    
    kernel = np.ones((4,4),np.uint8)
    erosion = cv2.dilate(th,kernel,iterations = 1)
    cv2.imwrite("erosion.jpg", erosion)    
    equ = cv2.equalizeHist(erosion)
    cv2.imwrite("equaliza.jpg", equ)    
    
    _ , contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt)>52:
            [x,y,w,h] = cv2.boundingRect(cnt)            
            if  h>34 and w<47:
                cuadro = equ[y:y+h,x:x+w]
                nombre = './cap%i'%i + '.jpg'
                cv2.imwrite(nombre, cuadro)
                i=i+1
    #cv2.imshow('blurred image 1',equ)         
    cv2.imwrite("roi1.jpg", equ)
    #OCR sobre primer numero----------------------------------------------------------------------------------------------
    roi1 = Image.open("roi1.jpg")
    t1=pytesseract.image_to_string(roi1, config=config)
    g= ''.join(c for c in t1 if c in '#0123456789')
    print('el primer número ingresado es')               
    print(g)
    print('---------------------------------------------')     #-------------------------------------------------------------------------------------------------------------------
    #ROI3 PROCESAMIENTO DE IMAGEN SOBRE SEGUNDO NUMERO------------------------------------------------------------------
    valor2=gray[y5:y6,x5:x6]
    blur2 = cv2.medianBlur(valor2,5)
    _,th2 = cv2.threshold(blur2,0,230,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    erosion2 = cv2.dilate(th2,kernel,iterations = 1)
    equ2 = cv2.equalizeHist(erosion2)
    _ , contours2, hierarchy2 = cv2.findContours(equ2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

   # cv2.imshow('blurred image 2',equ2)         
    cv2.imwrite("roi2.jpg", equ2)
    roi2 = Image.open("roi2.jpg")
    t2=pytesseract.image_to_string(roi2, config=config2)
    g2= ''.join(c for c in t2 if c in '-+Xx#0123456789')
    print('el segundo número ingresado es')                
    print(g2)
    print('---------------------------------------------') 
    #---------------------------------------------------------------------------------------------------------------------
    #ROI4: PROCESAMIENTO DE IMAGEN SOBRE  RESULTADO    -------------------------------------------------------------------
    valor3=gray[y7:y8,x7:x8]
    blur3 = cv2.medianBlur(valor3,5)
    _,th3 = cv2.threshold(blur3,0,230,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    erosion3 = cv2.dilate(th3,kernel,iterations = 1)
    equ3 = cv2.equalizeHist(erosion3)
    _ , contours3, hierarchy3 = cv2.findContours(equ3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

   # cv2.imshow('blurred image 3',equ3)         
    cv2.imwrite("roi3.jpg", equ3)
    roi3 = Image.open("roi3.jpg")
    t3=pytesseract.image_to_string(roi3, config=config3)
    g3= ''.join(c for c in t3 if c in '#0123456789')
    print("el resultado ingresado es:")
    print(g3)
    print('---------------------------------------------') 
    print('---------------------------------------------')   
    #---------------------------------------------------------------------------------------------------------------------

    #INICIO DE OPERACION MAS COMPARACION DE RESULTADOS--------------------------------------------------------------------
   #EXTRAE # DE LA CIFRA PARA OPERACION----------------------------------------------------------------------------------
    regex = re.compile('#')
    
    if (g.find(' ') != -1):
        engine.say('números ingresados incorrectos')
        print('números ingresados incorrectos')
        engine.runAndWait()
        return
            
    if((regex.search(g) and regex.search(g2) and regex.search(g3)) == None): 
        engine.say('números ingresados incorrectos inserte el signo numeral')
        print(('números ingresados incorrectos inserte el signo numeral'))
        engine.runAndWait() 
    else: 
        engine.say("números ingresados de manera correcta.")    
        print("números ingresados de manera correcta.")         
    #------------------------------------------------------------------------------------------------------------------
    #MULTIPLICACION-------------------------------------------------------------------------------------------------------------
        if (g2.find('x') != -1): 
            engine.say('el operador seleccionado es la multiplicación')
            print('el operador seleccionado es la multiplicación')            
            engine.runAndWait()
            f=g.replace("#")
            f2=g2.replace("x#","")
            f3=g3.replace("#","") 
            #print(f,f2)
            cifra1= int(f)
            cifra2= int(f2)
            cifra3= int(f3)
            engine.say('el primer número ingresado es')
            engine.say(cifra1)
            engine.runAndWait()        
            engine.say('el segundo número ingresado es')
            engine.say(cifra2)
            engine.runAndWait()     
            engine.say('el resultado ingresado es')
            engine.say(cifra3) #ojo
            engine.runAndWait()              
            operacion= (cifra1)*(cifra2)
    #SUMA--------------------------------------------------------------------------------------------------------------
        if (g2.find('+') != -1): 
            engine.say('el operador seleccionado es la suma')
            print('el operador seleccionado es la suma')            
            engine.runAndWait()
            f=g.replace("#","")
            f2=g2.replace("+#","")
            f3=g3.replace("#","") 
            #print(f,f2)
            cifra1= int(f)
            cifra2= int(f2)
            cifra3= int(f3)
            engine.say('el primer número ingresado es')
            engine.say(cifra1)
            engine.runAndWait()        
            engine.say('el segundo número ingresado es')
            engine.say(cifra2)
            engine.runAndWait()     
            engine.say('el resultado ingresado es')
            engine.say(cifra3) #ojo
            engine.runAndWait()              
            operacion= cifra1+cifra2
            #print(g3)
     #-----------------------------------------------------------------------------------------------------------------
     #RESTA------------------------------------------------------------------------------------------------------------
        if (g2.find('-') != -1): 
            engine.say('el operador seleccionado es la resta')
            engine.runAndWait()
            f=g.replace("#","")
            f2=g2.replace("-#","") 
            f3=g3.replace("#","")
            #print(f,f2)
            cifra1= int(f)
            cifra2= int(f2)
            cifra3= int(f3)
            engine.say('el primer número es')
            engine.say(cifra1)
            engine.runAndWait()        
            engine.say('el segundo número es')
            engine.say(cifra2)
            engine.runAndWait()     
            engine.say('el tercer número es')
            engine.say(cifra3)
            engine.runAndWait()   
            operacion= cifra1-cifra2
            #print(operacion) 
            #f3=g3.replace("#","")   ######******##### numeral en la columna3
    #------------------------------------------------------------------------------------------------------------------
    #COMPARACIÓN-------------------------------------------------------------------------------------------------------
        if (operacion == cifra3):
            engine.say('Resultado correcto')
            engine.say('¡Felicitaciones!')
            print('Resultado correcto')
            print('¡Felicitaciones!')
            engine.runAndWait()
        else:
            print('Resultado erroneo')
            print('la solución es')
            print(operacion)
            print('Por favor, Intente otra vez.')            
            engine.say('Resultado erroneo')
            engine.say('la solucion es')
            engine.say(cifra3)
            engine.say('Por favor, Intente otra vez.')
            engine.runAndWait()

    return



while(True):
    ret, frame = cap.read() 
    flp = cv2.flip(frame,-1)
    frame1 = cv2.resize(flp,(700,500))
    frame_clone = frame1.copy()

    #ROI 1-------------------------------------------------------------------------------------------------------------
    cv2.rectangle(frame_clone, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.imshow('frame',frame_clone)
    roi = frame_clone[y1:y2, x1:x2]
    #------------------------------------------------------------------------------------------------------------------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #c=cv2.waitKey(1)
    #------------------------------------------------------------------------------------------------------------------
    #Captura de imagen mediante tecla "v"------------------------------------------------------------------------------
    if cv2.waitKey(1) == ord('v'):
        cv2.imwrite("capture.jpg", roi)
        captura = cv2.imread("capture.jpg")
        proc(captura)
        break
    else:
        None
        
cap.release()
cv2.destroyAllWindows()