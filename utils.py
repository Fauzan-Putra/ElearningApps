def get_multiline_input(text_widget):
    """Mengambil input multi-baris dari widget ScrolledText di Tkinter."""
    return text_widget.get("1.0", "end-1c").strip() or None