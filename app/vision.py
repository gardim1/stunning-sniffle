from ultralytics import YOLO
import cv2
from datetime import datetime
from pathlib import Path

MODEL = YOLO("runs/detect/train4/weights/best.pt")

FRAMES_DIR = Path(__file__).resolve().parent.parent / "data" / "frames"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

def capturar_medida(tipo: str, cm_por_pixel: float = 0.0927) -> dict | None:
    """
    Abre a câmera 0, mostra janela, pressiona 'q' → mede e sai.
    Retorna dict com medidas ou None se falhar.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: câmera não pode ser aberta.")
        return None

    print(f"Aguardando detecção para medir {tipo}... Pressione 'q' para capturar ou sair.")
    medidas_dict = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame.")
            break

        results = MODEL.predict(source=frame, imgsz=640, conf=0.25, device='0')
        annotated = results[0].plot()
        boxes = results[0].boxes.xyxy.cpu().numpy()

        if len(boxes) > 0:
            x1, y1, x2, y2 = map(int, boxes[0][:4])
            larg_px, alt_px = x2 - x1, y2 - y1
            larg_cm, alt_cm = larg_px * cm_por_pixel, alt_px * cm_por_pixel

            if tipo == 'altura':
                medidas_dict = {'altura_cm': round(alt_cm, 2)}
                txt = f"Altura: {alt_cm:.1f} cm"
            else:
                medidas_dict = {
                    'largura_cm': round(larg_cm, 2),
                    'comprimento_cm': round(alt_cm, 2)
                }
                txt = f"{larg_cm:.1f} x {alt_cm:.1f} cm"

            cv2.putText(annotated, txt, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('Medindo...', annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            if medidas_dict:
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                cv2.imwrite(str(FRAMES_DIR / f"frame_{tipo}_{ts}.png"), frame)
            break

    cap.release()
    cv2.destroyAllWindows()
    return medidas_dict
