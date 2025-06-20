import yaml

def get_dvc_version(task, path):
    with open('dvc.lock') as f:
        lock_data = yaml.safe_load(f)

    data_md5 = lock_data['stages'][task][path][0]['md5']

    return data_md5