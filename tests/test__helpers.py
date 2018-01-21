import teleinfo
import teleinfo.helpers as th
import mysql.connector as mariadb

def test_frame_reader():
    for fname in ['frame00.dat',
                  'frame01.dat',
                  'frame02.dat']: 

        parser = th.FrameParser(open(fname, 'rb').read())
        fields = dict(parser.iterfields())

        assert( 'ADCO' in fields )
        assert( 'OPTARIF' in fields )
        assert( 'ISOUSC' in fields )
        assert( 'HCHC' in fields )
        assert( 'HCHP' in fields )
        assert( 'PTEC' in fields )
        assert( 'IINST' in fields )
        assert( 'IMAX' in fields )
        assert( 'PAPP' in fields )
        assert( 'HHPHC' in fields )
        assert( 'MOTDETAT' in fields )

def test_row_writer():
    import datetime as dt 
    import logging
    logging.basicConfig(level=logging.DEBUG)
    fname = 'frame00.dat'

    conn = mariadb.connect(user='teleinfo',
                           password='teleinfo',
                           database='teleinfo',
                           host='192.168.1.244',
                           port=3307)

    writer = th.SqlWriter(conn)
    frame = open(fname, 'rb').read()
    row = dict(th.FrameParser(frame).iterfields())
    row['TIME'] = dt.datetime.now()
    print(row)

    writer.write_rows([row])
