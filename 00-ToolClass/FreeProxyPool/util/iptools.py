import ipaddress


def ip_isvalid(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False


if __name__ == '__main__':
    address = "49.72.96.142"
    print(ip_isvalid(address))
