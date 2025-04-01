from fastapi import APIRouter, HTTPException, Depends
import psycopg2
from database import get_db_connection
from model import OperadoraResponse

router = APIRouter(prefix="/operadoras", tags=["Operadoras"])

@router.get("/{registro_operadora}", response_model=OperadoraResponse)
async def get_operadora(registro_operadora: int):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            REGISTRO_OPERADORA,
            CNPJ,
            Razao_Social,
            Nome_Fantasia,
            Modalidade,
            Cidade,
            UF,
            Telefone,
            Endereco_eletronico AS email,
            Representante,
            TO_CHAR(Data_Registro_ANS, 'DD/MM/YYYY') AS data_registro
        FROM operadora_plano_saude
        WHERE REGISTRO_OPERADORA = %s
        """
        
        cursor.execute(query, (registro_operadora,))
        operadora = cursor.fetchone()
        
        if not operadora:
            raise HTTPException(status_code=404, detail="Operadora não encontrada")
        
        return operadora
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")
    finally:
        if conn:
            conn.close()

@router.get("/")
async def search_operadoras(razao_social: str = None, nome_fantasia: str = None, uf: str = None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            REGISTRO_OPERADORA,
            Razao_Social,
            Nome_Fantasia,
            Cidade,
            UF,
            Telefone
        FROM operadora_plano_saude
        WHERE 1=1
        """
        params = []
        
        if razao_social:
            query += " AND Razao_Social ILIKE %s"
            params.append(f"%{razao_social}%")
        
        if nome_fantasia:
            query += " AND Nome_Fantasia ILIKE %s"
            params.append(f"%{nome_fantasia}%")
            
        if uf:
            query += " AND UF = %s"
            params.append(uf.upper())
            
        query += " LIMIT 50"
        
        cursor.execute(query, params)
        operadoras = cursor.fetchall()
        
        return {"count": len(operadoras), "results": operadoras}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")
    finally:
        if conn:
            conn.close()