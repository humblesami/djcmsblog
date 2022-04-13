import os
import glob
import shutil
from pathlib import Path


def remove_migrations():
    cnt = 0
    res = glob.glob('*/migrations/*', recursive=True)
    for file_path in res:
        if file_path.endswith('__pycache__'):
            file_path = file_path+'/*'
            sub_res = glob.glob(file_path)
            for file_path in sub_res:
                os.remove(file_path)
        elif not file_path.endswith('__init__.py'):
            os.remove(file_path)
            cnt += 1
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
    print(f'{cnt} migration files removed')


def remove_file_by_extension(ext):
    cnt = 0
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = Path(dir_path).rglob('*.'+ext)
    for path in files:
        os.remove(str(path))
        cnt += 1
    print(str(cnt) + ' ' + ext + ' files removed')


def remove_migrations2():
    cnt = walk_dirs('.', 0)
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
    print(f'{cnt} migration files removed')


def walk_dirs(path_now='.', cnt=0):
    for root, sub_dirs, files in os.walk(path_now):
        if path_now.endswith('migrations'):
            for file_name in files:
                if file_name != '__init__.py':
                    file_path = path_now + '/' + file_name
                    os.remove(file_path)
                    cnt += 1
        for dir_path in sub_dirs:
            if dir_path.endswith('__pycache__'):
                rm_path = path_now+'/'+dir_path
                shutil.rmtree(rm_path)
            else:
                cnt = walk_dirs(path_now+'/'+dir_path, cnt)
    return cnt


# remove_migrations()
remove_file_by_extension('pyc')
remove_file_by_extension('po')
print('done')
