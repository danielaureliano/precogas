import pkg_resources
import sys
import os

def check_dependencies():
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print(f"{req_file} não encontrado.")
        sys.exit(0) # Não falha se não tiver arquivo

    try:
        with open(req_file, "r") as f:
            # Extrai apenas o nome do pacote, ignorando versões e comentários
            requirements = []
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Pega o nome antes de qualquer operador de versão
                name = line.split("==")[0].split(">=")[0].split("<")[0].split("~=")[0].strip()
                requirements.append(name)

        installed = {pkg.key for pkg in pkg_resources.working_set}
        # Compara em lowercase
        missing = [req for req in requirements if req.lower() not in installed]

        if missing:
            print(f"ERRO: Dependências listadas em {req_file} não estão instaladas no ambiente atual:")
            print(f"  {', '.join(missing)}")
            print("Execute: pip install -r requirements.txt")
            sys.exit(1)

        print("Verificação de dependências: OK (Todas instaladas)")
        sys.exit(0)
    except Exception as e:
        print(f"Erro ao verificar dependências: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_dependencies()
