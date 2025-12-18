import matplotlib.pyplot as plt
import random
import re

class MaquinaDeTuring:
    def __init__(self):
        self.passos = 0
        self.fita = []

    def resetar_passos(self):
        self.passos = 0

    def carregar_fita(self, palavra):
        self.fita = list(palavra)

    def restaurar_fita(self, palavra_original):
        custo = len(palavra_original) * 2 
        self.passos += custo
        self.fita = list(palavra_original)

    def verificar_igualdade(self, char1, char2, ignorar_char):
        """
        Verifica se a quantidade de char1 é igual a char2, ignorando ignorar_char.
        Simula o vai-e-vem da cabeça de leitura.
        """
        fita = self.fita
        n = len(fita)

        while True:
            idx1 = -1
            for i in range(n):
                self.passos += 1 
                if fita[i] == char1:
                    idx1 = i
                    break
            
            if idx1 == -1:
                for j in range(n):
                    self.passos += 1
                    if fita[j] == char2:
                        return False
                return True

            fita[idx1] = 'X'

            encontrou_c2 = False
            for k in range(idx1 + 1, n):
                self.passos += 1
                if fita[k] == char2:
                    fita[k] = 'Y' 
                    encontrou_c2 = True
                    break
            
            if not encontrou_c2:
                return False

    def processar(self, palavra):
        self.resetar_passos()

        if not re.fullmatch(r'a*b*c*', palavra):
            self.passos += len(palavra)
            return False, self.passos

        self.carregar_fita(palavra)
        if self.verificar_igualdade('a', 'b', 'c'):
            return True, self.passos
        
        self.restaurar_fita(palavra)

        if self.verificar_igualdade('a', 'c', 'b'):
            return True, self.passos

        self.restaurar_fita(palavra)

        if self.verificar_igualdade('b', 'c', 'a'):
            return True, self.passos

        return False, self.passos

def gerar_casos_teste_controlados(qtd_por_tamanho, tamanho_max):
    todos_casos = []
    
    print(f"Gerando casos de teste de tamanho 1 a {tamanho_max}...")
    
    for tam in range(1, tamanho_max + 1):
        casos_do_tamanho = []
        
        while len(casos_do_tamanho) < qtd_por_tamanho:
            tipo = random.choice([1, 2, 3])
            
            if tipo == 1:
                max_i = tam // 2
                if max_i < 1: i = 0
                else: i = random.randint(0, max_i)
                j = i
                k = tam - i - j
            elif tipo == 2:
                max_i = tam // 2
                if max_i < 1: i = 0
                else: i = random.randint(0, max_i)
                k = i
                j = tam - i - k
            else:
                max_j = tam // 2
                if max_j < 1: j = 0
                else: j = random.randint(0, max_j)
                k = j
                i = tam - j - k
            
            if i + j + k == tam:
                palavra = 'a'*i + 'b'*j + 'c'*k
                casos_do_tamanho.append(palavra)
        
        todos_casos.extend(casos_do_tamanho)
        
        if tam % 100 == 0:
            print(f"Gerados casos até tamanho {tam}...")

    return todos_casos

def main():
    TAMANHO_MAX = 1000
    QTD_POR_TAMANHO = 50
    
    mt = MaquinaDeTuring()
    entradas = gerar_casos_teste_controlados(QTD_POR_TAMANHO, TAMANHO_MAX)
    
    dados_aceitos_por_tam = {}

    print("\nProcessando palavras na Máquina de Turing...")
    total_palavras = len(entradas)
    
    for idx, palavra in enumerate(entradas):
        aceita, passos = mt.processar(palavra)
        
        if aceita:
            tam = len(palavra)
            if tam not in dados_aceitos_por_tam:
                dados_aceitos_por_tam[tam] = []
            dados_aceitos_por_tam[tam].append(passos)
            
        if idx % 1000 == 0:
             print(f"Processado: {idx}/{total_palavras}")

    tamanhos = []
    pior_passos = []

    print("\nCalculando pior caso...")

    for tam in range(1, TAMANHO_MAX + 1):
        if tam in dados_aceitos_por_tam:
            lista_passos = dados_aceitos_por_tam[tam]
            pior_caso = max(lista_passos)
            
            tamanhos.append(tam)
            pior_passos.append(pior_caso)

    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, pior_passos, color='red', marker='o', linestyle='-', 
             linewidth=1, markersize=3, alpha=0.7, label='Pior Caso (Max Passos)')
    
    if len(tamanhos) > 1:
        import numpy as np
        z = np.polyfit(tamanhos, pior_passos, 2)
        p = np.poly1d(z)
        plt.plot(tamanhos, p(tamanhos), "k--", linewidth=1.5, label=f'Tendência O(n²)')

    plt.title(f"Complexidade de Pior Caso: L = {{a^i b^j c^k | i=j ou i=k ou j=k}}\n(Amostras: {QTD_POR_TAMANHO} palavras aceitas por tamanho)")
    plt.xlabel("Tamanho da Palavra (n)")
    plt.ylabel("Quantidade de Passos")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    print("\nGerando gráfico...")
    plt.show()

if __name__ == "__main__":
    main()