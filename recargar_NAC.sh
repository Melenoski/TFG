#! /bin/bash

cd /root/tfg/dhcp
/usr/bin/python3 gen_dhcp.py

diff /etc/kea/kea-dhcp4.conf ./kea-dhcp4.conf.json
rc=$?

if [ $rc == 1 ]; then
    # Comprobar que el fichero de configuración es correcto
    /usr/sbin/kea-dhcp4 -t kea-dhcp4.conf.json
    rc=$?
    if [ $rc != 0 ]; then
        exit 1;
    fi

#    /bin/cp -f /etc/kea/kea-dhcp4.conf /root/tfg/dhcp/kea-dhcp4.conf.json.$(date +%Y%m%d_%H%M)
    /bin/cp -f ./kea-dhcp4.conf.json /etc/kea/kea-dhcp4.conf
    /bin/chown _kea:_kea /etc/kea/kea-dhcp4.conf

   # Reiniciar el servicio
    systemctl restart isc-kea-dhcp4-server.service

elif [ $rc == 2 ]; then
#    mail -s "DHCPD: Error al comparar los ficheros /etd/dhcp.conf y ./kea-dhcp4.conf" $mailto
    exit 1;
fi

