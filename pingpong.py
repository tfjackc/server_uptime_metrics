from dataclasses import asdict
from ping_dataclass import ServerStatus
from datetime import datetime
import subprocess
import re
import pandas as pd
from database import append_table

ipaddresses = {
    'name': 'ipaddress',
    'name2': 'ipaddress2',
}
server = 'instance\server'
database = 'database'
trusted_conn = 'yes'
status_dicts = []


def ping_server(name, hostname):
    result = subprocess.run(['ping', hostname], stdout=subprocess.PIPE)
    cleaned_output = result.stdout.decode('utf-8').splitlines()

    for line in cleaned_output[2:6]:
        if "Destination host unreachable" in line:
            status = ServerStatus(name=name,
                                  ipaddress=hostname,
                                  byte_value=0,
                                  time="0ms",
                                  ttl=0,
                                  timestamp=datetime.now(),
                                  status='DOWN')

            status_dict = asdict(status)
            status_dicts.append(status_dict)
            continue
        else:
            byte_value = 0
            time_value = "0ms"
            ttl_value = 0

            split_line = line.partition(':')[2].strip().split()

            for rows in split_line:
                key, operator, value = re.split(r'([=<>])', rows)

                if key == 'bytes':
                    byte_value = int(value)
                elif key == 'time':
                    time_value = value
                elif key == 'ttl':
                    ttl_value = int(value)

            status = ServerStatus(
                name=name,
                ipaddress=hostname,
                byte_value=byte_value,
                time=time_value,
                ttl=ttl_value,
                timestamp=datetime.now(),
                status='UP'
            )
            status_dicts.append(asdict(status))

    df = pd.DataFrame(status_dicts)
    append_table(server, database, trusted_conn, 'dbo.server_uptime', df)


if __name__ == '__main__':
    for key, value in ipaddresses.items():
        ping_server(key, value)



