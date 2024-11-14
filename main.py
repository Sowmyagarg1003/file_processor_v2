import os
from file_watcher import Watcher

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data' directory for monitoring.")
    
    for folder in ['done', 'error']:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created '{folder}' directory.")

    watcher = Watcher(path='data/')
    watcher.run()
