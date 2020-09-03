# **OpenVPN**

### Installation openVPN

```shell script
sudo echo "deb http://build.openvpn.net/debian/openvpn/release/2.4 xenial main" > /etc/apt/sources.list.d/openvpn-aptrepo.list
sudo apt-get update
sudo apt-get install openvpn
```

### Update openVPN

**How to upgrade OpenVPN version 2.3 to 2.4 on Debian/Ubuntu**

There are are some important security updates are done with the OpenVPN version
2.4 compared with 2.3. So if you are using the old version, you can upgrade it
to 2.4 by keeping the current configurations including the files, certificates,
and other settings. 

Here I am providing the steps to do the upgrade:

Backup the current configuration files for safety. 
Check the current version using the command:
```shell script
openvpn --version
```

Import the public GPG key that is used to sign the packages:
```shell script
wget -O - https://swupdate.openvpn.net/repos/repo-public.gpg|apt-key add -
```

Create a new source list to find the updated OpenVPN packages:
```shell script
echo "deb http://build.openvpn.net/debian/openvpn/<version> <osrelease> main" > /etc/apt/sources.list.d/openvpn-aptrepo.list 
```

Where the <version> can be one of the following:

+ **stable**: stable releases only - no alphas, betas or RCs
+ **testing**: latest releases, including alphas/betas/RCs
+ **release/2.3**: OpenVPN 2.3 releases
+ **release/2.4**: OpenVPN 2.4 releases, including alphas/betas/RCs

Replace **<osrelease>** with the required one from the above list.
The area **<osrelease>** depends your distribution:

+ **wheezy**
+ **jessie**
+ **precise**
+ **trusty**
+ **xenial**

You can check it from your OS and use the appropriate one.

```shell bash
echo "deb http://build.openvpn.net/debian/openvpn/stable xenial main" > /etc/apt/sources.list.d/openvpn-aptrepo.list
```
Run an update.
```shell bash
apt-get update
```
The upgrade the OpenVPN package:
```shell bash
apt install -y openvpn
```
or
```shell bash
apt-get --only-upgrade install openvpn
```
Once the upgrade is done, please verify the new version and also check if
   the old configurations are still there.

