import pymysql
import json
import ipaddress

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "personalTIC",
    "password": "tfg_2025",
    "database": "IPs"
}

# Configuración de valores por defecto
interfaces = "eth1"
dhcp_socket_type = "udp"

valores_kea_defecto = {
    "reservations-global": False,
    "reservations-in-subnet": True,
    "reservations-out-of-pool": True,
    "valid-lifetime": 28800,
    "calculate-tee-times": True,
}

valores_red_IES_defecto = {
    "domain-name": "local",
    "domain-name-servers": "8.8.8.8",
    "time-servers": "150.214.94.5, 82.223.203.159",
}

############################################################
# Funciones para manejo de IPs
############################################################
def primer_y_ultimo_host(ip, mask):
    subnet = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(subnet.network_address + 1), str(subnet.broadcast_address - 1)

def dir_broadcast(ip, mask):
    subnet = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(subnet.broadcast_address)

def mask2cidr(mask):
    return ipaddress.IPv4Network(f"0.0.0.0/{mask}").prefixlen


############################################################
# Genera la estructura con la definición para cada subred
# Incluyendo los host para los que se reserva dirección IP
############################################################

def genera_subred_dhcp(datos_red, conexion):

   id_vlan = int(datos_red[0])
   nombre = datos_red[1]
   subred = datos_red[2]
   mascara = datos_red[3]
   gateway = datos_red[4]

   cidr = mask2cidr(mascara)

   # Creando la estructura JSON
   if nombre == "RED_Invitados":
      pool_range = "192.168.30.11 - 192.168.30.99"
      seccion_subnet = {
         "id": id_vlan,
         "subnet": f"{subred}/{cidr}",
         "pools": [{"pool": pool_range}],
         "option-data": [{"name": "routers", "data": gateway}], 
      }
   else:
      seccion_subnet = {
         "id": id_vlan,
         "subnet": f"{subred}/{cidr}",
         "option-data": [{"name": "routers", "data": gateway}], 
         "reservations": []
      }

      primer_host, ultimo_host = primer_y_ultimo_host(subred, mascara)

      subclase = f"INET_ATON(IP) BETWEEN INET_ATON('{primer_host}') AND INET_ATON('{ultimo_host}')"
      condiciones = f"AND (DireccionMAC IS NOT NULL) AND (DireccionMAC <> '00:00:00:00:00:00') AND (Equipos.valido='1')"
      orden = f"ORDER BY INET_ATON(IP)"
      
      get_datos_query = f"SELECT Equipos.*, COALESCE(CONCAT(datos_personales.Nombre, ' ', datos_personales.Apellido1), ' ') as Usuario " \
                        f"FROM Equipos " \
                        f"LEFT JOIN datos_personales ON Equipos.IdUsuario = datos_personales.id " \
                        f"WHERE ({subclase} {condiciones}) {orden}"
      
      with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
         cursor.execute(get_datos_query)
         resultados = cursor.fetchall()
         if resultados:
            for row in resultados:
               Reserva = {
                  #f"#Usuario: {row['Usuario']}",
                  "hostname": row['NombrePc'],
                  "hw-address": row['DireccionMAC'],
                  "ip-address": row['IP']
               }
            
               # Actualiza la seccion de reservas
               seccion_subnet["reservations"].append(Reserva)

   return seccion_subnet


############################################################
# Genera la estructura principal
# Parámetro: Array de subredes para incluir
############################################################

def genera_KEA_config(datos_redes):
   conexion = pymysql.connect(**db_config)
   archivo_nombre = "kea-dhcp4.conf.json"

   ############################################################
   # Cabecera global
   ############################################################
   Fich_completo = {
         "Dhcp4": {
               "interfaces-config": {
                  "interfaces": [interfaces],
                  "dhcp-socket-type": dhcp_socket_type
               },
               "lease-database": {
                  "type": "memfile",
                  "persist": True,
                  "name": "/var/lib/kea/kea-leases4.csv"
               },
               **valores_kea_defecto,
               "loggers": [{
                  "name": "*",
                  "severity": "INFO"
               }],
               "option-data": [
                  {"name": k, "data": v} for k, v in valores_red_IES_defecto.items()
               ],
               "subnet4": []
         }
      }

   ###########################################################
   ###########################################################
   #  Para cada sub red creamos una sección
   ###########################################################
   ###########################################################

   
   for datos_red in datos_redes:
      json_subred = genera_subred_dhcp(datos_red, conexion)
      Fich_completo["Dhcp4"]["subnet4"].append(json_subred)
      

   # Escribir la estructura en el archivo en formato JSON con indentación
   with open(archivo_nombre, 'w') as fich:
      fich.write(json.dumps(Fich_completo, indent=4))
      fich.write("\n")

   conexion.close()

#############################################################
#  MAIN
#############################################################

def main():
   
   # temp_dir = "temp"
   # os.makedirs(temp_dir, exist_ok=True)
   # Definición de las redes del IES
   # Formato: <vlan ID><Nombre subred><Dirección de Red><Mascara de Red><Gateway>
   datos_red_profesores = ["10","RED_profesores","192.168.10.0","255.255.255.0","192.168.10.1"]
   datos_red_PAS = ["20","RED_PAS","192.168.20.0","255.255.255.0","192.168.20.1"]
   datos_red_Invitados = ["30","RED_Invitados","192.168.30.0","255.255.255.0","192.168.30.1"]
   datos_redes = [datos_red_profesores, datos_red_PAS, datos_red_Invitados]

   genera_KEA_config(datos_redes)
    
   # os.system(f"cat {temp_dir}/Cabecera_$(hostname).add > kea-dhcp4.conf.json")


if __name__ == "__main__":
    main()


