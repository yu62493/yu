def password_list(servername, databasename):   
    db_list =   [   
                    ['F23101','scrapydb','172.16.5.20', 'web', 'scrapy']
                ]
    result_A = []
    for i1, inner_l in enumerate(db_list):
        for i2, item in enumerate(inner_l):
            if (db_list[i1][0] == servername and db_list[i1][1] == databasename): 
                result_A = db_list[i1]
#                print(i1, i2, item, db_list[i1][i2])
    return result_A

def MariaConn(servername, databasename):

    dsn_array = password_list(servername, databasename)

    server = dsn_array[2] 
    database = databasename
    username = dsn_array[3]
    password = dsn_array[4]

    config = {
    'user': username,
    'password': password,
    'host': server,
    'database': database,
    'raise_on_warnings': True
    }

#    dsn_str = "host=\'" + server + "\', user='" + username + "', passwd='" + password + "', db='" + database + "', charset='utf8'" 
    return config


if __name__ == "__main__":
    print ('This is main of module "DB_Maria.py"')