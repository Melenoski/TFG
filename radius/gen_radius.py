import pymysql
import ipaddress

# Configuración de la base de datos
db_equipos_config = {
    "host": "localhost",
    "user": "personalTIC",
    "password": "tfg_2025",
    "database": "IPs"
}

db_radius_config = {
    "host": "localhost",
    "user": "radius",
    "password": "radpass-JFL-2025",
    "database": "radius"
}

def connect_db(host, user, password, database):
    try:
        return pymysql.connect(host=host, user=user, password=password, database=database)
    except pymysql.MySQLError as e:
        print(f"Connection failed: {e}")
        exit(1)

def primer_y_ultimo_host(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    primer_host = str(network.network_address + 1)
    ultimo_host = str(network.broadcast_address - 1)
    return primer_host, ultimo_host


def genera_subred(vlan, subred, mascara, link_equipos, link_radius):
    cursor_equipos = link_equipos.cursor(pymysql.cursors.DictCursor)
    cursor_radius = link_radius.cursor()
    
    primer_host, ultimo_host = primer_y_ultimo_host(subred, mascara)
    
    subclase = f"INET_ATON(IP) BETWEEN INET_ATON('{primer_host}') AND INET_ATON('{ultimo_host}')"
    condiciones = "AND DireccionMAC IS NOT NULL AND DireccionMAC <> '00:00:00:00:00:00' AND valido='1'"
    orden = "ORDER BY DireccionMAC"
    
    query = f"SELECT * FROM Equipos WHERE ({subclase} {condiciones}) {orden}"

    cursor_equipos.execute(query)
    rows = cursor_equipos.fetchall()
    
    if rows:
        sql_radcheck = "INSERT INTO radcheck (username, attribute, op, value) VALUES "
        sql_radreply = "INSERT INTO radreply (username, attribute, op, value) VALUES "
        
        values_radcheck = []
        values_radreply = []
        
        for row in rows:
            campo_mac = row['DireccionMAC'].upper()
            values_radcheck.append(f"('{campo_mac}', 'Cleartext-Password', ':=', '{campo_mac}')")
            values_radreply.append(f"('{campo_mac}', 'Tunnel-Private-Group-Id', '=', '{vlan}')")
        if values_radcheck:
            #print(sql_radcheck + ", ".join(values_radcheck))
            try:
                cursor_radius.execute(sql_radcheck + ", ".join(values_radcheck))
            except pymysql.MySQLError as e:
                print(f"Insertion failed: {e}")
                exit(1)

            
        if values_radreply:
            #print(sql_radreply + ", ".join(values_radreply))
            try:
                cursor_radius.execute(sql_radreply + ", ".join(values_radreply))
            except pymysql.MySQLError as e:
                print(f"Insertion failed: {e}")
                exit(1)

        link_radius.commit()
    
    cursor_equipos.close()
    cursor_radius.close()

def main():
    # Conexión a las bases de datos
    link_equipos = connect_db(**db_equipos_config)
    link_radius = connect_db(**db_radius_config)
    
    cursor_radius = link_radius.cursor()
    
    # Truncate tables
    cursor_radius.execute("TRUNCATE TABLE radcheck")
    cursor_radius.execute("TRUNCATE TABLE radreply")
    
#    cursor_equipos = link_equipos.cursor(pymysql.cursors.DictCursor)
    
    datos_red_profesores = ["10","RED_profesores","192.168.10.0","255.255.255.0","192.168.10.1"]
    datos_red_PAS = ["20","RED_PAS","192.168.20.0","255.255.255.0","192.168.20.1"]
    datos_red_Invitados = ["30","RED_Invitados","192.168.30.0","255.255.255.0","192.168.30.1"]
    datos_redes = [datos_red_profesores, datos_red_PAS, datos_red_Invitados]

    for datos_red in datos_redes:
        genera_subred(datos_red[0], datos_red[2], datos_red[3], link_equipos, link_radius)


 #   cursor_equipos.close()
    cursor_radius.close()
    link_equipos.close()
    link_radius.close()

if __name__ == "__main__":
    main()
