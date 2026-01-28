# 20807

import ipaddress

net = ipaddress.ip_network('172.16.192.0/255.255.192.0', False)

N = 0
for ip in net:
    # Если в условии надо указать именно адреса компьютеров,
    # то пропустим адрес сети и широковещательный адрес:

    # if ip in [net.broadcast_address, net.network_address]:
    #    continue
    
    #print(ip)

    bin_str = format(ip, 'b')
    if bin_str.count('1') % 5 != 0:
        N += 1

print(N)
