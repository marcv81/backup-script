import lib
import yaml

with open('backup.yml') as stream:
    config = yaml.safe_load(stream)

lib.backup(config['backups_root'], config['sources'])
