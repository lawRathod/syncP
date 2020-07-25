import sys
import host, client, testmpv

def main(opt):
    if opt=="host":
        host.run()
    elif opt=="client":
        client.run()
    elif opt=="test":
        testmpv.run()
    else:
        print("use host/client/test as a parameter")


if __name__ == "__main__":
    args = sys.argv
    if len(args)==2:
        main(args[1])
    else:
        print("Pass host/client/test as a parameter")
