import os
from typing import Any, Union
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from ipaddress import IPv4Network, IPv6Network
from ipaddress import ip_address, ip_network

def cast_value(value: Any, target_type:
     Union[int, float, str, datetime, IPv4Address, IPv6Address, IPv4Network, IPv6Network]
) -> Union[int, float, str, datetime, IPv4Address, IPv6Address, IPv4Network, IPv6Network]:
    if   target_type == int:
        if isinstance(value, int): return value
        else: return int(value.replace(',', ''))
    elif target_type == float: return float(value)
    elif target_type == str:   return str(value)
    elif target_type == datetime:
        if   isinstance(value, datetime): return value
        elif isinstance(value, float):
            try: return datetime.fromtimestamp(value)
            except Exception as e: raise e
        # elif isinstance(value, str):
        #     try: return datetime.fromtimestamp(float(value))
        #     except: pass
    elif target_type == Union[IPv4Address, IPv6Address]: return ip_address(value)
    elif target_type == Union[IPv4Network, IPv6Network]: return ip_network(value)
    else: return str(value)

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        print(f"Error getting file size: {e}")
        return 0
