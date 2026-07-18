import random

# ============================================================
# DATA
# ============================================================
teachers  = ['Guru A', 'Guru B', 'Guru C']
subjects  = ['Matematika', 'Fisika', 'Kimia']
classes   = ['Kelas 1', 'Kelas 2', 'Kelas 3']
timeslots = ['Senin P1', 'Senin P2', 'Selasa P1', 'Selasa P2']


# ============================================================
# REPRESENTASI KROMOSOM
# Satu individu = SELURUH jadwal (bukan cuma satu entri)
# Terdiri dari 12 slot: 3 kelas x 4 timeslot
# Tiap slot: [guru, mata_pelajaran, kelas, waktu]
# Kelas dan waktu sudah fix per slot; yang dievolvasi adalah
# guru dan mata pelajaran yang mengisi setiap slot.
# ============================================================
def create_individual():
    schedule = []
    for kelas in classes:
        for slot in timeslots:
            schedule.append([
                random.choice(teachers),
                random.choice(subjects),
                kelas,
                slot
            ])
    return schedule


# ============================================================
# FUNGSI FITNESS (PERBAIKAN BUG 1 & 3)
# Hitung jumlah bentrok antar slot jadwal.
# Bentrok = guru yang sama mengajar di waktu yang sama
#           (di kelas yang berbeda).
# Semakin kecil nilainya, semakin bagus jadwalnya.
# Fitness = 0 artinya jadwal sempurna, tidak ada bentrokan.
# ============================================================
def fitness(individual):
    conflicts = 0
    n = len(individual)
    for i in range(n):
        for j in range(i + 1, n):
            same_teacher = individual[i][0] == individual[j][0]
            same_time    = individual[i][3] == individual[j][3]
            if same_teacher and same_time:
                conflicts += 1
    return conflicts


# ============================================================
# SELEKSI — TOURNAMENT (PERBAIKAN BUG 4)
# Ambil 3 individu secara acak dari populasi,
# lalu pilih yang nilai fitness-nya paling kecil.
# Metode tournament lebih stabil dibanding greedy sort.
# ============================================================
def selection(population):
    tournament = random.sample(population, 3)
    return min(tournament, key=fitness)


# ============================================================
# CROSSOVER — SATU TITIK
# Potong kromosom di satu titik acak,
# tukar bagian belakang antara dua induk.
# Menghasilkan dua anak baru.
# ============================================================
def crossover(parent1, parent2):
    point  = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


# ============================================================
# MUTASI (PERBAIKAN BUG 2)
# Dengan peluang mutation_rate per slot, ganti guru dan/atau
# mata pelajaran secara acak.
# Kelas dan waktu TIDAK diubah karena sudah fix dari struktur.
# ============================================================
def mutate(individual, mutation_rate=0.1):
    individual = [slot[:] for slot in individual]   # deep copy dulu
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i][0] = random.choice(teachers)
            individual[i][1] = random.choice(subjects)
    return individual


# ============================================================
# ALGORITMA GENETIKA UTAMA
# ============================================================
def genetic_algorithm(pop_size=50, generations=100):
    # Inisialisasi populasi awal secara acak
    population = [create_individual() for _ in range(pop_size)]

    print(f"{'Generasi':>10} | {'Fitness Terbaik':>15}")
    print("-" * 30)

    best_ever = None

    for gen in range(1, generations + 1):

        # Urutkan populasi: yang paling sedikit konfliknya duluan
        population.sort(key=fitness)
        best         = population[0]
        best_fitness = fitness(best)

        # Simpan solusi terbaik sepanjang semua generasi
        if best_ever is None or best_fitness < fitness(best_ever):
            best_ever = [slot[:] for slot in best]

        # Tampilkan progress setiap 10 generasi
        if gen % 10 == 0 or gen == 1:
            print(f"{gen:>10} | {best_fitness:>15}")

        # Stop lebih awal jika sudah tidak ada konflik
        if best_fitness == 0:
            print(f"\nSolusi sempurna ditemukan di generasi {gen}!")
            break

        # Buat generasi baru
        # Elitism: 2 individu terbaik langsung lolos ke generasi berikutnya
        new_population = [population[0], population[1]]

        while len(new_population) < pop_size:
            p1 = selection(population)
            p2 = selection(population)
            c1, c2 = crossover(p1, p2)
            new_population.extend([mutate(c1), mutate(c2)])

        population = new_population[:pop_size]

    # ---- Output Jadwal Terbaik ----
    print(f"\n{'='*55}")
    print(f"  JADWAL TERBAIK  (total konflik = {fitness(best_ever)})")
    print(f"{'='*55}")
    print(f"{'No':>3} | {'Kelas':^8} | {'Waktu':^12} | {'Guru':^7} | Mata Pelajaran")
    print("-" * 55)
    for i, entry in enumerate(best_ever, 1):
        print(f"{i:>3} | {entry[2]:^8} | {entry[3]:^12} | {entry[0]:^7} | {entry[1]}")


# ---- Jalankan ----
if __name__ == "__main__":
    random.seed(42)   # seed agar hasil bisa direproduksi
    genetic_algorithm()