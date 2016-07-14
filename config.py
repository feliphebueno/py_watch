
configs = {}

def databases():
    configs['databases'] = {
        'padrao' : {
            'host'      : "host",
            'database'  : "database",
            'user'      : "user",
            'password'  : "******",
            'port'      : "3306",
            'driver'    : "mysql",
            'prefix'    : ""
        },
        'prod_t1': {
            'host'      : "host",
            'database'  : "database",
            'user'      : "user",
            'password'  : "******",
            'port'      : "3306",
            'driver'    : "mysql",
            'prefix'    : ""
        },
        'prod_s2': {
            'host'      : "host",
            'database'  : "database",
            'user'      : "user",
            'password'  : "******",
            'port'      : "3306",
            'driver'    : "mysql",
            'prefix'    : ""
        }
    }

    return configs

databases()