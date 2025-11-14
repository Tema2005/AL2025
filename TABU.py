import random
from typing import List, Tuple, Set

def input_data() -> Tuple[int, int, List[int], int, int, int]: 
    print("=== Ввод данных для оптимизации расписания ===")
    n_workers = int(input("Количество работников: "))
    n_days = int(input("Количество дней в периоде: "))
    
    required_days = []
    for i in range(n_workers): 
        req = int(input(f"Требуемое число рабочих дней для работника {i+1}: "))
        required_days.append(req)
    
    max_consecutive = int(input("Максимальное число рабочих дней подряд (штраф за превышение): "))
    tabu_tenure = int(input("Длительность табу (число итераций): "))
    max_iterations = int(input("Максимальное число итераций: "))
    
    return n_workers, n_days, required_days, max_consecutive, tabu_tenure, max_iterations

def initial_solution(n_workers: int, n_days: int, required_days: List[int]) -> List[List[int]]: 
    """Генерирует начальное расписание (случайное, но с учётом требуемых дней)."""
    schedule = [[0] * n_days for _ in range(n_workers)]
    
    for w in range(n_workers): 
        days_needed = required_days[w]
        available_days = list(range(n_days))
        selected_days = random.sample(available_days, min(days_needed, n_days))
        for d in selected_days: 
            schedule[w][d] = 1
    return schedule

def evaluate(schedule: List[List[int]], required_days: List[int], max_consecutive: int) -> int: 
    """Вычисляет штраф (чем меньше, тем лучше)."""
    total_penalty = 0
    
    # Штраф за отклонение от требуемого числа дней
    for w, row in enumerate(schedule): 
        actual = sum(row)
        total_penalty += abs(actual - required_days[w]) * 10  # вес 10
    
    # Штраф за слишком много дней подряд
    for w, row in enumerate(schedule): 
        consecutive = 0
        for day in row: 
            if day == 1: 
                consecutive += 1
                if consecutive > max_consecutive: 
                    total_penalty += 5  # вес 5 за каждое превышение
            else: 
                consecutive = 0
    
    return total_penalty

def generate_neighbors(schedule: List[List[int]], tabu_set: Set[Tuple[int, int, int]]) -> List[Tuple[List[List[int]], Tuple[int, int, int]]]: 
    """Генерирует соседние решения (перемещение одного рабочего в один день)."""
    neighbors = []
    n_workers, n_days = len(schedule), len(schedule[0])
    
    for w in range(n_workers): 
        for d in range(n_days): 
            # Попробуем убрать рабочего w в день d (если он там есть)
            if schedule[w][d] == 1: 
                for w2 in range(n_workers): 
                    if w2 != w and schedule[w2][d] == 0: 
                        # Переместим w → w2 в день d
                        new_schedule = [row[:] for row in schedule]
                        new_schedule[w][d] = 0
                        new_schedule[w2][d] = 1
                        move = (w, d, w2)  # кто, откуда, куда
                        if move not in tabu_set: 
                            neighbors.append((new_schedule, move))
            # Попробуем добавить рабочего w в день d (если его там нет)
            else: 
                for w2 in range(n_workers): 
                    if w2 != w and schedule[w2][d] == 1: 
                        # Переместим w2 → w в день d
                        new_schedule = [row[:] for row in schedule]
                        new_schedule[w2][d] = 0
                        new_schedule[w][d] = 1
                        move = (w2, d, w)  # кто, откуда, куда
                        if move not in tabu_set: 
                            neighbors.append((new_schedule, move))
    
    return neighbors

def tabu_search(
    n_workers: int, 
    n_days: int, 
    required_days: List[int], 
    max_consecutive: int, 
    tabu_tenure: int, 
    max_iterations: int
) -> Tuple[List[List[int]], int]: 
    
    # Начальное решение
    current_schedule = initial_solution(n_workers, n_days, required_days)
    current_penalty = evaluate(current_schedule, required_days, max_consecutive)
    
    best_schedule = [row[:] for row in current_schedule]
    best_penalty = current_penalty
    
    tabu_list = []  # список табу-ходов (с истекающим сроком)
    tabu_set = set()  # для быстрого поиска
    
    print(f"\nНачальное качество (штраф): {current_penalty}")
    
    for iter in range(max_iterations): 
        # Генерируем соседей, не попадающих в табу
        neighbors = generate_neighbors(current_schedule, tabu_set)
        
        if not neighbors: 
            print("Нет доступных соседей (возможно, застряли). Прекращаем.")
            break
        
        # Выбираем лучшего соседа (с минимальным штрафом)
        best_neighbor = None
        best_neighbor_penalty = float('inf')
        best_move = None
        
        for neigh_schedule, move in neighbors: 
            penalty = evaluate(neigh_schedule, required_days, max_consecutive)
            if penalty < best_neighbor_penalty: 
                best_neighbor = neigh_schedule
                best_neighbor_penalty = penalty
                best_move = move
        
        # Если не нашли улучшение, прекращаем
        if best_neighbor is None:
            print("Не удалось найти улучшение. Прекращаем.")
            break
            
        # Обновляем текущее решение
        current_schedule = best_neighbor
        current_penalty = best_neighbor_penalty
        
        # Обновляем лучшее решение
        if current_penalty < best_penalty: 
            best_schedule = [row[:] for row in current_schedule]
            best_penalty = current_penalty
            print(f"Итерация {iter+1}: новое лучшее качество = {best_penalty}")
        
        # Добавляем ход в табу-лист
        if best_move is not None:
            tabu_list.append((best_move, iter))
            tabu_set.add(best_move)
        
        # Удаляем устаревшие табу
        tabu_list = [(move, it) for move, it in tabu_list if iter - it < tabu_tenure]
        tabu_set = {move for move, _ in tabu_list}
    
    return best_schedule, best_penalty

def print_schedule(schedule: List[List[int]], required_days: List[int]): 
    print("\n=== Финальное расписание ===")
    n_workers, n_days = len(schedule), len(schedule[0])
    print("День\t", end="")
    for d in range(n_days): 
        print(d+1, end="\t")
    print(" (рабочих дней)")
    
    for w in range(n_workers): 
        print(f"Р{w+1}\t", end="")
        for d in range(n_days): 
            print("X" if schedule[w][d] == 1 else ".", end="\t")
        actual = sum(schedule[w])
        print(f" ({actual}/{required_days[w]})")
    
    print("\nОбозначения: X - рабочий день, . - выходной")

def main():
    n_workers, n_days, required_days, max_consecutive, tabu_tenure, max_iterations = input_data()
    best_schedule, best_penalty = tabu_search(n_workers, n_days, required_days, max_consecutive, tabu_tenure, max_iterations)
    print_schedule(best_schedule, required_days)
    print(f"\nФинальный штраф: {best_penalty}")

if __name__ == "__main__":
    main()
