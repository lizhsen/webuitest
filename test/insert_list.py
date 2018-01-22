# -*- coding: utf-8 -*-

lists = [10,9,8,7,6,5,4,3,2,1]


def insert_list(lists):
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j+1] = lists[j]
                lists[j] = key
                j -= 1
    print lists
    return lists


def bubble_sort(lists):
    count = len(lists)
    for i in range(count):
        for j in range(i+1, count):
            if lists[i] > lists[j]:
                lists[i], lists[j] = lists[j], lists[i]
    print lists
    return lists


def quick_sort(lists, left, right):
    if left >= right:
        return lists
    key = lists[left]
    low = left
    high = right
    while left < right:
        while left < right and lists[right] >= key:
            right -= 1
        lists[left] = lists[right]
        while left < right and lists[left] <= key:
            left += 1
        lists[right] = lists[left]
    lists[left] = key
    quick_sort(lists, low, left-1)
    quick_sort(lists, left+1, high)
    print(lists)
    return lists


quick_sort(lists, 0, len(lists)-1)
# insert_list(lists)
# bubble_sort(lists)

