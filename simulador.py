# Classe que simula o funcionamento de uma linha de cache
class CacheLine:
    def _init_(self):
        self.valid = False
        self.tag = 0
        self.offset = 0


def simulate_cache(cache_size, line_size, associativity, file_name):
    # Inicializa a cache 
    # A partir do tamanho da cache e do tamanho da linha, calcula o número de linhas e conjuntos
    num_lines = cache_size // line_size
    num_sets = num_lines // associativity

    # Cria a cache
    cache = [[CacheLine() for _ in range(associativity)] for _ in range(num_sets)]

    hits = 0
    misses = 0
    set_misses = [0 for _ in range(num_sets)]

    # Função que atualiza a cache
    def update_cache(address):
        # Utiliza as variáveis hits e misses declaradas anteriormente
        nonlocal hits, misses
        # Calcula o índice do conjunto e a tag
        set_index = ((address // line_size) % num_lines) % num_sets
        tag = address // line_size

        # Calcula o offset
        offset = address % line_size

        # Verifica se o endereço está na cache
        for line in cache[set_index]:
            # Se estiver, incrementa o número de hits e retorna
            if line.valid and line.tag == tag:
                hits += 1
                return
        # Se não estiver, incrementa o número de misses

        # Substitui a linha que está há mais tempo na cache dentro daquele grupo (FIFO)
        line_to_replace = set_misses[set_index] % associativity
        
        misses += 1
        set_misses[set_index] += 1

        cache[set_index][line_to_replace].valid = True
        cache[set_index][line_to_replace].tag = tag
        cache[set_index][line_to_replace].offset = offset

    output_lines = []

    # Lê o arquivo de entrada
    with open(file_name, 'r') as file:
        # Para cada linha do arquivo, atualiza a cache e imprime o estado da cache
        for line in file:
            address = int(line.strip(), 16)
            update_cache(address)

            # Imprime o estado da cache de acordo com o formato especificado
            output_lines.append("================")
            output_lines.append("IDX V * ADDR *")
            # Para cada conjunto da cache
            for i, cache_set in enumerate(cache):
                # Para cada linha do conjunto
                for j, cache_line in enumerate(cache_set):
                    # Imprime o índice do conjunto, o bit de validade e a tag
                    index = i * associativity + j
                    valid_bit = int(cache_line.valid)
                    tag_str = f"0x{cache_line.tag:08X}" if cache_line.valid else " "
                    output_lines.append(f"{index:03d} {valid_bit} {tag_str}")
            output_lines.append("================\n")

    output_lines.append(f"#hits: {hits}")
    output_lines.append(f"#miss: {misses}")

    # Escreve o arquivo de saída
    with open('output.txt', 'w') as output_file:
        output_file.write('\n'.join(output_lines))

    return hits, misses


def main():
    # Lê os parâmetros de entrada
    cache_size = int(input("Cache size: "))
    line_size = int(input("Line size: "))
    associativity = int(input("Associativity: "))
    file_name = input("file: ")

    hits, misses = simulate_cache(cache_size, line_size, associativity, file_name)


if _name_ == "__main__":
    main()