import logging

logging.basicConfig(level=logging.DEBUG)


class FrameParser:

    def __init__(self, frame):
        self.frame = frame

    def iterfields(self):
        pos = 0
        frame = self.frame

        while pos < len(frame):
            if frame[pos] != 0xa:
                print('0x%02x' % frame[pos])
                raise SyntaxError
            pos += 1
            tag_pos = pos
            while frame[pos] != 0x20:
                pos += 1
                continue
            tag = frame[tag_pos:pos]
            pos += 1
            data_pos = pos
            while frame[pos] != 0x20:
                pos += 1
                continue
            data = frame[data_pos:pos]
            
            pos += 1 # jump to ctr
            checksum = frame[pos]
            # TODO: compute & check checksum
            pos += 1 # jump to carriage return
            if frame[pos] != 0xd:
                raise SyntaxError
            pos += 1 # jump to next sequence

            tag = tag.decode('ascii')
            data = data.decode('ascii')

            yield tag, data

class FrameReader:

    def __init__(self, device):
        self.device = device

    def __iter__(self):
        return self

    def __next__(self):
        # TODO: improve speed by reading
        # several characters at a time
        buf = None
        while True:
            c = self.device.read(1)
            if c[0] == 0x2:
                buf = b''
                continue
            if buf is None:
                continue
            if c[0] == 0x3:
                break
            buf += c
        return buf

class SqlWriter:

    def __init__(self, conn):
        self.conn = conn

    def write_rows(self, rows):
        # TODO: process several rows
        row = rows[0]

        # @HACK@: get rid of this
        row['TIME'] = row['TIME'].strftime('%Y-%m-%d %H:%M:%S')

        query = '''
        insert into teleinfo_data(
            time,
            adco,
            opttarif,
            hchc,
            hchp,
            ptec,
            iinst,
            imax,
            hhphc,
            motdetat)
        values(%(TIME)s, 
               %(ADCO)s,
               %(OPTARIF)s,
               %(HCHC)s,
               %(HCHP)s,
               %(PTEC)s,
               %(IINST)s,
               %(IMAX)s,
               %(HHPHC)s,
               %(MOTDETAT)s)
        '''
        c = self.conn.cursor()
        c.execute(query, row)
        self.conn.commit()

def print_char(c):
    if c < 127:
        return '%c' % c 
    else:
        return '.'
