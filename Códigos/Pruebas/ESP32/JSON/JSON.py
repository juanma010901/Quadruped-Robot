import json

# Definir la cadena JSON
json_string = '{"clave": "valor"}'

# Convertir la cadena en un objeto JSON
json_object = json.loads(json_string)

# Acceder a los datos del objeto JSON
print(json_object['clave'])