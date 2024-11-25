#Creacion de la conexion, eliminacion y creacion de tabla, carga DataSet
import happybase
import pandas as pd
from datetime import datetime
 
# Bloque principal de ejecución
try:
    connection = happybase.Connection('localhost')
    print("Conexión establecida con HBase")
 
    # 2. Crear la tabla con las familias de columnas     
    table_name = 'covid_19' 
    families = {
        'contagiados': dict(),        # información básica del contagio 
        'locacion': dict(),        # informacion de la ubicacion geografica
        'persona': dict()        # información del paciente
    } 
    # 3. Eliminar la tabla si ya existe
    if table_name.encode() in connection.tables():
        print(f"Eliminando tabla existente - {table_name}")
        connection.delete_table(table_name, disable=True)
    # Crear nueva tabla
    connection.create_table(table_name, families)
    table = connection.table(table_name)
    print("Tabla 'covid_19' creada exitosamente")
    # 3. Cargar datos del CSV
    covid_data = pd.read_csv('Covid_19_cun.csv')
    # Iterar sobre el DataFrame usando el índice
    for index, row in covid_data.iterrows():
    # Generar row key basado en el índice
        row_key = f'covid_{index}'.encode() 
        # Organizar los datos en familias de columnas    
        data = { 
                b'contagiados:Tipo de contagio': str(row['Tipo de contagio']).encode(),
                b'contagiados:Estado': str(row['Estado']).encode(),
                b'contagiados:Recuperado': str(row['Recuperado']).encode(),
                b'locacion:Nombre municipio': str(row['Nombre municipio']).encode(),
                b'persona:Edad': str(row['Edad']).encode(),
                b'persona:Sexo': str(row['Sexo']).encode()   
            } 
        table.put(row_key, data)
    print("Datos cargados exitosamente")

# Listar las tablas existentes
    print("Tablas existentes:", connection.tables())
    print("Conexión exitosa a HBase")
    contador = 0
    fallecido = 0
    for data in t.scan(filter='FirstKeyOnlyFilter() AND KeyOnlyFilter()'):
        contador += 1
    print("Total de registros ",contador)
    print("\n=== Fallecidos por sexo ===")
    fallecidos_df = b'contagiados:Estado' # variable que nos almacena el objeto
    for key, data in t.scan():
        if fallecidos_df in data and data[fallecidos_df] == b'Fallecido':  # Valor a buscar se define 
            fallecido += 1
    print("Total de fallecidos ",fallecido)

#Funcion para contar por municipio
    print("\n=== Casos por municipio ===")
    for key, data in t.scan():
        if columna_municipio in data:
            municipio = data[columna_municipio].decode() 
            cont_municipio[municipio] += 1
#Impresion en consola de resultados
    for municipio, conteo in cont_municipio.items():
        print(f"{municipio}: {conteo}")

# CREATE
def create_data(row_key, data):
    
    t.put(row_key, data)
    print(f"Registro creado: {row_key}")

# READ: 
def read_data(row_key):
    
    row = t.row(row_key)
    if row:
        print(f"Registro leído ({row_key}): {row}")
    else:
        print(f"Registro con clave {row_key} no encontrado.")
    return row

# UPDATE: 
def update_data(row_key, data):
    
    t.put(row_key, data)
    print(f"Registro actualizado: {row_key}")

# DELETE
def delete_data(row_key):
    
    t.delete(row_key)
    print(f"Registro eliminado: {row_key}")

# Main principal
if __name__ == "__main__":
    # CREATE
    create_data('row331339', {b'contagiados:Tipo de contagio': b'Relacionado', b'contagiados:Estado': b'Leve',b'contagiados:Recuperado': b'Fallecido',
                       b'locacion:Nombre municipio': b'SOACHA',b'persona:Edad': b'36',b'persona:Sexo': b'M'})
    create_data('row331340', {b'contagiados:Tipo de contagio': b'Comunitaria', b'contagiados:Estado': b'Fallecido',b'contagiados:Recuperado': b'Fallecido',
                       b'locacion:Nombre municipio': b'SIBATE',b'persona:Edad': b'36',b'persona:Sexo': b'M'})

    # READ
    read_data('row331339')
    read_data('row331341')  # Registro inexistente

    # UPDATE
    update_data('row331339', {b'contagiados:Tipo de contagio': b'Comunitaria', b'contagiados:Estado': b'Fallecido',b'contagiados:Recuperado': b'Fallecido',
                       b'locacion:Nombre municipio': b'FUNZA',b'persona:Edad': b'28',b'persona:Sexo': b'F'})

    # READ después de UPDATE
    read_data('row331339')

    # DELETE
    delete_data('row331340')

    # READ después de DELETE
    read_data('row331340')

# Solicitar al usuario la clave de fila
row_key = input("Ingresa la clave de fila que deseas consultar: ").strip()

# Leer la fila ingresada por el usuario
row = table.row(row_key)

# Verificar si la fila existe y mostrar datos
if row:
    print(f"Datos de la fila '{row_key}':")
    for columna, valor in row.items():
        print(f"{columna.decode('utf-8')}: {valor.decode('utf-8')}")
else:
    print(f"No se encontró la fila con clave '{row_key}'.")


except Exception as e: 
    print(f"Error: {str(e)}")
finally: 
    # Cerrar la conexión 
    connection.close()