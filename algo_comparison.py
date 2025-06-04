import timeit

# Підвантажуємо наші статті
def load_text(filename):
    with open(filename, 'r', encoding='ISO-8859-1') as f: # використовується ISO-8859-1 для кодування, бо текст містить символи, які не підтримуються UTF-8
        return f.read()
text1 = load_text('article1.txt')
text2 = load_text('article2.txt')


# Створюємо реальні та фейкові підрядки
real_substring1 = text1[:30] # перші 30 символів тексту 1
fake_substring1 = "нудний_фейковий_підрядок_який_не_існує"
real_substring2 = text2[-50:] # останні 50 символів тексту 2
fake_substring2 = "ще_один_фейковий_підрядок_який_не_існує"


# Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1


# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1


# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    base = 256 
    modulus = 101  
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1


# Функція для вимірювання часу виконання алгоритму
def measure_time(algorithm, text, pattern):
    start_time = timeit.default_timer()
    algorithm(text, pattern)
    end_time = timeit.default_timer()
    return end_time - start_time


# Порівняння алгоритмів
def compare_algorithms(text, real_pattern, fake_pattern):
    algorithms = {
        'KMP': kmp_search,
        'Boyer-Moore': boyer_moore_search,
        'Rabin-Karp': rabin_karp_search
    }
    result = {}
    for name, algo in algorithms.items():
        real_time = measure_time(algo, text, real_pattern)
        fake_time = measure_time(algo, text, fake_pattern)
        result[name] = {
            'real_substring': real_time,
            'fake_substring': fake_time
        }
    return result


# Виконуємо порівняння для кожного тексту
res1 = compare_algorithms(text1, real_substring1, fake_substring1)
res2 = compare_algorithms(text2, real_substring2, fake_substring2)

print("Results for Article 1:")
for alg, times in res1.items():
    print(f"{alg} - Real: {times['real_substring']:.6f}s | Fake: {times['fake_substring']:.6f}s")

print("\nResults for Article 2:")
for alg, times in res2.items():
    print(f"{alg} - Real: {times['real_substring']:.6f}s | Fake: {times['fake_substring']:.6f}s")
