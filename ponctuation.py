import re

def replace_punctuation(text):
    replacements = {
    "point": ".",
    "virgule": ",",
    "deux-points": ":",
    "point-virgule": ";",
    "point d'exclamation": "!",
    "point d'interrogation": "?",
    "tiret": "-",
    "parenthèse gauche": "(",
    "parenthèse droite": ")",
    "guillemets": "\"",
    "apostrophe": "'",
    "point de suspension": "...",
    "trois petits points": "...",
    "crochet gauche": "[",
    "crochet droit": "]",
    "accolade gauche": "{",
    "accolade droite": "}"
}


    for word, punctuation in replacements.items():
        text = re.sub(r'\b{}\b'.format(word), punctuation, text)
    
    # Remplacer la ponctuation
    text = re.sub(r'\s?(\.|\!|\?|\,|\:|\;)', r'\1 ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\.(\s*)(\w)', lambda match: '. ' + match.group(2).upper(), text)
    text = re.sub(r'^\s*', '', text)
    
    return text

if __name__ == "__main__":
    # Lire le contenu du fichier texte
    with open('resultRaw.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # Remplacer la ponctuation
    updated_content = replace_punctuation(content)

    # Écrire le contenu modifié dans un nouveau fichier texte
    with open('result.txt', 'w', encoding='utf-8') as file:
        file.write(updated_content)
