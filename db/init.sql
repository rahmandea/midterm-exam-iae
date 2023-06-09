CREATE DATABASE penjualan;
use penjualan;

CREATE TABLE produk (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  nama VARCHAR(255) NOT NULL,
  harga INTEGER NOT NULL,
  stok INTEGER NOT NULL
);

CREATE TABLE pesanan (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  id_produk INTEGER NOT NULL,
  jumlah INTEGER NOT NULL,
  tanggal DATE NOT NULL,
  FOREIGN KEY (id_produk) REFERENCES produk(id)
);
