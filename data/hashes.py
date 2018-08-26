class Hashlist:
    def __init__(self, file):
        self.hash_to_name = {}
        self.name_to_hash = {}
        self.hash_to_type = {}
        self.file = file
        self.__loadhashes()


    def __loadhashes(self):
        with open(self.file) as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for i in range(0, len(lines), 2):
            try:
                string = lines[i]
                hash = lines[i+1]
                self.hash_to_name[hash] = string
                self.name_to_hash[string] = hash
            except:
                pass