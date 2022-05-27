-- DATABASES = {
--     'default': {
--         'ENGINE': 'django.db.backends.mysql',
--         'NAME': 'quan_ly_phieu_tiet_kiem',
--         'USER': 'banking_dev',
--         'PASSWORD': 'asdfghjkl01',
--         'HOST': '127.0.0.1',
--         'PORT': '3306',
--         'OPTIONS': {  
--             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
--         }  
--     }
-- }

use quan_ly_phieu_tiet_kiem;

# Create tables
create table KhachHang 
( makh varchar(10) not null,
tenkh varchar(50) not null,
diachi varchar (50) not null,
cccd varchar (12) not null,
primary key (makh)) ;

create table Phieutietkiem 
( maptk varchar(10) not null,
makh varchar(10) not null,
maltk varchar (10) not null,
sotiengoi decimal(13,2) not null,
ngaymophieu date not null,
ngaydongphieu date,
sodu decimal(13,2) not null,
tinhtrang bool not null,
primary key (maptk)) ;

create table loaitietkiem 
( maltk varchar(10) not null,
ltk varchar(20) not null,
kyhan int not null,
sotiengoitoithieu decimal(13,2) not null,
thoigiangoitoithieu int not  null,
laisuat float not null,
primary key (maltk)) ;

create table Phieuruttien 
( maprt varchar(10) not null,
makh varchar(10) not null,
maptk varchar (10) not null,
ngayrut date,
sotienrut decimal(13,2) not null,
primary key (maprt)) ;

create table  Baocaothang
( ngaythang date not null,
maltk varchar(10) not null,
phieugoi int not null,
phieudong int not null,
chenhlechdonggoi int not null,
primary key (ngaythang,maltk)) ;

create table  Baocaongay
( ngay date not null,
maltk varchar(10) not null,
tongthu decimal(13,2) not null,
tongchi decimal(13,2) not null,
chechlechthuchi decimal(13,2) not null,
primary key (ngay,maltk)) ;


# Create foreign key
ALTER TABLE Phieutietkiem
ADD CONSTRAINT FK_PTK_1
FOREIGN KEY (makh) REFERENCES Khachhang(makh);

ALTER TABLE Phieutietkiem
ADD CONSTRAINT FK_PTK_2
FOREIGN KEY (maltk) REFERENCES Loaitietkiem(maltk);

ALTER TABLE Phieuruttien
ADD CONSTRAINT FK_PRT_1
FOREIGN KEY (makh) REFERENCES Khachhang(makh);

ALTER TABLE Phieuruttien
ADD CONSTRAINT FK_PRT_2
FOREIGN KEY (maptk) REFERENCES Phieutietkiem(maptk);

ALTER TABLE Baocaothang
ADD CONSTRAINT FK_BCT
FOREIGN KEY (maltk) REFERENCES Loaitietkiem(maltk);

ALTER TABLE Baocaongay
ADD CONSTRAINT FK_BCN
FOREIGN KEY (maltk) REFERENCES Loaitietkiem(maltk);

# Create privilege tables
create table Nguoidung 
( tendn varchar(50) not null,
matkhau varchar(50) not null,
manhom varchar(10) not null,
primary key (tendn));

create table Phanquyen
( macn varchar(10) not null,
manhom varchar(10) not null,
primary key (macn,manhom));

create table Nhomnguoidung
( tennhom varchar(50) not null,
manhom varchar(10) not null,
primary key (manhom));

create table Chucnang
( macn varchar(10) not null,
tencn varchar(20) not null,
tenmanhinhduocloat varchar(20) not null,
primary key (macn));

# Create thamso table
create table Thamso
( tenthamso varchar(20) not null,
giatri varchar(10) not null,
primary key (tenthamso));


# Create foreign key of privilege tables
ALTER TABLE Phanquyen
ADD CONSTRAINT FK_PQ_1
FOREIGN KEY (macn) REFERENCES Chucnang(macn);

ALTER TABLE Phanquyen
ADD CONSTRAINT FK_PQ_2
FOREIGN KEY (manhom) REFERENCES Nhomnguoidung(manhom);

-- SHOW VARIABLES LIKE "sql_safe_updates";
SET SQL_SAFE_UPDATES = 'OFF';

-- Processing --
show tables;

# Insert dữ liệu
# Bảng khách hàng
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0001','Nguyen Thi Mai Phuong','Nghe An', '012345678');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0002','Tran Van Huynh','Binh Dinh', '013678562');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0003','Nguyen Minh Hieu','Da Nang', '123456789');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0004','Truong Ngoc Nguyen','Ha Noi', '654789456');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0005','Vo Chi cong','Quang Tri', '657904356');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0006','Le Huong Ly','Dong Nai', '897654234');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0007','Truong Hong Ngoc','Binh Phuoc', '145678903');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0008','Tran Minh Hong','Phu Yen', '038714337');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0009','Pham Van Anh','Ha Tinh', '033520978');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0010','Nguyen Thi Ngoc Bich','Ninh Binh', '123657908');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0011','Pham Cong Hai','Nghe An', '098923434');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0012','Luong The Vinh','Tp.HCM', '687456908');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0013','Nguyen Thi Huyen','Long an', '012345679');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0014','Tran Hue Linh','Ca Mau', '012345987');
INSERT INTO KhachHang (makh, tenkh, diachi,cccd) VALUES ('0015','Pham Van Hung','Tp.HCM', '134798567');

select * from khachhang;

# Loại tiết kiệm
INSERT INTO loaitietkiem(maltk,ltk,kyhan,sotiengoitoithieu,thoigiangoitoithieu,laisuat) VALUES ('LTK01','Khong ky han',0,'100000',15,'0.5'); 
INSERT INTO loaitietkiem(maltk,ltk,kyhan,sotiengoitoithieu,thoigiangoitoithieu,laisuat) VALUES ('LTK02','3 thang ',3,'100000',90,'5.0');
INSERT INTO loaitietkiem(maltk,ltk,kyhan,sotiengoitoithieu,thoigiangoitoithieu,laisuat) VALUES ('LTK03','6 thang ',6,'100000',180,'5.5');

# Phieutietkiem
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK001','0001','LTK03','100000000',STR_TO_DATE('01-04-2022', '%d-%m-%Y'),Null,'100000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK002','0002','LTK02','250000000',STR_TO_DATE('10-05-2022', '%d-%m-%Y'),Null,'250000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK003','0003','LTK01','200000000',STR_TO_DATE('09-02-2022', '%d-%m-%Y'),STR_TO_DATE('07-05-2022', '%d-%m-%Y'),'0','0');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK004','0004','LTK02','50000000',STR_TO_DATE('14-01-2022', '%d-%m-%Y'),STR_TO_DATE('14-05-2022', '%d-%m-%Y'),'0','0');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK005','0005','LTK03','150000000',STR_TO_DATE('17-04-2022', '%d-%m-%Y'),Null,'150000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK006','0006','LTK01','500000000',STR_TO_DATE('06-04-2021', '%d-%m-%Y'),STR_TO_DATE('06-10-2021', '%d-%m-%Y'),'0','0');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK007','0007','LTK02','350000000',STR_TO_DATE('17-07-2021', '%d-%m-%Y'),STR_TO_DATE('17-11-2021', '%d-%m-%Y'),'0','0');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK008','0008','LTK01','600000000',STR_TO_DATE('08-04-2022', '%d-%m-%Y'),Null,'600000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK009','0009','LTK03','100000000',STR_TO_DATE('06-04-2022', '%d-%m-%Y'),Null,'100000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK010','0010','LTK02','780000000',STR_TO_DATE('24-05-2022', '%d-%m-%Y'),Null,'780000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK011','0011','LTK03','100000000',STR_TO_DATE('01-04-2022', '%d-%m-%Y'),Null,'100000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK012','0012','LTK01','800000000',STR_TO_DATE('01-03-2022', '%d-%m-%Y'),Null,'800000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK013','0013','LTK02','130000000',STR_TO_DATE('05-01-2022', '%d-%m-%Y'),STR_TO_DATE('05-05-2022', '%d-%m-%Y'),'0','0');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK014','0001','LTK03','440000000',STR_TO_DATE('11-01-2022', '%d-%m-%Y'),Null,'440000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK015','0001','LTK02','550000000',STR_TO_DATE('23-04-2022', '%d-%m-%Y'),Null,'550000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK016','0001','LTK02','160000000',STR_TO_DATE('21-04-2022', '%d-%m-%Y'),Null,'160000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK017','0002','LTK02','600000000',STR_TO_DATE('09-01-2022', '%d-%m-%Y'),STR_TO_DATE('09-05-2022', '%d-%m-%Y'),'0','0');


INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK777','0001','LTK02','160000000',STR_TO_DATE('21-02-2022', '%d-%m-%Y'),Null,'160000000','1');
INSERT INTO Phieutietkiem (maptk,makh,maltk,sotiengoi,ngaymophieu,ngaydongphieu,sodu,tinhtrang) VALUES ('PTK999','0001','LTK01','160000000',STR_TO_DATE('21-01-2022', '%d-%m-%Y'),Null,'160000000','1');

# Phiếu rút tiền
INSERT INTO Phieuruttien (maprt,makh,maptk,ngayrut,sotienrut) VALUES ('PRT001','0003','PTK003',STR_TO_DATE('07-05-2022', '%d-%m-%Y'),'200000000');
INSERT INTO Phieuruttien (maprt,makh,maptk,ngayrut,sotienrut) VALUES ('PRT002','0004','PTK004',STR_TO_DATE('14-05-2022', '%d-%m-%Y'),'500000000');
INSERT INTO Phieuruttien (maprt,makh,maptk,ngayrut,sotienrut) VALUES ('PRT003','0006','PTK006',STR_TO_DATE('06-10-2021', '%d-%m-%Y'),'500000000');
INSERT INTO Phieuruttien (maprt,makh,maptk,ngayrut,sotienrut) VALUES ('PRT004','0007','PTK007',STR_TO_DATE('17-11-2021', '%d-%m-%Y'),'350000000');
INSERT INTO Phieuruttien (maprt,makh,maptk,ngayrut,sotienrut) VALUES ('PRT005','0013','PTK013',STR_TO_DATE('05-05-2021', '%d-%m-%Y'),'130000000');
INSERT INTO Phieuruttien (maprt,makh,maptk,ngayrut,sotienrut) VALUES ('PRT006','0002','PTK017',STR_TO_DATE('09-05-2021', '%d-%m-%Y'),'600000000');

# bangthamso
Insert into thamso (tenthamso, giatri) values ('SLNguoiDung','1');
Insert into thamso (tenthamso, giatri) values ('SLKhachHang','15');
Insert into thamso (tenthamso, giatri) values ('SLPhieuTietKiem','17');
Insert into thamso (tenthamso, giatri) values ('SLPhieuRutTien','6');
Insert into thamso (tenthamso, giatri) values ('SLLoaiTietKiem','3');