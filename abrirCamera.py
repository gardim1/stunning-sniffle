from ultralytics import YOLO
import cv2

CAMERA_INDEX = 0
MODELO_PATH = r"runs\detect\train4\weights\best.pt"
CM_POR_PIXEL = 1 / 50  

model = YOLO(MODELO_PATH)
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("Erro: Nao foi possível abrir a camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro: Nao foi possível capturar o frame.")
        break

    results = model.predict(source=frame, imgsz=640, conf=0.25, device='0')
    annotated = results[0].plot()

    boxes = results[0].boxes.xyxy.cpu().numpy()
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box[:4])
        largura_px = x2 - x1
        altura_px = y2 - y1

        largura_cm = largura_px * CM_POR_PIXEL
        altura_cm = altura_px * CM_POR_PIXEL

        print(f"[{i}] 📏 Largura: {largura_cm:.2f} cm | Altura: {altura_cm:.2f} cm")

        cv2.putText(
            annotated,
            f"{largura_cm:.1f} x {altura_cm:.1f} cm",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    cv2.imshow('Camera', annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
