# Setup CoreOS infrastructure Utilizing Fleet and Docker Swarm

The goal is to have terraform create auto-scaling groups based upon each application.

- A role will be assigned via the launch configuration
- `bootstrap.py` will inteligently create a dns record for `rolename<[0-9]+.env.domain.com`
    - the DNS name will be reflected as the instances Tag Name
    - will replace missing dns records with new ones so dns doesnt exponentially grow
    - will add a label to docker enginek
    - this will become a systemd run-once startup service. eventually container-ized

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
