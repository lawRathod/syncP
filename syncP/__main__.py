import argparse
from syncP import host, client, testmpv

def main(opt, port=3456):
    if opt=="host":
        host.run(port)
    elif opt=="client":
        client.run()
    elif opt=="test":
        testmpv.run()
    else:
        print("use host/client/test as a parameter")


def run():
    parser = argparse.ArgumentParser(description="Local media sync tool.")
    parser.add_argument("action", help="the action can be host/test/client", type=str)
    parser.add_argument("--port", help="Specifying port, dafault 3456", type=int)
    args = parser.parse_args()

    if args.action:
        if args.port:
            if args.port in range(1000,10000):
                main(args.action, args.port)
        else:
            main(args.action)

if __name__=="__main__":
    run()
