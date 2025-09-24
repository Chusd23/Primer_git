import re
import os

class Tokenizer:
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []

    def tokenize(self):
        lines = self.source.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):  #
                continue

            regex_tokens = re.findall(
                r'"([^"]*)"|'                
                r'(\d+\.?\d*)|'              
                r'({|}|\[|\]|=|,|:)|'        
                r'([A-Za-zÁÉÍÓÚáéíóúñÑ_][\wÁÉÍÓÚáéíóúñÑ_]*)',  
                line
            )

            for group in regex_tokens:
                if group[0]:  
                    self.tokens.append(('STRING', group[0]))
                elif group[1]:  
                    if '.' in group[1]:
                        self.tokens.append(('NUMBER', float(group[1])))
                    else:
                        self.tokens.append(('NUMBER', int(group[1])))
                elif group[2]:  #
                    self.tokens.append(('OPERATOR', group[2]))
                elif group[3]:  
                    self.tokens.append(('IDENTIFIER', group[3]))

        return self.tokens


def load_file_content(filepath):
    if not os.path.exists(filepath):
        print(f"Error: El archivo '{filepath}' no existe.")
        return None

    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def analizar_archivo(filepath, titulo):
    source_code = load_file_content(filepath)
    if source_code:
        print(f"\n===== {titulo.upper()} =====")
        tokenizer = Tokenizer(source_code)
        tokens = tokenizer.tokenize()
        for token in tokens:
            print(token)



analizar_archivo("Snake.txt", "Snake")
analizar_archivo("Tetris.txt", "Tetris")

