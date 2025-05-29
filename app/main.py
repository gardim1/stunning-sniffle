import json
from datetime import datetime
from .vision import capturar_medida
from .repository import add_sample, persist_sample

def main():
    cpf    = input("CPF: ").strip()
    tecido = input("Nome do tecido: ").strip()

    sample = {
        "cpf": cpf,
        "data_medicao": datetime.now().isoformat(timespec="seconds"),
        "nome_tecido": tecido
    }

    while True:
        print("\n1-Altura | 2-Largura x Comprimento | 0-Salvar e sair")
        op = input("> ").strip()

        if op == '0':
            break
        elif op == '1':
            med = capturar_medida('altura')
            if med: sample.update(med)
        elif op == '2':
            med = capturar_medida('largura_comprimento')
            if med: sample.update(med)
        else:
            print("Opção inválida.")

    if len(sample) > 3:
        add_sample(cpf, sample)
        persist_sample(cpf, sample)
        print(json.dumps(sample, indent=4))
    else:
        print("Nenhuma medição registrada.")

if __name__ == "__main__":
    main()
