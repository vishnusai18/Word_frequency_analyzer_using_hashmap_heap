
# did not use ai or any other tools for this below class implementation


class HashMap:
    def __init__(self, size=10007):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

    def get(self, key, default=None):
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return default

    def increment(self, key, amount=1):
        current = self.get(key, 0)
        if current == 0 and self.get(key) is None:
            self.put(key, amount)
        else:
            self.put(key, current + amount)

    def items(self):
        for bucket in self.buckets:
            for item in bucket:
                yield item

    def keys(self):
        for k, _ in self.items():
            yield k

    def values(self):
        for _, v in self.items():
            yield v

    def __len__(self):
        return self.count