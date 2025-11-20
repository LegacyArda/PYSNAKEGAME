import pygame
import time
import random

KAYITLI_KULLANICILAR = {}
GIRIS_BASARILI = False

def kayit_ol():
    print("\n--- KAYIT OL ---")
    kullanici_adi = input("Yeni Kullanıcı Adı: ")
    
    if kullanici_adi in KAYITLI_KULLANICILAR:
        print("⛔ Bu kullanıcı adı zaten alınmış!")
        return

    sifre = input("Şifre: ")
    KAYITLI_KULLANICILAR[kullanici_adi] = sifre
    print(f"✅ Kayıt başarılı! Hoş geldin, {kullanici_adi}.")

def giris_yap():
    global GIRIS_BASARILI
    print("\n--- GİRİŞ YAP ---")
    kullanici_adi = input("Kullanıcı Adı: ")
    sifre = input("Şifre: ")

    if kullanici_adi in KAYITLI_KULLANICILAR:
        if KAYITLI_KULLANICILAR[kullanici_adi] == sifre:
            print(f"🎉 Başarıyla giriş yapıldı! {kullanici_adi}. Oyun Başlatılıyor...")
            GIRIS_BASARILI = True
            return
        else:
            print("❌ Kullanıcı adı veya şifre hatalı.")
    else:
        print("❌ Kullanıcı adı veya şifre hatalı.")
    
    GIRIS_BASARILI = False

while not GIRIS_BASARILI:
    print("\n--- MENU ---")
    print("1: Kayıt Ol")
    print("2: Giriş Yap")
    print("3: Çıkış")
    secim = input("Seçiminizi yapın (1/2/3): ")

    if secim == '1':
        kayit_ol()
    elif secim == '2':
        giris_yap()
    elif secim == '3':
        print("Görüşmek üzere!")
        exit()
    else:
        print("Lütfen geçerli bir seçim yapın.")

pygame.init()
beyaz = (255, 255, 255)
siyah = (0, 0, 0)
mavi = (50, 153, 213)
kirmizi = (213, 50, 80)
yesil = (0, 255, 0)
ekran_genislik = 1000
ekran_yukseklik = 800

ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))
pygame.display.set_caption('Python Snake Oyunu')

yilan_boyutu = 10
yilan_hizi = 15 

saat = pygame.time.Clock()
font_stili = pygame.font.SysFont("bahnschrift", 25)
skor_fontu = pygame.font.SysFont("comicsansms", 35)

def skorunuzu_goster(skor):
    deger = skor_fontu.render("Skorunuz: " + str(skor), True, beyaz)
    ekran.blit(deger, [0, 0])

def yilan_ciz(yilan_boyutu, yilan_listesi):
    for x in yilan_listesi:
        pygame.draw.rect(ekran, yesil, [x[0], x[1], yilan_boyutu, yilan_boyutu])

def mesaj_goster(msg, renk):
    mesaj = font_stili.render(msg, True, renk)
    ekran.blit(mesaj, [ekran_genislik / 6, ekran_yukseklik / 3])

def oyun_dongusu():
    oyun_bitti = False
    oyun_kapanisi = False

    x1 = ekran_genislik / 2
    y1 = ekran_yukseklik / 2

    x1_degisim = 0
    y1_degisim = 0

    yilan_listesi = []
    yilan_uzunlugu = 1

    yemekx = round(random.randrange(0, ekran_genislik - yilan_boyutu) / 30.0) * 20.0
    yemeky = round(random.randrange(0, ekran_yukseklik - yilan_boyutu) / 30.0) * 20.0

    while not oyun_bitti:
        
        while oyun_kapanisi == True:
            ekran.fill(siyah) 
            mesaj_goster("     Kaybettin! Çıkmak için ESC, Oynamak için R Bas-", kirmizi)
            skorunuzu_goster(yilan_uzunlugu - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        oyun_bitti = True     
                        oyun_kapanisi = False 
                    if event.key == pygame.K_r:
                        oyun_dongusu() 
                if event.type == pygame.QUIT:
                    oyun_bitti = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyun_bitti = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_degisim != yilan_boyutu:
                    x1_degisim = -yilan_boyutu
                    y1_degisim = 0
                elif event.key == pygame.K_RIGHT and x1_degisim != -yilan_boyutu:
                    x1_degisim = yilan_boyutu
                    y1_degisim = 0
                elif event.key == pygame.K_UP and y1_degisim != yilan_boyutu:
                    x1_degisim = 0
                    y1_degisim = -yilan_boyutu
                elif event.key == pygame.K_DOWN and y1_degisim != -yilan_boyutu:
                    x1_degisim = 0
                    y1_degisim = yilan_boyutu

        if x1 >= ekran_genislik or x1 < 0 or y1 >= ekran_yukseklik or y1 < 0:
            oyun_kapanisi = True
        
        x1 += x1_degisim
        y1 += y1_degisim
        
        ekran.fill(siyah)
        pygame.draw.rect(ekran, mavi, [yemekx, yemeky, yilan_boyutu, yilan_boyutu])

        yilan_bas = []
        yilan_bas.append(x1)
        yilan_bas.append(y1)
        yilan_listesi.append(yilan_bas)
        
        if len(yilan_listesi) > yilan_uzunlugu:
            del yilan_listesi[0]

        for x in yilan_listesi[:-1]:
            if x == yilan_bas:
                oyun_kapanisi = True

        yilan_ciz(yilan_boyutu, yilan_listesi)
        skorunuzu_goster(yilan_uzunlugu - 1)

        pygame.display.update()

        if x1 == yemekx and y1 == yemeky:
            yemekx = round(random.randrange(0, ekran_genislik - yilan_boyutu) / 10.0) * 10.0
            yemeky = round(random.randrange(0, ekran_yukseklik - yilan_boyutu) / 10.0) * 10.0
            yilan_uzunlugu += 1
            
        saat.tick(yilan_hizi)

    pygame.quit()
    quit()
    
oyun_dongusu()