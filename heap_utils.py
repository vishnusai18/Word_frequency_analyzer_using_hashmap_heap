from heapq import heapify, heappop, heappush, heapreplace

# did not use ai or other tools
def top_k_word_counts(items, k):
    if k <= 0:
        return []

    min_heap = []
    for word, count in items:
        count = int(count)
        entry = (count, word)
        if len(min_heap) < k:
            heappush(min_heap, entry)
        elif entry > min_heap[0]:
            heapreplace(min_heap, entry)

    max_heap = [(-count, word) for count, word in min_heap]
    heapify(max_heap)

    result = []
    while max_heap:
        neg_count, word = heappop(max_heap)
        result.append((word, -neg_count))
    return result


def least_k_word_counts(items, k):
    if k <= 0:
        return []

    max_heap = []
    for word, count in items:
        count = int(count)
        entry = (-count, word)
        if len(max_heap) < k:
            heappush(max_heap, entry)
            continue

        current_largest_count = -max_heap[0][0]
        if count < current_largest_count:
            heapreplace(max_heap, entry)

    min_heap = [(-neg_count, word) for neg_count, word in max_heap]
    heapify(min_heap)

    result = []
    while min_heap:
        count, word = heappop(min_heap)
        result.append((word, count))
    return result


def at_least_k_word_counts(items, min_count):
    max_heap = [(-int(count), word) for word, count in items]
    heapify(max_heap)

    result = []
    while max_heap and -max_heap[0][0] >= min_count:
        neg_count, word = heappop(max_heap)
        result.append((word, -neg_count))
    return result


def to_dict_list(items):
    return [{"word": word, "count": count} for word, count in items]
