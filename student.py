import utils
import time

def join_class(user, um):
    utils.clear_screen()
    print("Bergabung ke Kelas")
    try:
        class_code = input("Masukkan kode kelas: ")
        success, message = um.join_class(user.username, class_code)
        print(message)
        if success:
            user.class_codes.append(class_code)
        input("Tekan Enter untuk lanjut...")
    except EOFError:
        print("Input dibatalkan.")
        input("Tekan Enter untuk lanjut...")

def read_articles(class_code, am, store):
    utils.clear_screen()
    class_name = store.get_class_name(class_code) or class_code
    print(f"Kelas: {class_name} - Baca Artikel")
    articles = am.list(class_code)
    if not articles:
        print("Belum ada artikel.")
    else:
        for i, art in enumerate(articles, 1):
            print(f"{i}. {art.title}")
        try:
            idx = int(input("Pilih artikel: ")) - 1
            if 0 <= idx < len(articles):
                print(f"\nJudul: {articles[idx].title}")
                print(f"Isi:\n{articles[idx].text}")
                if articles[idx].image_path:
                    print(f"Gambar: {articles[idx].image_path}")
            else:
                print("Pilihan tidak valid.")
        except (ValueError, EOFError):
            print("Pilihan tidak valid.")
    input("Tekan Enter untuk kembali...")

def take_quiz(class_code, user, qpm, qm, pm, store):
    utils.clear_screen()
    class_name = store.get_class_name(class_code) or class_code
    print(f"Kelas: {class_name} - Kerjakan Paket Soal")
    packages = qpm.list(class_code)
    available_packages = [p for p in packages if not pm.has_taken_package(user.username, p.package_id)]
    if not available_packages:
        print("Tidak ada paket soal yang tersedia.")
    else:
        for i, pkg in enumerate(available_packages, 1):
            print(f"{i}. {pkg.package_name} (Timer: {pkg.total_timer}s)")
        try:
            idx = int(input("Pilih paket soal: ")) - 1
            if 0 <= idx < len(available_packages):
                package = available_packages[idx]
                questions = qm.list(package.package_id)
                if not questions:
                    print("Paket soal kosong.")
                    input("Tekan Enter untuk kembali...")
                    return
                answers = []
                correct_count = 0
                start_time = time.time()
                for q in questions:
                    if time.time() - start_time > package.total_timer:
                        print("Waktu paket soal habis!")
                        break
                    utils.clear_screen()
                    print(f"Pertanyaan:\n{q.question}")
                    for i, opt in enumerate(q.options, 1):
                        print(f"{i}. {opt}")
                    time_per_question = (package.total_timer - (time.time() - start_time)) / (len(questions) - len(answers)) if len(questions) > len(answers) else package.total_timer
                    answer = utils.input_with_timeout(f"Jawaban Anda (1-{len(q.options)}): ", time_per_question)
                    if answer.strip() == '':
                        print("Tidak ada jawaban, melanjutkan ke soal berikutnya.")
                    try:
                        if 1 <= int(answer) <= len(q.options):
                            answers.append(answer)
                            if answer == q.answer:
                                correct_count += 1
                        else:
                            answers.append('')
                    except ValueError:
                        answers.append('')
                score = (correct_count / len(questions)) * 100 if questions else 0
                pm.record(user.username, package.package_id, score, answers)
                print(f"Skor Anda: {score:.2f}")
            else:
                print("Pilihan tidak valid.")
        except (ValueError, EOFError):
            print("Pilihan tidak valid.")
    input("Tekan Enter untuk kembali...")

def review_quizzes(class_code, user, qpm, qm, pm, store):
    utils.clear_screen()
    class_name = store.get_class_name(class_code) or class_code
    print(f"Kelas: {class_name} - Review Paket Soal")
    progresses = pm.list_by_user(user.username)
    packages = qpm.list(class_code)
    taken_packages = [(p, next(pkg for pkg in packages if pkg.package_id == p['package_id'])) for p in progresses if any(pkg.package_id == p['package_id'] for pkg in packages)]
    if not taken_packages:
        print("Belum ada paket soal yang dikerjakan.")
    else:
        for i, (prog, pkg) in enumerate(taken_packages, 1):
            print(f"{i}. {pkg.package_name} (Skor: {prog['score']})")
        try:
            idx = int(input("Pilih paket untuk review: ")) - 1
            if 0 <= idx < len(taken_packages):
                prog, pkg = taken_packages[idx]
                questions = qm.list(pkg.package_id)
                answers = prog['answers'].split('|')
                for i, q in enumerate(questions):
                    print(f"\nPertanyaan {i+1}:\n{q.question}")
                    for j, opt in enumerate(q.options, 1):
                        print(f"{j}. {opt}")
                    print(f"Jawaban Anda: {answers[i] if i < len(answers) else 'Tidak dijawab'}")
                    print(f"Jawaban Benar: {q.answer}")
                    print(f"Penjelasan: {q.explanation}")
                print(f"\nSkor: {prog['score']}")
            else:
                print("Pilihan tidak valid.")
        except (ValueError, EOFError):
            print("Pilihan tidak valid.")
    input("Tekan Enter untuk kembali...")

def class_menu(user, class_code, am, qpm, qm, pm, store):
    while True:
        utils.clear_screen()
        class_name = store.get_class_name(class_code) or class_code
        print(f"Kelas: {class_name}")
        print("1. Baca Artikel")
        print("2. Kerjakan Paket Soal")
        print("3. Review Paket Soal")
        print("4. Kembali")
        try:
            sub_choice = input("> Pilih: ")
        except EOFError:
            sub_choice = ''

        if sub_choice == '1':
            read_articles(class_code, am, store)
        elif sub_choice == '2':
            take_quiz(class_code, user, qpm, qm, pm, store)
        elif sub_choice == '3':
            review_quizzes(class_code, user, qpm, qm, pm, store)
        elif sub_choice == '4':
            break

def student_menu(user, store, um, am, qpm, qm, pm):
    while True:
        utils.clear_screen()
        print(f"Selamat datang, Murid {user.username}")
        print("Pilih Kelas:")
        for i, code in enumerate(user.class_codes, 1):
            class_name = store.get_class_name(code) or code
            print(f"{i}. {class_name}")
        print(f"{len(user.class_codes) + 1}. Bergabung ke Kelas")
        print(f"{len(user.class_codes) + 2}. Logout")
        try:
            choice = input("> Pilih: ")
        except EOFError:
            choice = ''

        if choice == str(len(user.class_codes) + 1):
            join_class(user, um)
            continue
        if choice == str(len(user.class_codes) + 2):
            break
        try:
            class_idx = int(choice) - 1
            if 0 <= class_idx < len(user.class_codes):
                class_code = user.class_codes[class_idx]
                class_menu(user, class_code, am, qpm, qm, pm, store)
        except ValueError:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")