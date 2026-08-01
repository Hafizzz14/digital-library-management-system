from django import forms
from .models import Buku, Kategori, Anggota

class BookForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = [
            'kategori', 'judul', 'penulis', 'penerbit', 
            'tahun_terbit', 'isbn', 'total_stok', 
            'stok_tersedia', 'status', 'cover_image'
        ]

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama_kategori', 'deskripsi']

class AnggotaForm(forms.ModelForm):
    class Meta:
        model = Anggota
        fields = ['nomor_anggota', 'nama_lengkap', 'email', 'no_telepon', 'alamat']