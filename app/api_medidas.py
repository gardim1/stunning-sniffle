from fastapi import FastAPI, HTTPException
from .repository import load_samples_from_disk

app = FastAPI(title="API de Medidas de Tecidos")

@app.get("/medidas/{cpf}")
def get_medidas(cpf: str):
    dados = load_samples_from_disk(cpf)
    if not dados:
        raise HTTPException(status_code=404, detail="CPF sem medições")
    return {"cpf": cpf, "total_medidas": len(dados), "medidas": dados}
