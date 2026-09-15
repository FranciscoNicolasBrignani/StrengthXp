import pandas as pd
import numpy as np
import gspread
from gspread_dataframe import set_with_dataframe


#Autenticacion y apertura de la hoja
gc = gspread.service_account(filename='credenciales.json')
sheet_id = "1qucC77cgO43_20nhHXfvckuhOcAgeuaQL5hzlkSL1rE"
sh = gc.open_by_key(sheet_id)
worksheet = sh.worksheet("Rutina")


#Lectura dinamica de los datos
datos = worksheet.get_all_values()
header_index = None

for i, fila in enumerate(datos):
    fila_limpia = [str(celda).strip() for celda in fila]
    if "Fecha" in fila_limpia:
        header_index = i
        break

if header_index is None:
    raise ValueError("No se encontró la columna 'Fecha' en la planilla.")

#Construccion del Dataframe
encabezados = [str(col).strip() for col in datos[header_index]]
filas_datos = datos[header_index + 1:]

df = pd.DataFrame(filas_datos, columns=encabezados)

#Limpieza de encavbezados e indice
df.columns = df.columns.str.strip() # Limpiar espacios en blanco invisibles en los encabezados
df = df.loc[:, df.columns != ''] #Eliminar columnas con encabezado vacío

#Limpieza de valores nulos o duplicados
df.drop_duplicates(inplace=True) #elimina las celdas duplicadas
df.replace('', np.nan, inplace=True)
df.dropna(how='all', inplace=True) #Elimina las filas donde no haya datos en ningun atributo
df.reset_index(drop=True, inplace=True)

#Parseo de tipos de datos
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce') #Le decimos a python que la celda "Fecha" es de tipo Fecha y el formato
df['Ejercicio'] = df['Ejercicio'].fillna('Sin registro') #Si la celda "Ejercicio" no tiene datos imprime "Sin registro"


#Conversion de tipos de datos numericos (KPIS)
df['Peso(Kg)'] = pd.to_numeric(df['Peso(Kg)'], errors='coerce').fillna(0)
if 'Repeticiones' in df.columns:
    df['Repeticiones'] = pd.to_numeric(df['Repeticiones'], errors='coerce').fillna(0)
if 'Series' in df.columns:
    df['Series'] = pd.to_numeric(df['Series'], errors='coerce').fillna(0)


#Manipulacion de fechas
df['Año'] = df['Fecha'].dt.year
df['Mes_nombre'] = df['Fecha'].dt.strftime('%B')
df['Dia_Semana'] = df['Fecha'].dt.strftime('%A')

dias = {
    'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 
    'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}

meses = {
    'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril', 
    'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto', 
    'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
}

df['Dia_Semana'] = df['Dia_Semana'].map(dias)
df['Mes_nombre'] = df['Mes_nombre'].map(meses)

#Definición del diccionario de ejercicios (mapeo estructurado)
EJERCICIOS_MAP = {
    "banco plano": {"musculo_principal": "Pecho", "musculo_secundario": "Hombro"},
    "banco inclinado": {"musculo_principal": "Pecho", "musculo_secundario": "Hombro"},
    "banco declinado": {"musculo_principal": "Pecho", "musculo_secundario": "Tríceps"},
    "mariposa": {"musculo_principal": "Pecho", "musculo_secundario": "Hombro"},
    "curl de bíceps": {"musculo_principal": "Bíceps", "musculo_secundario": "Braquial"},
    "martillo": {"musculo_principal": "Bíceps", "musculo_secundario": "Braquiorradial"},
    "sentadillas": {"musculo_principal": "Cuadriceps", "musculo_secundario": "Glúteo"}
}

df['ejercicio_clean'] = df['Ejercicio'].astype(str).str.lower().str.strip()

#Normalizacion de columnas
def obtener_musculo_principal(row):
    ejercicio = row['ejercicio_clean']
    #Buscar en el diccionario
    if ejercicio in EJERCICIOS_MAP:
        return EJERCICIOS_MAP[ejercicio]['musculo_principal']
    #Fallback a la columna 'Musculo' de Sheets si existe y no está vacía
    if 'Musculo' in row and pd.notna(row['Musculo']) and str(row['Musculo']).strip() != '':
        return str(row['Musculo']).strip()
    #Categoría por defecto
    return 'Sin categoría'

def obtener_musculo_secundario(row):
    ejercicio = row['ejercicio_clean']
    if ejercicio in EJERCICIOS_MAP:
        return EJERCICIOS_MAP[ejercicio]['musculo_secundario']
    return 'Sin categoría'

df['musculo_principal'] = df.apply(obtener_musculo_principal, axis=1)
df['musculo_secundario'] = df.apply(obtener_musculo_secundario, axis=1)

#agupamos por semana
df['Semana'] = df['Fecha'].dt.to_period('W').astype(str)

#volumen de carga, tonelaje y 1RM estimado
df['Volumen_Fila_Kg'] = df['Series'] * df['Repeticiones'] * df['Peso(Kg)']
df['1RM_Estimado'] = np.where(
    df['Repeticiones'] > 0,
    df['Peso(Kg)'] * (1 + (df['Repeticiones'] / 30)),
    0
)

#Tablas KPIS

#KPI 1: Volumen de hipertrofia semanal
volumen_hipertrofia = df.groupby(['Semana', 'musculo_principal']).agg(
    series_totales=('Series', 'sum'),
    tonelaje_total_kg=('Volumen_Fila_Kg', 'sum'),
).reset_index()

#Intensidad relativa
volumen_hipertrofia['tonelaje_por_serie'] = (
    volumen_hipertrofia['tonelaje_total_kg'] / volumen_hipertrofia['series_totales']
).round(2)

#KPI 2 Maximo 1RM estimado por ejercicio y semana
rm_estimado = df.groupby(['Semana', 'Ejercicio']).agg(
    max_1rm_estimado=('1RM_Estimado', 'max'),
    peso_maximo=('Peso(Kg)', 'max')
).reset_index()


#KPI PR
pr_historico = df.groupby('Ejercicio').agg(
    pr_peso_max_kg=('Peso(Kg)', 'max'),
    pr_1rm_estimado=('1RM_Estimado', 'max'),
    total_serie_acumuladas=('Series', 'sum')
).reset_index()

#fecha PR
idx_max_1rm = df.groupby('Ejercicio')['1RM_Estimado'].idxmax()
pr_detalle = df.loc[idx_max_1rm, ['Ejercicio', 'Fecha', 'Peso(Kg)', 'Repeticiones', '1RM_Estimado']].copy()
pr_detalle.rename(columns={
    'Fecha': 'fecha_del_pr',
    'Peso(Kg)': 'peso_del_pr',
    'Repeticiones': 'reps_del_pr'
}, inplace=True)


tablas_kpi = {
    "KPI_Volumne": volumen_hipertrofia,
    "KPI_1RM_Semanal": rm_estimado,
    "KPI_PR_Historico": pr_historico,
    "KPI_PR_Detalle": pr_detalle,
    "Datos_Procesados": df
}

for nombre_pestaña, dataframe in tablas_kpi.items():
    try:
        ws = sh.worksheet(nombre_pestaña)
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=nombre_pestaña, rows="100", cols=20)

    set_with_dataframe(ws, dataframe)

print("\n Se exportaron las tablas de KPIs exitosamente a Google Sheets!")
