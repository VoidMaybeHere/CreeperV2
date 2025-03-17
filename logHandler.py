import logging
import logging.handlers

class logHandler:
    def genLogger(self, logName, logger=None):
        if logger == None:
            logger = logName
        logDir = "./data/log/"+logName+".log"
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        Log = logging.getLogger(logger)
        
        handler = logging.handlers.RotatingFileHandler(
            filename=logDir,
            mode='wb',
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
            )
        
        Log.addHandler(logging.StreamHandler().setFormatter(formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')))
        Log.addHandler(handler.setFormatter(formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')))
        Log.setLevel(logging.INFO)
        Log.info(logName+" Logger Initalized")
        self._logger = Log
        