import argparse
from syncP import host, client, testmpv

def main(opt, port, limit):
    if opt=="host":
        host.run(port, limit)
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
    parser.add_argument("--limit", help="Specifying limit of clients, dafault 5", type=int)
    args = parser.parse_args()

    if args.action:
        port = args.port if args.port else 3456
        limit = args.limit if args.limit else 5
        main(args.action, port, limit)

if __name__=="__main__":
    run()
