import dns.query
import dns.zone
import dns.resolver

class HostARecords:
    def __init__(self, dns_server, zone_name):
        self.dns_server = dns_server
        self.zone_name = zone_name

    def fetch_records(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.dns_server]
        zone = dns.zone.from_xfr(dns.query.xfr(self.dns_server, self.zone_name))

        host_a_records = []

        for name, node in zone.nodes.items():
            rdatasets = node.rdatasets
            for rdataset in rdatasets:
                if rdataset.rdtype == dns.rdatatype.A:
                    for record in rdataset:
                        host_a_records.append({"IPv4Address": str(record),"Hostname": str(name),} )

        return host_a_records
