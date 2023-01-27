#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import dns.resolver
from dns import reversename
from collections import OrderedDict

from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators


resolver = dns.resolver.Resolver()
cache = OrderedDict()
CACHE_LIMIT = 100

def dnslookup(query, record_type = 'A'):
    record_type=record_type.upper()
    try:
        record_type = record_type.upper()
        if record_type == 'PTR' or record_type=='REVERSE':
            record_type = 'PTR'
            try:
                query = reversename.from_address(query)
            except:
                pass
        elif record_type=='FORWARD':
            record_type = 'A'
        answer = resolver.resolve(query, record_type)
        answers = []
        if hasattr(answer, 'rrset'):
            for a in answer.rrset:
                b = a.to_text()
                # Dot record is identical to the query
                if b == ".":
                    b = query
                if b[-1] == '.':
                    b = b[0:-1]
                answers.append(b)
            return answers
        else:
            return ["Error:NoResults"]
    except dns.resolver.NoAnswer:
        sys.stderr.write("No answer: " + str(query) + "\n")
        return ["Error:NoAnswer"]
    except dns.resolver.NXDOMAIN:
        sys.stderr.write("Does not resolve: " + str(query) + "\n")
        return ["Error:NXDOMAIN"]
    except BaseException as e:
        sys.stderr.write("query=" + query + " error=\"" + str(e) + "\"\n")
        return ["Error:"+str(e)]


def cache_lookup(input,search_type):
    if input in cache:
        return cache[input]
    else:
        result = dnslookup(input, record_type=search_type)
        if len(cache) >= CACHE_LIMIT:
            ignore=cache.popitem(last=False)
        cache[input] = result
        return result



@Configuration()
class DnslookupCommand(StreamingCommand):
    """ %(synopsis)

    ##Syntax

    .. code-block::
        dnslookup  (recordtype=<string>) (input_field=<string>) | (output_field=<string>) | (search_suffix=<string>)*
                    
    ##Description

    This streaming command resolves the host/ip or other string in from 
    input_field in the data and outputs to output_field using the 
    custom server and search suffix provided.

    ##Example

    This example resolves the name "www" using the first domain in the suffix 
    list (google.com), and using the name servers in the server list.

    ..code-block::
            "| makeresults 
             | eval hostname = "www",
               ip = "4.2.2.2",
               _raw = "www.google.com,4.2.2.2"
             | dnslookup recordtype="FORWARD" input_field=hostname 
               output_field="xyz"  search_suffix="google.com,yahoo.com
               server=8.8.8.8,8.8.4.4""
    """
    recordtype = Option(
        doc='''
        **Syntax:** **recordtype=** *A|PTR|forward|reverse|MX*
        **Description:** Type of dns record being requested''',
        require=True, validate=validators.Fieldname())
    input_field = Option(
        doc='''
        **Syntax:** **input_field=** *<fieldname>*
        **Description:** Name of the field that holds the input value to be looked up''',
        require=True, validate=validators.Fieldname())
    output_field = Option(
        doc='''
        **Syntax:** **output_field=** *<fieldname>*
        **Description:** Name of the field that will result of the command''',
        require=True, validate=validators.Fieldname())
    server = Option(
        doc='''
        **Syntax:** **server=** *hostname|IPv4|IPv6*
        **Description:** Custom DNS resolver to use ''',
        require=False)
    search_suffix = Option(
        doc='''
        **Syntax:** **server=** *server|IPv4|IPv6*
        **Description:** Comma separated list of DNS search suffix to use to resolve relative hostnames ''',
        require=False)

    def stream(self, events):
        # Put your event transformation code here
        if self.server:
            dns_servers = self.server.split(',')
            resolver.nameservers = dns_servers
        resolver.timeout = 2.5
        resolver.lifetime = 2.5
        if self.search_suffix:
            resolver.search = [dns.name.from_text(s) for s in self.search_suffix.split(',')]
            resolver.use_search_by_default = True

        for event in events:
            if self.input_field and self.output_field:
                event[self.output_field] = cache_lookup(event[self.input_field], self.recordtype)
            yield event

dispatch(DnslookupCommand, sys.argv, sys.stdin, sys.stdout, __name__)
