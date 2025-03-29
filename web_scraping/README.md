# Web Scraping

Neste desafio, o objetivo é realizar o download e a compactação dos anexos disponíveis no site do governo [governo](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos).

## Principais etapas

- Busca por todos os links presentes no site que terminavam em pdf. Após isso uma busca por todas as tags de link que tinha a palavra chave em especifico.
- Após identificar os links válidos, foi realizado o download de cada anexo individualmente e armazenado localmente em uma pasta dedicada que é criada caso ainda não exista.
- Por fim, após o download de todos os anexos, os arquivos são compactados em um único arquivo ZIP.