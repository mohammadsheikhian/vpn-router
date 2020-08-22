import subprocess
import re
import time


class TestColor:
    def __init__(self):
        pass

    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING_YELLO = '\033[93m'
    FAIL_RED = '\033[91m'

    HEADER = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    ENDC = '\033[0m'


vpn_restart = 'service vpn restart'
vpn_status = 'service vpn status'


def get_packet_loss_percent():
    bash_command = "ping -c 10 1.1.1.1"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    # print(f'\nOutput: {output.decode()}')

    if 'unreachable' in output.decode().lower():
        return 100

    if len(output.decode()) == 0:
        return 100

    packet_loss = re.findall('(\d*% packet loss)', output.decode())[0]
    print(f'\nping 1.1.1.1, {packet_loss}')
    packet_loss_percent = packet_loss.replace('% packet loss', '')
    return int(packet_loss_percent)


def reset_vpn_service():
    print(f'{TestColor.BOLD}Reset the vpn service{TestColor.ENDC}')
    process = subprocess.Popen(vpn_restart.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #print(f'Output: {output.decode()}')

    while True:
        process = subprocess.Popen(vpn_restart.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
            return

        time.sleep(15)
        process = subprocess.Popen(vpn_restart.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()


def status_vpn_service():
    process = subprocess.Popen(vpn_status.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print(f'{TestColor.OK_GREEN}VPN Is Active{TestColor.ENDC}')
        return True
    else:
        print(f'{TestColor.FAIL_RED}VPN Is Inactive{TestColor.ENDC}')
        return False


while True:
    try:
        packet_loss_percent = get_packet_loss_percent()

        if packet_loss_percent > 90:
            reset_vpn_service()

        elif 75 > packet_loss_percent > 90:
            packet_loss_percent = get_packet_loss_percent()
            if packet_loss_percent > 90:
                reset_vpn_service()

        else:
            time.sleep(10)

        status = status_vpn_service()
        if status is False:
            reset_vpn_service()

    except Exception as exp:
        print(exp)
