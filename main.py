import math
import cv2
import mediapipe as mp
import os  # Para rodar comandos do sistema

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
def calculate_distance(landmark1, landmark2):
    # Distância euclidiana entre dois pontos 3D
    return math.sqrt((landmark1.x - landmark2.x) ** 2 + 
                     (landmark1.y - landmark2.y) ** 2 + 
                     (landmark1.z - landmark2.z) ** 2)

while cap.isOpened():
    success, image = cap.read(0)
    if not success:
        continue
    
    # Pega a imagem da camera
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Trata na foto para ficar facil da biblioteca funciona
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Verifica se achou alguma mao
    if results.multi_hand_landmarks:
        # Roda em todas as mãos
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenhar as landmarks da mão
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Obter as landmarks do polegar e do indicador
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Calcular a distância euclidiana entre os dois pontos
            distance = calculate_distance(thumb_tip, index_finger_tip)
            
            # Definir um limite para determinar o toque
            if distance < 0.02:  # Ajuste este valor para melhorar a sensibilidade
                print("toquei")
                os.system("")  # Simula clique do mouse no Linux
            
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# Adicionar area de usuario para detecção