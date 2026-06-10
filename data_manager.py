import pandas as pd
from openpyxl import load_workbook

PATH_EXCEL = "caja.xlsx"

def cargar_todo():
    """Lee todas las hojas y las unifica en un solo DataFrame."""
    try:
        hojas = pd.read_excel(PATH_EXCEL, sheet_name=None, engine="openpyxl")
        lista_df = []
        for nombre, df in hojas.items():
            df.columns = df.columns.str.strip()
            if all(c in df.columns for c in ['Fecha actualizacion', 'nominales', 'saldo']):
                df = df.rename(columns={'Fecha actualizacion': 'Fecha', 'nominales': 'Nominales', 'saldo': 'Saldo'})
                df['Fecha'] = pd.to_datetime(df['Fecha']).dt.normalize()
                df['Inversion'] = nombre
                lista_df.append(df)
        return pd.concat(lista_df, ignore_index=True) if lista_df else pd.DataFrame()
    except:
        return pd.DataFrame()

def guardar_registro(inversion, fecha, nominales, saldo):
    """Inserta una nueva fila en la hoja correspondiente."""
    try:
        wb = load_workbook(PATH_EXCEL)
        if inversion in wb.sheetnames:
            ws = wb[inversion]
            ws.append([fecha.strftime('%Y-%m-%d'), nominales, saldo])
            wb.save(PATH_EXCEL)
            return True, f"¡Guardado con éxito en '{inversion}'!"
        return False, f"La hoja '{inversion}' no existe."
    except Exception as e:
        return False, f"Error al escribir: {e}. ¿Está abierto el Excel?"