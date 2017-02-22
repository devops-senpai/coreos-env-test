# Setup CoreOS infrastructure Utilizing Fleet and Docker Swarm

The goal is to have terraform create auto-scaling groups based upon each application.

- A role will be assigned via the launch configuration
- `bootstrap.py` will inteligently create a dns record for `rolename<[0-9]+.env.domain.com`
    - the DNS name will be reflected as the instances Tag Name
    - will replace missing dns records with new ones so dns doesnt exponentially grow
    - will add a label to docker enginek
    - this will become a systemd run-once startup service. eventually container-ized

### scripts / bootstrap.py

How it works:

- looks for instance tag "Role" and "Zone"
    - Role: "etcd"
    - Zone: "dev.example.com." this should be the zone attached to the VPC for private DNS

Result:

- hostname will be set to: etcd01.dev.example.com if 01 is taken by another running instance 02, 03, etc  will be used instead.
- DNS will be set to etcd01.dev.example.com using the private IP value, it will either, create update, or skip if already exists
- the instance's "Name" tag will be updated to reflect the hostname/dns record.

**Notes:**
if there are only 3 nodes with the Role "etcd" there will only be dns records for etcd01, etcd02, etcd03 as records that point to ips of instances not running will be overwritten, and non-existing records will be created.

- This should make bootstraping nodes in an autoscaling group easy and logical if you every need to scale the group up.
    - As this only runs once on startup scaling a group down could result in a non linear lineup. However this could be corrected by terminating the highest numerated node and it will come back as the next sequencial number in the group available. 

## Goal

- to have an infrastructure setup where you can take advantage of coreos's utilitizes.
- fleet could propagate new systemd services from central location.
- systemd logs for all instances are accessable from fleet as to keeps logs centralized.
- use one jumpbox to deploy docker-compose files via swarm based on docker-engine labels under placement category

## Todo

- Finish up bootstrap.py.
- create service to have all instances auto join a docker swarm
    - possibly store join token in etcd
- create `cloud_init` script to create initial services.
- come up with a way to bootstrap setting up inital etcd cluster
- create modular terraform
