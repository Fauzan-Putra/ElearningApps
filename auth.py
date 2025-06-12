import utils

def login_menu(um):
    utils.clear_screen()
    print("Login")
    try:
        username = input("Username: ")
        password = input("Password: ")
        user = um.login(username, password)
        if user:
            return user
        else:
            print("Username atau password salah.")
            input("Tekan Enter untuk kembali...")
            return None
    except EOFError:
        print("Input dibatalkan.")
        input("Tekan Enter untuk kembali...")
        return None

def register_menu(um):
    utils.clear_screen()
    print("Registrasi")
    try:
        while True:
            username = input("Username: ")
            if not username.strip():
                print("Username tidak boleh kosong.")
                continue
            break
        while True:
            password = input("Password: ")
            if not password.strip():
                print("Password tidak boleh kosong.")
                continue
            break
        while True:
            role = input("Role (guru/murid): ").lower()
            if role not in ['guru', 'murid']:
                print("Role tidak valid.")
                continue
            break
        class_name = None
        if role == 'guru':
            while True:
                class_name = input("Nama kelas: ")
                if not class_name.strip():
                    print("Nama kelas tidak boleh kosong.")
                    continue
                break
        success, class_code = um.register(username, password, role, class_name)
        if success:
            print(f"Registrasi berhasil! {'Kode kelas Anda: ' + class_code if role == 'guru' else ''}")
            input("Tekan Enter untuk kembali...")
            return class_code
        else:
            print(class_code)
            input("Tekan Enter untuk kembali...")
            return None
    except EOFError:
        print("Input dibatalkan.")
        input("Tekan Enter untuk kembali...")
        return None