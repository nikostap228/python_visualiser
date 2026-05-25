from django.shortcuts import render
from django.http import JsonResponse
import json
from collections import deque
from django.views.decorators.csrf import csrf_exempt


def index(request):
    algorithms = [
        {'name': 'Пузырьковая сортировка', 'url': 'bubble_sort', 'type': 'Сортировка'},
        {'name': 'Быстрая сортировка', 'url': 'quick_sort', 'type': 'Сортировка'},
        {'name': 'Сортировка вставками', 'url': 'insertion_sort', 'type': 'Сортировка'},
        {'name': 'Сортировка слиянием', 'url': 'merge_sort', 'type': 'Сортировка'},
        {'name': 'Поиск в ширину (BFS)', 'url': 'bfs', 'type': 'Графы'},
        {'name': 'Поиск в глубину (DFS)', 'url': 'dfs', 'type': 'Графы'},
        {'name': 'Пирамидальная сортировка', 'url': 'heap_sort', 'type': 'Сортировка'}
    ]
    return render(request, 'algorithms/index.html', {'algorithms': algorithms})


@csrf_exempt
def bubble_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []
        n = len(arr)

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                steps.append({
                    'array': arr.copy(),
                    'i': i,
                    'j': j,
                    'sorted_upto': n - i,
                    'swap': False,
                    'phase': 'compare'
                })
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    steps[-1]['swap'] = True

            steps.append({
                'array': arr.copy(),
                'i': i,
                'sorted_upto': n - i,
                'phase': 'pass_done'
            })

            if not swapped:
                break

        return JsonResponse({'steps': steps, 'code_step': 'bubble sort'})
    return render(request, 'algorithms/bubble_sort.html')


@csrf_exempt
def insertion_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []
        sorted_upto = 0

        for i in range(1, len(arr)):
            # Выбор ключа
            key = arr[i]
            steps.append({
                'array': arr.copy(),
                'i': i,
                'j': i - 1,
                'key': key,
                'phase': 'key',
                'sorted_upto': sorted_upto
            })

            j = i - 1
            # Сдвиги
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                steps.append({
                    'array': arr.copy(),
                    'i': i,
                    'j': j,
                    'key': key,
                    'phase': 'shift',
                    'sorted_upto': sorted_upto
                })
                j -= 1

            # Вставка
            insert_pos = j + 1
            arr[insert_pos] = key
            sorted_upto = max(sorted_upto, insert_pos + 1)
            steps.append({
                'array': arr.copy(),
                'i': i,
                'j': insert_pos,
                'key': key,
                'phase': 'insert',
                'sorted_upto': sorted_upto
            })

        return JsonResponse({'steps': steps})
    return render(request, 'algorithms/insertion_sort.html')


@csrf_exempt
def merge_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []

        def merge(left, right, left_start, right_start):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                steps.append({
                    'left': left[:],
                    'right': right[:],
                    'i': i,
                    'j': j,
                    'merged': result[:],
                    'left_start': left_start,
                    'right_start': right_start,
                    'phase': 'compare'
                })
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            while i < len(left):
                result.append(left[i])
                i += 1
                steps.append({
                    'left': left[:],
                    'right': right[:],
                    'i': i,
                    'j': j,
                    'merged': result[:],
                    'left_start': left_start,
                    'right_start': right_start,
                    'phase': 'append_left'
                })

            while j < len(right):
                result.append(right[j])
                j += 1
                steps.append({
                    'left': left[:],
                    'right': right[:],
                    'i': i,
                    'j': j,
                    'merged': result[:],
                    'left_start': left_start,
                    'right_start': right_start,
                    'phase': 'append_right'
                })

            return result

        def msort(a, start):
            if len(a) <= 1:
                return a

            mid = len(a) // 2
            left = msort(a[:mid], start)
            right = msort(a[mid:], start + mid)
            merged = merge(left, right, start, start + mid)
            return merged

        final_arr = msort(arr, 0)
        return JsonResponse({'steps': steps, 'final': final_arr, 'code_step': 'merge sort'})
    return render(request, 'algorithms/merge_sort.html')


@csrf_exempt
def quick_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []

        def partition(low, high):
            pivot = arr[high]
            i = low - 1

            steps.append({
                'array': arr.copy(),
                'pivot': pivot,
                'pivot_idx': high,
                'i': i,
                'j': high,
                'low': low,
                'high': high,
                'phase': 'choose_pivot'
            })

            for j in range(low, high):
                steps.append({
                    'array': arr.copy(),
                    'pivot': pivot,
                    'pivot_idx': high,
                    'i': i,
                    'j': j,
                    'low': low,
                    'high': high,
                    'phase': 'compare'
                })

                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    steps.append({
                        'array': arr.copy(),
                        'pivot': pivot,
                        'pivot_idx': high,
                        'i': i,
                        'j': j,
                        'low': low,
                        'high': high,
                        'phase': 'swap'
                    })

            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            pi = i + 1

            steps.append({
                'array': arr.copy(),
                'pivot': pivot,
                'pivot_idx': pi,
                'i': i,
                'j': high,
                'pi': pi,
                'low': low,
                'high': high,
                'phase': 'pivot_swap'
            })

            steps.append({
                'array': arr.copy(),
                'pivot': pivot,
                'pivot_idx': pi,
                'i': i,
                'j': high,
                'pi': pi,
                'low': low,
                'high': high,
                'sorted_left': pi,
                'sorted_right': pi,
                'phase': 'partition_done'
            })

            return pi

        def qsort(low, high):
            if low < high:
                pi = partition(low, high)
                qsort(low, pi - 1)
                qsort(pi + 1, high)

        qsort(0, len(arr) - 1)

        steps.append({
            'array': arr.copy(),
            'phase': 'done',
            'sorted_left': 0,
            'sorted_right': len(arr) - 1
        })

        return JsonResponse({'steps': steps, 'code_step': 'quick sort'})

    return render(request, 'algorithms/quick_sort.html')


@csrf_exempt
def heap_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []

        def heapify(n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            steps.append({
                'array': arr.copy(),
                'n': n,
                'i': i,
                'largest': largest,
                'l': l if l < n else -1,
                'r': r if r < n else -1,
                'heap_size': n,
                'phase': 'heapify'
            })

            if l < n and arr[l] > arr[largest]:
                largest = l
            if r < n and arr[r] > arr[largest]:
                largest = r

            steps[-1]['largest'] = largest

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                steps[-1]['swap'] = True
                steps.append({
                    'array': arr.copy(),
                    'n': n,
                    'i': i,
                    'largest': largest,
                    'l': l if l < n else -1,
                    'r': r if r < n else -1,
                    'heap_size': n,
                    'phase': 'swap_done'
                })
                heapify(n, largest)

        n = len(arr)

        for i in range(n // 2 - 1, -1, -1):
            steps.append({
                'array': arr.copy(),
                'i': i,
                'heap_size': n,
                'phase': 'build_heap'
            })
            heapify(n, i)

        for i in range(n - 1, 0, -1):
            steps.append({
                'array': arr.copy(),
                'i': i,
                'heap_size': i,
                'phase': 'extract'
            })
            arr[0], arr[i] = arr[i], arr[0]
            steps[-1]['swap_root'] = True
            steps.append({
                'array': arr.copy(),
                'i': i,
                'heap_size': i,
                'phase': 'root_swapped',
                'swap_root': True
            })
            heapify(i, 0)

        return JsonResponse({'steps': steps, 'code_step': 'heap sort'})
    return render(request, 'algorithms/heap_sort.html')


@csrf_exempt
def bfs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        graph = data['graph']
        start = data['start']
        steps = []

        visited = [False] * len(graph)
        queue = deque([start])
        visited[start] = True

        while queue:
            node = queue.popleft()
            steps.append({
                'queue': list(queue),
                'visited': visited[:],
                'current': node,
                'graph': graph
            })

            for neighbor in graph[node]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    steps[-1]['added'] = neighbor

        return JsonResponse({'steps': steps})

    return render(request, 'algorithms/bfs.html')


@csrf_exempt
def dfs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        graph = data['graph']
        start = data['start']
        steps = []

        visited = [False] * len(graph)

        def dfs_recursive(node, stack):
            visited[node] = True
            steps.append({
                'visited': visited[:],
                'current': node,
                'stack': stack[:] + [node],
                'graph': graph
            })

            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs_recursive(neighbor, stack + [node])

        dfs_recursive(start, [])
        return JsonResponse({'steps': steps})

    return render(request, 'algorithms/dfs.html')