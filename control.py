import pyodbc
from datetime import datetime
import pandas as pd
# Configura la cadena de conexión
server = r'GONVABUR\GONVABUR2008'  # Por ejemplo, 'localhost' o 'mi_servidor'
database = 'SQLREGISTROPESAJES'
username = 'BASC'
password = 'BASC'
conexion_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def obten_datos_basc():
    # Conectar a la base de datos
    conexion = pyodbc.connect(conexion_str)

    # Crear un cursor
    cursor = conexion.cursor()
    #Fecha_Hora_Entrada_R
    cursor.execute('SELECT Matricula_Camion_R , HORA_E , Descripcion_Transp_T FROM [dbo].[Consulta ESTADO DIARIO] where FECH_S is NULL AND Cod_Transport_R <> 001969')
    filas = cursor.fetchall()
    conexion.close()
    return filas

def datos_tabla():
    # Cargar el archivo Excel
    file_path = r'\\filebur\EXPEDICIONES\ZSD_GTTR10\orders.xlsx'  # Reemplaza con la ruta a tu archivo
    df = pd.read_excel(file_path, engine='openpyxl')

    # Seleccionar las columnas 'NumTrnsprt', 'Denom.' y 'Nom.dest.mercancías'
    selected_columns = df[['NumTrnsprt', 'Denom.', 'Nom.dest.mercancías']]

    # Conectar a la base de datos
    conexion = pyodbc.connect(conexion_str)

    # Crear un cursor
    cursor = conexion.cursor()

    # Ejecutar la consulta SQL
    cursor.execute('SELECT Matricula_Camion_R, OCARGA_R FROM [dbo].[Tabla REGISTRO] WHERE Fecha_Hora_Salida_R IS NULL AND Cod_Transport_R <> 001969 AND OCARGA_R IS NOT NULL ')
    filas = cursor.fetchall()
    print(len(filas))
    print(filas)
    filas_list = [list(fila) for fila in filas]
    # Convertir los resultados de la consulta SQL en un DataFrame de pandas
    df_sql = pd.DataFrame(filas_list, columns=['Matricula_Camion_R', 'OCARGA_R'])
    # Realizar el join entre el DataFrame del Excel y el DataFrame de la consulta SQL usando la columna 'NumTrnsprt' y 'Cod_Transport_R'
    selected_columns['NumTrnsprt'] = selected_columns['NumTrnsprt'].astype(str)
    #df_sql['OCARGA_R'] = df_sql['OCARGA_R'].astype(str)

    df_joined = pd.merge(selected_columns, df_sql, left_on='NumTrnsprt', right_on='OCARGA_R', how='right')
    df_grouped = df_joined.groupby(['Denom.', 'Matricula_Camion_R', 'NumTrnsprt']).size().reset_index(name='counts')
    camiones_por_denom = df_grouped.groupby('Denom.').size().reset_index(name='counts')
    # Mostrar las primeras filas del resultado del join
    print(camiones_por_denom)
    for a, b, c in zip(df_grouped['NumTrnsprt'], df_grouped['Matricula_Camion_R'], df_grouped['Denom.']):
        print(a, b, c)

    # Cerrar la conexión a la base de datos
    conexion.close()
    return df_grouped, camiones_por_denom
datos_tabla()