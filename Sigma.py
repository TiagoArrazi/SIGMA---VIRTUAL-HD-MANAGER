# Grupo Sigma
# Tiago Costa Arrazi - 222160319
# Guilherme Coelho Small Zicari - ?????????


import pickle
import subprocess
from binascii import hexlify
import sys
import re
import pysnooper

selected_hd = ""
path_in_structure = ""
str_path = "/"


def release_the_kraken():

    cmd_list = ['\n',
                '               CREATEHD       ALLOWS YOU TO CREATE AN HD',
                '               DIRHD          SHOW ALL CREATED HDs',
                '               SELECTHD       SELECT AN HD TO BE MANIPULATED',
                '               TYPEHD         SHOWS HD CONTENT',
                '               FORMATHD       WIPE HD RECORDED DATA',
                '\n',
                '               CREATE         CREATE A FILE',
                '               DEL            DELETE A FILE',
                '               MKDIR          CREATE A DIRECTORY',
                '               CD             HD NAVIGATION',
                '\n',
                '               CLS            CLEAR SCREEN',
                '\n']


    for line in cmd_list:
        print(line)



cmd_help = {'createhd': """ 

             createhd <HD name> <Number of blocks> <Bytes per block> 
                            
             This command is used to create a new HD with specified size.
                            
             Example: createhd HD1 1024 32
                             
                        """,
            'dirhd': """
            
             dirhd <no parameters>
                            
             This commmand is used to list all HDs created so far.
                            
             Example: dirhd (no shit Sherlock!)
                            
                        """,
            'selecthd': """ 
            
             selecthd <HD name>

             This command is used to select an HD.

             Example: selecthd HD1
                                      
                        """,
            'typehd': """ 
            
             typehd <no parameters>
                            
             This command is used to print the HD's content 
             in both patterns hexadecimal and characters.
                            
             Example: typehd (an HD must be selected previously)
                            
                        """,
            'formathd': """ 

             formathd <no parameters>

             This command is used to wipe out recorded data inside an HD
             returning to its initial state.
                            
             Example: typehd (an HD must be selected previously)

                    """,
            'create': """ 

             create <filename>

             This command is used to create a file inside your current directory.

             Example: create sample_file
                                     
                      Press ENTER then Ctrl+Z to end input

                      """,
            'type': """ 

             type <filename>

             This command is used to print a file's content.
                            
             Example: type sample_file

                        """,
            'cls': """ 

             cls <no parameters>

             This command is used to get the screen cleared.

                   """,
            'mkdir': """ 

             mkdir <directory name>

             This command is used to create a directory.

             Example: mkdir sample_directory

                        """,
            'cd': """ 

             cd <path>

             This command is used to navigate through the HD's hierarchy.

             Example 1: cd dir1 (single directory path)
             Example 2: cd dir1/dir2 (absolute path)
             Example 3: cd .. (goes back to the parent directory)

                        """,
            'dir': """ 

             dir <no parameters>

             This command is used to list all content inside a directory.

             Example: dir

                        """,
            'del': """ 

             typehd <filename>

             This command is used delete a file

             Example: del sample_file

                        """,
            'exit': """ 

             If you wanna stay, don't type it. 
             As a matter of fact you can type it, but don't press ENTER, 'K?
                            
             USE WITH CAUTION!
                            
                        """
            }

class File:

    def __init__(self, filename, content):
        self.filename = filename
        self.content = content


class Directory:

    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.structure = {}


# @pysnooper.snoop()
def create_hd(hd_name, blocks, _bytes):

    with open(hd_name, 'wb') as f:

        dummy = {}
        pickle.dump(dummy, f)
        f.seek(blocks * _bytes - 1)
        f.write(b'\0')
        with open('HD_List', 'a+') as hd_list:
            hd_list.write(f'{hd_name} {blocks} {_bytes}\n')


# @pysnooper.snoop()
def dir_hd():

    try:
        for line in open('HD_List', 'r'):
            print(line)

    except FileNotFoundError:
        print('[ERROR] In order to list all HDs you must create one first')


# @pysnooper.snoop()
def select_hd(hd_name):

    try:
        with open('HD_List', 'r') as hd_list:
            for line in hd_list:
                hd_info = line.split(' ')

                if hd_name in hd_info:
                    global selected_hd
                    selected_hd = hd_name
                    print(f'Switched to \"{hd_name}\"')
                    return True

            else:
                print(f'[ERROR] No such HD')
                return False
    except FileNotFoundError:
        print('[ERROR] There are no HDs')


# @pysnooper.snoop()
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# @pysnooper.snoop()
def type_hd():

    try:
        with open(selected_hd, 'rb') as pickle_in:

            with open('HD_List', 'r') as hd_list:

                for line in hd_list:
                    if selected_hd in line:
                        hd_info = line.split(' ')
                        _bytes = int(hd_info[2])

                root = pickle.load(pickle_in)
                root_list = []

                for element in str(root):
                    root_list.append(element)

                splitted_list = list(divide_chunks(root_list, _bytes))

                i = 0

                for l in splitted_list:
                    print(f"BLOCK {i}   {'  '.join(l)}")
                    print(f"       {b' '.join([hexlify(bytes(element, encoding='utf-8')) for element in l])}")
                    i += 1
                    input()

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


# @pysnooper.snoop()
def format_hd():

    try:
        with open(selected_hd, 'wb') as hd:

            with open('HD_List', 'r') as hd_list:

                for line in hd_list:
                    if selected_hd in line:
                        hd_info = line.split(' ')
                        blocks = int(hd_info[1])
                        _bytes = int(hd_info[2])

                dummy = {}
                pickle.dump(dummy, hd)
                hd.seek(blocks * _bytes - 1)
                hd.write(b'\0')
        global str_path
        global path_in_structure

        str_path = "/"
        path_in_structure = ""

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


# @pysnooper.snoop()
def mk_dir(dir_name):

    try:
        directory = Directory(dir_name)

        with open(selected_hd, 'rb') as pickle_in:

            with open('HD_List', 'r') as hd_list:

                for line in hd_list:
                    if selected_hd in line:
                        hd_info = line.split(' ')
                        blocks = int(hd_info[1])
                        _bytes = int(hd_info[2])

                root = pickle.load(pickle_in)
                eval(f'root{path_in_structure}')[dir_name] = directory.structure

        with open('HD_List', 'r') as hd_list:

            for line in hd_list:
                if selected_hd in line:
                    hd_info = line.split(' ')
                    blocks = int(hd_info[1])
                    _bytes = int(hd_info[2])

            with open(selected_hd, 'wb') as pickle_out:
                pickle.dump(root, pickle_out)
                pickle_out.seek(blocks * _bytes - 1)
                pickle_out.write(b'\0')

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


# @pysnooper.snoop()
def pop_from_str_path(path):

    str_path_list = path.split('/')
    str_path_list.pop(-1)
    path = '/'.join(str_path_list)

    if path == '':
        return '/'

    return path


# @pysnooper.snoop()
def from_path_in_structure_to_path_list(path):

    filtered_path_in_structure = re.sub('\[', ' ', path)
    filtered_path_in_structure = re.sub('\]', ' ', filtered_path_in_structure)
    new_path_list = filtered_path_in_structure.split()

    return new_path_list


# @pysnooper.snoop()
def change_dir(my_path):

    try:
        with open(selected_hd, 'rb') as f:
            pass

        global path_in_structure
        global str_path
        global path_list

        if len(path_in_structure) != 0:
            if my_path == '..':
                path_list = from_path_in_structure_to_path_list(path_in_structure)
                path_list.pop(-1)
                str_path = pop_from_str_path(str_path)

            else:
                path_list.append(my_path)
                str_path += '/' + my_path

        else:
            path_list = my_path.split('/')
            str_path += my_path

        path_in_structure = ""

        for element in path_list:
            path_in_structure += f'[\'{element}\']'

        path_in_structure = re.sub('\[\'\'', '[\'', re.sub('\'\'\]', '\']', path_in_structure))

        if my_path == '':
            path_list = []
            path_in_structure = ""
            str_path = "/"

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


# @pysnooper.snoop()
def list_dir():

    try:
        with open(selected_hd, 'rb') as pickle_in:

            root = pickle.load(pickle_in)

            for key in eval(f'root{path_in_structure}').keys():
                print(key)

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


# =============================================================================================================


# @pysnooper.snoop()
def mk_file(filename):

    try:
        content = sys.stdin.readlines()
        file = File(filename, content)

        with open(selected_hd, 'rb') as pickle_in:

            with open('HD_List', 'r') as hd_list:

                for line in hd_list:
                    if selected_hd in line:
                        hd_info = line.split(' ')
                        blocks = int(hd_info[1])
                        _bytes = int(hd_info[2])

                root = pickle.load(pickle_in)
                eval(f'root{path_in_structure}')[filename] = file.content

        with open('HD_List', 'r') as hd_list:

            for line in hd_list:
                if selected_hd in line:
                    hd_info = line.split(' ')
                    blocks = int(hd_info[1])
                    _bytes = int(hd_info[2])

            with open(selected_hd, 'wb') as pickle_out:
                pickle.dump(root, pickle_out)
                pickle_out.seek(blocks * _bytes - 1)
                pickle_out.write(b'\0')

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


# @pysnooper.snoop()
def type_file(filename):

    try:
        with open(selected_hd, 'rb') as pickle_in:

            root = pickle.load(pickle_in)

        if isinstance(eval(f'root{path_in_structure}')[filename], list) or \
           isinstance(eval(f'root{path_in_structure}')[filename], str):

           for line in eval(f'root{path_in_structure}')[filename]:
                    print(line.strip('\n'))

        else:
            print(f'[ERROR] {filename} is a directory')

    except KeyError:
        print('[ERROR] no such file')

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


# @pysnooper.snoop()
def delete_file(filename):

    try:
        with open(selected_hd, 'rb') as pickle_in:

            with open('HD_List', 'r') as hd_list:

                for line in hd_list:
                    if selected_hd in line:
                        hd_info = line.split(' ')
                        blocks = int(hd_info[1])
                        _bytes = int(hd_info[2])

                root = pickle.load(pickle_in)
                eval(f'root{path_in_structure}').pop(filename)

        with open('HD_List', 'r') as hd_list:

            for line in hd_list:
                if selected_hd in line:
                    hd_info = line.split(' ')
                    blocks = int(hd_info[1])
                    _bytes = int(hd_info[2])

            with open(selected_hd, 'wb') as pickle_out:
                pickle.dump(root, pickle_out)
                pickle_out.seek(blocks * _bytes - 1)
                pickle_out.write(b'\0')

    except KeyError:
        print('[ERROR] no such file')

    except FileNotFoundError:
        print('[ERROR] no HD is selected')


def clear():
    subprocess.Popen('cls', shell=True).communicate()

    print("""
                  ==========/
                   \\\\
                    \\\\
                     \\\\
                     //
                    //
                   // 
                  ==========\\

             """)


if __name__ == '__main__':


    clear()

    while True:

        shell = input(f'{selected_hd}:{str_path}>').split(' ')

        if shell[0] == 'createhd':  # OK
            try:
                create_hd(shell[1], int(shell[2]), int(shell[3]))

            except IndexError as e:
                print('[ERROR] Missing arguments -- createhd <HD name> <Number of blocks> <Bytes per block>')

            except ValueError:
                print('[ERROR] Integer values are required for the HD dimensions')

        elif shell[0] == 'dirhd':  # OK
            dir_hd()

        elif shell[0] == 'selecthd':  # OK
            try:
                select_hd(shell[1])
            except IndexError:
                print('[ERROR] Missing arguments -- selecthd <HD name>')

        elif shell[0] == 'typehd':  # OK
            type_hd()

        elif shell[0] == 'formathd':  # OK
            format_hd()

        elif shell[0] == 'create':  # OK
            try:
                mk_file(shell[1])

            except IndexError:
                print('[ERROR] Missing arguments -- create <file>')

        elif shell[0] == 'type':  # OK
            try:
                type_file(shell[1])

            except IndexError:
                print('[ERROR] Missing arguments -- type <file>')

        elif shell[0] == 'cls':  # OK
            clear()

        elif shell[0] == 'mkdir':  # OK
            try:
                mk_dir(shell[1])

            except IndexError:
                print('[ERROR] Missing arguments -- mkdir <directory>')

        elif shell[0] == 'cd':  # OK
            change_dir(shell[1])

        elif shell[0] == 'dir':  # OK
            list_dir()

        elif shell[0] == 'del':  # OK
            try:
                delete_file(shell[1])

            except IndexError:
                print('[ERROR] Missing arguments -- del <file>')

        elif shell[0] == 'help':
            try:
                print(cmd_help[shell[1]])

            except IndexError:
                release_the_kraken()

            except KeyError:
                print('[ERROR] No such command')

        elif shell[0] == 'show':
            with open(selected_hd, 'rb') as pickle_in:
                root = pickle.load(pickle_in)
                print(root)

        elif shell[0] == 'exit':  # OK
            subprocess.Popen('cls', shell=True).communicate()
            exit()
