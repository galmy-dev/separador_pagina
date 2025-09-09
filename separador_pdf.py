import os
import re
from pypdf import PdfReader, PdfWriter

def encontrar_email(texto):
    """
    Usa uma expressão regular para encontrar o primeiro endereço de e-mail válido no texto.
    """
    # Expressão regular para encontrar e-mails
    padrao_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    match = re.search(padrao_email, texto)
    if match:
        return match.group(0) # Retorna o primeiro e-mail encontrado
    return None

def separar_pdf(arquivo_entrada):
    """
    Função principal que separa o PDF de 2 em 2 páginas.
    """
    # Verifica se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
        return

    # Cria uma pasta para salvar os arquivos separados, se ela não existir
    pasta_saida = "documentos_separados"
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"Pasta '{pasta_saida}' criada para salvar os arquivos.")

    try:
        leitor_pdf = PdfReader(arquivo_entrada)
        total_paginas = len(leitor_pdf.pages)
        print(f"O documento tem {total_paginas} páginas. Iniciando o processo...")

        # Itera sobre o documento de 2 em 2 páginas
        for i in range(0, total_paginas, 2):
            escritor_pdf = PdfWriter()
            
            # Extrai o texto das duas páginas do bloco
            texto_bloco = ""
            if i < total_paginas:
                texto_bloco += leitor_pdf.pages[i].extract_text() or ""
            if (i + 1) < total_paginas:
                texto_bloco += leitor_pdf.pages[i+1].extract_text() or ""

            # Encontra o e-mail no texto extraído
            email_encontrado = encontrar_email(texto_bloco)
            
            # Define o nome do arquivo de saída
            if email_encontrado:
                # Substitui caracteres inválidos no nome do arquivo
                nome_arquivo_limpo = re.sub(r'[\\/*?:"<>|]', "_", email_encontrado)
                nome_arquivo_saida = f"{nome_arquivo_limpo}.pdf"
            else:
                # Caso nenhum e-mail seja encontrado no bloco
                nome_arquivo_saida = f"sem_email_paginas_{i+1}-{i+2}.pdf"
                print(f"AVISO: Nenhum e-mail encontrado nas páginas {i+1}-{i+2}. Salvando como '{nome_arquivo_saida}'.")

            caminho_completo_saida = os.path.join(pasta_saida, nome_arquivo_saida)
            
            # Adiciona as páginas ao novo arquivo PDF
            escritor_pdf.add_page(leitor_pdf.pages[i])
            if (i + 1) < total_paginas:
                escritor_pdf.add_page(leitor_pdf.pages[i+1])
            
            # Salva o novo arquivo PDF
            with open(caminho_completo_saida, "wb") as f_saida:
                escritor_pdf.write(f_saida)
            
            print(f"Salvo: '{caminho_completo_saida}' (Páginas {i+1} e {i+2})")

        print("\nProcesso concluído com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")


# --- PONTO DE ATENÇÃO ---
# Altere o nome do arquivo abaixo para o nome do seu PDF
NOME_DO_SEU_ARQUIVO_PDF = "TodosEmail.pdf"
separar_pdf(NOME_DO_SEU_ARQUIVO_PDF)