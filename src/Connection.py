from typing import Dict
from dataclasses import dataclass
from hashlib import sha1

@dataclass
class BaseConnection:
    proto: str
    recvQ: int
    sendQ: int
    localSocket: str
    remoteSocket: str

    def _process_socket(self, socket_attr, socket_str, socket_location) -> None:
        address = '.'.join(socket_str.split('.')[:-1])
        port = socket_str.split('.')[-1]
        if socket_str != '*.*':
            setattr(self, socket_attr, f"{address}:{port}")
            setattr(self, f"{socket_location}Addr", address)
            setattr(self, f"{socket_location}Port", int(port))
        else:
            setattr(self, socket_attr, '*:*')
            setattr(self, f"{socket_location}Addr", address)
            setattr(self, f"{socket_location}Port", 0)

    def _convert_to_int(self, *attributes) -> None:
        for attribute in attributes:
            setattr(self, attribute, int(getattr(self, attribute)))

    def __post_init__(self) -> None:
        self._convert_to_int('recvQ', 'sendQ', 'pid', 'epid', 'rhiwat', 'shiwat')
        self.family = 4 if self.proto.endswith('4') else 6
        self.proto = ''.join(char for char in self.proto if char.isalpha())
        self._process_socket("localSocket", self.localSocket, "local")
        self._process_socket("remoteSocket", self.remoteSocket, "remote")

    @property
    def as_dict(self) -> Dict:
        return self.__dict__

    def to_dict(self) -> Dict:
        '''Returns the minimal representation of the Connection
        object for further processing (storing/comparison)'''
        connection_dict = {
            'pid': self.pid,
            'family': self.family, 'proto': self.proto,
            'localAddr': self.localAddr, 'localPort': self.localPort,
            'remoteAddr': self.remoteAddr, 'remotePort': self.remotePort
        }
        if self.proto == 'tcp':
            connection_dict['state'] = self.state
        connection_dict['state_str'] = self.state_str
        
        return connection_dict

    @property
    def connection_hash(self):
        '''Generate a hash for the object based on its attributes'''
        hash_obj = sha1()
        hash_obj.update(str(self.to_dict()).encode('utf-8'))
        return hash_obj.hexdigest()

@dataclass
class TCP_State():
    state: str

@dataclass
class Common_Connection_properties_and_metrics():
    rhiwat: int
    shiwat: int
    pid: int
    epid: int
    state_str: str
    options: str
    gencnt: str
    flags: str
    flags1: str
    usscnt: int
    rtncnt: int
    fltrs: int
    family: int = None
    localAddr: str = None
    localPort: int = None
    remoteAddr: str = None
    remotePort: int = None

@dataclass
class TCP_Connection(Common_Connection_properties_and_metrics, TCP_State, BaseConnection):
    '''Defined by inheritance'''
    ...

@dataclass
class UDP_Connection(Common_Connection_properties_and_metrics, BaseConnection):
    '''Defined by inheritance'''
    ...
