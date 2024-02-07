

def check_port_sus(port):
    if is_whitelist(port) == True:
        return True
    else:

        return False

def is_whitelist(port):
    safe_ports = [443, 22, 8080, 53, 123]
    for port_list in safe_ports:
        if port == port_list:
            return True
        else:
            pass
    return False
