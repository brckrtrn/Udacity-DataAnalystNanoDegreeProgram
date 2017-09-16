import csv, sqlite3

#Read given file and return the sql query
def get_sql_query_string(sqlFile):
    fd = open(sqlFile, 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile

#Execute given aggregate query(Like sum, count) and return result.
def execute_aggregate_query(sqlFile):
    result = cur.execute(get_sql_query_string(sqlFile))
    return result.fetchone()[0]

#Execute given query and return result.
def execute_query(sqlFile):
    result = []
    for row in cur.execute(get_sql_query_string(sqlFile)):
        result.append(" ".join(map(str, row)))
        #print (" ".join(map(str, row)))
    return result

if __name__ == '__main__':
    con = sqlite3.connect("OpenStreetMap.db")
    cur = con.cursor()

    print("Number of ways: ", execute_aggregate_query("sql/select_way_size.sql"))
    print("Number of nodes: ", execute_aggregate_query("sql/select_nodes_size.sql"))
    print("Number of unique users: ", execute_aggregate_query("sql/unique_users.sql"))
    print( "Top 10 contributing users: ", execute_query("sql/contributing_user.sql"))
    print("Number of users appearing only once: ", execute_query("sql/users_appearing_only_once.sql"))
    print("Biggest religion : ", execute_query("sql/biggest_religion.sql"))
    print("First contribution : ", execute_query("sql/first_contribution.sql"))
    print("Most popular amenity : ", execute_query("sql/amenity.sql"))

    con.close()
