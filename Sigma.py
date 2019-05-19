# Grupo Sigma
# Tiago Costa Arrazi - 222160319
# Guilherme Coelho Small Zicari - 222170300


import pickle
import subprocess
from binascii import hexlify
import sys
import re
import pysnooper
import math

selected_hd = ""
path_in_structure = ""
str_path = "/"

dir_count = 0
file_count = 0
dir_total_size = 0
file_total_size = 0


def release_the_kraken():

    cmd_list = ['\n',
                '               CREATEHD       ALLOWS YOU TO CREATE AN HD',
                '               DIRHD          SHOWS ALL CREATED HDs',
                '               SELECTHD       SELECTS AN HD TO BE MANIPULATED',
                '               TYPEHD         SHOWS HD CONTENT',
                '               FORMATHD       WIPES HD RECORDED DATA',
                '               STATUSHD       SHOWS CURRENT HD INFO',
                '\n',
                '               CREATE         CREATES A FILE',
                '               DEL            DELETES A FILE',
                '               RENAME         RENAMES A FILE',
                '               MKDIR          CREATES A FOLDER',
                '               RMDIR          REMOVES A FOLDER',
                '               RENAMEDIR      RENAMES A FOLDER',
                '               MOVE           MOVES A FILE/FOLDER',
                '               COPY           COPIES A FILE/FOLDER',
                '               CD             HD NAVIGATION',
                '\n',
                '               CLS            CLEARS SCREEN',
                '               TREE           GRAPHICALLY SHOWS DIRECTORY TREE',
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
                            
             Example: dirhd 
                            
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
                            
                        """,
            'tree': """
            
            tree <no parameters>
            
            This command graphically shows the directory hierarchy from /
            
            Example: tree
            
                        """,
            'statushd': """
            
            statushd <no parameters>
            
            This command is used to get the current hd info, such as its free and used space, 
            so as the file and folder count
            
            Example: statushd
            
                        """,
            'rename': """
            
            rename <current filename> <new filename>
            
            This command is used to change the name of a file
            
            Example: rename sample_file new_sample_file
            
                        """,
            'renamedir': """
            
            renamedir <current directory name> <new directory name>
            
            This command is used to change the name of a directory
            
            Example: renamedir <current directory name> <new directory name>
            
                        """,
            'rmdir': """
            
            rmdir <directory name>
            
            This command is used to remove a directory and all its content
            
            Example: rmdir sample_directory
            
                        """,
            'move': """
            
            move <filename/directory name> <destination directory>
            
            This command is used to move a file/folder to another directory
            ONLY WORKS WITH ABSOLUTE PATHS
            
            Example: move sample_file sample_dest_dir
                     move sample_directory sample_dest_dir
            
                        """,
            'copy': """
            
            copy <filename/directory name> <destination directory>
            
            This command is used to copy a file/folder to another directory
            ONLY WORKS WITH ABSOLUTE PATHS
            
            Example: copy sample_file sample_dest_dir
                     copy sample_directory sample_dest_dir
            
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
def status_hd():

    try:
        with open(selected_hd, 'rb') as pickle_in:

            with open('HD_List', 'r') as hd_list:

                for line in hd_list:
                    if selected_hd in line:
                        hd_info = line.split(' ')
                        blocks = int(hd_info[1])
                        _bytes = int(hd_info[2])

                root = pickle.load(pickle_in)
                root_list = []

                for element in str(root):
                    root_list.append(element)

                splitted_list = list(divide_chunks(root_list, _bytes))

                i = 0
                deceiver = 0

                for l in splitted_list:
                    i += 1
                deceiver = i * _bytes

                print(f'Max size: {blocks * _bytes} bytes')
                print(f'Free:  {(blocks * _bytes) - deceiver} bytes')
                print(f'Used: {deceiver} bytes')
                count_dir_file(root)
                print('Number of folders:', dir_count)
                print('Number of files:', file_count)

    except FileNotFoundError:
        print('[ERROR] No HD is selected')


# @pysnooper.snoop()
def count_dir_file(input):
    global dir_count
    global file_count

    for key, value in input.items():
        if isinstance(value, dict):
            dir_count += 1
            count_dir_file(value)

        else:
            file_count += 1


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


# @pysnooper.snoop()
def remove_hd(hd_name):

    global selected_hd
    global str_path
    global path_in_structure

    with open('HD_List', 'r') as hd_list:
        all_hds = [line if hd_name not in line.split(' ') else '' for line in list(hd_list.readlines())]

    with open('HD_List', 'w') as hd_list:
        [hd_list.write(line) if line != '' else None for line in all_hds]

    if hd_name == selected_hd:
        selected_hd = ''
        str_path = '/'
        path_in_structure = ''


    subprocess.Popen('del {}'.format(hd_name), shell=True).communicate()


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


# @pysnooper.snoop()
def rename_file(filename, new_name):

    try:
        with open(selected_hd, 'rb') as pickle_in:
            root = pickle.load(pickle_in)
            if not isinstance(eval(f'root{path_in_structure}')[filename], dict):
                eval(f'root{path_in_structure}')[new_name] = eval(f'root{path_in_structure}').pop(filename)
            else:
                print('[ERROR] Not a file')

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
        print('[ERROR] No such file')


# @pysnooper.snoop()
def copyfrom(real_name, virtual_name):

        try:
            with open(real_name, 'rb') as image:
                image_content = image.readlines()

            file = File(virtual_name, image_content)
        except FileNotFoundError:
            print('[ERROR] No such file in the physical HD')

        try:
            with open(selected_hd, 'rb') as pickle_in:

                with open('HD_List', 'r') as hd_list:

                    for line in hd_list:
                        if selected_hd in line:
                            hd_info = line.split(' ')
                            blocks = int(hd_info[1])
                            _bytes = int(hd_info[2])

                    root = pickle.load(pickle_in)
                    eval(f'root{path_in_structure}')[virtual_name] = file.content

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
            print('[ERROR] No HD is selected')


# @pysnooper.snoop()
def copyto(virtual_name, real_name):

    try:
        with open(selected_hd, 'rb') as pickle_in:
            with open(real_name, 'wb+') as image:
                root = pickle.load(pickle_in)
                image.write(b''.join((eval(f'root{path_in_structure}')[virtual_name])))

    except KeyError:
        print('[ERROR] No such file')


# @pysnooper.snoop()
def rmdir(dirname):

    try:
        with open(selected_hd, 'rb') as pickle_in:
            root = pickle.load(pickle_in)

            if isinstance(eval(f'root{path_in_structure}')[dirname], dict):
                del eval(f'root{path_in_structure}')[dirname]
            else:
                print('[ERROR] not a directory')

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
        print('[ERROR] No HD is selected')

    except KeyError:
        print('[ERROR] No such directory')


# @pysnooper.snoop()
def move(src_path, dest_path):

    try:
        with open(selected_hd, 'rb') as pickle_in:
            root = pickle.load(pickle_in)

            src_path_list = src_path.split('/')[1:]
            dest_path_list = dest_path.split('/')[1:]
            to_be_popped = src_path_list[-1]
            path_to_be_popped_list = src_path_list[:-1]

            src_path_in_structure = ''.join([f"[\'{_dir}\']" for _dir in src_path_list])
            dest_path_in_structure = ''.join([f"[\'{_dir}\']" for _dir in dest_path_list])
            path_to_be_popped_in_structure = ''.join([f"[\'{_dir}\']" for _dir in path_to_be_popped_list])

            if dest_path == '/':
                root[to_be_popped] = eval(f"root{src_path_in_structure}")
            else:
                eval(f"root{dest_path_in_structure}")[to_be_popped] = eval(f"root{src_path_in_structure}")

            eval(f"root{path_to_be_popped_in_structure}").pop(to_be_popped)

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
        print('[ERROR] No HD is selected')

    except KeyError:
        print('[ERROR] No such file or directory')


# @pysnooper.snoop()
def copy(src_path, dest_path):

    try:
        with open(selected_hd, 'rb') as pickle_in:
            root = pickle.load(pickle_in)

            src_path_list = src_path.split('/')[1:]
            dest_path_list = dest_path.split('/')[1:]

            src_path_in_structure = ''.join([f"[\'{_dir}\']" for _dir in src_path_list])
            dest_path_in_structure = ''.join([f"[\'{_dir}\']" for _dir in dest_path_list])

        eval(f"root{dest_path_in_structure}")[src_path_list[-1]] = eval(f"root{src_path_in_structure}")

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
        print('[ERROR] No HD is selected')

    except KeyError:
        print('[ERROR] No such file or directory')

# @pysnooper.snoop()
def renamedir(dirname, new_name):
    try:
        with open(selected_hd, 'rb') as pickle_in:
            root = pickle.load(pickle_in)
            if isinstance(eval(f'root{path_in_structure}')[dirname], dict):
                eval(f'root{path_in_structure}')[new_name] = eval(f'root{path_in_structure}').pop(dirname)
            else:
                print('[ERROR] Not a directory')

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
        print('[ERROR] No HD is selected')

    except KeyError:
        print('[ERROR] No such directory')


# @pysnoopper.snoop()
def tree(structure, depth=0):

    for key in structure.keys():

        if isinstance(structure[key], dict):
            print('{}|{}{}'.format((depth ** 2) * ' ', depth * '__', key))
            tree(structure[key], depth + 1)

        else:
            print('{}|{}{}'.format((depth ** 2) * ' ', depth * '__', key))


# @pysnooper.snoop()
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

        elif shell[0] == 'statushd':  # OK
            status_hd()

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

        elif shell[0] == 'rename':
            try:
                rename_file(shell[1], shell[2])

            except IndexError:
                print('[ERROR] Missing arguments -- rename <file> <new file>')

        elif shell[0] == 'cls':  # OK
            clear()

        elif shell[0] == 'mkdir':  # OK
            try:
                mk_dir(shell[1])

            except IndexError:
                print('[ERROR] Missing arguments -- mkdir <directory>')

        elif shell[0] == 'rmdir':  # OK
            try:
                rmdir(shell[1])

            except IndexError:
                print('[ERROR] Missing arguments -- rmdir <directory>')

        elif shell[0] == 'renamedir':  # OK
            try:
                renamedir(shell[1], shell[2])

            except IndexError:
                print('[ERROR] Missing arguments -- renamedir <directory>')

        elif shell[0] == 'cd':  # OK
            change_dir(shell[1])

        elif shell[0] == 'dir':  # OK
            list_dir()

        elif shell[0] == 'del':  # OK
            try:
                delete_file(shell[1])

            except IndexError:
                print('[ERROR] Missing arguments -- del <file>')

        elif shell[0] == 'help':  # OK
            try:
                print(cmd_help[shell[1]])

            except IndexError:
                release_the_kraken()

            except KeyError:
                print('[ERROR] No such command')

        elif shell[0] == 'copyfrom':  # OK
            try:
                copyfrom(shell[1], shell[2])

            except IndexError:
                print('[ERROR] Missing arguments -- copyfrom <file in physical HD> <file in virtual HD>')

        elif shell[0] == 'copyto':  # OK
            try:
                copyto(shell[1], shell[2])

            except IndexError:
                print('[ERROR] Missing arguments -- copyto <file in physical HD> <file in virtual HD>')


        elif shell[0] == 'tree':  # OK
            with open(selected_hd, 'rb') as pickle_in:
                root = pickle.load(pickle_in)
                tree(root)

        elif shell[0] == 'move':  # OK
            try:
                move(shell[1], shell[2])

            except IndexError:
                print('[ERROR] Missing arguments -- move <file/directory> <destination>')

        elif shell[0] == 'copy':  # OK
            try:
                copy(shell[1], shell[2])

            except IndexError:
                print('[ERROR] Missing arguments -- copy <file/directory> <destination>')

        elif shell[0] == 'removehd':  # OK
            try:
                remove_hd(shell[1])

            except:
                print('[ERROR] Missing arguments -- removehd <HD name>')

        elif shell[0] == 'show':
            with open(selected_hd, 'rb') as pickle_in:
                root = pickle.load(pickle_in)
                print(root)

        elif shell[0] == 'exit':  # OK
            subprocess.Popen('cls', shell=True).communicate()
            exit()
