from django.db import models
from django.contrib.auth.models import User

class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_kategori

class Buku(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]

    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='buku')
    judul = models.CharField(max_length=255)
    penulis = models.CharField(max_length=150)
    penerbit = models.CharField(max_length=150)
    tahun_terbit = models.IntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    total_stok = models.IntegerField(default=0)
    stok_tersedia = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul

class Anggota(models.Model):
    nomor_anggota = models.CharField(max_length=50, unique=True)
    nama_lengkap = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, blank=True, null=True)
    no_telepon = models.CharField(max_length=20)
    alamat = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nomor_anggota} - {self.nama_lengkap}"

class Transaksi(models.Model):
    STATUS_CHOICES = [
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
    ]

    buku = models.ForeignKey(Buku, on_delete=models.PROTECT, related_name='transaksi')
    anggota = models.ForeignKey(Anggota, on_delete=models.PROTECT, related_name='transaksi')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transaksi_diproses')
    tanggal_pinjam = models.DateField()
    batas_kembali = models.DateField()
    tanggal_kembali = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Borrowed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.anggota.nama_lengkap} meminjam {self.buku.judul} ({self.status})"