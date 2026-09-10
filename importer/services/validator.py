class ExcelValidator:

    REQUIRED_HEADER_GROUPS = [
        ("Kategori",),
        ("Pertanyaan", "Soal"),
        ("A",),
        ("B",),
        ("C",),
        ("D",),
        ("E",),
        ("Jawaban",),
        ("Pembahasan", "Penjelasan"),
    ]

    def __init__(self, headers):
        self.headers = [
            str(header).strip().lower()
            for header in headers
            if header is not None
        ]

    def _has_header(self, names):
        for header in names:
            if header.strip().lower() in self.headers:
                return True
        return False

    def validate(self):
        missing = []

        for group in self.REQUIRED_HEADER_GROUPS:
            if not self._has_header(group):
                missing.append("/".join(group))

        return missing
