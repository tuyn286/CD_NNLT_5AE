from loguru import logger
import datetime
import os

from src.config import cfg

logger_cfg = cfg.logger

def create_logger():
    """Create logger object
    Returns: a logger object
    """
    # Check if there is any logger handler running
    if len(logger._core.handlers) < 2 or logger_cfg.log_dir not in logger._core.handlers[1]._name:
        # Get the current date and time
        current_time = datetime.datetime.now()
        # Format the current date and time as a string
        timestamp = current_time.strftime(logger_cfg.time_format)
        os.makedirs(logger_cfg.log_dir, exist_ok=True)
        # Construct log file name
        filepath = os.path.join(logger_cfg.log_dir, f"{timestamp}{logger_cfg.log_file_extension}")
        # Create logger file
        logger.add(filepath, format=logger_cfg.log_format, level=logger_cfg.level, rotation=logger_cfg.rotation)
        # delete old log files 
        delete_old_logs(logger_cfg.log_dir)
        print(f"Create log file at: {filepath}")
    return logger

def delete_old_logs(log_dir):
    """Delete log files which created before last 30 days

    Args:
        log_dir (str): directory of logs folder
    """
    today = datetime.date.today()
    for file_name in os.listdir(log_dir):
        if file_name.endswith(logger_cfg.log_file_extension):
            try:
                log_date = datetime.datetime.strptime(file_name.split(".")[0], logger_cfg.time_format).date()
                if (today - log_date).days > logger_cfg.log_existence_days:
                    file_path = os.path.join(log_dir, file_name)
                    os.remove(file_path)
                    print(f"Deleted file: {file_name}")
            except ValueError:
                continue

logger = create_logger()  
