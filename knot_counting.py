#!/usr/bin/env python3

def knot_count(tree):
    """
    Função recursiva que conta o número total de nós na árvore.
    
    Parâmetros:
        tree (dict): Representação da árvore em forma de dicionário.
    
    Retorno:
        int: Número total de nós na árvore.
    """
    # Inicializa a contagem com 1 para incluir o nó atual.
    total_knots = 1
    
    # Para cada filho no dicionário (subárvore), chama a função recursivamente.
    for subtree in tree.values():
        total_knots += knot_count(subtree)
    
    return total_knots

def main():
    """
    Função principal do programa.
    Lê o arquivo de entrada contendo a árvore, processa a contagem de nós e exibe o resultado.
    """
    import json  # Importa o módulo para manipulação de dados no formato JSON.

    # Solicita o nome do arquivo ao usuário.
    arquivo_txt = input("Digite o nome do arquivo contendo a árvore: ")
    
    try:
        # Abre o arquivo no modo leitura.
        with open(arquivo_txt, 'r') as arquivo:
            # Lê o conteúdo do arquivo e converte de JSON para um dicionário Python.
            tree = json.load(arquivo)
        
        # Chama a função knot_count para calcular o total de nós.
        total = knot_count(tree)
        
        # Exibe o total de nós na árvore.
        print(f"O número total de nós na árvore é: {total}")
    
    except FileNotFoundError:
        # Caso o arquivo não seja encontrado, exibe uma mensagem de erro.
        print("Erro: Arquivo não encontrado. Verifique o nome e tente novamente.")
    
    except json.JSONDecodeError:
        # Caso o arquivo não seja um JSON válido, exibe uma mensagem de erro.
        print("Erro: O arquivo não está no formato esperado (JSON).")

# Ponto de entrada do programa.
if __name__ == "__main__":
    main()
