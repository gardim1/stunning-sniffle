from ultralytics import YOLO
import cv2
import json
import time

CAMERA_INDEX = 0
MODELO_PATH = r"runs\detect\train4\weights\best.pt"
CM_POR_PIXEL = 1 / 50  

print("O que deseja medir?")
print("1 - Altura (visao lateral)")
print("2 - Comprimento e Largura (visao de cima)")
opcao = input("Digite 1 ou 2: ").strip()

if opcao not in ['1', '2']:
    print(" Opcao invalida.")
    exit()

model = YOLO(MODELO_PATH)
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print(" Erro: camera nao pode ser aberta.")
    exit()

print("Pressione 'q' para capturar o frame final e sair...")

frame_salvo = None
medidas_cm = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame.")
        break

    results = model.predict(source=frame, imgsz=640, conf=0.25, device='0')
    annotated = results[0].plot()

    boxes = results[0].boxes.xyxy.cpu().numpy()
    if len(boxes) > 0:
        x1, y1, x2, y2 = map(int, boxes[0][:4]) 
        largura_px = x2 - x1
        altura_px = y2 - y1

        largura_cm = largura_px * CM_POR_PIXEL
        altura_cm = altura_px * CM_POR_PIXEL

        if opcao == '1':
            print(f"📏 Altura: {altura_cm:.2f} cm")
            cv2.putText(annotated, f"Altura: {altura_cm:.1f} cm", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            print(f"📏 Largura: {largura_cm:.2f} cm | Comprimento: {altura_cm:.2f} cm")
            cv2.putText(annotated, f"{largura_cm:.1f} x {altura_cm:.1f} cm", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow('Medindo...', annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        frame_salvo = frame.copy()
        if opcao == '1':
            medidas_cm['altura_cm'] = round(altura_cm, 2)
        else:
            medidas_cm['largura_cm'] = round(largura_cm, 2)
            medidas_cm['comprimento_cm'] = round(altura_cm, 2)
        break

cap.release()
cv2.destroyAllWindows()

timestamp = int(time.time())
cv2.imwrite(f"frame_salvo_{timestamp}.png", frame_salvo)

with open(f"resultado_{timestamp}.json", "w") as f:
    json.dump(medidas_cm, f, indent=4)

print(f"Saalvo em 'resultado_{timestamp}.json' e 'frame_salvo_{timestamp}.png'")
