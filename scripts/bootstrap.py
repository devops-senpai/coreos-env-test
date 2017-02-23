"""Bootstrap instance for name and hostname and dns."""
import requests
import boto3
import re
from subprocess import call

"""
setup run: sudo apt-get update -y && sudo apt-get install -y python-pip && \
sudo pip install -U pip bpython boto3.
"""


def getrole(instance):
    """Return the role of the instance."""
    for i in instance.tags:
        if i['Key'] == "Role":
            return i['Value']


def getzone(instance):
    """Get zone the instance is in."""
    for i in instance.tags:
        if i['Key'] == "Zone":
            return i['Value']


def activeroleips(instancerole):
    """Get ips of other instances with same role."""
    roleiplist = []
    for i in ec2.instances.filter(Filters=[{'Name': 'instance-state-name',
                                  'Values': ['running']}]):
        for d in ec2.Instance(i.id).tags:
            if d.get('Key', None) == 'Role':
                if d['Value'] == instanceRole:
                    roleiplist.append(ec2.Instance(i.id).private_ip_address)
    return roleiplist


def getzoneid(zonename):
    """Get id of zone."""
    zones = dns.list_hosted_zones()
    for zone in zones['HostedZones']:
        if zone['Name'] == zoneName:
            return zone['Id'].split("/")[-1]


def rolerecords(zoneid, zonename, roleiplist):
    """Return records that match the role."""
    rolere = re.compile(instanceRole + '[0-9]+')
    d = {}
    for arecord in dns.list_resource_record_sets(
            HostedZoneId=zoneId)['ResourceRecordSets']:
        if arecord['Type'] == 'A':
            match = rolere.match(arecord['Name'][:-len(zoneName) - 1])
            if match:
                d.update({match.string: arecord['ResourceRecords'][0]['Value']}
                         )
                if arecord['ResourceRecords'][0]['Value'] not in roleIpList:
                    d[match.string] = None
    return d


def doesrecordexist(rolerecordsdict, privateip):
    """Check if record exists."""
    for k, v in roleRecordsDict.iteritems():
        if v == privateIp:
            return k
        else:
            return None


def newrecordname(sortedrecords, rolerecordsdict, zonename, instancerole):
    """Create new record name."""
    if not sortedrecords:
        return instancerole + "01" + '.' + zonename
    for record in sortedrecords:
        if not rolerecordsdict[record]:
            recordname = record + '.' + zonename
            return recordname
    newrecord = instanceRole + str(int(
                                   sortedrecords[-1].lstrip(instanceRole)
                                   ) + 1).zfill(2)
    return newrecord


def updaterecord(zonename, recordname, rolerecordsdict, zoneid, privateip):
    """Update DNS record."""
    if recordname.rstrip('.' + zonename) in rolerecordsdict.keys():
        createrecord("UPSERT", zoneid, recordname, privateip)
    else:
        createrecord("CREATE", zoneid, recordname, privateip)


def updatename(recordname):
    """Update instance name."""
    instance.create_tags(
        Resources=[instanceId],
        Tags=[
            {
                'Key': "Name",
                'Value': recordName.rstrip('.')
            }
        ])


def sethostname(recordname):
    """Set instance hostname."""
    retval = call(["hostnamectl", "set-hostname", recordName.rstrip('.')])
    return retval


def createrecord(action, zoneid, recordname, value):
    """Create DNS record."""
    dns.change_resource_record_sets(
        HostedZoneId=zoneId,
        ChangeBatch={
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': recordName,
                        'Type': 'A',
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': value
                            },
                        ],
                    }
                },
            ]
        }
    )

r = requests.get(
    'http://169.254.169.254/latest/meta-data/placement/availability-zone')
region = r.text[:-1]
r = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
instanceId = r.text
r = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4')
privateIp = r.text
r = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
if r.status_code == 200:
    publicIp = r.text
else:
    publicIp = None

ec2 = boto3.resource('ec2', region_name=region)

dns = boto3.client('route53', region_name=region)

instance = ec2.Instance(instanceId)

instanceRole = getrole(instance)

zoneName = getzone(instance)

roleIpList = activeroleips(instanceRole)

zoneId = getzoneid(zoneName)

roleRecordsDict = rolerecords(zoneId, zoneName, roleIpList)

if doesrecordexist(roleRecordsDict, privateIp):
    recordName = doesrecordexist(roleRecordsDict, privateIp) + '.' + zoneName
else:
    sortedrecords = sorted(roleRecordsDict.keys())
    recordname = newrecordname(sortedrecords,
                               roleRecordsDict,
                               zoneName,
                               instanceRole)
    updaterecord(zoneName, recordName, roleRecordsDict, zoneId, privateIp)

updatename(recordName)

if sethostname(recordName) != 0:
    print("ERROR: unable to set hostname")
