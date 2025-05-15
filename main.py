import random


def generate_dna_sequence(length):
    """Generuje losową sekwencję DNA o podanej długości"""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choice(nucleotides) for _ in range(length))


def insert_name(sequence, name):
    """Wstawia imię w losowym miejscu sekwencji"""
    if len(name) == 0:
        return sequence

    insert_pos = random.randint(0, len(sequence))
    return sequence[:insert_pos] + name + sequence[insert_pos:]


def calculate_stats(sequence, name):
    """Oblicza statystyki sekwencji (ignorując imię jeśli jest wstawione)"""
    # Usuwamy imię z sekwencji przed obliczeniem statystyk
    pure_sequence = sequence.replace(name, '')
    total = len(pure_sequence)

    if total == 0:
        return None

    counts = {
        'A': pure_sequence.count('A'),
        'C': pure_sequence.count('C'),
        'G': pure_sequence.count('G'),
        'T': pure_sequence.count('T')
    }

    percentages = {n: (count / total) * 100 for n, count in counts.items()}

    # Obliczanie stosunku CG do AT
    cg = counts['C'] + counts['G']
    at = counts['A'] + counts['T']
    cg_at_ratio = cg / at if at != 0 else float('inf')

    return {
        'percentages': percentages,
        'cg_at_ratio': cg_at_ratio,
        'total_length': total
    }


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
    dna_with_name = insert_name(dna_sequence, my_name)

    # Obliczanie statystyk
    stats = calculate_stats(dna_with_name, my_name)

    # Tworzenie zawartości pliku FASTA
    fasta_content = f">{seq_id} {description}\n{dna_with_name}"

    # Zapisywanie do pliku
    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(fasta_content)

    print(f"\nSekwencja została zapisana do pliku: {filename}")
    print("\nStatystyki sekwencji:")
    print(f"Całkowita długość (bez imienia): {stats['total_length']} nukleotydów")
    print("Procentowa zawartość nukleotydów:")
    for nuc, percent in stats['percentages'].items():
        print(f"{nuc}: {percent:.2f}%")
    print(f"Stosunek C+G do A+T: {stats['cg_at_ratio']:.2f}")

    # Dodatkowe informacje o wstawionym imieniu
    print(f"\nUwaga: W sekwencji wstawiono imię '{my_name}' w losowym miejscu.")
    print("Imię nie jest uwzględniane w statystykach ani w długości sekwencji.")


if __name__ == "__main__":
    main()