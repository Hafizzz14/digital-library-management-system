from django import forms
from .models import Buku, Kategori, Anggota, Transaksi

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

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['anggota', 'buku']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter dropdown Buku: Hanya tampilkan buku yang stoknya > 0 dan berstatus 'Available'
        self.fields['buku'].queryset = Buku.objects.filter(
            stok_tersedia__gt=0, 
            status='Available'
        )
        self.fields['buku'].empty_label = "-- Pilih Buku yang Tersedia --"
        self.fields['anggota'].empty_label = "-- Pilih Anggota --"

    def clean_buku(self):
        # Double validation backend: Mencegah manipulasi input dari frontend
        buku = self.cleaned_data.get('buku')
        if buku:
            if buku.stok_tersedia <= 0:
                raise forms.ValidationError(f'Maaf, stok buku "{buku.judul}" sedang habis.')
            if buku.status != 'Available':
                raise forms.ValidationError(f'Maaf, buku "{buku.judul}" saat ini tidak tersedia untuk dipinjam.')
        return buku