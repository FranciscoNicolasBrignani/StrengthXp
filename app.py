import pandas as pd
import numpy as np

sheet_id = "1qucC77cgO43_20nhHXfvckuhOcAgeuaQL5hzlkSL1rE"
sheet_name = "Rutina"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"



df = pd.read_csv(url)

df.drop_duplicates(inplace=True) #elimina las celdas duplicadas
df.dropna(how='all', inplace=True) #Elimina las filas donde no haya datos en ningun atributo

df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce') #Le decimos a python que la celda "Fecha" es de tipo Fecha y el formato
df['Ejercicio'] = df['Ejercicio'].fillna('Sin registro') #Si la celda "Ejercicio" no tiene datos imprime "Sin registro"
df['Peso(Kg)'] = df['Peso(Kg)'].fillna(0) #Si la celda "Peso(Kg)" no tiene datos imprime 0


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

#Clasificacion de datos

print(df.head())