import os
import ftplib


class Ftp:
    def __init__(self, host, port, login, password, base_path):
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.base_path = base_path

    def get_file(self, working_dir, *args):
        ftp = ftplib.FTP()
        files = []

        try:
            ftp.connect(self.host, self.port)
            ftp.login(self.login, self.password)
            ftp.cwd(self.base_path)

            for file_name in args:
                print '-> Downloading %s' % file_name

                try:
                    full_file_name = os.path.join(working_dir, file_name)

                    with open(full_file_name, 'wb') as f:
                        ftp.retrbinary("RETR " + file_name, f.write)

                    files.append(full_file_name)

                except ftplib.Error as e:
                    print 'FTP error: %s' % e.message

                    if (os.path.exists(full_file_name) and
                            os.access(full_file_name, os.W_OK)):
                        os.remove(full_file_name)
                except IOError as e:
                    print 'IO Error: %s' % e.message

                    if (os.path.exists(full_file_name) and
                            os.access(full_file_name, os.W_OK)):
                        os.remove(full_file_name)
                except:
                    print 'Some error occur'

        except IOError as e:
            print 'IO Error: %s' % e.message
        except:
            print 'Some error occur'
        finally:
            ftp.close()

        return files

    def list_of_files(self):
        data = []

        ftp = ftplib.FTP()

        try:
            ftp.connect(self.host, self.port)
            ftp.login(self.login, self.password)
            ftp.cwd(self.base_path)
            ftp.dir(data.append)

        except ftplib.Error as e:
            print 'FTP error: %s' % e.message
        except IOError as e:
            print 'IO Error: %s' % e.message
        except:
            print 'Some error occur'
        finally:
            ftp.close()

        return data
