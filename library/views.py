from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from .models import Buku, Kategori, Anggota, Transaksi
from .forms import BookForm, KategoriForm, AnggotaForm, TransaksiForm

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
            messages.error(request, f'Gagal menghapus! Kategori "{kategori.nama_kategori}" sedang digunakan.')
            
        return redirect('kategori_list')
        
    return render(request, 'library/kategori_confirm_delete.html', {'kategori': kategori})

@login_required
def anggota_list(request):
    query = request.GET.get('q', '')
    anggota_query = Anggota.objects.all().order_by('-created_at')
    
    # Logika Pencarian menggunakan Q objects
    if query:
        anggota_query = anggota_query.filter(
            Q(nama_lengkap__icontains=query) |
            Q(nomor_anggota__icontains=query) |
            Q(email__icontains=query)
        )
        
    # Paginasi
    paginator = Paginator(anggota_query, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'library/anggota_list.html', context)

@login_required
def anggota_create(request):
    if request.method == 'POST':
        form = AnggotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anggota baru berhasil ditambahkan.')
            return redirect('anggota_list')
        else:
            messages.error(request, 'Terdapat kesalahan input. Silakan periksa kembali.')
    else:
        form = AnggotaForm()
        
    context = {'form': form, 'title': 'Tambah Anggota Baru'}
    return render(request, 'library/anggota_form.html', context)

@login_required
def anggota_update(request, pk):
    anggota = get_object_or_404(Anggota, pk=pk)
    
    if request.method == 'POST':
        form = AnggotaForm(request.POST, instance=anggota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data anggota berhasil diperbarui.')
            return redirect('anggota_list')
        else:
            messages.error(request, 'Terdapat kesalahan input. Silakan periksa kembali.')
    else:
        form = AnggotaForm(instance=anggota)
        
    context = {'form': form, 'title': 'Edit Data Anggota'}
    return render(request, 'library/anggota_form.html', context)

@login_required
def anggota_delete(request, pk):
    anggota = get_object_or_404(Anggota, pk=pk)
    
    if request.method == 'POST':
        try:
            anggota.delete()
            messages.success(request, f'Anggota "{anggota.nama_lengkap}" berhasil dihapus.')
        except ProtectedError:
            # Menangkap ProtectedError jika anggota memiliki riwayat transaksi peminjaman
            messages.error(request, f'Gagal menghapus! Anggota "{anggota.nama_lengkap}" memiliki riwayat transaksi peminjaman.')
            
        return redirect('anggota_list')
        
    return render(request, 'library/anggota_confirm_delete.html', {'anggota': anggota})

@login_required
def peminjaman_create(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            try:
                # Menggunakan Database Transaction untuk mencegah data inkonsisten
                with transaction.atomic():
                    # commit=False agar kita bisa memanipulasi objek sebelum disimpan ke DB
                    transaksi = form.save(commit=False)
                    
                    # 1. Set User (Admin yang login)
                    transaksi.user = request.user
                    
                    # 2. Set Tanggal Otomatis
                    hari_ini = timezone.localtime().date()
                    transaksi.tanggal_pinjam = hari_ini
                    # Batas kembali di-set 7 hari dari sekarang
                    transaksi.batas_kembali = hari_ini + timedelta(days=7)
                    
                    # Status default 'Borrowed'
                    transaksi.status = 'Borrowed'
                    
                    # 3. Kurangi stok buku secara otomatis
                    buku_dipinjam = transaksi.buku
                    buku_dipinjam.stok_tersedia -= 1
                    buku_dipinjam.save()
                    
                    # 4. Simpan transaksi ke database
                    transaksi.save()
                    
                    messages.success(request, f'Transaksi peminjaman buku "{buku_dipinjam.judul}" berhasil dicatat.')
                    
                    # 5. Set HTTP Response dan Cookie
                    response = redirect('dashboard') 
                    
                    # Set cookie dengan key 'last_borrowed_book' yang berisi judul buku
                    # max_age = 604800 (berlaku selama 7 hari)
                    response.set_cookie('last_borrowed_book', buku_dipinjam.judul, max_age=604800)
                    
                    return response
                    
            except Exception as e:
                # Jika di tengah proses database mati / error, semua query dibatalkan (rollback)
                messages.error(request, f'Terjadi kesalahan sistem: {str(e)}')
        else:
            messages.error(request, 'Terdapat kesalahan input. Silakan periksa kembali.')
    else:
        form = TransaksiForm()
        
    context = {'form': form, 'title': 'Proses Peminjaman Buku'}
    return render(request, 'library/peminjaman_form.html', context)

@login_required
def transaksi_list(request):
    query = request.GET.get('q', '')
    
    transaksi_query = Transaksi.objects.select_related('buku', 'anggota', 'user').all().order_by('-tanggal_pinjam', '-id')
    
    if query:
        transaksi_query = transaksi_query.filter(
            Q(anggota__nama_lengkap__icontains=query) |
            Q(buku__judul__icontains=query) |
            Q(anggota__nomor_anggota__icontains=query)
        )
        
    paginator = Paginator(transaksi_query, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Logika Kalkulasi Keterlambatan Dinamis
    hari_ini = timezone.localtime().date()
    for t in page_obj:
        t.is_terlambat = False
        # Jika belum dikembalikan DAN hari ini sudah melewati batas kembali
        if t.status == 'Borrowed' and hari_ini > t.batas_kembali:
            t.is_terlambat = True
            
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'library/transaksi_list.html', context)

@login_required
def pengembalian_proses(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    
    # Proteksi: Hanya transaksi yang masih "Borrowed" yang bisa dikembalikan
    if request.method == 'POST' and transaksi.status == 'Borrowed':
        try:
            with transaction.atomic():
                # 1. Update status dan tanggal kembali aktual
                transaksi.status = 'Returned'
                transaksi.tanggal_kembali = timezone.localtime().date()
                transaksi.save()
                
                # 2. Kembalikan stok buku (+1)
                buku_dikembalikan = transaksi.buku
                buku_dikembalikan.stok_tersedia += 1
                buku_dikembalikan.save()
                
                messages.success(request, f'Buku "{buku_dikembalikan.judul}" berhasil dikembalikan. Stok telah diperbarui.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat memproses pengembalian: {str(e)}')
            
        return redirect('transaksi_list')
        
    context = {'transaksi': transaksi}
    return render(request, 'library/pengembalian_confirm.html', context)