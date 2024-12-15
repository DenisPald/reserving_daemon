import os
import time
import json
import shutil
import logging
import signal
import sys

def load_config():
    with open('/home/denispald/w/linux/semestr_3/linux/daemon/config.json', 'r') as f:
        return json.load(f)

def backup_files(source, backup):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup, f"backup_{timestamp}")
    
    try:
        shutil.copytree(source, backup_path)
        logging.info(f"Backup created at: {backup_path}")
    except Exception as e:
        logging.error(f"Error during backup: {e}")

def signal_handler(signum, frame):
    logging.info("Daemon received termination signal. Exiting...")
    sys.exit(0)

def run_daemon():
    config = load_config()
    source = config['source_directory']
    backup = config['backup_directory']
    frequency = config['backup_frequency']
    log_file = config['log_file']
    
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info("Daemon started.")

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        backup_files(source, backup)
        time.sleep(frequency)

if __name__ == "__main__":
    try:
        run_daemon()
    except Exception as e:
        logging.error(f"Daemon got an error: {e}")
        sys.exit(1)
