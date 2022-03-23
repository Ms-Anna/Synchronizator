import os
import filecmp
from shutil import copy2, rmtree, copytree
import argparse
from datetime import datetime
from time import sleep
from itertools import chain


def log_data(path, isdir, log_type, log_f, iserr):
    text = f'{datetime.now().strftime("%Y-%m-%d %X")} {"SUCCESS" if not iserr else "ERROR"}; ' \
           f'operation: {log_type}; object type:{"directory" if isdir else "file"}; path: {path};'
    if iserr:
        text += f'\nError: {iserr}'
    print(text)
    with open(log_f, 'a') as f:
        f.write(f'{text}\n')


class FolderMatch:
    def __init__(self, left_f, right_f, log_f):
        self.left_f = left_f
        self.right_f = right_f
        self.log_f = log_f
        self.f_match = filecmp.dircmp(self.left_f, self.right_f)
        self.delete_funny_match()
        self.create_data()
        self.remove_data()
        self.change_files()
        self.check_common_folders()

    def create_data(self):
        for new in chain(self.f_match.left_only, self.f_match.funny_files, self.f_match.common_funny):
            old_path = os.path.join(self.left_f, new)
            new_path = os.path.join(self.right_f, new)
            er = ''
            try:
                if os.path.isdir(old_path):
                    copytree(old_path, new_path)
                else:
                    copy2(old_path, new_path)
            except Exception as err:
                er = err.__repr__()
            finally:
                log_data(new_path, os.path.isdir(new_path), 'creation', self.log_f, er)

    def remove_data(self):
        for rm_data in self.f_match.right_only:
            the_path = os.path.join(self.right_f, rm_data)
            er = ''
            try:
                if os.path.isdir(the_path):
                    rmtree(the_path)
                else:
                    os.remove(the_path)
            except Exception as err:
                er = err.__repr__()
            finally:
                log_data(the_path, os.path.isdir(the_path), 'removal', self.log_f, er)

    def change_files(self):
        for changed in self.f_match.diff_files:
            er = ''
            try:
                copy2(os.path.join(self.left_f, changed), os.path.join(self.right_f, changed))
            except Exception as err:
                er = err.__repr__()
            finally:
                log_data(os.path.join(self.right_f, changed), False, 'copying', self.log_f, er)

    def delete_funny_match(self):
        for funny_smtng in chain(self.f_match.funny_files, self.f_match.common_funny):
            path_to_delete = os.path.join(self.right_f, funny_smtng)
            er = f'Object exists in both folders {self.left_f} and {self.right_f}, but couldn\'t be compared. It is removed and will be created again.'
            try:
                if os.path.isdir(path_to_delete):
                    rmtree(path_to_delete)
                else:
                    os.remove(path_to_delete)
            except Exception as err:
                er += f'\n{err.__repr__()}'
            finally:
                log_data(funny_smtng, False, 'comparison', self.log_f, er)

    def check_common_folders(self):
        for folder in self.f_match.common_dirs:
            FolderMatch(os.path.join(self.left_f, folder), os.path.join(self.right_f, folder), self.log_f)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-source_folder', '--sf', help='the source folder that will be replicated')
    parser.add_argument('-replica_folder', '--rf', help='the folder to make a source folder replication')
    parser.add_argument('-sync_interval', '--i', help='synchronization interval (minutes by default)')
    parser.add_argument('-log_file', '--lf', help='the name of the file to log file creation/copying/removal operations')
    parser.add_argument('-time-measure', '--tm', choices=['h', 'm', 'd'], help='Choices for time-measuring', default='m')
    args = parser.parse_args()

    time_multiplier = {'h': 3600, 'm': 60, 'd': 86400}

    source_folder = args.sf
    replica_folder = args.rf
    sync_interval = args.i
    sync_m = time_multiplier[args.tm]
    log_file = args.lf

    while not source_folder or not os.path.isdir(source_folder):
        source_folder = input('The path to the source folder:\n')

    while not replica_folder or not os.path.isdir(replica_folder):
        replica_folder = input('The path to the replica folder:\n')

    while not sync_interval or (type(sync_interval) == str and not sync_interval.isdigit()) or int(sync_interval) <= 0:
        try:
            sync_interval = int(input('Time interval in minutes (positive number):\n'))
        except ValueError as valerr:
            print('ATTENTION: Time interval must be a positive whole-number.')

    while not log_file:
        log_file = input('The path to the log file:\n')

    while True:
        try:
            print(f'{datetime.now().strftime("%Y-%m-%d %X")} Starting synchronization...')
            FolderMatch(source_folder, replica_folder, log_file)
            print(f'{datetime.now().strftime("%Y-%m-%d %X")} Synchronization is completed. Next sync will be in {sync_interval}{args.tm}')
            sleep(int(sync_interval) * sync_m)
        except KeyboardInterrupt:
            print('Program was interrupted.')
            exit(0)
