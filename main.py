import start
import util
from time import sleep

if __name__ == "__main__":

    while(True):
        try:
            start.run()
        except:
            util.log_exception()
            sleep(1)
            pass