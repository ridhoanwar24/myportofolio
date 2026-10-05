Nama    : Muhammad Ridho Anwar

NPM     : 2506595745

Kelas   : PBP B

### Tugas 1

1. Saat merancang struktur HTML, saya menggunakan <section> seperti yang disediakan di tutorial untuk menambah bagian yang baru. Tag tersebut membantu saya membuat tampilan web yang lebih terorganisir sesuai bagiannya masing-masing. Saya tidak menggunakan tag lain seperti <article> maupun <aside> karena tidak memiliki referensi bagaimana cara menggunakannya. Selain itu, saya merasa bahwa dengan <section> saja sudah cukup.

2. Tantangan saat mengatur CSS adalah menentukan bagaimana cara kerja flex dan grid. Dari mana bagian tersebut dimulai dan seperti apa kira-kira layoutnya. Saya sempat menemukan masalah saat ingin mengatur agar content berada di tengah, dan ternyata masalah tersebut berada di perbedaan antara justify-content dan text-align. Selain itu, penggunaan margin dan padding juga cukup membingungkan saat pertama kali. Saya juga berusaha mengikuti contoh kode dari tutorial supaya harapannya tidak perlu melakukan banyak adjusment untuk tampilan versi mobile.

3. Saya tidak terlalu merasakan batasan dari static web, utamanya karena saya tidak tahu what to expect dan seberapa berbedanya antara static web dan dinamic web. Belum ada fungsionalitas dinamis yang ingin saya tambahkan, saya menunggu apa yang PBP siapkan untuk saya kedepannya.

Mencari referensi dari W3School, menggunakan Gen AI Gemini untuk membantu menjelaskan beberapa konsep HTML & CSS, serta menjelaskan bagaimana mengimplementasikan ide ke dalam HTML & CSS. Prompt yang digunakan sebagai berikut:

> cara menambah new tab di html
> cara membuat navbar
> ul li itu apa
> terus untuk href-href yang ada # nya, nanti kalo diklik bakal gimana jadinya, apakah harus buat file html baru untuk setiap list tersebut
> kalo bikin beberapa page, nanti cssnya gimana, apakah bikin baru juga sesuai dengan page html masing2
> <html><head><script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script></head><body><i class="fas fa-cloud"></i><i class="fas fa-heart"></i><i class="fas fa-car"></i><i class="fas fa-file"></i><i class="fas fa-bars"></i></body></html>jelaskan semua maksud dari tulisan di tag script, dan apakah nambahin icon harus pake tag <i> atau bebas
> <section class="projects" id="projects">apakah aman penulisan seperti itu, atau harus dibedain

> cara memisahkan antar section dengan garis

> cara styling font awesome di css
> buat contohnya
> ikon rumah dan ikon hati itu tinggal ganti sesuai kebutuhan dan diletakkan di akhir class ya
> .site-header nav a { color: var(--ink); text-decoration: none; font-size: 0.95rem; transition: all 0.2 ease;}.site-header nav a:hover { border: 1px solid var(--shadow); background-color: var(--shadow); border-radius: 8px;}kenapa pas dihover malah wiggle

### Tugas 2

1. Saat membuka halaman portofolio, client akan mengirimkan request ke server. Django akan memeriksa URL dengan data yang ada di urls.py. Model sebagai database, template sebagai tampilan di client, dan view sebagai jembatan yang menghubungkan keduanya.

2. Menyimpan data pada model membuat maintenance lebih mudah dilakukan. Selain itu, bisa langsung menambahkan data tanpa menambahkan baris kode baru di file HTML.

3. Fungsi makemigrations adalah menyimpan perubahan yang dibuat di models.py, sedangkan migrate menerapkan perubahan yang sudah disimpan ke seluruh projek kita. Contohnya seperti menambahkan atribut baru di class Experience.

Penggunaan AI(Gemini):
https://share.google/aimode/B6gEjQDATSSbiCjLw

### Tugas 3

1. Menggunakan ModelForm agar tidak perlu menulis kode html lagi setiap kali ingin membuat form baru. Penggunaan CSRF adalah untuk mencegah hacker meretas request yang kita kirim ke django.

2. JSON lebih disukai daripada XML karena lebih ringkas, parser yang sangat cepat, dan integrasi yang sangat natural dengan Javascript di sisi frontend.

3. Mula-mula klien mengirim request, kemudian Django mencocokkan dengan url yang ada di urls.py, django mengambil data dan melakukan serialize menjadi format JSON, kemudian mengirim respons ke klien. Serialization dilakukan karena data awal masih berupa object django, serialize membuat data menjadi format JSON yang dimengerti oleh web API.

Penggunaan AI(Claude):
https://claude.ai/share/2a35ed31-983b-4457-85be-4a967e6c992b

### Tugas 4

Penggunaan AI(Gemini):
https://share.google/aimode/vrkuLzsfO7KUe1fbF

### Tugas 5

1. Debouncing adalah menunda eksekusi fungsi selama jeda waktu tertentu. Misal user sedang mencari/mengetik sesuatu, dengan debouncing browser akan menunggu sekian ms untuk mengecek apakah user sudah berhenti mengetik atau belum. Jika sudah selesai, browser baru akan mengirim request. Tanpa debouncing, setiap kali user mengetik satu huruf, browser akan mengirim request ke server melalui AJAX, sehingga akan ada request berkali-kali. Debouncing membuat request ke server lebih efisien.

2. Keyword await digunakan untuk menunggu hasil dari fetch sebelum lanjut ke proses berikutnya. Tanpa await, kode bisa saja terus berjalan padahal hasil dari fetch belum selesai diproses sehingga kita mendapat hasil yang tidak diharapkan.

3. XSS (Cross-Site Scripting) adalah serangan yang menyisipkan kode JavaScript ke halaman web, kemudian dijalankan di browser oleh pengguna lain. Misalnya ketika kode berbahaya tersebut tersimpan ke database lalu ikut dijalankan ketika data ditampilkan. Data yang ditampilkan dengan AJAX lebih rentan daripada template Django karena Django sudah melakukan auto-escaping, sehingga karakter yang berkemungkinan berbahaya diubah dan dijalankan sebagai teks biasa dan bukan kode yang harus dieksekusi. Pada AJAX tidak ada lagi yang melakukan auto-escaping, sehingga penanganan terhadap XSS harus dilakukan secara manual.

Penggunaan AI(Claude):
https://claude.ai/share/43dce2ae-cdb8-4b87-b19e-5995e5e76005