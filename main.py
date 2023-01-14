import socket
import sys

MAX_HOPS = 30
TIMEOUT = 5
PORT = 33434
MESSAGE = "Say hello to my little friends!"


def create_udp_socket(ttl: int) -> socket.socket:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl+1)
    return udp_socket


def create_icmp_socket() -> socket.socket:
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(TIMEOUT)
    return icmp_socket


def run_tracert(target):
    try:
        target_name, _, target_ip = socket.gethostbyaddr(target)
    except socket.error:
        print("Хост не найден")
        exit(1)
    print("traceroute to", target_name, str(target_ip), str(MAX_HOPS), "hops max", sep=" ")
    for i in range(int(MAX_HOPS)):
        udp_socket = create_udp_socket(i)
        icmp_socket = create_icmp_socket()
        udp_socket.sendto(bytes(MESSAGE, "utf-8"), (target, PORT))
        name = ""
        try:
            _, address = icmp_socket.recvfrom(1024)
            address = address[0]
            try:
                name, _, _ = socket.gethostbyaddr(address)
            except socket.error:
                name = address
        except socket.error:
            address = None
        if address:
            print(str(i + 1), name, address, sep=" ")
            if address == target_ip[0] or name == target_name:
                break
        else:
            print(str(i + 1), " *", sep=" ")
        udp_socket.close()
        icmp_socket.close()


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == "traceroute":
        run_tracert(sys.argv[2])
    else:
        print("Вид запроса: python main.py traceroute {IP адрес или имя хоста}")


