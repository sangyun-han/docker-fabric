# Docker Image for CORD Fabric Emulation

A docker image that allows us to emulate a [CORD](http://opencord.org) Fabric data plane easily.

## Quickstart
* Modify controller IP address in `docker-compose.yml`
* Run `docker-compose run fabric`

## Reference
* [Tutorial](https://wiki.onosproject.org/display/ONOS/Software+Switch+Installation+Guide) - How to setup ONOS
* [Network Config](https://github.com/opennetworkinglab/onos/blob/master/tools/package/config/samples/network-cfg-fabric-2x2-min.json) for the 2x2 leaf-spine topology generated by this docker image

## TODO
* Support mutiple controllers
