--INE5426 - Construção de compiladores
(rascunho)

acho que precisa de python >=3.5 para funcionar

dependencia: ply
    - pip install ply
    - ou tambem: pip install -r requirements.txt

executar:
    - Windows:  python main.py 'arquivo.lcc'
    - Linux:    python3 main.py 'arquivo.lcc'

por enquanto esta gerando somente a lista de tokens como saida, contendo linha, coluna, tipo do token e lexema do token

**verificar: a expressao regular do token 'string_constant' parece estar funcionando (pega tudo que tiver entre '' ou ""), mas é bem esquisita e nao entendi como ela funciona (foi copiada de um exemplo pronto que servia para definir strings em C)