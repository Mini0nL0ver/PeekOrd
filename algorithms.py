# example algorithms:

def split(lst):
    mid = len(lst)//2
    return lst[:mid], lst[mid:]


def merge(lst_x, lst_y):
    match (lst_x, lst_y):
        case ([], []):
            return []
        case (_, []):
            return lst_x
        case ([], _):
            return lst_y
        case ([x, *xs], [y, *ys]):
            if x < y:
                return [x] + merge(xs, lst_y)
            else:
                return [y] + merge(lst_x, ys)


def merge_sort(lst):
    match lst:
        case []:
            return []
        case [x]:
            return [x]
        case _:
            mid = len(lst)//2
            return merge(merge_sort(lst[mid:]), merge_sort(lst[:mid]))

