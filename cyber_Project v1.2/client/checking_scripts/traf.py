import scapy.all as scapy
from scapy.layers import http
import re

# List of sensitive data regexes
filters = [
    "user=.*",
    "pass=.*",
    "ssid=.*",
    "account=.*",
    "routing=.*",
    "ssn=.*"
]

target_ips = ["192.168.1.1", "192.168.1.2"]  # Add your target IPs
target_ports = [62896, 80, 443, 445]  # Add your target ports


def decode_payload(raw_data):
    try:
        # Attempt UTF-8 decoding
        decoded_data = raw_data.decode('utf-8', 'ignore')
        return decoded_data
    except UnicodeDecodeError:
        pass

    try:
        # Attempt ASCII decoding
        decoded_data = raw_data.decode('ascii', 'ignore')
        return decoded_data
    except UnicodeDecodeError:
        pass

    # Add more decoding methods as needed

    # If none of the decoding methods work, return raw data
    return raw_data


def packet_callback(packet):
    ip = packet.getlayer(scapy.IP)
    tcp = packet.getlayer(scapy.TCP)
    if tcp and ip and (ip.dst in target_ips or tcp.dport in target_ports):
        raw = packet.getlayer(scapy.Raw)
        if raw:
            data = bytes(raw)
            print(data)
            # Attempt to decode payload
            decoded_data = decode_payload(data)
            print(f"{ip}, {tcp}, {decoded_data}")
            print()

            for f in filters:
                if re.search(f, decoded_data):
                    print(f"[!] ALERT: Data match found in packet to {ip.dst}:{tcp.dport}: {decoded_data}")
                    return

        if packet.haslayer(http.HTTPRequest):
            http_data = packet[http.HTTPRequest].payload
            # Attempt to decode HTTP payload
            decoded_http_data = decode_payload(http_data)
            print(f"Decoded HTTP Request: {decoded_http_data}")


try:
    # Start sniffing packets
    print("Starting packet sniffing...")
    scapy.sniff(prn=packet_callback, store=0)

except KeyboardInterrupt:
    # Handle exit
    print("\nExiting...")
