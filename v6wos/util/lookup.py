import dns.resolver
import dns.exception


NAMESERVERS = ["8.8.8.8", "8.8.4.4"]


def check_aaaa(host):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = NAMESERVERS
    try:
        return [i.address.decode() for i in resolver.query(host, 'AAAA')]
    except dns.exception.DNSException:
        return []
