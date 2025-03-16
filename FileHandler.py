import pickle as pk
import logging
from pathlib import Path



class pkFileHandler:
    
    def __init__(self, fileName="stats.pk1", logFileName = "FileHandler.log", docker: bool=False):
        fileName = "stats.pk1" if None else fileName
        logFileName = "FileHandler.log" if None else fileName
        if docker:
            self._dataFile = "./data/"+fileName
            self._logFile = "./log/"+logFileName
            
            Path("./data").mkdir(parents=True, exist_ok=True)
            Path("./log").mkdir(parents=True, exist_ok=True)
        else:
            self._dataFile = "/data/"+fileName
            self._logFile = "/data/log/"+logFileName
            Path("/data/log").mkdir(parents=True, exist_ok=True)
            
        self._generateLogger(self)
        self._loadData(self)
        self._logger.info("File Handler succesfully got data")
        self._logger.debug(self._data)
        
    def load(self):
        if self._data == None:
            return {}
        return self._data
        
    def save(self, newData):
        if self._data == newData:
            return
        try: 
            with open(self._dataFile, "wb") as file:
                pk.dump(newData, file)
                file.close()
                self._logger.info(f"Stats successfully written to file")
                self._logger.debug(newData)
                self._data = newData
                return
        except Exception as e:
            self._logger.error(f"Unable to write to {self._dataFile} due to: {e}")
            self._logger.warning("Stats not saved.")
            return
        
    def _loadData(self):
        data = None
        try:
            with open(self._dataFile, "rb") as file:
                data = pk.load(file)
                file.close()
                self._data = data
        except Exception as e:
            self._logger.error(f"Error loading data from {self._dataFile} due to: {e}")
        
        if data != dict() and data != None:
            self._logger.critical(f"Stats File corrupted, terminating program")
            exit(100)
        else:
            self._logger.warning("Empty stats file, continuing with empty dict")
            self._data = {}
        
        self._logger.critical("File handler really fucked up in _loadData")
        exit(300)    
        

    def _generateLogger(self):
        fLog = logging.getLogger("File Handler")
        fLog.addHandler(logging.StreamHandler())
        fLog.addHandler(logging.FileHandler(filename=self._logFile, mode="a", encoding="utf-8"))
        fLog.setLevel(logging.INFO)
        fLog.info("Class Initalized")
        self._logger = fLog
            
        