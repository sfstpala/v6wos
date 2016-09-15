
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


def check_glue(host, nameservers=None):
    if nameservers is None:
        nameservers = DEFAULT_NAMESERVERS
    resolver = dns.resolver.Resolver()
    resolver.nameservers = nameservers
    try:
        ns = [i.to_text() for i in resolver.query(host, 'NS')]
    except dns.exception.DNSException:
        ns = []
    result = []
    for i in ns:
        result.extend(check_aaaa(i, nameservers=nameservers))
    return result
