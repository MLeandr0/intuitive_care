# Transformar dados

Este script tem como objetivo extrair e processar tabelas de um arquivo PDF, gerando uma planilha no formato CSV. A planilha resultante é, então, compactada em um arquivo ZIP.

## Principais etapas

- Antes de executar este script, é necessário rodar o processo de web scraping para baixar e salvar o arquivo PDF em uma pasta específica. O script depende deste arquivo PDF para realizar a extração das tabelas.
- O script localiza e descompacta o arquivo ZIP que contém o PDF. O ZIP deve estar presente na pasta de web scraping, permitindo o acesso ao PDF para a próxima etapa.
- Após a extração das tabelas do PDF, o script renomeia duas colunas específicas, conforme os requisitos definidos: as colunas "OD" e "AMB" são renomeadas para "Seg. Odontológica" e "Seg. Ambulatorial", respectivamente.
- Após salvar os dados extraídos como um arquivo CSV, o script compacta este CSV em um arquivo ZIP com o nome "Teste_meu_nome.zip", conforme solicitado.

