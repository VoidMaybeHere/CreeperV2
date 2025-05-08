import logging
import logging.handlers




class logHandler:

    def getFormatter(self=None):
        discordLogger = logging.getLogger('discord')
        if discordLogger == None:
            raise RuntimeError("Discord logger not found")
        return discordLogger.handlers[-1].formatter
    
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
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[{asctime}] [{levelname:<8}] {name}: {message}',
            dt_fmt,
            style='{'
            )
        
        handler.setFormatter(formatter)
        Log.addHandler(handler)
        
        del handler
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.getFormatter())
        
        Log.addHandler(handler)
        
        Log.setLevel(logging.INFO)
        Log.info(logName+" Logger Initalized")
        return Log


        