from fastapi import FastAPI, HTTPException
from typing import List
import glob
#import os
import json

app = FastAPI(title="API de Medidas", description="API para capturar e armazenar medidas de pessoas", version="1.0")

@app.get("/medidas/{cpf}")
async def obter_medidas(cpf: str):
    padrao_arquivo = f"medidas_{cpf}_*.json"
    arquivos = glob.glob(padrao_arquivo)

    if not arquivos:
        raise HTTPException(status_code=404, detail="Nenhum arquivo encontrado para o CPF fornecido.")
    

    medidas = []
    for arquivo in arquivos:
        try:
            with open(arquivo, "r") as f:
                dados = json.load(f)
                medidas.append(dados)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao ler o arquivo {arquivo}: {str(e)}")
        

    return{
        "cpf": cpf,
        "total_medidas_paciente": len(medidas),
        "medidas": medidas
    }
    
