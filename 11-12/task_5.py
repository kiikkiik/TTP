def execute_task_5_algorithm(arr, target_sum):
    arr = list(map(int, arr)) 
    target = int(target_sum)
    count = 0
    n = len(arr)
    
    for i in range(n):
        sum_now = 0
        for j in range(i, n):
            sum_now += arr[j]
            if sum_now == target:
                count += 1
    return count
if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5]
    target = 5
    print(execute_task_5_algorithm(arr, target))
    # Вывод: ([2], 2) - подмассивы [2,3] и [5]
  