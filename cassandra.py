#!/opt/mm-agent/python/bin/python
import sys
import re
import subprocess
from subprocess import PIPE

nodetool_host = None
try:
    nodetool_host = os.environ['NODETOOL_HOST']
except:
    pass

processAndArgs = ['nodetool', 'cfstats']
if nodetool_host:
    processAndArgs = ['nodetool', '-h', nodetool_host, 'cfstats']

try:
    p = subprocess.Popen(processAndArgs, stdout=PIPE)
except:
    sys.stderr.write("FATAL: Failed to run 'nodetool cfstats'. Maybe it's not installed?\n")
    sys.exit(1)
ks = {}
tables = {}
lineregex = re.compile("([\w\s]+?)\s*?:\s*?([\w\.]+)")
current_ks = None
current_table = None
counter_keys = [
    'read_count',
    'write_count',
    'local_read_count',
    'local_write_count',
]

for line in p.stdout.readlines():
    line = line.strip()
    
    matches = lineregex.search(line)
    if matches:
        keyname = matches.group(1).lower().replace(' ', '_')
        value = matches.group(2)

        if keyname == 'keyspace':
            if not value.startswith('system'):
                current_ks = value
                ks[current_ks] = {}
                tables[current_ks] = {}
            else:
                current_ks = None
            current_table = None
            continue

        if not current_ks:
            continue

        if keyname == 'table':
            if not value.startswith('role'):
                current_table = value
                tables[current_ks][current_table] = {}
            else:
                current_table = None
            continue

        if not current_table:
            ks[current_ks][keyname] = value
        else:
            tables[current_ks][current_table][keyname] = value

for keyspace, data in ks.iteritems():
    for metric, value in data.iteritems():
        if metric in counter_keys:
            metric_prefix = '_counter.'
        else:
            metric_prefix = ''
        print "%scassandra.cfstats.%s.%s: %s" % (
                metric_prefix, keyspace, metric, value)

for keyspace, tabledata in tables.iteritems():
    for table, data in tabledata.iteritems():
        for metric, value in data.iteritems():
            if metric in counter_keys:
                metric_prefix = '_counter.'
            else:
                metric_prefix = ''
            print "%scassandra.cfstats.%s.%s.%s: %s" % (
                    metric_prefix, keyspace, table, metric, value)

p.wait()

try:
    p = subprocess.Popen(['nodetool', 'compactionstats'], stdout=PIPE)
except:
    sys.exit(0)

for line in p.stdout.readlines():
    matches = re.search(r'^pending tasks:\s+(\d+)', line)
    if matches:
        print "cassandra.pending_tasks:", matches.group(1)
p.wait()

