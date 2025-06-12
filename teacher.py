import utils

def manage_articles(user, am):
    while True:
        utils.clear_screen()
        print("Kelola Artikel")
        articles = am.list(user.class_codes[0])
        for i, art in enumerate(articles, 1):
            print(f"{i}. {art.title}")
        print("\n1. Tambah Artikel")
        print("2. Edit Artikel")
        print("3. Hapus Artikel")
        print("4. Kembali")
        try:
            sub_choice = input("> Pilih: ")
        except EOFError:
            sub_choice = ''

        if sub_choice == '1':
            try:
                title = input("Judul artikel: ")
                text = utils.get_multiline_input("Isi artikel")
                if text is None:
                    print("Input dibatalkan.")
                    input("Tekan Enter untuk lanjut...")
                    continue
                image_path = input("Path gambar (kosongkan jika tidak ada): ")
                am.create(user.class_codes[0], title, text, image_path)
                print("Artikel dibuat!")
                input("Tekan Enter untuk lanjut...")
            except EOFError:
                print("Input dibatalkan.")
                input("Tekan Enter untuk lanjut...")

        elif sub_choice == '2' and articles:
            try:
                idx = int(input("Pilih nomor artikel: ")) - 1
                if 0 <= idx < len(articles):
                    title = input(f"Judul baru (lama: {articles[idx].title}): ") or articles[idx].title
                    print(f"Isi lama:\n{articles[idx].text}")
                    text = utils.get_multiline_input("Isi baru") or articles[idx].text
                    if text is None:
                        print("Input dibatalkan.")
                        input("Tekan Enter untuk lanjut...")
                        continue
                    image_path = input(f"Path gambar baru (lama: {articles[idx].image_path}): ") or articles[idx].image_path
                    am.update(articles[idx].id, title=title, text=text, image_path=image_path)
                    print("Artikel diperbarui!")
                    input("Tekan Enter untuk lanjut...")
            except (ValueError, EOFError):
                print("Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")

        elif sub_choice == '3' and articles:
            try:
                idx = int(input("Pilih nomor artikel: ")) - 1
                if 0 <= idx < len(articles):
                    am.delete(articles[idx].id)
                    print("Artikel dihapus!")
                    input("Tekan Enter untuk lanjut...")
            except (ValueError, EOFError):
                print("Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")

        elif sub_choice == '4':
            break

def create_question(qm, package_id):
    try:
        question = utils.get_multiline_input("Pertanyaan")
        if question is None:
            print("Input dibatalkan.")
            return False
        options = []
        for i in range(4):
            opt = input(f"Opsi {i+1}: ")
            options.append(opt)
        answer = input("Jawaban benar (masukkan opsi): ")
        explanation = input("Penjelasan: ")
        qm.create(package_id, question, options, answer, explanation)
        print("Soal dibuat!")
        return True
    except (ValueError, EOFError):
        print("Input tidak valid.")
        return False

def manage_quizzes(user, qpm, qm):
    while True:
        utils.clear_screen()
        print("Kelola Paket Soal")
        packages = qpm.list(user.class_codes[0])
        for i, pkg in enumerate(packages, 1):
            print(f"{i}. {pkg.package_name} (Timer: {pkg.total_timer}s)")
        print("\n1. Tambah Paket Soal")
        print("2. Edit Paket Soal")
        print("3. Hapus Paket Soal")
        print("4. Kembali")
        try:
            sub_choice = input("> Pilih: ")
        except EOFError:
            sub_choice = ''

        if sub_choice == '1':
            try:
                while True:
                    package_name = input("Nama paket soal: ")
                    if not package_name.strip():
                        print("Nama paket soal tidak boleh kosong.")
                        input("Tekan Enter untuk lanjut...")
                        continue
                    total_timer = input("Total waktu (detik, minimal 1): ")
                    try:
                        total_timer = int(total_timer)
                        if total_timer < 1:
                            print("Waktu harus minimal 1 detik.")
                            input("Tekan Enter untuk lanjut...")
                            continue
                    except ValueError:
                        print("Input waktu tidak valid. Masukkan dalam format bilangan bulat!!!")
                        input("Tekan Enter untuk lanjut...")
                        continue
                    package_id = qpm.create(user.class_codes[0], package_name, total_timer)
                    print("Paket soal dibuat. Tambahkan soal:")
                    while True:
                        if create_question(qm, package_id):
                            add_more = input("Tambah soal lagi? (ya/tidak): ").lower()
                            if add_more != 'ya':
                                print("Paket soal selesai dibuat!")
                                break
                        else:
                            print("Gagal menambahkan soal.")
                            break
                    input("Tekan Enter untuk lanjut...")
                    break  # Keluar dari loop input paket soal setelah berhasil
            except EOFError:
                print("Input dibatalkan.")
                input("Tekan Enter untuk lanjut...")

        elif sub_choice == '2' and packages:
            try:
                idx = int(input("Pilih nomor paket soal: ")) - 1
                if 0 <= idx < len(packages):
                    package = packages[idx]
                    while True:
                        utils.clear_screen()
                        print(f"Edit Paket: {package.package_name}")
                        questions = qm.list(package.package_id)
                        for i, q in enumerate(questions, 1):
                            print(f"{i}. {q.question.split('\n')[0][:50]}{'...' if len(q.question) > 50 else ''}")
                        print("\n1. Edit Soal")
                        print("2. Tambah Soal")
                        print("3. Hapus Soal")
                        print("4. Kembali")
                        try:
                            edit_choice = input("> Pilih: ")
                        except EOFError:
                            edit_choice = ''

                        if edit_choice == '1' and questions:
                            try:
                                q_idx = int(input("Pilih nomor soal: ")) - 1
                                if 0 <= q_idx < len(questions):
                                    print(f"Pertanyaan lama:\n{questions[q_idx].question}")
                                    question = utils.get_multiline_input("Pertanyaan baru") or questions[q_idx].question
                                    if question is None:
                                        print("Input dibatalkan.")
                                        input("Tekan Enter untuk lanjut...")
                                        continue
                                    options = questions[q_idx].options
                                    for i, opt in enumerate(options):
                                        new_opt = input(f"Opsi {i+1} baru (lama: {opt}): ") or opt
                                        options[i] = new_opt
                                    answer = input(f"Jawaban benar baru (lama: {questions[q_idx].answer}): ") or questions[q_idx].answer
                                    explanation = input(f"Penjelasan baru (lama: {questions[q_idx].explanation}): ") or questions[q_idx].explanation
                                    qm.update(questions[q_idx].question_id, question=question, options=options, answer=answer, explanation=explanation)
                                    print("Soal diperbarui!")
                                    input("Tekan Enter untuk lanjut...")
                            except (ValueError, EOFError):
                                print("Pilihan tidak valid.")
                                input("Tekan Enter untuk lanjut...")

                        elif edit_choice == '2':
                            if create_question(qm, package.package_id):
                                input("Tekan Enter untuk lanjut...")
                            else:
                                input("Tekan Enter untuk lanjut...")

                        elif edit_choice == '3' and questions:
                            try:
                                q_idx = int(input("Pilih nomor soal: ")) - 1
                                if 0 <= q_idx < len(questions):
                                    qm.delete(questions[q_idx].question_id)
                                    print("Soal dihapus!")
                                    input("Tekan Enter untuk lanjut...")
                            except (ValueError, EOFError):
                                print("Pilihan tidak valid.")
                                input("Tekan Enter untuk lanjut...")

                        elif edit_choice == '4':
                            break
                else:
                    print("Pilihan tidak valid.")
                    input("Tekan Enter untuk lanjut...")
            except (ValueError, EOFError):
                print("Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")

        elif sub_choice == '3' and packages:
            try:
                idx = int(input("Pilih nomor paket soal: ")) - 1
                if 0 <= idx < len(packages):
                    qpm.delete(packages[idx].package_id)
                    print("Paket soal dihapus!")
                    input("Tekan Enter untuk lanjut...")
            except (ValueError, EOFError):
                print("Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")

        elif sub_choice == '4':
            break

def view_statistics(user, pm):
    utils.clear_screen()
    print("Statistik Murid")
    progresses = pm.list_by_class(user.class_codes[0])
    students = set(p['username'] for p in progresses)
    for student in students:
        student_progress = [p for p in progresses if p['username'] == student]
        scores = [float(p['score']) for p in student_progress]
        avg_score = sum(scores) / len(scores) if scores else 0
        print(f"Murid: {student}, Jumlah Paket: {len(scores)}, Rata-rata Nilai: {avg_score:.2f}")
    input("Tekan Enter untuk kembali...")

def teacher_menu(user, store, um, am, qpm, qm, pm):
    while True:
        utils.clear_screen()
        print(f"Selamat datang, Guru {user.username} (Kode Kelas: {user.class_codes[0]})")
        print("1. Kelola Artikel")
        print("2. Kelola Paket Soal")
        print("3. Lihat Statistik Murid")
        print("4. Logout")
        try:
            choice = input("> Pilih menu: ")
        except EOFError:
            choice = ''

        if choice == '1':
            manage_articles(user, am)
        elif choice == '2':
            manage_quizzes(user, qpm, qm)
        elif choice == '3':
            view_statistics(user, pm)
        elif choice == '4':
            break