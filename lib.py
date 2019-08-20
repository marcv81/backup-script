import datetime
import os
import subprocess

def backup_dirs(backups_root):
    return tuple(reversed(sorted(
        dir.path for dir in os.scandir(backups_root)
        if dir.is_dir() and os.path.basename(dir.path)[:7] == 'backup-')))

def last_backup_dir(backups_root):
    dirs = backup_dirs(backups_root)
    if len(dirs) > 0: return dirs[0]

def new_backup_dir(backups_root):
    previous_backup_dir = last_backup_dir(backups_root)
    backup_dir = backups_root + '/backup-{date:%Y-%m-%d-%H-%M-%S}'.format(date=datetime.datetime.now())
    if previous_backup_dir is None:
        print('INFO: creating ' + backup_dir)
        subprocess.check_call(['mkdir', backup_dir])
    else:
        print('INFO: creating ' + backup_dir + ' (from ' + previous_backup_dir + ')')
        subprocess.check_call(['cp', '--archive', '--link', previous_backup_dir, backup_dir])
    return backup_dir

def backup(backups_root, sources):
    backup_dir = new_backup_dir(backups_root)
    for source in sources:
        print('INFO: syncing ' + source)
        subprocess.check_call(['rsync', '--archive', '--delete', '--verbose', source, backup_dir])
