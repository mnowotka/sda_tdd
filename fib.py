class Fibbonacci:
    def __init__(self, n):
        self.n = n
        self.current = 0
        self.iteration = 0
        self.next = 1
    def __next__(self):
        print("method __next__ returned!")
        if self.iteration == self.n:
            raise StopIteration
        self.iteration += 1
        ret = self.current
        self.current = self.next
        self.next += ret
        return ret
    def __iter__(self):
        print("method __iter__ returned!")
        return self
if __name__=='__main__':
    for i in Fibbonacci(10):
        print(i)