from ultralytics import YOLO
import cv2
import json
import time

CAMERA_INDEX = 0
MODELO_PATH = r"runs\detect\train4\weights\best.pt"
CM_POR_PIXEL = 1 / 50  

lista_altura = []
lista_largura = []
lista_comprimento = []

while True:
    print("O que deseja medir?")
    print("1 - Altura (visao lateral)")
    print("2 - Comprimento e Largura (visao de cima)")
    print("0 - Sair")
    opcao = input("Digite 1, 2 ou 0: ").strip()


    if opcao == '0':
        break
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
                altura = round(altura_cm, 2)
                medidas_cm['altura_cm'] = altura
                lista_altura.append(altura)
            else:
                largura = round(largura_cm, 2)
                comprimento = round(altura_cm, 2)
                medidas_cm['largura_cm'] = largura
                medidas_cm['comprimento_cm'] = comprimento
                lista_largura.append(largura)
                lista_comprimento.append(comprimento)

            print(f"lista altura: {lista_altura}")
            print(f"lista largura: {lista_largura}")
            print(f"lista comprimento: {lista_comprimento}")
            break  


    cap.release()
    cv2.destroyAllWindows()

    timestamp = int(time.time())
    cv2.imwrite(f"frame_salvo_{timestamp}.png", frame_salvo)

    with open(f"resultado_{timestamp}.json", "w") as f:
        json.dump(medidas_cm, f, indent=4)


    print(f"Saalvo em 'resultado_{timestamp}.json' e 'frame_salvo_{timestamp}.png'")


print(f"altura {lista_altura}")
print(f"comprimento  {lista_comprimento}")
print(f"largura {lista_largura}")

def binary_search(lista, valor):
    esquerda, direita = 0, len(lista) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if lista[meio] == valor:
            return meio
        elif lista[meio] < valor:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1

def buscar_medida(tipo, medida):
    if tipo == 'altura':
        lista = lista_altura
    elif tipo == 'largura':
        lista = lista_largura
    elif tipo == 'comprimento':
        lista = lista_comprimento
    else:
        print("Tipo de medida inválido.")
        return None 

    index = binary_search(sorted(lista), medida)

    if index != -1:
        print(f"{tipo.capitalize()} de {medida} encontrado na posicao {index + 1} da lista.")
    else:
        print(f"{tipo.capitalize()} de {medida} nao encontrado na lista.")




print("Lista de altura ordenada", sorted(lista_altura))
print("Lista de largura ordenada", sorted(lista_largura))
print("Lista de comprimento, ordenada", sorted(lista_comprimento))



if not lista_altura and not lista_largura and not lista_comprimento:
    print("Nenhuma medida foi salva.")
else:
    a = input("Digite o tipo de medida a ser buscado: ")
    b = float(input("Digite o valor da medida a ser buscado: "))
    buscar_medida(a, b)