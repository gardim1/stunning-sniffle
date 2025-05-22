from ultralytics import YOLO
import cv2
import json
from datetime import datetime

def capturar_medida(tipo, model, cap, cm_por_pixel=0.0927):
    print(f"Aguardando detecção para medir {tipo}... Pressione 'q' para capturar.")
    medida = None

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

            largura_cm = largura_px * cm_por_pixel
            altura_cm = altura_px * cm_por_pixel

            if tipo == 'altura':
                valor = altura_cm
                cv2.putText(annotated, f"Altura: {valor:.1f} cm", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                valor = (largura_cm, altura_cm)
                cv2.putText(annotated, f"{largura_cm:.1f} x {altura_cm:.1f} cm", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow('Medindo...', annotated)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                frame_salvo = frame.copy()
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                cv2.imwrite(f"frame_{tipo}_{timestamp}.png", frame_salvo)
                print(f"Imagem salva: frame_{tipo}_{timestamp}.png")
                medida = valor
                break
        else:
            cv2.imshow('Medindo...', annotated)

    return medida

def medir_com_menu():
    cpf = input("Digite o CPF da pessoa: ").strip()
    nome_tecido = input("Digite o nome do tecido: ").strip()
    modelo = YOLO(r"runs\detect\train4\weights\best.pt")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise Exception("Erro: câmera não pode ser aberta.")

    medidas = {
        "cpf": cpf,
        "data_medicao": datetime.now().isoformat(),
        "nome_tecido": nome_tecido
    }

    while True:
        print("\nO que deseja medir?")
        print("1 - Altura (visão lateral)")
        print("2 - Comprimento e Largura (visão de cima)")
        print("0 - Finalizar e salvar")

        opcao = input("Digite 1, 2 ou 0: ").strip()

        if opcao == '0':
            break
        elif opcao == '1':
            altura = capturar_medida('altura', modelo, cap)
            if altura:
                medidas['altura_cm'] = round(altura, 2)
        elif opcao == '2':
            largura, comprimento = capturar_medida('largura_comprimento', modelo, cap)
            medidas['largura_cm'] = round(largura, 2)
            medidas['comprimento_cm'] = round(comprimento, 2)
        else:
            print("Opção inválida.")

    cap.release()
    cv2.destroyAllWindows()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f"medidas_{cpf}_{timestamp}.json", "w") as f:
        json.dump(medidas, f, indent=4)

    print(f"\nMedições salvas em: medidas_{cpf}_{timestamp}.json")
    print(json.dumps(medidas, indent=4))

if __name__ == "__main__":
    medir_com_menu()
