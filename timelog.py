import sqlite3, datetime, textwrap

# conn = sqlite3.Connection('timelog')
# curs = conn.cursor()
#
# drop = "drop table if exists timelog;"
# curs.execute(drop)
# conn.commit()
# conn.close()
#
#
conn = sqlite3.Connection('timelog')
curs = conn.cursor()
TABLEDEF = '''
    create table if not exists timelog
    (
    id integer primary key autoincrement,
    timestamp text,
    description text
    );
    '''
curs.execute(TABLEDEF)
conn.commit()
conn.close()

def new_entry(desc, ts=None):
    if not ts:
        ts = datetime.datetime.now().isoformat()
    query = 'insert into timelog values (null, "{}", "{}");'.format(ts, desc)
    try:
        conn = sqlite3.Connection('timelog')
        curs = conn.cursor()
        res = curs.execute(query)
        conn.commit()
        conn.close()
        return res
    except Exception as e:
        return e

def delete_entry(entry_id):
    conn = sqlite3.Connection('timelog')
    curs = conn.cursor()
    query = 'DELETE FROM timelog where id={};'.format(entry_id)
    myres = curs.execute(query)
    myres = myres.fetchall()
    conn.commit()
    conn.close()
    return myres

def read_entry(entry_id):
    conn = sqlite3.Connection('timelog')
    curs = conn.cursor()
    query = 'select * FROM timelog where id={};'.format(entry_id)
    myres = curs.execute(query)
    myres = myres.fetchall()
    conn.commit()
    conn.close()
    return myres

def get_entries_by_day(date_string=datetime.date.today().isoformat()):
    conn = sqlite3.Connection('timelog')
    curs = conn.cursor()
    query = '''
        SELECT * FROM timelog
        where date(timestamp)=date("{}")
        ORDER BY datetime(timestamp) ASC;
        '''.format(date_string)
    myres = curs.execute(query)
    myres = myres.fetchall()
    conn.commit()
    conn.close()
    return myres

def edit_entry(timestamp):
    conn = sqlite3.Connection('timelog')
    curs = conn.cursor()
    query = 'SELECT * FROM timelog where timestamp = "{}";'.format(timestamp)
    myres = curs.execute(query)
    ts, desc = myres.fetchone()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    time_format = '%I:%M:%S %p'
    datetime_format = '%b %d, %Y %I:%M %p'
    parse_format = '%Y-%m-%dT%H:%M:%S.%f'
    print('=' * 79)
    print('\n')
    print('{0:^79}'.format("TIME LOGGER"))
    print('\n')
    print('-' * 79)
    # print('\n')
    print('{0:^79}'.format('Keep track of your day with short descriptive entries'))


    while True:
        print('\n' + '*' * 79 + '\n')
        choice_format = '{0:^15}{1:^15}{2:^15}{3:^15}'
        prompt_names = choice_format.format('create', 'read', 'delete', 'exit')
        prompt_names = '{0:^79}'.format(prompt_names)
        prompt_short = choice_format.format('[c]', '[r]', '[d]', '[x]')
        prompt_short = '{0:^79}'.format(prompt_short)
        # prompt += '\n' + '>>'
        print(prompt_names)
        print(prompt_short)
        choice = input('>> ')
        print('\n' + '*' * 79 + '\n')
        if choice.lower() == 'c':
            desc = input('enter description: ')
            ts = input('enter time (press enter to use now): ')
            if not ts:
                resp = new_entry(desc)
            else:
                resp = new_entry(desc, ts)
            # print(resp)
            if resp:
                print('entry successfully added')
            else:
                print(resp)
        elif choice.lower() == 'r':
            user_choice = input("by [day], or by [id]?\n>> ")
            if user_choice == 'id':
                entry_id = input('entry ID: ')
                res = read_entry(entry_id)
                # print(res)
                for entry in res:
                    id, ts, desc = entry
                    desc_lines = textwrap.wrap(desc)
                    print('='*79)
                    myformat = '{0:<40}{1:>39}'
                    idinfo = 'entry ID: {}'.format(id)
                    dt = datetime.datetime.strptime(ts, parse_format)
                    pretty_date = dt.strftime(datetime_format)
                    print(myformat.format(pretty_date, idinfo))
                    print('-'*79)
                    print('\n')
                    for line in desc_lines:
                        print(line)
                    print('\n')

            elif user_choice == 'day':
                day_string = input('select day YYYY-MM-DD (leave blank for today):\n>>')

                if day_string:
                    res = get_entries_by_day(day_string)
                else:
                    res = get_entries_by_day()

                for entry in res:
                    id, ts, desc = entry
                    desc_lines = textwrap.wrap(desc)
                    print('='*79)
                    myformat = '{0:<40}{1:>39}'
                    idinfo = 'entry ID: {}'.format(id)
                    dt = datetime.datetime.strptime(ts, parse_format)
                    pretty_date = dt.strftime(datetime_format)
                    print(myformat.format(pretty_date, idinfo))
                    print('-'*79)
                    print('\n')
                    for line in desc_lines:
                        print(line)
                    print('\n')

        elif choice.lower() == 'd':
            entry_id = input('entry ID: ')
            res = delete_entry(entry_id)
            # print(res)


        elif choice.lower() == 'x':
            exit()

