"""
The module is designed to provide information about persons birthdays. 
The entire module is based on the concept of a set of birthday records (which are implemented through the Birthday class). 
Each entry contains information about a person with an indication of the birthday and, optionally, a tag and a host.
A tag is just some kind of word that can be associated with a record. 
But in most cases, it's kind of like a "hashtag" on the internet - in this case, to group records.
The owner is also a simple string that characterizes who the birthday record is intended for. 
It is convenient when, for example, in one file you describe all the birthday records for each member of your family 
(and everyone can have their own acquaintances, friends). 
Then, in the program, it is convenient to get records for the owner field specifically for him.
The module includes the following classes:

1) Birthday:
This class encapsulates information about the birthday of a certain person. 
In particular, he only needs the date of birth to synthesize all the other useful pieces of information. 
It also stores the tag and the host of the record.

2) BRTFile:
This class reads information from a file of a certain text format in which birthday records are actually stored 
(documentation for this format can be understood from the code, and the description usually goes separately in the corresponding file).
The end product of this class is a list of Birthday objects ready to be used.

3) BRTRequest:
And this class was created for convenient filtering of the list of records of Birthday objects. 
It kind of vaguely resembles linq from .Net. 
To work with it, you just need to know the list of keywords representing the designation of fields of the Birthday class, not quite ideal, but much more convenient than resorting to writing "your own additional functions that were not out of the box." 
The result of this class is a selected list (and/or sorted) list of Birthday objects.

You don't have to follow everything that this module offers: You can use any class from this as a self-contained unit - they are independent of each other.
It is not necessary to create any at all for work .brt files, you can just use, for example, the Birthday class at your discretion in the program.
"""

import datetime as dt, time, os, copy

class Birthday:
    __CURRENT_DATE = dt.date.today()

    LANG = "En"

    STAR_CAPRICORN = 0
    STAR_AQUARIUS = 1
    STAR_CANCER = 2
    STAR_LEO = 3
    STAR_PISCES = 4
    STAR_ARIES = 5
    STAR_VIRGO = 6
    STAR_LIBRA = 7
    STAR_TAURUS = 8
    STAR_GEMINI = 9
    STAR_SCORPIO = 10
    STAR_SAGITTARIUS = 11

    def __init__(self, name : str, birthDate : str, tag : str = None, recOwner : str = None):
        try:
            stt = time.strptime(birthDate, "%d.%m.%Y")
            self.__birthDate = dt.date(stt.tm_year, stt.tm_mon, stt.tm_mday)
            self.__valid = True
        except:
            self.__valid = False
            return
        
        self.__name = name
        self.__tag = tag
        self.__recOwner = recOwner

    def is_Valid(self) -> bool:
        return self.__valid
    
    def get_Name(self) -> str:
        return self.__name
    
    def get_Tag(self) -> str | None:
        return self.__tag
    
    def get_Owner(self) -> str | None:
        return self.__recOwner

    def get_BirthDate(self) -> dt.date:
        return self.__birthDate

    def get_BirthDateStr(self, format : str = "%d.%m.%Y") -> str:
        try:
            timeStr = self.__birthDate.strftime(format)
            return timeStr
        except:
            return ""
        
    def get_DaysTo(self) -> int:
        temp = self.__birthDate.replace(year=self.__CURRENT_DATE.year)
        days = (temp - self.__CURRENT_DATE).days
        if days < 0:
            temp = self.__birthDate.replace(year=self.__CURRENT_DATE.year + 1)
        return (temp - self.__CURRENT_DATE).days

    def is_Today(self) -> bool:
        return self.get_DaysTo() == 0

    def is_InThisYear(self) -> bool:
        temp = self.__birthDate.replace(year=self.__CURRENT_DATE.year)
        return temp > self.__CURRENT_DATE

    def get_YearsOld(self) -> int:
        return self.__CURRENT_DATE.year - self.__birthDate.year - ((self.__CURRENT_DATE.month, self.__CURRENT_DATE.day) < (self.__birthDate.month, self.__birthDate.day))

    def get_Star(self) -> int:
        bd = self.__birthDate
        
        isDayMonthBeetween = lambda day, month, day1, month1 : bd >= dt.date(bd.year, month, day) and bd <= dt.date(bd.year, month1, day1)

        if isDayMonthBeetween(20, 1, 19, 2):
            return self.STAR_AQUARIUS
        elif isDayMonthBeetween(20, 2, 20, 3):
            return self.STAR_PISCES
        elif isDayMonthBeetween(21, 3, 19, 4):
            return self.STAR_ARIES
        elif isDayMonthBeetween(20, 4, 20, 5):
            return self.STAR_TAURUS
        elif isDayMonthBeetween(21, 5, 20, 6):
            return self.STAR_GEMINI
        elif isDayMonthBeetween(21, 6, 22, 7):
            return self.STAR_CANCER
        elif isDayMonthBeetween(23, 7, 22, 8):
            return self.STAR_LEO
        elif isDayMonthBeetween(23, 8, 22, 9):
            return self.STAR_VIRGO
        elif isDayMonthBeetween(23, 9, 23, 10):
            return self.STAR_LIBRA
        elif isDayMonthBeetween(24, 10, 22, 11):
            return self.STAR_SCORPIO
        elif isDayMonthBeetween(23, 11, 21, 12):
            return self.STAR_SAGITTARIUS
        elif isDayMonthBeetween(21, 12, 31, 12) or isDayMonthBeetween(1, 1, 19, 1): #trick for capricorn star, because it range beetween end year and start next year
            return self.STAR_CAPRICORN
        return -1

    def get_StarName(self) -> str:
        starCode : int = self.get_Star()
        if starCode == self.STAR_AQUARIUS:
            return "Aquarius" if self.LANG == "En" else "Водолей" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_PISCES:
            return "Pisces" if self.LANG == "En" else "Рыбы" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_ARIES:
            return "Aries" if self.LANG == "En" else "Овен" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_TAURUS:
            return "Taurus" if self.LANG == "En" else "Телец" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_GEMINI:
            return "Gemini" if self.LANG == "En" else "Близнецы" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_CANCER:
            return "Cancer" if self.LANG == "En" else "Рак" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_LEO:
            return "Leo" if self.LANG == "En" else "Лев" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_VIRGO:
            return "Virgo" if self.LANG == "En" else "Дева" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_LIBRA:
            return "Libra" if self.LANG == "En" else "Весы" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_SCORPIO:
            return "Scorpio" if self.LANG == "En" else "Скорпион" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_SAGITTARIUS:
            return "Sagittarius" if self.LANG == "En" else "Стрелец" if self.LANG == "Ru" else ""
        elif starCode == self.STAR_CAPRICORN:
            return "Capricorn" if self.LANG == "En" else "Козерог" if self.LANG == "Ru" else ""
        return ""

    def __str__(self):
        if self.LANG == "En":
            return "Invalid birthday!" if not self.is_Valid() else f"{self.__name}, {self.get_BirthDateStr()} " + \
                f"({self.get_StarName()}) " + \
                f"[{"" if not self.__recOwner else self.__recOwner}, {"" if not self.__tag else self.__tag}]: " + \
                f"{self.get_YearsOld()} year(s), {self.get_DaysTo()} days to {"(not in this year)" if not self.is_InThisYear() else ""}"
        elif self.LANG == "Ru":
            return "Невалидная запись!" if not self.is_Valid() else f"{self.__name}, {self.get_BirthDateStr()} " + \
                f"({self.get_StarName()}) " + \
                f"[{"" if not self.__recOwner else self.__recOwner}, {"" if not self.__tag else self.__tag}]: " + \
                f"{self.get_YearsOld()} лет(год), {self.get_DaysTo()} дней до {"(не в этом году)" if not self.is_InThisYear() else ""}"
    
    def __repr__(self):
        return self.__str__()
    

class BRTFile:
    def __init__(self, path : str, onlyValids : bool = True):
        self.__path = path
        self.__fn = str(os.path.basename(self.__path))
        self.__ready = False
        try:
            file = open(self.__path, "r")
            lines = file.read().splitlines()
        except:
            return

        lines = list(map(lambda s : s.strip(), lines)) #trim all lines
        lines = list(filter(lambda s : s and not s.startswith('#'), lines)) #remove empty lines and comment lines

        self.__mainOwner = None
        self.__mainTag = None

        #find and parse brt header:
        for line in lines:
            headSplit = line.split(':')
            if len(headSplit) > 1:
                headKey = headSplit[0].strip()
                headVal = headSplit[1].strip()
                if headKey == "!Owner":
                    self.__mainOwner = headVal
                elif headKey == "!Tag":
                    self.__mainTag = headVal

        self.__records = list()

        #find and parse brt records:
        for line in lines:
            recSplit = line.split(',')
            if len(recSplit) > 1:
                name = recSplit[0].strip()
                dtStr = recSplit[1].strip()
                try:
                    time.strptime(dtStr, "%d.%m.%Y") #dummy check for valid date format
                except:
                    continue

                recTag = recOwner = None
                if len(recSplit) > 2:
                    recOwner = recSplit[2].strip()
                    if not recOwner: recOwner = None
                    if len(recSplit) > 3:
                        recTag = recSplit[3].strip()
                        if not recTag: recTag = None

                if self.__mainOwner:
                    recOwner = self.__mainOwner
                if self.__mainTag:
                    recTag = self.__mainTag

                newRec = Birthday(name, dtStr, recTag, recOwner)
                if (onlyValids and newRec.is_Valid()) or (not onlyValids): 
                    self.__records.append(newRec)
                self.__ready = True
            
        
    def is_Ready(self) -> bool:
        return self.__ready
    
    def get_FileName(self) -> str:
        return self.__fn
    
    def get_MainOwner(self) -> str:
        return self.__mainOwner if self.__ready else None

    def get_MainTag(self) -> str | None:
        return self.__mainTag if self.__ready else None
    
    def get_Records(self) -> list[Birthday]:
        return copy.deepcopy(self.__records)
    

class BRTRequest:
    def __init__(self, recs : list[Birthday]):
        self.__recs = copy.deepcopy(recs)

    def __get_RecPropName(self, key : str) -> str | None:
        key = key.lower()
        if key == "isvalid":
            return "_Birthday__valid"
        if key == "name":
            return "_Birthday__name"
        if key == "tag":
            return "_Birthday__tag"
        if key == "birthdate":
            return "_Birthday__birthDate"
        if key == "owner":
            return "_Birthday__recOwner"
        if key == "daysto":
            return "get_DaysTo"
        if key == "istoday":
            return "is_Today"
        if key == "isinthisyear":
            return "is_InThisYear"
        if key == "yearsold":
            return "get_YearsOld"
        if key == "star":
            return "get_Star"
        return None

    def where(self, key : str, val):
        newRecs = list()
        propName = self.__get_RecPropName(key)
        if not propName:
            self.__recs = newRecs
            return self
        for rec in self.__recs:
            propVal = getattr(rec, propName)
            if callable(propVal):
                propVal = propVal()
            if type(val) is not type(propVal):
                self.__recs = newRecs
                return self
            if val == propVal:
                newRecs.append(rec)
        self.__recs = newRecs
        return self

    def sort(self, key : str, desk : bool):
        propName = self.__get_RecPropName(key)
        if not propName:
            return self
        def sortVal(rec : Birthday):
            propVal = getattr(rec, propName)
            if callable(propVal):
                propVal = propVal()
            return propVal
        
        self.__recs = sorted(self.__recs, key=sortVal, reverse=desk)
        return self

    def to_list(self) -> list[Birthday]:
            return self.__recs