import sqlite3, datetime, textwrap

#conn = sqlite3.Connection('timelog')
#curs = conn.cursor()

#TABLEDEF = 'create table timelog (timestamp datetime, description text);'
#curs.execute(TABLEDEF)

def new_entry(desc, ts=None):
    if not ts:
        ts = datetime.datetime.now().isoformat()
    query = 'insert into timelog values ("{}", "{}");'.format(ts, desc)
    try:
        conn = sqlite3.Connection('timelog')
        curs = conn.cursor()
        curs.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return e

def get_entries(range=None):
    conn = sqlite3.Connection('timelog')
    curs = conn.cursor()
    query = 'SELECT * FROM timelog ORDER BY date(timestamp) ASC'
    myres = curs.execute(query)
    myres = myres.fetchall()
    conn.commit()
    conn.close()
    return myres

if __name__ == '__main__':
    while True:
        choice = input('new entry: [n], list entries: [l]: ')
        if choice.lower() == 'n':
            desc = input('enter description: ')
            ts = input('enter time (leave blank for now): ')
            if not ts:
                resp = new_entry(desc)
            else:
                resp = new_entry(desc, ts)
            if resp:
                print('entry successfully added')
            else:
                print(resp)
        elif choice.lower() == 'l':
            res = get_entries()
            for entry in res:
                ts, desc = entry
                desc_lines = textwrap.wrap(desc)
                print('='*79)
                print(ts)
                print('-'*79)
                print('\n')
                for line in desc_lines:
                    print(line)
                print('\n')

