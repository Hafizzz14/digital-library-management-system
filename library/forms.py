from django import forms
from .models import Buku

class BookForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = [
            'kategori', 'judul', 'penulis', 'penerbit', 
            'tahun_terbit', 'isbn', 'total_stok', 
            'stok_tersedia', 'status', 'cover_image'
        ]