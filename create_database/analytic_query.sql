-- Search query last year
WITH periodo_ano AS (
    SELECT 
        MAX(DATA) AS data_fim,
        MAX(DATA) - INTERVAL '1 year' AS data_inicio,
        EXTRACT(YEAR FROM MAX(DATA)) AS ano_referencia
    FROM plano_contas
),
despesas_ano AS (
    SELECT 
        op.Razao_Social,
        op.Nome_Fantasia,
        op.UF,
        pa.ano_referencia,
        SUM(pc.VL_SALDO_FINAL - pc.VL_SALDO_INICIAL) AS total_despesas
    FROM 
        plano_contas pc
    JOIN 
        operadora_plano_saude op ON pc.REG_ANS = op.REGISTRO_OPERADORA
    CROSS JOIN
        periodo_ano pa
    WHERE 
        pc.DESCRICAO = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
        AND pc.DATA BETWEEN pa.data_inicio AND pa.data_fim
    GROUP BY 
        op.Razao_Social, op.Nome_Fantasia, op.UF, pa.ano_referencia
)
SELECT 
    ano_referencia AS "Ano de Referência",
    Razao_Social AS "Razão Social",
    Nome_Fantasia AS "Nome Fantasia",
    UF,
    total_despesas AS "Total de Despesas",
    ROUND(total_despesas / 1000000, 2) AS "Despesas (em milhões)",
    RANK() OVER (ORDER BY total_despesas DESC) AS "Ranking"
FROM 
    despesas_ano
ORDER BY 
    total_despesas DESC
LIMIT 10;

-- Search query last quarter
WITH periodo_trimestre AS (
    SELECT 
        MAX(DATA) AS data_fim,
        MAX(DATA) - INTERVAL '3 months' AS data_inicio
    FROM plano_contas
),
despesas_trimestre AS (
    SELECT 
        op.Razao_Social,
        op.Nome_Fantasia,
        op.UF,
        pt.data_inicio,
        pt.data_fim,
        SUM(pc.VL_SALDO_FINAL - pc.VL_SALDO_INICIAL) AS total_despesas
    FROM 
        plano_contas pc
    JOIN 
        operadora_plano_saude op ON pc.REG_ANS = op.REGISTRO_OPERADORA
    CROSS JOIN
        periodo_trimestre pt
    WHERE 
        pc.DESCRICAO = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
        AND pc.DATA BETWEEN pt.data_inicio AND pt.data_fim
    GROUP BY 
        op.Razao_Social, op.Nome_Fantasia, op.UF, pt.data_inicio, pt.data_fim
)
SELECT 
    Razao_Social,
    Nome_Fantasia,
    UF,
    data_inicio AS "Início do Período",
    data_fim AS "Fim do Período",
    total_despesas,
    ROUND(total_despesas / 1000000, 2) AS total_despesas_milhoes,
    RANK() OVER (ORDER BY total_despesas DESC) AS ranking
FROM 
    despesas_trimestre
ORDER BY 
    total_despesas DESC
LIMIT 10;