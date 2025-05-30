# Sprint Dynamic Programming – Dimensionamento Automático de Amostras Patológicas

## Documento de Envoltória

### Identificação do Grupo  
| Nome | RM | 
|------|----|
| Camila Feitosa | 558808 |
| Gabriel Miranda | 559102 | 
| Gustavo Berlanga | 555298 |
| Leonardo Taschin | 554583 |
| Vinicius Gardim | 556013 |

### Resumo Executivo  
Este projeto entrega um sistema em **Python** capaz de medir automaticamente amostras de tecido patológico usando visão computacional (YOLOv8). O operador aponta a webcam para a amostra, pressiona **q** e o sistema devolve altura, largura e comprimento em centímetros, salvando um arquivo JSON associado ao CPF do paciente e expondo esses dados via API **FastAPI**.

---  
## Hipóteses e Dados Considerados
* **Câmera fixa** a 44 cm da bancada; ângulo perpendicular (top‑down) para largura × comprimento e lateral a 90 ° para altura.  
* **Fator de calibração**: 0.0927 mm / pixel (obtido empiricamente).  
* **Modelo YOLO** treinado apenas para a classe **mouse** na pasta `runs/detect/train4/weights/best.pt`; toda detecção é assumida como amostra.  
* Iluminação ambiente controlada; contraste suficiente para segmentação.  
* Amostras cabem integralmente no frame (≤ 20 cm).  

---  
## Estrutura & Documentação de Código

| Arquivo | Responsabilidade | DP / Algoritmos |
|---------|------------------|-----------------|
| `app/main.py` | Menu CLI; orquestra medições. | – |
| `app/vision.py` | Captura webcam, YOLO + cálculo cm. | Conversão pixels→mm; uso do *cache* implícito em fator fixo |
| `app/repository.py` | Lista ordenada por timestamp + persistência JSON. | `bisect.insort` **O(log n)**, memoização `pixels_to_mm` **O(1)** |
| `app/api_medidas.py` | Endpoint `GET /medidas/{cpf}`. | – |
| `utils/conversions.py` | `@lru_cache` pixels→mm. | Memoização (DP) |

---  

## Passos para Execução

```bash
# 1. instalar dependências
python -m venv .venv && source .venv/bin/activate (linux)
python -m venv venv && python venv/Scripts/activate (Windows)
pip install -r requirements.txt

# 2. medir uma amostra
python -m app.main

# 3. servir API
uvicorn app.api_medidas:app --reload
#utilizar endpoint /docs
#ex: http://127.0.0.1:8000/docs
```

---

## Código Operacional

Todos os scripts foram testados em:
* **Windows 11 + Python 3.11 + GPU RTX 4060**  
* **Ubuntu 22.04 + Python 3.10**

Arquivos de saída:
* JSONs salvos em `data/medidas/`
* Frames de auditoria em `data/frames/`


