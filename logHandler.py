import logging

class logHandler:
    def genLogger(self, logName):
        logDir = "./data/log/"+logName+".log"
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        Log = logging.getLogger(logName)
        Log.addHandler(logging.StreamHandler().setFormatter(formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')))
        Log.addHandler(logging.FileHandler(filename=logDir, mode="a", encoding="utf-8").setFormatter(formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')))
        Log.setLevel(logging.INFO)
        Log.info(logName+" Logger Initalized")
        self._logger = Log
        