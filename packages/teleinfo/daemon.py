from serial import Serial
import argparse
import logging

def run_daemon():

    parser = argparse.ArgumentParser(description='Daemon to read & store teleinfo data')
    parser.add_argument('-p', '--port', dest='port',
                        default='/dev/ttyS0',
                        help='Serial device to access teleinfo data')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--mysql-user', default='teleinfo')
    parser.add_argument('--mysql-password', default='teleinfo')
    parser.add_argument('--mysql-host', default='192.168.1.244')
    parser.add_argument('--mysql-dbname', default='teleinfo')
    parser.add_argument('--mysql-port', type=int, default=3307)

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    baudrate = 1200
    bytesize = 7
    ser = Serial(args.port, baudrate, bytesize)

    conn = mariadb.connect(user=args.mysql_user,
                           password=args.mysql_password,                                             
                           database=args.dbname,
                           host=args.host,
                           port=args.port)

    reader = FrameReader(ser)
    writer = SqlWriter(conn)

    for frame in reader:
        parser = FrameParser(frame)
        for row in dict(parser.iterfields()):
            print(row)

