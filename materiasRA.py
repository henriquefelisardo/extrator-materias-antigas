import pdfplumber
import re
import csv
import os

def extrair_dados_pdf(caminho_pdf, caminho_csv):
    """
    Lê um arquivo PDF com o modelo de matrículas deferidas e exporta para CSV.
    """
    # Expressão regular para capturar os 3 grupos:
    # 1. RA: ^(\d+) -> Início da linha, capturando apenas números.
    # 2. Código: ([A-Za-z0-9\-]+) -> Captura letras, números e hifens.
    # 3. Disciplina: (.+)$ -> Captura todo o resto até o final da linha.
    padrao_linha = re.compile(r"^(\d+)\s+([A-Za-z0-9\-]+)\s+(.+)$")
    
    dados_extraidos = []

    print(f"Lendo o arquivo: {caminho_pdf}...")
    
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                
                if not texto:
                    continue
                
                linhas = texto.split('\n')
                for linha in linhas:
                    # Remove espaços em branco nas pontas e tenta aplicar o regex
                    linha_limpa = linha.strip()
                    match = padrao_linha.match(linha_limpa)
                    
                    if match:
                        ra = match.group(1)
                        codigo = match.group(2)
                        disciplina = match.group(3).strip()
                        
                        dados_extraidos.append([ra, codigo, disciplina])
                        
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return

    if not dados_extraidos:
        print("Nenhum dado válido encontrado no PDF.")
        return

    # Escrita do arquivo CSV
    # Utilizando ';' como delimitador para facilitar a abertura direta no Excel em português
    try:
        with open(caminho_csv, mode='w', encoding='utf-8', newline='') as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            
            # Escreve o cabeçalho
            escritor.writerow(['RA', 'Código_Turma', 'Nome_Disciplina'])
            
            # Escreve os dados
            escritor.writerows(dados_extraidos)
            
        print(f"Sucesso! {len(dados_extraidos)} registros foram salvos em: {caminho_csv}")
        
    except Exception as e:
        print(f"Erro ao salvar o CSV: {e}")

# Execução do script
if __name__ == "__main__":
    # Nomes dos arquivos de entrada. Altere conforme necessário.
    arquivos_entrada = [
        "ajuste_2026_2_matriculas_deferidas.pdf",
        "ajuste_2026_1_matriculas_deferidas.pdf"
    ]
    
    for arquivo in arquivos_entrada:
        if os.path.exists(arquivo):
            nome_base = os.path.splitext(arquivo)[0]
            arquivo_saida = f"{nome_base}.csv"
            extrair_dados_pdf(arquivo, arquivo_saida)
        else:
            print(f"Arquivo não encontrado no diretório: {arquivo}")