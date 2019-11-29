import cv2
import numpy as np

#cuadro azul
h1 = 100
w1 = 100
x1=100 + w1
y1= 150 

#cuadro verde
h2 = 100
w2 = 200
x2=100 + w2
y2= 150 

#cuadro rojo 
h3 = 100
w3 = 300
x3=100 + w3
y3= 150

#cuadro amarillo
h4 = 100
w4 = 400
x4=100 + w4
y4= 150

#cuadro negro sale
h5 = 100
w5 = 500
x5=100 + w5
y5= 150



def main():    
    a1 = False
    a2 = False
    a3 = False
    a4 = False
    a5 = False
    sas =True

    r = np.zeros((480,640,3))
   
    cap = cv2.VideoCapture(0)

    #rangos de verde que va a coger
    verdeBajo = np.array([40, 50, 50],np.uint8)
    verdeAlto = np.array([80, 255, 255],np.uint8)
    

    while True:
     
     #leemos frame por frame
      ret,frame = cap.read()
     
     
      if ret==True:
        r=frame

        mask2 = np.zeros(frame.shape[:2],np.uint8)
        mask2 [:,:] = 0
        mask2 [h1:y1,w1:x5] = 255
        mascara =cv2.bitwise_and (frame, frame, mask=mask2)

        frameHSV = cv2.cvtColor(mascara,cv2.COLOR_BGR2HSV)#cambiamos el formato del frame
        mask = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
        contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        for c in contornos:
          #solo tomamos los contornos y los volvemos areas
          area = cv2.contourArea(c)
          if area > 3500:

          #si el area es mayor a 3000 px la 
            M = cv2.moments(c)

            #para la posicion del pto
            if (M["m00"]==0): M["m00"]=1 
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])

            #acciones
            if x<=x1 and y <= y1 and y >= h1 and x >=w1:
                 a1 = True
                 a2 = False
                 a3 = False
                 a4 = False
                 a5 = False
                 sas= False
                 

            elif x<=x2 and y <= y2 and y >= h2 and x >=w2:
                 a1 = False
                 a2 = True
                 a3 = False
                 a4 = False
                 a5 = False
                 sas= False




            elif x<=x3 and y <= y3 and y >= h3 and x >=w3:
                    a1 = False
                    a2 = False
                    a3 = True
                    a4 = False
                    a5 = False
                    sas= False




            elif x<=x4 and y <= y4 and y >= h4 and x >=w4:
                    a1 = False
                    a2 = False
                    a3 = False
                    a4 = True
                    a5 = False
                    sas= False

            elif x<=x5 and y <= y5 and y >= h5 and x >=w5:
                    a1 = False
                    a2 = False
                    a3 = False
                    a4 = False
                    a5 = True
                    sas= False
        

            else:
             r=frame

      
            cv2.circle(frame, (x,y), 7, (0,255,0), -1)
            cv2.circle(r, (x,y), 7, (0,255,0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            #cv2.putText(r, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno], 0, (0,255,0), 3)
            #cv2.drawContours(r, [nuevoContorno], 0, (0,255,0), 3)
        #cv2.imshow('maskAzul',mask)
        if a1:
                 #blanco y negromask2 = np.zeros(frame.shape[:2],np.uint8)
                                 
                 gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                 ret, tresh=cv2.threshold(gray,50,200,cv2.THRESH_BINARY)
                 r = tresh
                 r = cv2.cvtColor(r, cv2.COLOR_GRAY2RGB)
          
        elif a2:
                 #saca los bordes
                 gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                 r = cv2.Canny(gray, 100,200)
                 r = cv2.cvtColor(r, cv2.COLOR_GRAY2RGB) 

        elif a3:
                 #escala de grises
               r = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
               r = cv2.cvtColor(r, cv2.COLOR_GRAY2RGB)

        elif a4:            
                  #negativo
               r = 255-frame

        elif a5:
                 #suavisa la img
               r = cv2.medianBlur(frame,15) 

        else:                                  
              # r = frame
               pass
        r[h1:y1,w1:x5,:]= frame[h1:y1,w1:x5,:]
        cv2.rectangle(frame,(w1,y1),(x1,h1),(255,0,0), 2)
        cv2.rectangle(frame,(w2,y2),(x2,h2),(0,255,0), 2)
        cv2.rectangle(frame,(w3,y3),(x3,h3),(0,0,255), 2)
        cv2.rectangle(frame,(w4,y4),(x4,h4),(0,255,255), 2)
        cv2.rectangle(frame,(w5,y5),(x5,h5),(55,150,80), 2)
        cv2.rectangle(r,(w1,y1),(x1,h1),(255,0,0), 2)
        cv2.rectangle(r,(w2,y2),(x2,h2),(0,255,0), 2)
        cv2.rectangle(r,(w3,y3),(x3,h3),(0,0,255), 2)
        cv2.rectangle(r,(w4,y4),(x4,h4),(0,255,255), 2)
        cv2.rectangle(r,(w5,y5),(x5,h5),(55,150,80), 2)
        cv2.imshow('frame',r)
        if cv2.waitKey(1) & 0xFF == ord('s'):
          break
    cap.release()
    cv2.destroyAllWindows()

main()