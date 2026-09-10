document.addEventListener("DOMContentLoaded", function () {

    const content = document.getElementById("content-box");

    if (!content) return;

    document.getElementById("materi").onclick = function () {

        content.innerHTML = `
            <h2>Materi Pembelajaran</h2>

            <ul>
                <li>📘 Matematika Dasar</li>
                <li>📘 Penalaran Umum</li>
                <li>📘 Literasi Bahasa Indonesia</li>
                <li>📘 Literasi Bahasa Inggris</li>
                <li>📘 Pengetahuan Kuantitatif</li>
            </ul>
        `;
    };

    document.getElementById("easy").onclick = function () {

        content.innerHTML = `
            <h2>TRY OUT EASY</h2>

            <p>Paket yang tersedia :</p>

            <ul>
                <li>Paket Easy 1</li>
                <li>Paket Easy 2</li>
                <li>Paket Easy 3</li>
            </ul>
        `;
    };

    document.getElementById("medium").onclick = function () {

        content.innerHTML = `
            <h2>TRY OUT MEDIUM</h2>

            <p>Daftar paket akan ditampilkan di sini.</p>
        `;
    };

    document.getElementById("hard").onclick = function () {

        content.innerHTML = `
            <h2>TRY OUT HARD</h2>

            <p>Daftar paket akan ditampilkan di sini.</p>
        `;
    };

    document.getElementById("konsep1").onclick = function () {

        content.innerHTML = `
            <h2>Konsep Dasar 1</h2>

            <p>Materi Konsep Dasar 1.</p>
        `;
    };

    document.getElementById("konsep2").onclick = function () {

        content.innerHTML = `
            <h2>Konsep Dasar 2</h2>

            <p>Materi Konsep Dasar 2.</p>
        `;
    };

});