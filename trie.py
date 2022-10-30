class Trie:

    def __init__(self, extension: str):
        self.root = {}
        self.extension = extension

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.setdefault(char, {})    
        node['key'] = True                      

    def search(self, word: str) -> bool:

        node = self.root                

        for char in word:
                if char in node:                    
                    node = node[char]               
                else:                               
                    if char !='\n':
                        return False

        return True if 'key' in node else False



        



        