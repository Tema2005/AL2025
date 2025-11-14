def read_graph(): 
    print("Введите количество вершин графа: ")
    n = int(input().strip())
    
    print("Введите рёбра в формате 'u v' (без кавычек),  по одному на строку.")
    print("Чтобы завершить ввод,  введите пустую строку.")
    
    edges = []
    while True: 
        try:
            line = input().strip()
            if not line: 
                break
            u, v = map(int, line.split())
            if u < 1 or u > n or v < 1 or v > n: 
                print(f"Вершина должна быть от 1 до {n}. Пропускаем ребро.")
                continue
            if u == v: 
                print("Ребро не может соединять вершину саму с собой. Пропускаем.")
                continue
            edges.append((u, v))
        except ValueError:
            print("Некорректный формат ввода. Пропускаем строку.")
            continue
    
    return n, edges



def max_cut_greedy(n, edges): 
    # Группы: 0 и 1
    group = [0] * (n + 1)  # group[1..n], индекс 0 не используется
    
    # Для каждой вершины (начиная со 2-й) выбираем группу, максимизирующую текущий разрез
    for v in range(2, n + 1): 
        count_0 = 0  # число рёбер из v в группу 0
        count_1 = 0  # число рёбер из v в группу 1
        
        for u, w in edges: 
            if u == v and group[w] == 0: 
                count_0 += 1
            elif u == v and group[w] == 1: 
                count_1 += 1
            elif w == v and group[u] == 0: 
                count_0 += 1
            elif w == v and group[u] == 1: 
                count_1 += 1
        
        # Назначаем вершину v в группу, где больше «выигрышных» рёбер
        if count_0 >= count_1: 
            group[v] = 1  # больше рёбер в группу 0 → ставим в 1 (увеличиваем разрез)
        else: 
            group[v] = 0  # иначе в 0
    
    # Собираем группы
    group_0 = [i for i in range(1, n + 1) if group[i] == 0]
    group_1 = [i for i in range(1, n + 1) if group[i] == 1]
    
    # Считаем число рёбер в разрезе
    cut_size = 0
    for u, v in edges: 
        if group[u] != group[v]: 
            cut_size += 1
    
    return group_0, group_1, cut_size



def main(): 
    print("=== Жадный алгоритм для MAX-CUT ===\n")
    
    try:
        n, edges = read_graph()
    except ValueError:
        print("Ошибка ввода данных.")
        return
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        return
    
    if n == 0: 
        print("Граф без вершин.")
        return
    
    if not edges: 
        print("Граф без рёбер. Разрез = 0.")
        print("Группа 0: ", list(range(1, n + 1)))
        print("Группа 1: ", [])
        return
    
    group_0, group_1, cut_size = max_cut_greedy(n, edges)
    
    print("\n=== Результат ===")
    print("Группа 0 (метка 0): ", sorted(group_0))
    print("Группа 1 (метка 1): ", sorted(group_1))
    print("Количество рёбер в разрезе: ", cut_size)



if __name__ == "__main__": 
    main()
