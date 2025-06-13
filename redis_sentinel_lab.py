from redis.sentinel import Sentinel
from redis.exceptions import ConnectionError, TimeoutError

def get_master_node(_tuple_list, _master_name, _timeout=5):
    # load tuple list 
    sentinel = Sentinel(_tuple_list)
    # discover which node in tuple list is the current master node
    master_ip, master_port = sentinel.discover_master(_master_name)
    # create connection object and check master availability
    master_conn = sentinel.master_for(_master_name, socket_timeout=_timeout)
    master_conn.ping()
    # return master node ip and port number
    if master_conn.ping():
        return master_ip, master_port
    return True


if __name__ == "__main__":

    try:
        # set hosts in tuple list
        sentinel_tuple_list = [('redis-1', 26379), ('redis-2', 26379), ('redis-3', 26379)]
        # set master name in redis-sentinel cluster
        master_name = "xlabs"
        host_ip, host_port = get_master_node(sentinel_tuple_list, master_name)
        if host_ip and host_port:
            print(host_ip, host_port)

    except (ConnectionError, TimeoutError) as err:
        print(err)
