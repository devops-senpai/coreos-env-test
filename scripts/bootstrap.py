#setup dev
# sudo apt-get update -y && sudo apt-get install -y python-pip && sudo pip install -U pip bpython boto3

import requests
import boto3
import re

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


ec2 = boto3.resource('ec2', region_name=region)

instance = ec2.Instance(instanceId)

for i in instance.tags:
    if i['Key'] == "Role":
        instanceRole = i['Value']

instance.create_tags(
        Resources = [instanceId], 
        Tags = [
                {
                    'Key': "Name", 
                    'Value': "changed"
                }
            ])

roleIpList = []
for i in ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]):
    for d in ec2.Instance(i.id).tags:
        if d.get('Key', None) == 'Role':
            instanceList.append({ "instanceId": i.id, "role": d['Value'] })
            if d['Value'] == instanceRole:
                roleIpList.append(ec2.Instance(i.id).private_ip_address)


zoneName="dev.example.com."

dns = boto3.client('route53', region_name=region)
zones = dns.list_hosted_zones()
for zone in zones['HostedZones']:
    if zone['Name'] == zoneName:
        zoneId = zone['Id'].split("/")[-1]

roleRe = re.compile(instanceRole + '[0-9]+')
recordList= []
for aRecord in dns.list_resource_record_sets(HostedZoneId=zoneId)['ResourceRecordSets']:
    if aRecord['Type'] == 'A':
        match = roleRe.match(aRecord['Name'][:-len(zoneName)-1])
        if match:
            if aRecord['ResourceRecords'][0]['Value'] not in roleIpList:
                recordName = match.string + "." + zoneName
                createRecord(action="UPSERT", zoneId=zoneId, recordName, privateIp )
        

createRecord(action="UPSERT", zoneId=zoneId, recordName, match.string )

def createRecord(action="UPSERT", zoneId=zoneId, name, value )
# Actions are UPSERT, CREATE, DELETE
    response = dns.change_resource_record_sets(
        HostedZoneId = zoneId,
        ChangeBatch={
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': name,
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