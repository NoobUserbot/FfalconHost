# Server distribution support for MH

import aiohttp as areq
import MHoperator as op
import asyncio
import requests

slows_p = 'verlangsamung.json'
main_p = 'haupt.json'
masters_p = 'meister.json'
servrmap_p = 'serverkarte.json'

class ConnectionError(Exception):
    pass

class Server:
    def __init__(self, url: str, master: str):
        """
        Makes a Server object to perform actions with API.
        :param url: URL of the server
        :param master: Master key of the server
        """
        self.url = url
        self.master = master

        try:
            r = requests.get(f'{url}/pingme', params={'key': master})
        except:
            raise ConnectionError('Server not reachable')
        
        if list(r.json().keys()) != ['OK']:
            if r.json()['error'][0] == 401:
                raise ConnectionError('Master key is wrong')
            else:
                raise ConnectionError('Server is not a FH server')
        
        self.version = r.json()['OK'][1]
    
    def __repr__(self):
        return f'<Server {self.url} (FH {self.version})>'
    
    def __str__(self):
        return self.url
    
    async def install(self, recepient: int, port: int) -> bool | dict:
        """
        Installs FH on a server.
        :param recepient: ID of the recepient
        :param port: Port of the server
        :return: True if installed, dict if error
        """
        async with areq.ClientSession() as session:
            async with session.get(f'{self.url}/fhapi/scontrols/install/{recepient}', params={'key': self.master, 'port': port}) as r:
                dictionary = await r.json()
                if 'OK' in dictionary.keys():
                    return True
                else:
                    return dictionary
    
    
    async def uninstall(self, recepient: int) -> bool | dict:
        """
        Uninstalls FH from a server.
        :param recepient: ID of the recepient
        :return: True if uninstalled, dict if error
        """
        async with areq.ClientSession() as session:
            async with session.get(f'{self.url}/fhapi/scontrols/uninstall/{recepient}', params={'key': self.master}) as r:
                dictionary = await r.json()
                if 'OK' in dictionary.keys():
                    return True
                else:
                    return dictionary
    

    async def start(self, recepient: int) -> bool | dict:
        """
        Starts FH on a server.
        :param recepient: ID of the recepient
        :return: True if started, dict if error
        """
        async with areq.ClientSession() as session:
            async with session.get(f'{self.url}/fhapi/scontrols/start/{recepient}', params={'key': self.master}) as r:
                dictionary = await r.json()
                if 'OK' in dictionary.keys():
                    return True
                else:
                    return dictionary
    

    async def stop(self, recepient: int) -> bool | dict:
        """
        Stops FH on a server.
        :param recepient: ID of the recepient
        :return: True if stopped, dict if error
        """
        async with areq.ClientSession() as session:
            async with session.get(f'{self.url}/fhapi/scontrols/stop/{recepient}', params={'key': self.master}) as r:
                dictionary = await r.json()
                if 'OK' in dictionary.keys():
                    return True
                else:
                    return dictionary
    

    async def restart(self, recepient: int) -> bool | dict:
        """
        Restarts FH on a server.
        :param recepient: ID of the recepient
        :return: True if restarted, dict if error
        """
        async with areq.ClientSession() as session:
            async with session.get(f'{self.url}/fhapi/scontrols/restart/{recepient}', params={'key': self.master}) as r:
                dictionary = await r.json()
                if 'OK' in dictionary.keys():
                    return True
                else:
                    return dictionary
    