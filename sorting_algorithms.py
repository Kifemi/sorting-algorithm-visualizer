# BUBBLE SORT
def bubble_sort(visualizer, ascending=True, *args):
    lst = visualizer.lst
    for i in range(len(lst) - 1):
        is_sorted = True
        for j in range(1, len(lst) - i):
            if (lst[j - 1] > lst[j] and ascending) or (lst[j - 1] < lst[j] and not ascending):
                lst[j - 1], lst[j] = lst[j], lst[j - 1]
                visualizer.draw_list({j - 1: visualizer.settings.GREEN, j: visualizer.settings.RED}, clear_bg=True)
                is_sorted = False
                yield True
        if is_sorted:
            return


# INSERTION SORT
def insertion_sort(visualizer, ascending=True, *args):
    lst = visualizer.lst
    for i in range(1, len(lst)):
        anchor = lst[i]
        j = i - 1
        while j >= 0 and ((lst[j] > anchor and ascending) or (lst[j] < anchor and not ascending)):
            lst[j+1] = lst[j]
            visualizer.draw_list({j: visualizer.settings.GREEN, j + 1: visualizer.settings.RED}, clear_bg=True)
            yield True
            j -= 1
        lst[j+1] = anchor


# SHELL SORT
def shell_sort(visualizer, ascending=True, *args):
    lst = visualizer.lst
    size = len(lst)
    if size < 2:
        yield True
        return
    step = size // 2

    while step > 0:
        for i in range(step):
            for j in range(step + i, size, step):
                if step != 1:
                    color_positions = {n: visualizer.settings.PURPLE for n in range(i, size, step)}
                else:
                    color_positions = {}
                anchor = lst[j]
                while j >= step and ((lst[j - step] > anchor and ascending) or
                                     (lst[j - step] < anchor and not ascending)):
                    lst[j] = lst[j - step]
                    color_positions[j - step] = visualizer.settings.GREEN
                    color_positions[j] = visualizer.settings.RED
                    visualizer.draw_list(color_positions=color_positions, clear_bg=True)
                    yield True
                    j -= step
                    if step != 1:
                        color_positions = {n: visualizer.settings.PURPLE for n in range(i, size, step)}
                    else:
                        color_positions = {}
                    visualizer.draw_list(color_positions=color_positions, clear_bg=True)
                lst[j] = anchor
        step //= 2


# QUICK SORT
def quick_sort(visualizer, ascending=True, start=0, end=None):
    lst = visualizer.lst
    if len(lst) < 2:
        yield True
        return
    end = end if end is not None else len(lst) - 1
    if 0 <= start < end:
        size = len(lst)
        pivot_index = start
        pivot = lst[pivot_index]
        start_temp = start
        end_temp = end

        while start_temp < end_temp:
            while start_temp < size and ((lst[start_temp] <= pivot and ascending) or
                                         (lst[start_temp] >= pivot and not ascending)):
                start_temp += 1
            while end_temp > 0 and ((lst[end_temp] > pivot and ascending) or (lst[end_temp] < pivot and not ascending)):
                end_temp -= 1

            if start_temp < end_temp:
                swap(visualizer, start_temp, end_temp)
                yield True
        swap(visualizer, pivot_index, end_temp)
        yield True
        partition_index = end_temp
        yield from quick_sort(visualizer, ascending, start, partition_index - 1)
        yield from quick_sort(visualizer, ascending, partition_index + 1, end)


# MERGE SORT
def merge_sort(visualizer, ascending, *args, start=None, end=None):
    start_temp = start if start is not None else 0
    end_temp = end if end is not None else len(visualizer.lst)

    size = end_temp - start_temp

    if size < 2:
        yield True
        return

    mid = size // 2

    yield from merge_sort(visualizer, ascending, start=start_temp, end=start_temp + mid)
    yield from merge_sort(visualizer, ascending, start=start_temp + mid, end=start_temp + size)
    yield from merge_sorted_arrays(visualizer, ascending, start_temp, start_temp + mid, start_temp + size)


def merge_sorted_arrays(visualizer, ascending, start, mid, end):
    lst = visualizer.lst
    left = lst[start:mid]
    right = lst[mid:end]
    len_left = len(left)
    len_right = len(right)
    i = j = 0
    k = start

    color_positions = {i: visualizer.settings.GREEN if i < mid else visualizer.settings.RED for i in range(start, end)}
    visualizer.draw_list(color_positions=color_positions,
                         clear_bg=True)
    while i < len_left and j < len_right:
        if (left[i] < right[j] and ascending) or (left[i] > right[j] and not ascending):
            lst[k] = left[i]
            i += 1
            visualizer.draw_list(color_positions=color_positions, clear_bg=True)
            yield True
        else:
            lst[k] = right[j]
            j += 1
            visualizer.draw_list(color_positions=color_positions, clear_bg=True)
            yield True
        k += 1
    while i < len_left:
        lst[k] = left[i]
        i += 1
        k += 1
        visualizer.draw_list(color_positions=color_positions, clear_bg=True)
        yield True
    while j < len_right:
        lst[k] = right[j]
        j += 1
        k += 1
        visualizer.draw_list(color_positions=color_positions, clear_bg=True)
        yield True


# HEAP SORT
def heapify(visualizer, ascending, size, i):
    root = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < size and ((visualizer.lst[left] > visualizer.lst[root] and ascending) or
                        (visualizer.lst[left] < visualizer.lst[root] and not ascending)):
        root = left
        yield True

    if right < size and ((visualizer.lst[right] > visualizer.lst[root] and ascending) or
                         (visualizer.lst[right] < visualizer.lst[root] and not ascending)):
        root = right
        yield True

    if root != i:
        swap(visualizer, root, i, check_if_equal=False)
        yield True
        yield from heapify(visualizer, ascending, size, root)


def heap_sort(visualizer, ascending, *args):
    size = len(visualizer.lst)
    if size < 2:
        return

    # Build a max heap
    for i in range(size // 2, -1, -1):
        yield from heapify(visualizer, ascending, size, i)

    # Sort the max heap
    for i in range(size - 1, 0, -1):
        swap(visualizer, 0, i, check_if_equal=False)
        yield True
        yield from heapify(visualizer, ascending, i, 0)


# UTILITY
def swap(visualizer, a, b, check_if_equal=True):
    if check_if_equal and a == b:
        return
    visualizer.lst[a], visualizer.lst[b] = visualizer.lst[b], visualizer.lst[a]
    visualizer.draw_list({a: visualizer.settings.GREEN, b: visualizer.settings.RED}, clear_bg=True)
