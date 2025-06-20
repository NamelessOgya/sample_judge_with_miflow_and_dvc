import yaml

def get_current_run_id():
    """
    Get the current run ID from the current_run.yaml file.
    
    Returns:
        str: The current run ID.
    """
    try:
        with open('current_run.yaml', 'r') as file:
            data = yaml.safe_load(file)
            return data.get('mikoto_run_id', None)
    except FileNotFoundError:
        print("current_run.yaml file not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        return None