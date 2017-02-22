#setup dev
# sudo apt-get update -y && sudo apt-get install -y python-pip && sudo pip install -U pip bpython boto3

import requests
import boto3
import re
from subprocess import call

def getRole(instance):
    for i in instance.tags:
        if i['Key'] == "Role":
            return i['Value']

def activeRoleIps(instanceRole):
    roleIpList = []
    for i in ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]):
        for d in ec2.Instance(i.id).tags:
            if d.get('Key', None) == 'Role':
                if d['Value'] == instanceRole:
                    roleIpList.append(ec2.Instance(i.id).private_ip_address)
    return roleIpList

def getZoneId(zoneName):
    zones = dns.list_hosted_zones()
    for zone in zones['HostedZones']:
        if zone['Name'] == zoneName:
            return zone['Id'].split("/")[-1]


def roleRecords(zoneId, zoneName, roleIpList):
    d = {}
    for aRecord in dns.list_resource_record_sets(HostedZoneId=zoneId)['ResourceRecordSets']:
        if aRecord['Type'] == 'A':
            match = roleRe.match(aRecord['Name'][:-len(zoneName)-1])
            if match:
                d.update({ match.string: aRecord['ResourceRecords'][0]['Value'] })
                if aRecord['ResourceRecords'][0]['Value'] not in roleIpList:
                    d[match.string] = None
    return d

def newRecordName(sortedRecords, roleRecordsDict, zoneName, instanceRole):
    if not sortedRecords:
        return instanceRole + "01" + '.' + zoneName
    for record in sortedRecords:
        if roleRecordsDict[record] == None:
            recordName = record + '.' + zoneName
            return recordName
    newRecord = instanceRole + str(int(sortedRecords[-1].lstrip(instanceRole)) + 1).zfill(2)
    return newRecord

def updateRecord(recordName, roleRecordsDict, zoneId, privateIp):
    if recordName.rstrip('.' + zoneName) in roleRecordsDict.keys():
        createRecord("UPSERT", zoneId, recordName, privateIp)
    else:
        createRecord("CREATE", zoneId, recordName, privateIp)

def updateName(recordName):
    instance.create_tags(
            Resources = [instanceId], 
            Tags = [
                    {
                        'Key': "Name", 
                        'Value': recordName
                    }
                ])

def setHostname(recordName):
    retval = call(["hostnamectl", "set-hostname", recordName.rstrip('.')])
    return retval

def createRecord(action, zoneId, recordName, value ):
    response = dns.change_resource_record_sets(
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

r = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone')
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

zoneName = "dev.example.com."

ec2 = boto3.resource('ec2', region_name=region)

dns = boto3.client('route53', region_name=region)

instance = ec2.Instance(instanceId)

instanceRole = getRole(instance)

roleIpList = activeRoleIps(instanceRole)

zoneId = getZoneId(zoneName)

roleRe = re.compile(instanceRole + '[0-9]+')

roleRecordsDict = roleRecords(zoneId, zoneName, roleIpList)
sortedRecords = sorted(roleRecordsDict.keys())

recordName = newRecordName(sortedRecords, roleRecordsDict, zoneName, instanceRole)

updateRecord(recordName, roleRecordsDict, zoneId, privateIp)

updateName(recordName)

if setHostname(recordName) != 0:
    print("ERROR: unable to set hostname")
