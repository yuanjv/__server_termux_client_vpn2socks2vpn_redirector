import socket, subprocess, re, time
                                                                                                                                                                                                            DISC_PORT = 45454                                                                                                                                                                                           LOCAL_PORT = 1080                                                                                                                                                                                           REMOTE_PORT = 1080                                                                                                                                                                                                                                                                                                                                                                                                      current_ip = None
forward_proc = None

def stop_forward():                                                                                                                                                                                             global forward_proc
    if forward_proc and forward_proc.poll() is None:
        forward_proc.terminate()
        forward_proc.wait()
    forward_proc = None

def start_forward(ip):                                                                                                                                                                                          global forward_proc                                                                                                                                                                                         print(f"[{time.strftime('%F %T')}] forwarding localhost:{LOCAL_PORT} -> {ip}:{REMOTE_PORT}")                                                                                                                forward_proc = subprocess.Popen(
        ["socat", f"TCP-LISTEN:{LOCAL_PORT},reuseaddr,fork", f"TCP:{ip}:{REMOTE_PORT}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                                                                                                                     sock.bind(('', DISC_PORT))
buffer = b''

while True:
    data, _ = sock.recvfrom(1024)
    buffer += data
    # extract every sequence of digits+dots (handles concatenated IPs)
    for match in re.findall(rb'[\d\.]+', buffer):
        ip = match.decode()
        if ip != current_ip:
            if current_ip:
                stop_forward()
            current_ip = ip
            start_forward(current_ip)
    buffer = b''
    time.sleep(0.01)
