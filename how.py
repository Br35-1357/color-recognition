#Bibliotecas
import cv2
import numpy as np
import time

#1. Obtener imagen de camara
#Indice de la camara a usar. Usualmente es 0
cap = cv2.VideoCapture(0)

#Crear txt de historial
file1 = open("History.txt","a+") 

print("commands:")

print("start, info, exit")

while(True):
    bootup = input("Insert command: ")
    if bootup == "start":
        start = input("Start the program(y/n): ")
        if start == "y":
            hora = time.ctime()
            file1.write(hora)
            file1.write(": ")
            file1.write("\n")
            print(time.ctime())
            print("\n")
            time.sleep(2)
            print("You can stop the program by pressing the key: q")
            print("\n")
            time.sleep(2)
            print("The color detection might not work properly if the ambient illumination is too bright or too dark.")
            print("\n")
            time.sleep(2)
            print("Starting program...")
            print("\n")
            time.sleep(2)
            
            while(True):
                # Capturar cuadro a cuadro o frame a frame
                ret, frame = cap.read()
                #En caso no se haya podido capturar correctamente, terminamos el bucle
                if not ret:
                    break

                #2. Recortar la imagen en la zona que nos interesa (Ajustar la zona)
                #Obtenemos dimensiones de la imagen
                camara_alto, camara_ancho, camara_colores = frame.shape
                #Definimos tamano de la zona que nos interesa
                zona_recorte = 180
                #Calculamos el inicio de la zona de recorte
                x = int ( (camara_ancho/2) - (zona_recorte/2) )
                y = int ( (camara_alto/2) - (zona_recorte/2) )
                #Obtenemos zona de recorte
                recorte = frame[y:y+zona_recorte,x:x+zona_recorte]

                #3. Filtrado por Colores
                #Obtener la imagen en HSV para detectar colores
                hsv = cv2.cvtColor(recorte, cv2.COLOR_BGR2HSV)

                #Definimos el rango para todos los colores
                rojo_bajo = np.array([0,100,100])
                rojo_alto = np.array([8,255,255])
                
                azul_bajo = np.array([100,100,100])
                azul_alto = np.array([130,255,255])
                
                verde_bajo = np.array([40,100,100])
                verde_alto = np.array([80,255,255])
                
                amarillo_bajo = np.array([27,150,100])
                amarillo_alto = np.array([32,255,255])
                
                anaranjado_bajo = np.array([11,100,100])
                anaranjado_alto = np.array([20,255,255])
                
                rosa_bajo = np.array([148,100,100])
                rosa_alto = np.array([160,255,255])
                
                negro_bajo = np.array([0,0,0])
                negro_alto = np.array([255,35,100])
                
               

                #Obtenemos los filtros/mascara
                rojo_mascara = cv2.inRange(hsv,rojo_bajo,rojo_alto)
                azul_mascara = cv2.inRange(hsv,azul_bajo,azul_alto)
                verde_mascara = cv2.inRange(hsv,verde_bajo,verde_alto)
                amarillo_mascara = cv2.inRange(hsv,amarillo_bajo,amarillo_alto)
                anaranjado_mascara = cv2.inRange(hsv,anaranjado_bajo,anaranjado_alto)
                rosa_mascara = cv2.inRange(hsv,rosa_bajo,rosa_alto)
                negro_mascara = cv2.inRange(hsv,negro_bajo,negro_alto)
                #

                #Por cada mascara debemos asignarle un peso
                rojo_peso = cv2.countNonZero(rojo_mascara)
                azul_peso = cv2.countNonZero(azul_mascara)
                verde_peso = cv2.countNonZero(verde_mascara)
                amarillo_peso = cv2.countNonZero(amarillo_mascara)
                anaranjado_peso = cv2.countNonZero(anaranjado_mascara)
                rosa_peso = cv2.countNonZero(rosa_mascara)
                negro_peso = cv2.countNonZero(negro_mascara)
                #rojo_peso, azul_peso, ....


                #4. Identificar el color predominante
                color = None
                if rojo_peso > 250: #and rojo_peso > azul_peso > verde_peso > amarillo_peso > anaranjado_peso > negro_peso:
                    color = "ROJO"
                elif azul_peso > 250: #and azul_peso > rojo_peso > verde_peso > amarillo_peso > anaranjado_peso > negro_peso:
                    color = "AZUL"
                elif verde_peso > 250: #and verde_peso > rojo_peso > azul_peso > amarillo_peso > anaranjado_peso > negro_peso:
                    color = "VERDE"
                elif amarillo_peso > 250: #and amarillo_peso > rojo_peso > azul_peso > verde_peso > anaranjado_peso > negro_peso:
                    color = "AMARILLO"
                elif anaranjado_peso > 250: #and anaranjado_peso > rojo_peso > azul_peso > verde_peso > amarillo_peso > negro_peso:
                    color = "ANARANJADO"
                elif rosa_peso > 250:
                    color = "ROSADO"
                #elif negro_peso > 250: #and negro_peso > rojo_peso > azul_peso > verde_peso > amarillo_peso > anaranjado_peso:
                #    color = "NEGRO"
                else:
                    color = "NEUTRAL"


                #5. Mostramos el color predominante
                #Dibujar un recuadro en la zona que estamos identificando
                punto_inicial = (x,y)
                punto_final = (x+zona_recorte,y+zona_recorte)
                color_blanco = (255,255,255)

                cv2.rectangle(frame, punto_inicial , punto_final, color_blanco, 2 )

                #Preparar Texto
                texto_fuente = cv2.FONT_HERSHEY_SIMPLEX
                texto_inicio = (x,y+zona_recorte+30)
                texto_tamano = 0.75
                texto_color = (255,255,255)

                #Escribir Texto
                if color == "ROJO":
                    print("El color identificado es ROJO")
                    cv2.putText(frame, "COLOR ROJO", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)

                elif color == "VERDE":
                    print("El color identificado es VERDE")
                    cv2.putText(frame, "COLOR VERDE", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)
                    
                elif color == "AZUL":
                    print("El color identificado es AZUL")
                    cv2.putText(frame, "COLOR AZUL", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)
                    
                elif color == "AMARILLO":
                    print("El color identificado es AMARILLO")
                    cv2.putText(frame, "COLOR AMARILLO", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)
                    
                elif color == "ANARANJADO":
                    print("El color identificado es ANARANJADO")
                    cv2.putText(frame, "COLOR ANARANJADO", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)
                    
                elif color == "NEGRO":
                    print("El color identificado es NEGRO")
                    cv2.putText(frame, "COLOR NEGRO", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)
                    
                elif color == "ROSADO":
                    print("El color identificado es Rosado")
                    cv2.putText(frame, "COLOR ROSADO", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)
                    
                else:
                    print("No se ha identificado el color")
                    cv2.putText(frame, "Colocar objeto", texto_inicio, texto_fuente, texto_tamano, texto_color, 2)
                    

                #Guardamos los datos
                file1.write(color) 
                file1.write("\n")


                # Mostramos el frame capturado
                cv2.imshow('Identificador de Color',frame)
                #cv2.imshow('Transformacion',rojo_mascara)
                #cv2.imshow('Transformacion',azul_mascara)
                #cv2.imshow('Transformacion',amarillo_mascara)
                #cv2.imshow('Transformacion',anaranjado_mascara)
                #cv2.imshow('Transformacion',verde_mascara)
                #cv2.imshow('Transformacion',negro_mascara)
                
                #if cv2.waitKey(1) & 0xFF == ord('r'):
                 #   cv2.imshow('Transformacion',rojo_mascara)
                
                #El bucle se seguira ejecutando hasta que presionemos la tecla 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    time.sleep(3)
                    print("The detection frame may freeze, however you can still using the console")
                    break

        if start == "n":
            break

    if bootup == "info":
        file1.read()
        print(file1)
        #with open("History.txt") as fobj:
         #   bio = fobj.read()
        #print(bio)
        
    if bootup == "exit":
        break

        # Antes de finalizar el programa, liberamos la camara
cap.release()
cv2.destroyAllWindows()
