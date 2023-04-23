import random
import json

tumHanelerinPozisyonlari = list(range(14))
takim1 = tumHanelerinPozisyonlari[:6]
takim2 = tumHanelerinPozisyonlari[7:13]
"""sayac = [0]"""


""" # Oynanmış oyunlar için kayıt kontrolü
try:
    dosya = open("oynanmislar.json","r")
    veritabani = json.load(dosya)
    oynanmislar = [x['hamleler'] for x in veritabani]
except:
    dosya = open("oynanmislar.json","a")
    dosya.write("[\n]")
    veritabani = {}
    oynanmislar = []
finally:
    dosya.close()
"""
while True:
    baslangic = input(
        "\nBilgisayarların oynamasını istiyorsanız 1 yazınız.\nKendiniz oynamak istiyorsanız 2 yazınız."
        "\nHerhangi bir pozisyondan devam etmek için 3 yazınız.\n=> ")
    if baslangic == "1" or "2" or "dene" or "3":
        break

def oyna(numara, taraf, konum): # Oyunun hamle fonksiyonu
    hazinekontrol = False # Hazinekontrol değişkeni True olursa hamleyi yapan 'taraf' tekrardan oynayabilecek.
    index = 0
    if taraf == 0: # Hamleyi yapan tarafın kuyularının konumu belirtiliyor
        tarafkuyu = takim1
    else:
        tarafkuyu = takim2
    if numara in tarafkuyu: # Hamleyi yapan kişinin kendi tarafındaki kuyulardan oynadığından emin olunuyor
        tekrar = int(konum.pop(numara)) # Hamleyi yaptığı kuyudaki taş sayısı
        konum.insert(numara, "0")
        if tekrar == 1: # Eğer sadece bir tane taş bulunan kuyuda hamle yaptıysa o taş bir ilerideki kuyuya taşınacak
            artan = int(konum.pop(numara + 1))
            konum.insert(numara + 1, str(artan + 1))
            index = numara + 1
        else: # Değilse kendi kuyusuna 1 tane bırakarak saat yönünde tüm kuyulara birer birer dağıtılacak
            x = 0
            while x < tekrar:
                if (numara + x) % 14 != (tarafkuyu[-1] + 1 + 7) % 14:
                    artan = int(konum.pop((numara + x) % 14))
                    konum.insert((numara + x) % 14, str(artan + 1))
                else:
                    tekrar += 1
                index = numara + x
                x += 1
        if (index % 14 == 6 or index % 14 == 13): # Taşların hazinede mi bittiği kontrol ediliyor
            if index % 14 == (tarafkuyu[-1] + 1): # Kendi hazinesiyse tekrar oynama hakkı kazandırılıyor
                hazinekontrol = True
            else: # Değilse orada bittiği
                index += 1
                artan = int(konum.pop(index % 14))
                konum.insert(index % 14, str(artan + 1))
        if (konum[index % 14] == "1") and (index % 14 in tarafkuyu):
            if tarafkuyu == takim1 and int(konum[takim2[5 - takim1.index(index % 14)]]) > 0:
                artan = int(konum.pop(index % 14))
                konum.insert(index % 14, "0")
                artan += int(konum.pop(takim2[5 - takim1.index(index % 14)]))
                konum.insert(takim2[5 - takim1.index(index % 14)], "0")
                artan += int(konum.pop(tarafkuyu[-1] + 1))
                konum.insert(tarafkuyu[-1] + 1, str(artan))
            elif tarafkuyu == takim2 and int(konum[takim1[5 - takim2.index(index % 14)]]) > 0:
                artan = int(konum.pop(index % 14))
                konum.insert(index % 14, "0")
                artan += int(konum.pop(takim1[5 - takim2.index(index % 14)]))
                konum.insert(takim1[5 - takim2.index(index % 14)], "0")
                artan += int(konum.pop(tarafkuyu[-1] + 1))
                konum.insert(tarafkuyu[-1] + 1, str(artan))
        elif (int(konum[index % 14]) % 2 == 0) and (index % 14 not in tarafkuyu):
            artan = int(konum.pop(index % 14))
            konum.insert(index % 14, "0")
            artan += int(konum.pop(tarafkuyu[-1] + 1))
            konum.insert(tarafkuyu[-1] + 1, str(artan))
        if list(konum[takim1[0]:takim1[-1] + 1]) == list("0" * 6):
            skor = 0
            for i in tumHanelerinPozisyonlari:
                if i != 6 and i != 13:
                    skor += int(konum[i])
                    konum[i] = "0"
            artan = int(konum.pop(takim1[-1] + 1))
            konum.insert(takim1[-1] + 1, str(artan + skor))
        elif list(konum[takim2[0]:takim2[-1] + 1]) == list("0" * 6):
            skor = 0
            for i in tumHanelerinPozisyonlari:
                if i != 6 and i != 13:
                    skor += int(konum[i])
                    konum[i] = "0"
            artan = int(konum.pop(takim2[-1] + 1))
            konum.insert(takim2[-1] + 1, str(artan + skor))
        if baslangic != "dene":
            veriler['hamleler'].append(numara)
        return hazinekontrol
    else:
        if baslangic != "3":
            print("HATA: Kural dışı hamle")
        else: return "HATA"

""" Daha bitmedi
def pozisyondan_devam(veriler=list):
    fen = list((["4"] * 6 + ["0"]) * 2)
    cnt = 0
    def dongu(veriler,cnt):
        for i in list(veriler):
            veri = oyna(int(i), cnt % 2, fen)
            if veri == "HATA":
                return veri,cnt+1
            if veri is not True:
                cnt += 1
    if veriler[-1] == "0-1" or "1-0" or "0.5":
        print(veriler.split(",")[:-1])
        dongu(list(veriler.split(",")[:-1]),cnt)
    else: dongu(list(veriler),cnt)
    return fen,cnt
"""

def kuyular(fen2): #Mangala tahtasının görsel gösterimi (pek de önemli değil)
    numaralar = [f"{str(x)} " if len(str(x)) == 1 else x for x in fen2]
    print("\n")
    konsolnumara = []
    solpuan = str(fen2[6])
    sagpuan = str(fen2[-1])
    for j in numaralar:
        konsolnumara.append(f"|  {str(j)}  | ")
    konsolnumara.reverse()
    print(f" /========\\  \t" + f" /====\\ \t" * 6 + f"  /========\\")
    if len(solpuan) < 2:
        solpuan = f"{solpuan} "
    if len(str(sagpuan)) < 2:
        sagpuan = f"{sagpuan} "
    print(f"|          |  \t" + f"\t".join(konsolnumara[-6:]) + f"\t |          |")
    konsolnumara.reverse()
    print(f"|          |  \t" + f" \\====/ \t" * 6 + f" |          |")
    print(f"|    {solpuan}    |  \t" + f"\t" * 18 + f" |    {sagpuan}    |")
    print(f"|          |  \t" + f" /====\\ \t" * 6 + f" |          |")
    print(f"|          |  \t" + f"\t".join(konsolnumara[-7:-1]) + f"\t |          |")
    print(f" \\========/  \t" + f" \\====/ \t" * 6 + f"  \\========/")


if baslangic != "dene":
    for i in range(10):
        fen = list((["4"] * 6 + ["0"]) * 2)
        veriler = {'hamleler':[],'sonuc': None}
        """if baslangic == "3":
            veriler['hamleler'] = input("Hamle sıralamasını giriniz: ")"""
        cnt = 0
        if baslangic == "1":
            print("\n\nİlk hamle yukarı tarafındır.")
        while int(fen[6]) + int(fen[13]) < 48:
            while True:
                if baslangic == "3":
                    """for i in veriler:
                        veriler"""
                    pass
                elif baslangic == "1":
                    if cnt % 2 == 0:
                        girdikontrol = str(random.choice(takim1.copy()))
                    else:
                        girdikontrol = str(random.choice(takim2.copy()))
                else:
                    kuyular(fen)
                    girdikontrol = input("Hamle giriniz => ")
                if girdikontrol.isdigit():
                    girdi = int(girdikontrol)
                    break
                else:
                    print("Lütfen sayı giriniz.")
            if girdi in tumHanelerinPozisyonlari:
                if girdi is not (6 or 13):
                    if fen[girdi] != "0":
                        if oyna(girdi, cnt % 2,fen) is True:
                            if baslangic == "2":
                                print("Bir kez daha oynama hakkı kazandınız.")
                            pass
                        else:
                            cnt += 1
                    else:
                        if baslangic == "2":
                            print("HATA: Boş kuyuda hamle yapılamaz.")
                        pass
                else:
                    print("HATA: Hazinelere dokunulamaz.")
            else:
                print("HATA: Oynamak istediğiniz kuyu bulunmamakta.")
        if int(fen[6]) > int(fen[13]):
            print(f"Yukarı taraf oyunu {abs(int(fen[6]) - int(fen[13]))} puan farkla kazandı.")
            #veriler["sonuc"] = 1
        elif int(fen[6]) < int(fen[13]):
            print(f"Aşağı taraf oyunu {abs(int(fen[6]) - int(fen[13]))} puan farkla kazandı.")
            #veriler["sonuc"] = 0
        else:
            print("Oyun berabere bitti.")
            #veriler["sonuc"] = 5
        kuyular(fen)
        """if veriler['hamleler'] in oynanmislar:
            print("Ayrıca böyle bir oyun zaten oynanmıştı.")
        else:
            veritabani.append(veriler)
            oynanmislar.append(veriler['hamleler'])"""
else:

    # Her hamleyi bulmaya çalıştığı yer burada başlıyor

    pozisyon = list((["4"] * 6 + ["0"]) * 2)
    """veriler = {"hamleler": [], "sonuc": None}"""
    def deneme(konum,sira,veri=list):
        son_konum = konum.copy()
        kuyular(konum)
        sira = sira%2
        if sira == 0 and list(konum[takim1[0]:takim1[-1] + 1]) != list("0" * 6):
            # Sıra birinci oyundaysa ve o oyuncunun kuyuları bomboş değilse (oyuncu yenik durumda değilse)
            for i in takim1: # Tüm oynanabilinecek ihtimaller sıra sıra sınanıyor
                if str(son_konum[i]) != "0": # Eğer boş değilse oynatıyor
                    son_veri = veri.copy()
                    veri.append(i)
                    if oyna(i,sira,konum) is not True: # hazinekontrol eğer Doğru ise oyuncu tekrar oynama hakkı kazanacak.
                        sira += 1
                    """sayac[0] += 1
                    print(sayac)"""
                    deneme(konum,sira,veri)
                    konum = son_konum.copy()
                    veri = son_veri.copy()
        elif sira == 1 and list(konum[takim2[0]:takim2[-1] + 1]) != list("0" * 6): # İkinci oyuncu kontrol edilir
            for i in takim2: # Aynı işlemler
                if str(son_konum[i]) != "0":
                    son_veri = veri.copy()
                    veri.append(i)
                    if oyna(i, sira, konum) is not True:
                        sira += 1
                    """sayac[0] += 1
                    print(sayac)"""
                    deneme(konum, sira, veri)
                    konum = son_konum.copy()
                    veri = son_veri.copy()
        if int(konum[6]) + int(konum[13]) == 48: # Her iki oyuncunun kuyuları boşsa oyun bitmiş demektir
            """veriler = {"hamleler": [], "sonuc": None}
            veriler["hamleler"] = veri"""
            if int(konum[6]) > int(konum[13]):
                print(f"Yukarı taraf oyunu {abs(int(konum[6]) - int(konum[13]))} puan farkla kazandı.")
                veriler["sonuc"] = 1
            elif int(konum[6]) < int(konum[13]):
                print(f"Aşağı taraf oyunu {abs(int(konum[6]) - int(konum[13]))} puan farkla kazandı.")
                veriler["sonuc"] = 0
            else:
                print("Oyun berabere bitti.")
                veriler["sonuc"] = 5
            """if veri in oynanmislar:
                print("Ayrıca böyle bir oyun zaten oynanmıştı.")
            else:
                veritabani.append(veriler)
                oynanmislar.append(veri)"""
    deneme(pozisyon,0,[]) # Her şeyi tetikleyen başlangıç
    pass

#with open("oynanmislar.json","w") as dosya:
#    veritabani = sorted(veritabani, key=lambda k: k["hamleler"], reverse=False)
#    json.dump(veritabani,dosya)
#    for i in veritabani:
#        print(i["sonuc"])
