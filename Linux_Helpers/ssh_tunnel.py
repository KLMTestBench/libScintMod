import os
import base64
import paramiko
from sshtunnel import SSHTunnelForwarder


def get_port(host):
  if hasattr(host, 'port'):
    return host.port

  return 22



def ssh_tunnel_impl(host1,host2,new_port):
  tunnel1 =  SSHTunnelForwarder(
    (host1.HostName, get_port(host1)),
    ssh_username=host1.UserName,
    ssh_password=host1.PassWord,
    remote_bind_address=(host2.HostName, 22),
    local_bind_address=('0.0.0.0', new_port)
  )
  tunnel1.__enter__()

  host2.HostName="127.0.0.1"
  host2.port=new_port
  return (host2,tunnel1)


def ssh_tunnel(path,target):

    tunnels = []
    for i in range(0,len(path)-2):
        h1 =  path[i]
        h2 =  path[i+1]
        new_port = max(10050,get_port(h1)+1)
        (host2 , tunnel)=  ssh_tunnel_impl(h1,h2,new_port)
        tunnels.append(tunnel)

    i = len(path)-2
    h1 =  path[i]
    h2 =  path[i+1]
    (host2 , tunnel)=  ssh_tunnel_impl(h1,h2,target.port)



