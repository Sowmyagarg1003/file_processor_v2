import os
from file_watcher import Watcher

if __name__ == "__main__":
    # Create 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data' directory for monitoring.")
    
    # Create 'done' and 'error' directories as independent folders if they don't exist
    for folder in ['done', 'error']:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created '{folder}' directory.")

    watcher = Watcher(path='data/')
    watcher.run()
