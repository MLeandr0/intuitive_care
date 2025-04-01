CREATE TABLE plano_contas (
    DATA DATE NOT NULL,
    REG_ANS INT NOT NULL,
    CD_CONTA_CONTABIL INT NOT NULL,
    DESCRICAO VARCHAR(150) NOT NULL,
    VL_SALDO_INICIAL DECIMAL(15,2) NOT NULL,
    VL_SALDO_FINAL DECIMAL(15,2) NOT NULL
);

CREATE TABLE operadora_plano_saude (
    REGISTRO_OPERADORA INT PRIMARY KEY,
    CNPJ VARCHAR(14) NOT NULL UNIQUE,               
    Razao_Social VARCHAR(140) NOT NULL,             
    Nome_Fantasia VARCHAR(140),                      
    Modalidade VARCHAR(40),                         
    Logradouro VARCHAR(40),                         
    Numero VARCHAR(20),                             
    Complemento VARCHAR(40),                        
    Bairro VARCHAR(30),                             
    Cidade VARCHAR(30),                             
    UF CHAR(2),                                     
    CEP VARCHAR(8),                                 
    DDD VARCHAR(4),                                 
    Telefone VARCHAR(20),                           
    Fax VARCHAR(20),                                
    Endereco_eletronico VARCHAR(255),               
    Representante VARCHAR(50),                      
    Cargo_Representante VARCHAR(40),                
    Regiao_de_Comercializacao SMALLINT,             
    Data_Registro_ANS DATE NOT NULL
);