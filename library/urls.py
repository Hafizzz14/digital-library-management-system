from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Root Redirect (/)
    path('', views.root_redirect, name='root'),
    
    # URL Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # URL Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Book CRUD URLs
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # Kategori CRUD URLs
    path('kategori/', views.kategori_list, name='kategori_list'),
    path('kategori/create/', views.kategori_create, name='kategori_create'),
    path('kategori/<int:pk>/update/', views.kategori_update, name='kategori_update'),
    path('kategori/<int:pk>/delete/', views.kategori_delete, name='kategori_delete'),

    # Anggota CRUD URLs
    path('anggota/', views.anggota_list, name='anggota_list'),
    path('anggota/create/', views.anggota_create, name='anggota_create'),
    path('anggota/<int:pk>/update/', views.anggota_update, name='anggota_update'),
    path('anggota/<int:pk>/delete/', views.anggota_delete, name='anggota_delete'),

    # Transaksi (Sirkulasi) URLs
    path('transaksi/', views.transaksi_list, name='transaksi_list'),
    path('transaksi/pinjam/', views.peminjaman_create, name='peminjaman_create'),
    path('transaksi/<int:pk>/kembali/', views.pengembalian_proses, name='pengembalian_proses'),
]