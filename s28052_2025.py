import random


def generate_dna_sequence(length, gc_content=0.5):
    """Generuje losową sekwencję DNA o podanej długości"""
    nucleotides = ['A', 'C', 'G', 'T'] # tabela nukleotydów
    # ORIGINAL: 
    #     return ''.join(random.choice(nucleotides) for _ in range(length))
    # MODIFIED ( dodanie prawdopodobieństwa GC do AT):
    prob_gc = gc_content / 2 # prawdopodobieństwo G i C z zawartości gc_content
    prob_at = (1 - gc_content) / 2 # prawdopodobieństwo A i T proporcjonalnie odwrotna do gc_content
    probabilities = [prob_at, prob_gc, prob_gc, prob_at] #prawdopodobieństwa dla A, C, G, T
    return ''.join(random.choices(nucleotides, probabilities, k=length)) # zwraca sekwencję o długości length z prawdopodobieństwem dla A, C, G, T



def insert_name(sequence, name):
    """Wstawia imię w losowym miejscu sekwencji"""
    if len(name) == 0: # jeśli imię jest puste, nie wstawia
        return sequence

    insert_pos = random.randint(0, len(sequence)) # losowa pozycja do wstawienia imienia
    return sequence[:insert_pos] + name + sequence[insert_pos:] # wstawia imię w losowej pozycji


def calculate_stats(sequence, name):
    """Oblicza statystyki sekwencji (ignorując imię jeśli jest wstawione)"""
    # Usuwamy imię z sekwencji przed obliczeniem statystyk
    pure_sequence = sequence.replace(name, '') # zastepuje imię pustym ciągiem
    total = len(pure_sequence) # długość sekwencji bez imienia

    if total == 0:
        return None # jeśli sekwencja jest pusta, zwraca None

    counts = {
        'A': pure_sequence.count('A'),
        'C': pure_sequence.count('C'),
        'G': pure_sequence.count('G'),
        'T': pure_sequence.count('T')
    } # zlicza ilość A, C, G, T w sekwencji

    percentages = {n: (count / total) * 100 for n, count in counts.items()} # oblicza procentową zawartość A, C, G, T w sekwencji

    # Obliczanie stosunku CG do AT
    cg = counts['C'] + counts['G'] # suma C i G
    at = counts['A'] + counts['T'] # suma A i T
    cg_at_ratio = cg / at if at != 0 else float('inf') # unikalny przypadek, gdy AT = 0, wtedy stosunek jest nieskończonością

    return {
        'percentages': percentages,
        'cg_at_ratio': cg_at_ratio,
        'total_length': total
    } # zwraca słownik z procentową zawartością A, C, G, T, stosunkiem CG do AT i długością sekwencji


def main():
    print("Generator sekwencji DNA w formacie FASTA")
    print("----------------------------------------")

    # Pobieranie danych od użytkownika
    seq_id = input("Podaj ID sekwencji: ").strip()
    description = input("Podaj opis sekwencji: ").strip()
    length = int(input("Podaj długość sekwencji DNA (liczba nukleotydów): "))
    my_name = "Rozalia"  # Tutaj wpisz swoje imię

    # Generowanie sekwencji
    dna_sequence = generate_dna_sequence(length)
    print(f"\nWygenerowana sekwencja DNA: {dna_sequence}")
    dna_with_name = insert_name(dna_sequence, my_name)
    print(f"Zmieniona sekwencja DNA: {dna_with_name}")
    # Obliczanie statystyk
    stats = calculate_stats(dna_with_name, my_name)
    # ORIGINAL: 
    #     
    # MODIFIED (dodanie sprawdzenia w przypadku pustej sekwencji):
    if stats is None:
        print("Nie można obliczyć statystyk dla pustej sekwencji.")
        return
    
    # Tworzenie zawartości pliku FASTA
    fasta_content = f">{seq_id} {description}\n{dna_with_name}" # dodaje ID i opis do pliku FASTA

    # Zapisywanie do pliku
    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(fasta_content)
    
    print(f"\nSekwencja została zapisana do pliku: {filename}")
    print("\nStatystyki sekwencji:")
    print(f"Całkowita długość (bez imienia): {stats['total_length']} nukleotydów")
    print("Procentowa zawartość nukleotydów:")
    for nuc, percent in stats['percentages'].items():
        print(f"{nuc}: {percent:.2f}%") # wyświetla procentową zawartość A, C, G, T w sekwencji
    # ORIGINAL: 
    # print(f"Stosunek C+G do A+T: {stats['cg_at_ratio']:.2f}")
    # MODIFIED (dodanie lepszej czytelności):
    print(f"Stosunek C+G do A+T: {100*stats['cg_at_ratio']:.2f}%") # wyświetla stosunek C+G do A+T w procentach

    # Dodatkowe informacje o wstawionym imieniu
    print(f"\nUwaga: W sekwencji wstawiono imię '{my_name}' w losowym miejscu.")
    print("Imię nie jest uwzględniane w statystykach ani w długości sekwencji.")


if __name__ == "__main__":
    main()