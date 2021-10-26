import time

import comm

while True:
    comm.receive_file('./received/')
    time.sleep(5)
