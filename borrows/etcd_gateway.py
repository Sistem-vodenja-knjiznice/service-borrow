import subprocess, os

def get_etcd_key(key):
    host = os.getenv('ETCD_HOST')
    port = os.getenv('ETCD_PORT')
    username = os.getenv('ETCD_USERNAME')
    password = os.getenv('ETCD_PASSWORD')

    command = f'etcdctl --endpoints=http://{host}:{port} --user={username}:{password} get {key}'

    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result.stdout.decode('utf-8').split('\n')[1] if result.stdout else None
