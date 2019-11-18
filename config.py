from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # print('i am config method') # ok

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section
    db = {}
    if parser.has_section(section): # [section] 이거 말하는듯
        params = parser.items(section) # [section] 소속 문단 가져오나 ?
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('section not found')

    return db