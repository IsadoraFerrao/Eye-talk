from turtle import left, width
import cv2
import numpy as np
import dlib 
from math import hypot
import gtts
from playsound import playsound


#Codigo para abertura de camera

cap = cv2.VideoCapture(0) #0 para a webcam do pc
board = np.zeros((500, 500), np.uint8)
board[:] = 255

#codigo para deteccao da face
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#teclado
keyboard = np.zeros((600,1000,3),np.uint8) #tamanho do teclado
#Keyboard setting 
keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",
              5: "A", 6: "S", 7: "D", 8: "F", 9: "G",
              10: "Z", 11: "X", 12: "C", 13: "V", 14: "<"}

keys_set_2 = {0: "Y", 1: "U", 2: "I", 3: "O", 4: "P",
              5: "H", 6: "J", 7: "K", 8: "L", 9: "_",
              10: "V", 11: "B", 12: "N", 13: "M", 14: "<"}
def letter(letter_index, text, letter_light):
    #chaves

    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 200
        y = 0
    elif letter_index == 2:
        x = 400
        y = 0
    elif letter_index == 3:
        x = 600
        y = 0
    elif letter_index == 4:
        x = 800
        y = 0
    elif letter_index == 5:
        x = 0
        y = 200
    elif letter_index == 6:
        x = 200
        y = 200
    elif letter_index == 7:
        x = 400
        y = 200
    elif letter_index == 8:
        x = 600
        y = 200
    elif letter_index == 9:
        x = 800
        y = 200
    elif letter_index == 10:
        x = 0
        y = 400
    elif letter_index == 11:
        x = 200
        y = 400
    elif letter_index == 12:
        x = 400
        y = 400
    elif letter_index == 13:
        x = 600
        y = 400
    elif letter_index == 14:
        x = 800
        y = 400
        
    width = 200
    height = 200
    th = 3

    if letter_light is True:
        cv2.rectangle(keyboard, (x+th,y+th), (x+width-th, y+height-th), (135,206,250), -1) #pintando o fundo das teclas
    else:
        cv2.rectangle(keyboard, (x+th,y+th), (x+width-th, y+height-th), (0, 0, 0), th) #desenhando as linhas das teclas


    # configuracoes do teclado
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize("A", font_letter, font_scale, font_th)[0]
    with_text, height_text = text_size[0], text_size[1]

    #centralizando as letras
    text_x = int((width - with_text)/2)+x
    text_y = int((height + height_text)/2)+y

    cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (0, 0, 0), 4)
    #cv2.rectangle(keyboard, (200+th,0+th), (200+width-th, 0+height-th), (255, 0, 0), th) #desenhando as teclas

def draw_menu():
    rows, cols, _ = keyboard.shape
    th_lines = 4 # thickness lines
    cv2.line(keyboard, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
             (51, 51, 51), th_lines)
    cv2.putText(keyboard, "Esquerdo", (80, 300), font, 4, (0, 0, 0), 5)
    cv2.putText(keyboard, "Direito", (80 + int(cols/2), 300), font, 4, (0, 0, 0), 5)


#codigo pra deteccao do meio do olho

def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye

def midpoint(p1,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y) #ponto do olho esquerdo no lado esquerdo
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y) #ponto do olho esquerdo no ponto direito
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    
    
    #hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2) #linha na detecção do olho
    #ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2) #linha na detecção do olho
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1])) #responsividade horizontal
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1])) #responsividade vertical
    #print(hor_line_lenght/ver_line_lenght)
    ratio = hor_line_lenght/ ver_line_lenght
    return ratio

def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
    
    
    #cv2.polylines(frame, [left_eye_region], True, (0,0,255), 2) #definicao do que tem dentro do olho
    #print(left_eye_region)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)
    
    
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y= np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y:max_y, min_x:max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape 
    left_side_threshold =  threshold_eye[0: height, 0: int(width/2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    
    right_side_threshold =  threshold_eye[0: height, int(width/2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)
    
    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:       
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

frames = 0
letter_index = 0
blinking_frames = 0
frames_to_blink = 6
frames_active_letter = 9


text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
selected_keyboard_menu = True
keyboard_selection_frames = 0

    
while True:
    _, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    rows,cols,_ = frame.shape
    keyboard[:] = (255,255,255)
    #keyboard[:] = (26,26,26)
    frames +=1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convertendo as cores para gray scale
    
    
    frame[rows - 50: rows, 0:cols] = (255,255,255) #camera
    
    #new_frame = np.zeros((500,500,3), np.uint8)
    
    #espaco da escrita
    
    if selected_keyboard_menu is True:
        draw_menu()
    
    if keyboard_selected == "left":
        keys_set = keys_set_1
    else:
        keys_set = keys_set_2
    
    active_letter = keys_set[letter_index]
   
    #fase de deteccao
    faces = detector(gray)

    #for pra pegar todas as faces
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x,y), (x1,y1), (0, 255, 0), 2) #pegando o retangulo do rosto
        #print(face)
                
        landmarks = predictor(gray, face)
        left_eye,right_eye = eyes_contour_points(landmarks)
        
        #Detect Blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
        
        # Eyes color
        #right now colo red around eyes cause we are not blinking them
        #cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
        #cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)
        
        if selected_keyboard_menu is True:
            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
            
            if gaze_ratio <= 0.9:
                keyboard_selected = "right"
                #frase = gtts.gTTS(keyboard_selected,lang='pt-br')
                #frase.save('frase.mp3')
                #playsound('frase.mp3')
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 15:
                    selected_keyboard_menu = False
                    frames = 0
                    keyboard_selection_frames = 0
                    if last_keyboard_selected != keyboard_selected:
                        last_keyboard_selected = keyboard_selected
                        keyboard_selection_frames = 0
            else:
                keyboard_selected = "left"
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 15:
                    selected_keyboard_menu = False
                    frames = 0
                    if last_keyboard_selected != keyboard_selected:
                        last_keyboard_selected = keyboard_selected
                        keyboard_selection_frames = 0
        else:
            if blinking_ratio>5:
                #cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0),thickness = 3)
                blinking_frames = blinking_frames + 1
                frames = frames -1
                
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)
                
                if blinking_frames == frames_to_blink:
                    if active_letter != "<" and active_letter != "_":
                        text += active_letter
                    if active_letter == "_":
                        text += " "
                    selected_keyboard_menu = True
                    
            else:
                blinking_frames = 0   

    # Letras do teclado
    
 
    #Display letters on the keyboard            
    if selected_keyboard_menu is False:
        if frames == frames_active_letter:
            letter_index += 1
            frames = 0
        if letter_index == 15:
            letter_index = 0
        for i in range(15):
            if i == letter_index:
                light = True
            else:
                light = False
            letter(i, keys_set[i], light)
    
    
    
    cv2.putText(board, text, (80, 100), font, 9, 0, 3)
    percentage_blinking = blinking_frames / frames_to_blink
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)
    
    #cv2.imshow("Camera", frame)
    cv2.imshow("Eye talk", keyboard)
    cv2.imshow("Texto", board)    

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()