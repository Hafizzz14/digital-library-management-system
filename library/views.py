from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
from .models import Buku, Kategori
from .forms import BookForm, KategoriForm

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')

@login_required
def book_list(request):
    query = request.GET.get('q', '')
    
    books_query = Buku.objects.select_related('kategori').all().order_by('-created_at')
    
    # Logika Pencarian menggunakan Q objects
    if query:
        books_query = books_query.filter(
            Q(judul__icontains=query) |
            Q(penulis__icontains=query) |
            Q(isbn__icontains=query)
        )
        
    # Paginasi
    paginator = Paginator(books_query, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'library/book_list.html', context)

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data buku berhasil ditambahkan.')
            return redirect('book_list')
        else:
            messages.error(request, 'Terdapat kesalahan input. Silakan periksa kembali.')
    else:
        form = BookForm()
        
    context = {'form': form, 'title': 'Tambah Buku Baru'}
    return render(request, 'library/book_form.html', context)

@login_required
def book_update(request, pk):
    book = get_object_or_404(Buku, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data buku berhasil diperbarui.')
            return redirect('book_list')
        else:
            messages.error(request, 'Terdapat kesalahan input. Silakan periksa kembali.')
    else:
        form = BookForm(instance=book)
        
    context = {'form': form, 'title': 'Edit Data Buku'}
    return render(request, 'library/book_form.html', context)

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Buku, pk=pk)
    
    if request.method == 'POST':
        try:
            book.delete()
            messages.success(request, f'Buku "{book.judul}" berhasil dihapus.')
        except ProtectedError:
            messages.error(request, f'Gagal menghapus! Buku "{book.judul}" masih memiliki riwayat peminjaman.')
            
        return redirect('book_list')
        
    return render(request, 'library/book_confirm_delete.html', {'book': book})

@login_required
def kategori_list(request):
    query = request.GET.get('q', '')
    kategori_query = Kategori.objects.all().order_by('-created_at')
    
    # Logika Pencarian menggunakan Q objects
    if query:
        kategori_query = kategori_query.filter(
            Q(nama_kategori__icontains=query) |
            Q(deskripsi__icontains=query)
        )
        
    # Paginasi
    paginator = Paginator(kategori_query, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'library/kategori_list.html', context)

@login_required
def kategori_create(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil ditambahkan.')
            return redirect('kategori_list')
        else:
            messages.error(request, 'Terdapat kesalahan input. Silakan periksa kembali.')
    else:
        form = KategoriForm()
        
    context = {'form': form, 'title': 'Tambah Kategori Baru'}
    return render(request, 'library/kategori_form.html', context)

@login_required
def kategori_update(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil diperbarui.')
            return redirect('kategori_list')
        else:
            messages.error(request, 'Terdapat kesalahan input. Silakan periksa kembali.')
    else:
        form = KategoriForm(instance=kategori)
        
    context = {'form': form, 'title': 'Edit Data Kategori'}
    return render(request, 'library/kategori_form.html', context)

@login_required
def kategori_delete(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    
    if request.method == 'POST':
        try:
            kategori.delete()
            messages.success(request, f'Kategori "{kategori.nama_kategori}" berhasil dihapus.')
        except ProtectedError:
            # Meskipun relasi saat ini CASCADE, menangkap ProtectedError adalah best practice 
            # untuk mencegah aplikasi crash jika arsitektur database diubah di masa depan.
            messages.error(request, f'Gagal menghapus! Kategori "{kategori.nama_kategori}" sedang digunakan.')
            
        return redirect('kategori_list')
        
    return render(request, 'library/kategori_confirm_delete.html', {'kategori': kategori})