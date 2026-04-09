from django.shortcuts import render
from django.http import JsonResponse
import json
from collections import deque
from django.views.decorators.csrf import csrf_exempt
import heapq

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

def bubble_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []
        
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                steps.append({
                    'array': arr.copy(),
                    'i': i, 'j': j,
                    'swap': False
                })
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps[-1]['swap'] = True
        
        return JsonResponse({'steps': steps, 'code_step': 'i=0..n-1, j=0..n-i-2: if arr[j]>arr[j+1] swap'})
    
    return render(request, 'algorithms/bubble_sort.html')

@csrf_exempt
def insertion_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []
        
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            steps.append({'array': arr.copy(), 'i': i, 'j': j, 'key': key})
            
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                steps.append({'array': arr.copy(), 'i': i, 'j': j, 'key': key, 'shift': True})
            
            arr[j + 1] = key
            steps[-1]['insert'] = True
        
        return JsonResponse({'steps': steps, 'code_step': 'for i=1..n: key=arr[i], j=i-1, while j>=0 and arr[j]>key: arr[j+1]=arr[j], j-=1, arr[j+1]=key'})
    
    return render(request, 'algorithms/insertion_sort.html')

@csrf_exempt
def merge_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []
        
        def merge(left, right):
            result = []
            i = j = 0
            merge_steps = []
            
            while i < len(left) and j < len(right):
                merge_steps.append({
                    'left': left[:], 'right': right[:],
                    'i': i, 'j': j, 'merged': result[:]
                })
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result += left[i:]
            result += right[j:]
            return result, merge_steps
        
        def msort(arr):
            if len(arr) <= 1:
                return arr, []
            
            mid = len(arr) // 2
            left, left_steps = msort(arr[:mid])
            right, right_steps = msort(arr[mid:])
            
            merged, merge_steps = merge(left, right)
            steps.extend(left_steps + right_steps + merge_steps)
            return merged, steps
        
        final_arr, all_steps = msort(arr)
        return JsonResponse({'steps': steps, 'final': final_arr, 'code_step': 'divide: merge(left, right)'})
    
    return render(request, 'algorithms/merge_sort.html')

def quick_sort(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arr = [int(x) for x in data['numbers']]
        steps = []
        
        def partition(low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                steps.append({'array': arr.copy(), 'pivot': pivot, 'i': i, 'j': j, 'low': low, 'high': high})
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def qsort(low, high):
            if low < high:
                pi = partition(low, high)
                qsort(low, pi - 1)
                qsort(pi + 1, high)
        
        qsort(0, len(arr) - 1)
        return JsonResponse({'steps': steps, 'code_step': 'partition: i=low-1, for j=low..high-1 if arr[j]<pivot swap'})
    
    return render(request, 'algorithms/quick_sort.html')

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
        
        def dfs_recursive(node):
            visited[node] = True
            steps.append({
                'visited': visited[:],
                'current': node,
                'stack': [],
                'graph': graph
            })
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start)
        return JsonResponse({'steps': steps})
    
    return render(request, 'algorithms/dfs.html')

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
                'n': n, 'i': i, 'largest': largest,
                'l': l if l < n else -1,
                'r': r if r < n else -1,
                'heap_size': n,
                'phase': 'heapify'
            })
            
            if l < n and arr[l] > arr[largest]:
                largest = l
            
            if r < n and arr[r] > arr[largest]:
                largest = r
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                steps[-1]['swap'] = True
                heapify(n, largest)
        
        # Строим Max Heap
        n = len(arr)
        for i in range(n//2 - 1, -1, -1):
            steps.append({
                'array': arr.copy(),
                'i': i, 'phase': 'build_heap',
                'heap_size': n
            })
            heapify(n, i)
        
        # Извлекаем максимумы
        for i in range(n-1, 0, -1):
            steps.append({
                'array': arr.copy(),
                'i': i, 'phase': 'extract',
                'heap_size': i
            })
            arr[0], arr[i] = arr[i], arr[0]
            steps[-1]['swap_root'] = True
            heapify(i, 0)
        
        return JsonResponse({'steps': steps, 'code_step': 'heapify + extract max'})
    
    return render(request, 'algorithms/heap_sort.html')
