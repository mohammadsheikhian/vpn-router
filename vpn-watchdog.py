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


def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error, process.returncode


def get_packet_loss_percent():
    output, error, return_code = run_command(command="ping -c 10 1.1.1.1")

    if 'unreachable' in output.lower():
        return 100

    if len(output) == 0:
        return 100

    packet_loss = re.findall('(\d*% packet loss)', output)[0]
    print(f'\nping 1.1.1.1, {packet_loss}')
    return int(packet_loss.replace('% packet loss', ''))


def reset_vpn_service():
    print(f'{TestColor.BOLD}Reset the vpn service{TestColor.ENDC}')
    while True:
        output, error, return_code = run_command(command='service vpn restart')
        if return_code == 0:
            return

        time.sleep(15)


def status_vpn_service():
    output, error, return_code = run_command(command='service vpn status')
    if return_code == 0:
        print(f'{TestColor.OK_GREEN}VPN Is Active{TestColor.ENDC}')
        return True

    else:
        print(f'{TestColor.FAIL_RED}VPN Is Deactive{TestColor.ENDC}')
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
