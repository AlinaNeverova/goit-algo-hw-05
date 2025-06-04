def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        if arr[mid] < x:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1

    return (iterations, upper_bound)


arr = [1/5, 1/2, 1.1, 2.2, 3.3, 4.4, 5.5] # перебрала різні дробові значення
x = 1.3

result = binary_search(arr, x)
print(result)