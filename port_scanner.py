import socket
import re
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    
    # Determinar si es IP o hostname
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    is_ip = re.match(ip_pattern, target) is not None
    
    try:
        # Manejar hostname
        if not is_ip:
            try:
                ip = socket.gethostbyname(target)
                hostname = target
            except socket.gaierror:
                return "Error: Invalid hostname"
        # Manejar IP
        else:
            octets = target.split('.')
            if len(octets) != 4 or not all(0 <= int(octet) <= 255 for octet in octets):
                return "Error: Invalid IP address"
            ip = target
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = None

        # Escanear puertos en el rango especificado
        for port in range(port_range[0], port_range[1] + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        # Modo verbose
        if verbose:
            # Construir encabezado
            header = f"Open ports for {hostname} ({ip})" if hostname else f"Open ports for {ip}"
            if not open_ports:
                return header
            
            # Formatear salida
            result = f"{header}\nPORT     SERVICE"
            for port in open_ports:
                service = ports_and_services.get(port, str(port))
                result += f"\n{port:<8} {service}"
            return result
            
        # Modo normal
        return open_ports
        
    except Exception:
        if is_ip:
            return "Error: Invalid IP address"
        return "Error: Invalid hostname"