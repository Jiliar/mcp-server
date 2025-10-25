from fastmcp import FastMCP
import mcp
from datetime import datetime, timedelta
import csv

mcp = FastMCP('Gastos MCP Server', '25565')

# Utilidad para leer gastos del CSV
def _leer_gastos_csv():
    gastos = []
    try:
        with open('data/gastos.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalizar nombres de campo para compatibilidad
                if 'metodo de pago' in row:
                    row['metodo_pago'] = row['metodo de pago']
                    del row['metodo de pago']
                row['cantidad'] = float(row['cantidad'])
                gastos.append(row)
    except FileNotFoundError:
        # Si el archivo no existe, retornar lista vacía
        pass
    return gastos

# Función auxiliar para obtener gastos recientes (NO decorada como tool)
def _obtener_gastos_recientes(dias: int = 5):
    """
    Función interna para obtener gastos recientes para uso en prompts.
    """
    try:
        gastos = _leer_gastos_csv()
        
        # Calcular fecha límite
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        # Filtrar gastos de los últimos N días
        gastos_recientes = []
        for gasto in gastos:
            fecha_gasto = datetime.strptime(gasto['fecha'], "%Y-%m-%d")
            if fecha_gasto >= fecha_limite:
                gastos_recientes.append(gasto)
        
        return gastos_recientes
        
    except Exception as e:
        print(f"Error al obtener gastos recientes: {e}")
        return []

@mcp.tool
def agregar_gasto(fecha:str, categoria:str, cantidad:float, metodo_pago:str):
    """
    Agrega un nuevo gasto al archivo data/gastos.csv.

    Parámetros:
        fecha (str | datetime): Fecha del gasto en formato 'YYYY-MM-DD' o como objeto datetime.
        categoria (str): Categoría del gasto.
        cantidad (float): Monto del gasto.
        metodo_pago (str): Método de pago utilizado.

    Retorna:
        str: Mensaje de confirmación o error.
    """
    try:
        # Validar y convertir fecha a datetime
        if isinstance(fecha, str):
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        elif isinstance(fecha, datetime):
            fecha_dt = fecha
        else:
            raise ValueError("El parámetro 'fecha' debe ser str en formato YYYY-MM-DD o datetime.")

        # Verificar si el archivo existe para escribir los headers
        file_exists = False
        try:
            with open('data/gastos.csv', 'r', encoding='utf-8') as f:
                file_exists = True
        except FileNotFoundError:
            file_exists = False

        with open('data/gastos.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Escribir headers si el archivo no existe
            if not file_exists:
                writer.writerow(['fecha', 'categoria', 'cantidad', 'metodo_pago'])
            writer.writerow([
                fecha_dt.strftime("%Y-%m-%d"),
                categoria,
                cantidad,
                metodo_pago
            ])
        return f"Gasto agregado: {fecha_dt.strftime('%Y-%m-%d')}, {categoria}, {cantidad}, {metodo_pago}"
    except Exception as e:
        return f"Error al agregar gasto: {e}"

@mcp.tool
def obtener_gastos_recientes(dias: int = 5):
    """
    Obtiene los gastos de los últimos N días para que la IA pueda generar un resumen.

    Parámetros:
        dias (int): Número de días a consultar (por defecto 5)

    Retorna:
        list: Lista de gastos de los últimos N días
    """
    return _obtener_gastos_recientes(dias)

@mcp.resource('resource://gastos')
def obtener_gastos():
    """
    Lee y retorna todos los gastos almacenados en el archivo data/gastos.csv.

    Retorna:
        list: Lista de diccionarios con los campos: fecha, categoria, cantidad, metodo_pago.
    """
    return _leer_gastos_csv()

@mcp.prompt(
        name="Resumen de Gastos Recientes",
        description="Genera un resumen analítico de los gastos de los últimos 5 días usando IA.",
        tags={"finanzas", "gastos", "resumen", "analisis"},
        meta={"version": "1.0", "author": "Jiliar Silgado"}
)
def prompt_resumen_gastos():
    """
    Prompt que proporciona los datos de gastos recientes para que la IA genere un resumen analítico.

    Retorna:
        str: Prompt con datos estructurados para el análisis de IA
    """
    # Usar la función interna, NO la herramienta MCP
    gastos_recientes = _obtener_gastos_recientes(dias=5)
    
    if not gastos_recientes:
        return "No hay gastos registrados en los últimos 5 días para analizar."
    
    # Preparar datos para el análisis de IA
    prompt = f"""
    POR FAVOR GENERA UN RESUMEN ANALÍTICO DE LOS GASTOS:

    DATOS DE GASTOS DE LOS ÚLTIMOS 5 DÍAS:
    {gastos_recientes}

    INSTRUCCIONES PARA EL ANÁLISIS:

    1. CÁLCULOS ESTADÍSTICOS:
       - Total gastado en el período
       - Promedio diario de gastos
       - Número total de transacciones
       - Día con mayor gasto

    2. ANÁLISIS POR CATEGORÍA:
       - Identifica las categorías con mayor gasto
       - Calcula porcentajes por categoría
       - Detecta patrones de consumo

    3. ANÁLISIS POR MÉTODO DE PAGO:
       - Distribución de gastos por método de pago
       - Preferencias de pago identificadas

    4. TENDENCIAS Y OBSERVACIONES:
       - Identifica tendencias temporales
       - Señala gastos inusuales o atípicos
       - Proporciona insights sobre hábitos de gasto

    5. RECOMENDACIONES:
       - Sugerencias para optimizar gastos
       - Alertas sobre categorías con alto consumo
       - Consejos para el control financiero

    FORMATO DE SALIDA:
    Usa un formato claro con emojis y secciones bien estructuradas.
    Incluye números específicos, porcentajes y análisis contextual.

    Por favor, genera un resumen completo y útil basado en estos datos.
    """
    
    return prompt

def main():
    """
    Función principal que inicia el servidor MCP.
    """
    print("Hello I am a mcp-server!")
    mcp.run()

if __name__ == "__main__":
    main()