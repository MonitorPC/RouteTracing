from scapy.all import *
import sys
import time
import argparse


def parser():
    p = argparse.ArgumentParser(description="Ping the target IP with custom settings.")
    p.add_argument("target_ip", help="The IP address of destination.")
    p.add_argument("-p", "--protocol", default="I", help="Network protocol (default: ICMP).")
    p.add_argument("-m", "--max_hops", default=30, help="Maximum number of hops (default: 30).", type=int)
    p.add_argument("-t", "--timeout", default=2, help="Timeout in seconds (default: 2.0).", type=int)
    p.add_argument("-v", "--verbose", default=False, help="Verbose mode (default: False).")

    args = p.parse_args()
    return (args.protocol, args.target_ip, args.max_hops, args.timeout, args.verbose)


def udp(target_ip, max_hops, timeout, verbose):
    try:
        dport = 33434
        packet = IP(dst=target_ip, ttl=max_hops) / UDP(dport=dport)
        reply = sr1(packet, timeout=timeout, verbose=verbose)

        if reply is None:
            return (f"{max_hops}\t* * * Timeout", None)
        else:
            hop_ip = reply.src
            try:
                hop_name = socket.gethostbyaddr(hop_ip)[0]
            except socket.herror:
                hop_name = hop_ip

            rtt = (reply.time - packet.sent_time) * 1000  # Round-trip time in ms
            return (f"{max_hops}\t{hop_ip} ({hop_name})  {rtt:.2f} ms", hop_ip)

    except socket.gaierror:
        return (f"Cannot resolve address: {target_ip}", None)


def tcp(target_ip, max_hops, timeout, verbose):
    try:
        sport = 8080
        dport = 80
        packet = IP(dst=target_ip, ttl=max_hops) / TCP(sport=sport, dport=dport, flags="S")
        reply = sr1(packet, timeout=timeout, verbose=verbose)

        if reply is None:
            return (f"{max_hops}\t* * * Timeout", None)
        else:
            hop_ip = reply.src
            try:
                hop_name = socket.gethostbyaddr(hop_ip)[0]
            except socket.herror:
                hop_name = hop_ip

            rtt = (reply.time - packet.sent_time) * 1000
            if reply.haslayer(TCP):  # Check if it's a TCP response
              if reply[TCP].flags == "SA":  # SYN-ACK received 
                  return (f"{max_hops}\t{hop_ip} ({hop_name})  {rtt:.2f} ms", hop_ip)
              elif reply[TCP].flags == "RA":  # RST-ACK (port closed)
                  return (f"{max_hops}\t{hop_ip} ({hop_name})  {rtt:.2f} ms (Port closed)", hop_ip)
            elif reply.haslayer(ICMP):
                icmp_type = reply[ICMP].type
                return (f"{max_hops}\t{hop_ip} ({hop_name})  {rtt:.2f} ms (ICMP {icmp_type})", hop_ip)

    except socket.gaierror:
        return (f"Cannot resolve address: {target_ip}", None)


def icmp(target_ip, max_hops, timeout, verbose, icmp_id=random.randint(0, 65535)):
    try:
        packet = IP(dst=target_ip, ttl=max_hops) / ICMP(id=icmp_id, seq=max_hops)
        reply = sr1(packet, timeout=timeout, verbose=verbose)

        if reply is None:
            return (f"{max_hops}\t* * * Timeout", None)
        else:
            hop_ip = reply.src
            try:
                hop_name = socket.gethostbyaddr(hop_ip)[0]
            except socket.herror:
                hop_name = hop_ip

            if reply.haslayer(ICMP):
                icmp_type = reply[ICMP].type
                rtt = (reply.time - packet.sent_time) * 1000
                return (f"{max_hops}\t{hop_ip} ({hop_name})  {rtt:.2f} ms  (ICMP type {icmp_type}) default", hop_ip)

    except socket.gaierror:
        return (f"Cannot resolve address: {target_ip}", None)


PROTOCOLS  = {
    "U": udp,
    "T": tcp,
    "I": icmp
}


if __name__ == "__main__":
    args = parser()
    protocol, target, max_hops, timeout, verbose = PROTOCOLS[args[0]], *args[1:]
    target_ip = socket.gethostbyname(target)

    # print(protocol, target, target_ip, max_hops, timeout, verbose)
    # print(protocol(target_ip, max_hops, timeout, verbose))

    print(f"Tracing route to {target} ({target_ip}) with a maximum of {max_hops} hops:")
    for mh in range(1, max_hops+1):
        res = protocol(target_ip, mh, timeout, verbose)
        print(res[0])
        if res[1] == target_ip:
            print("  \tAddress reached!")
            break
