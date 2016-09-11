import dns.resolver
import dns.exception


DEFAULT_NAMESERVERS = ["8.8.8.8", "8.8.4.4"]


def check_aaaa(host, nameservers=None):
    if nameservers is None:
        nameservers = DEFAULT_NAMESERVERS
    resolver = dns.resolver.Resolver()
    resolver.nameservers = nameservers
    try:
        return [i.address.decode() for i in resolver.query(host, 'AAAA')]
    except dns.exception.DNSException:
        return []
