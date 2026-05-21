class InfiniteWord:
    def __init__(self):
        pass
    
    def get_range(self, start, end):
        return [0]*(end-start)
    
    def __len__(self):
        return float("inf")
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return [0]*((index.stop-index.start)//index.step)
        return 0

    def __radd__(self, other):
        return other