import argparse
import os
from subprocess import Popen, PIPE


def run_sql_query(sqlCommand, connectString):
    session = Popen(['sqlplus', '-S', connectString],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)

    session.stdin.write('SET LINESIZE 150;\n')
    session.stdin.write('SET PAGESIZE 4000;\n')
    session.stdin.write('SET LONG 50000;\n')
    session.stdin.write('SET WRAP OFF;\n')
    session.stdin.write('SET HEADING OFF;\n')

    session.stdin.write(sqlCommand)
    return session.communicate()


def get_conn_str(host, port, sid, login, password):
    host_port = "(HOST=%s)(PORT=%s)" % (host, port)
    conn_data = "(CONNECT_DATA=(SID=%s))" % sid
    desc = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)%s)%s)" % (
        host_port, conn_data)
    return "%s/%s@'%s'" % (login, password, desc)


def __main__():
    parser = argparse.ArgumentParser(prog='unzip archive')
    parser.add_argument('-s', '--server', help='DB host', required=True)
    parser.add_argument('--port', help='DB port', default='1521')
    parser.add_argument('-n', '--sid', help='SID name', required=True)
    parser.add_argument('-l', '--login', help='DB user', required=True)
    parser.add_argument('-p', '--password', help='DB password', required=True)
    parser.add_argument('-r',
                        '--repo',
                        help='Siebel Repository Name',
                        default='Siebel Repository')
    parser.add_argument('-w',
                        '--working-dir',
                        help='Folder with project.txt file',
                        required=True)
    args = parser.parse_args()

    connectString = get_conn_str(args.server,
                                 args.port,
                                 args.sid,
                                 args.login,
                                 args.password)
    print connectString
    working_dir = os.path.abspath(args.working_dir)

    projects_file = os.path.join(working_dir, 'projects.txt')
    if not os.path.exists(projects_file):
        print 'There is not projects.txt file found in working dir'
        exit(1)

    with open(projects_file, 'r') as f:
        content = f.readlines()

    projects = [x.strip() for x in content]

    projects_sql_list = "('" + "','".join(projects) + "')"

    sqlGetListOfProjects = """
        SELECT p.NAME
          FROM SIEBEL.S_PROJECT p
          JOIN SIEBEL.S_REPOSITORY repo
            ON repo.ROW_ID = p.REPOSITORY_ID
           AND repo.NAME = '%s'
           WHERE p.NAME IN %s ;
    """ % (args.repo, projects_sql_list)

    # print sqlGetListOfProjects

    queryResult, errorMessage = run_sql_query(sqlGetListOfProjects,
                                              connectString)

    # result = [x.strip() for x in queryResult]
    print '-----------------'
    print queryResult
    print '-----------------'

    sqlGetRowId = """
        SELECT SIEBEL.S_SEQUENCE_PKG.GET_NEXT_ROWID() AS ROW_ID
          FROM DUAL;
    """

    queryResult, errorMessage = run_sql_query(sqlGetRowId,
                                              connectString)

    print '-----------------'
    print queryResult
    print '-----------------'


if __name__ == '__main__':
    __main__()
