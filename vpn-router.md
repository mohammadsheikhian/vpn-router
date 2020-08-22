https://thepi.io/how-to-use-your-raspberry-pi-as-a-vpn-router/
https://pimylifeup.com/raspberry-pi-vpn-access-point/

# How to use your Raspberry Pi as a wireless access point
The Raspberry Pi can do a lot, especially now that the new Raspberry Pi comes with wireless capabilities already on board. It can take the place of a ton of different (and more expensive) devices – including a router! If you turn your Raspberry Pi into a wireless access point, you can make it act as a router. It’s not the most powerful thing in the world, but it does work, and the project is a lot of fun.

We’re going to get into the command line a bit here, but this project isn’t really all that difficult. All we’re really doing is using Raspbian and installing a couple packages that give the Pi the ability to do router-like things like assign IP addresses to devices that connect to it.

---

## Step 1: Install and update Raspbian
Check out our complete guide to installing Raspbian for the details on this one. Then plug everything in and hop into the terminal and check for updates and ugrades:
```
sudo apt-get update
sudo apt-get upgrade
```
If you get an upgrade, It’s a good idea to reboot with sudo reboot.

## Step 2: Install hostapd and dnsmasq
These are the two programs we’re going to use to make your Raspberry Pi into a wireless access point. To get them, just type these lines into the terminal:
```
sudo apt-get install hostapd
sudo apt-get install dnsmasq
```
Both times, you’ll have to hit y to continue. hostapd is the package that lets us create a wireless hotspot using a Raspberry Pi, and dnsmasq is an easy-to-use DHCP and DNS server.

We’re going to edit the programs’ configuration files in a moment, so let’s turn the programs off before we start tinkering:
```
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
```

## Step 3: Configure a static IP for the wlan0 interface
For our purposes here, I’m assuming that we’re using the standard home network IP addresses, like 192.168.###.###. Given that assumption, let’s assign the IP address 192.168.0.10 to the wlan0 interface by editing the dhcpcd configuration file. Start editing with this command:
```
sudo vim /etc/dhcpcd.conf
```
Now that you’re in the file, add the following lines at the end:
```
interface wlan0
    static ip_address=192.168.220.1/24
    nohook wpa_supplicant
```
Now we need to restart our dhcpd service so it will load in all our configuration changes. To do this run the following command to reload the dhcpd service.
```
sudo systemctl restart dhcpcd
```

## Step 4: Configure the DHCP server (dnsmasq)
We’re going to use dnsmasq as our DHCP server. The idea of a DHCP server is to dynamically distribute network configuration parameters, such as IP addresses, for interfaces and services.

dnsmasq’s default configuration file contains a lot of unnecessary information, so it’s easier for us to start from scratch. Let’s rename the default configuration file and write a new one:

```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo vim /etc/dnsmasq.conf
```

You’ll be editing a new file now, and with the old one renamed, this is the config file that dnsmasq will use. Type these lines into your new configuration file:

```
interface=wlan0                 # Use interface wlan0  
server=1.1.1.1                  # Use Cloudflare DNS  
dhcp-range=192.168.220.50,192.168.220.150,12h   # IP range and lease time  
```

The lines we added mean that we’re going to provide IP addresses between 192.168.0.11 and 192.168.0.30 for the wlan0 interface.

## Step 5: Configure the access point host software (hostapd)
Another config file! This time, we’re messing with the hostapd config file. Open ‘er up:

```
sudo vim /etc/hostapd/hostapd.conf
```

This should create a brand new file. Type in this:

```
interface=wlan0
driver=nl80211

hw_mode=g
channel=6
ieee80211n=1
wmm_enabled=0
macaddr_acl=0
ignore_broadcast_ssid=0

auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

# This is the name of the network
ssid=Pi3-AP
# The network passphrase
wpa_passphrase=pimylifeup
```

Note that where I have “NETWORK” and “PASSWORD,” you should come up with your own names. This is how you’ll join the Pi’s network from other devices.

We still have to show the system the location of the configuration file:

```
sudo vim /etc/default/hostapd
```

In this file, track down the line that says #DAEMON_CONF=”” – delete that # and put the path to our config file in the quotes, so that it looks like this:

```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

The # keeps the line from being read as code, so you’re basically bringing this line to life here while giving it the right path to our config file.

Now we need to edit the second configuration file, this file is located within the init.d folder. We can edit the file with the following command:
```
sudo nano /etc/init.d/hostapd
```
In this file, we need to find the following line and replace it.
Find:
```
DAEMON_CONF= 
```
Replace with:
```
DAEMON_CONF=/etc/hostapd/hostapd.conf
```
## Step 6: Set up traffic forwarding
The idea here is that when you connect to your Pi, it will forward the traffic over your Ethernet cable. So we’re going to have wlan0 forward via Ethernet cable to your modem. This involves editing yet another config file:

```
sudo vim /etc/sysctl.conf
```

Now find this line:

```
#net.ipv4.ip_forward=1
```
…and delete the “#” – leaving the rest, so it just reads:

```
net.ipv4.ip_forward=1
```

## Step 7: Add a new iptables rule
Next, we’re going to add IP masquerading for outbound traffic on eth0 using iptables:

**Internet router:**
```bash
sudo iptables -F
sudo iptables -t nat -F
sudo iptables -X
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

**VPN router:**
```bash
sudo iptables -F
sudo iptables -t nat -F
sudo iptables -X
sudo iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE
sudo iptables -A FORWARD -i tun0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o tun0 -j ACCEPT
```
…and save the new iptables rule:

```
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```
To load the rule on boot, we need to edit the file /etc/rc.local and add the following
line just above the line exit 0:
```
sudo vim  /etc/rc.local
iptables-restore < /etc/iptables.ipv4.nat
```

## Step 8: Reboot

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl restart hostapd
sudo systemctl restart dnsmasq
```
Now that we’re ready, let’s reboot with sudo reboot.

Now your Pi should be working as a wireless access point. Try it out by hopping on another device and looking for the network name you used back in step 5.
