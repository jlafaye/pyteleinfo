import mysql
import mysql.connector as mariadb

# mariaDb client
conn = mariadb.connect(user='teleinfo', password='teleinfo',
                       database='teleinfo', host='192.168.1.244', port=3307)

cursor = conn.cursor()

query = '''
create table teleinfo_data(
    time TIMESTAMP,
    adco CHAR(12),
    opttarif CHAR(4),
    base INTEGER,
    hchc INTEGER,
    hchp INTEGER,
    ptec CHAR(4),
    iinst INTEGER,
    adps INTEGER,
    imax INTEGER,
    hhphc CHAR(1),
    motdetat CHAR(6) 
)
'''

# ADCO: addresse concentrateur teleport
# OPTTARIF
# BASE: Index option base 8
# HCHC: Index option heure creuse
# HCPC: Index option heure pleine
# EJPHN: Index option EJP Heures Normale
# EJPHPM: Index option EJP Heures Pointe
# GAZ: Index gaz

cursor.execute(query)
