import http.server
import socketserver
import json
import urllib.parse
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

PERFUMES_DATA = [
    {
        "id": "angels-share",
        "name": "Angels' Share",
        "brand": "Kilian Paris",
        "concentration": "Eau de Parfum",
        "gender": "Unisex",
        "category": "Niş / Sıcak & Gurme",
        "family": "Amber / Baharatlı",
        "image": "https://fimgs.net/mdimg/perfume/375x500.62615.jpg",
        "year": 2020,
        "perfumer": "Benoist Lapouza",
        "trivia": {
            "title": "Viski Kadehi Tasarımı & Hennessy Hanedanlığı Mirası",
            "text": "Şişesi lüks ve ağır bir art-deco kristal viski/konyak bardağını andırır. Kilian Hennessy, dünyaca ünlü Hennessy konyak hanedanlığının 8. kuşak doğrudan varisidir. Parfümün adı olan 'Angels' Share' (Meleklerin Payı), meşe fıçılarda konyak yıllandırılırken ahşabın gözeneklerinden buharlaşarak havaya karışan ve tanrılara/meleklere adandığına inanılan %2'lik konyak buharını simgeler.",
            "highlight": "Konyak fıçılarından damıtılmış gerçek likör özleri içerir ve şişesi doldurulabilir (refillable) kristal kadeh formundadır."
        },
        "vibe": {
            "summary": "Karlı bir kış gecesinde loş ışıklı gizli bir speakeasy caz barda, elde bir kadeh yıllanmış konyak ve sıcak tarçınlı elmalı turta aurası.",
            "mood": "Gizemli, Baştan Çıkarıcı, Sıcak, Elit",
            "longevity": "9.4 / 10 (12+ Saat)",
            "sillage": "9.1 / 10 (Girdiği odayı dolduran aura)",
            "season": "Sonbahar - Kış (Soğuk Havalar)",
            "occasion": "Özel Akşam Yemekleri, Gece Kulübü, Romantik Randevular"
        },
        "notes": {
            "top": ["Konyak Likörü Esansı", "Meşe Ağacı"],
            "heart": ["Seylan Tarçını", "Tonka Fasulyesi", "Meşe Ağacı Özü"],
            "base": ["Pralin", "Vanilya", "Sandal Ağacı"]
        },
        "prices": [
            {
                "store": "Parfüm Noktası",
                "price": 9850,
                "old_price": 11450,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "Peşin Fiyatına 3 Taksit",
                "shipping": "Aynı Gün Ücretsiz Kargo",
                "link": "https://www.parfumnoktasi.com/kilian-angels-share-edp-50ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 10450,
                "old_price": 10950,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Bonus'a 4 Taksit",
                "shipping": "Ücretsiz Mağazadan Teslim / Kargo",
                "link": "https://www.sephora.com.tr/p/angels-share---eau-de-parfum-P10014022.html"
            },
            {
                "store": "Boyner",
                "price": 10750,
                "old_price": 10750,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Hopi ile %10 Paracık",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/kilian-angels-share-edp-50-ml-parfum-1002931"
            },
            {
                "store": "Beymen",
                "price": 10950,
                "old_price": 10950,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club Avantajları",
                "shipping": "Özel Kurye ile Hızlı Teslimat",
                "link": "https://www.beymen.com/tr/p_kilian-angels-share-edp-50-ml-parfum_872195"
            },
            {
                "store": "Sevil Parfümeri",
                "price": 11200,
                "old_price": 11200,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "6 Taksit İmkanı",
                "shipping": "3 İş Gününde Kargo",
                "link": "https://www.sevil.com.tr/kilian-angels-share-edp-50ml"
            }
        ]
    },
    {
        "id": "baccarat-rouge-540",
        "name": "Baccarat Rouge 540",
        "brand": "Maison Francis Kurkdjian",
        "concentration": "Extrait de Parfum",
        "gender": "Unisex",
        "category": "Niş / Çiçeksi Amber",
        "family": "Amber / Odunsu",
        "image": "https://fimgs.net/mdimg/perfume/375x500.33452.jpg",
        "year": 2017,
        "perfumer": "Francis Kurkdjian",
        "trivia": {
            "title": "540 Santigrat Derecede Kristalin Kızıla Dönüşümü",
            "text": "Parfümün adındaki '540' sayısı, Baccarat kristalinin imza yakut kırmızısı rengini alabilmesi için 24 ayar saf altın tozuyla birlikte fırında tam 540 santigrat derecede eritilmesinden gelir. Francis Kurkdjian bu başyapıtı dünyanın en köklü kristal üreticisi Baccarat'nın 250. kuruluş yıl dönümünü onurlandırmak için üretmiştir.",
            "highlight": "Kırmızı altın rengi şişesi, simyacıların fırınındaki 540°C ısının kristalleşmiş halini temsil eder."
        },
        "vibe": {
            "summary": "Monaco'da lüks bir kumarhane, kırmızı kadife halılar, amberimsi pamuk şekeri ve gökdelenlerin penthouse katında saf ışıltı.",
            "mood": "Ultra Lüks, Manyetik, Hipnotize Edici, Zengin",
            "longevity": "9.9 / 10 (Ertesi gün bile teninizde)",
            "sillage": "9.7 / 10 (Odaya girmeden önce kokusu gelen efsane)",
            "season": "4 Mevsim / Sonbahar & Kış Ağırlıklı",
            "occasion": "Gala, Kırmızı Halı, Prestijli Davetler"
        },
        "notes": {
            "top": ["Acı Badem", "İran Safranı"],
            "heart": ["Mısır Yasemini", "Sedir Ağacı"],
            "base": ["Ambergris (Doğal Balina Kehribarı)", "Odunsu Misk"]
        },
        "prices": [
            {
                "store": "Parfüm Noktası",
                "price": 15600,
                "old_price": 17800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "3 Taksit",
                "shipping": "Sigortalı Kargo",
                "link": "https://www.parfumnoktasi.com/mfk-baccarat-rouge-540-extrait-70ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 16900,
                "old_price": 17500,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Vade Farksız 3 Taksit",
                "shipping": "Ücretsiz Teslimat",
                "link": "https://www.sephora.com.tr/p/baccarat-rouge-540-extrait-P3647005.html"
            },
            {
                "store": "Boyner",
                "price": 17200,
                "old_price": 17200,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Kredi Kartına 4 Taksit",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/mfk-baccarat-rouge-540-extrait-70ml"
            },
            {
                "store": "Beymen",
                "price": 17500,
                "old_price": 17500,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club Puan",
                "shipping": "Aynı Gün Kurye",
                "link": "https://www.beymen.com/tr/p_mfk-baccarat-rouge-540-extrait-70ml_643210"
            }
        ]
    },
    {
        "id": "creed-aventus",
        "name": "Aventus",
        "brand": "Creed",
        "concentration": "Eau de Parfum",
        "gender": "Erkek / Unisex",
        "category": "Niş / Şipre Meyveli",
        "family": "Meyveli / Dumanlı Deri",
        "image": "https://fimgs.net/mdimg/perfume/375x500.9828.jpg",
        "year": 2010,
        "perfumer": "Erwin & Olivier Creed",
        "trivia": {
            "title": "İmparator Napolyon ve Şahlanan At Motifi",
            "text": "Şişenin ön yüzündeki gümüş at ve binici kabartması, İmparator Napolyon Bonapart'ın tarihi zaferlerinden ve askeri gücünden ilham almıştır. Şişenin alt kısmını saran siyah dokulu kaplama ise antik askeri zırhı ve gücü temsil eder. Parfüm dünyasında 'batch code' (üretim partisi) çılgınlığını başlatan ilk kokudur.",
            "highlight": "Güç, vizyon ve başarıyı kutlayan; tarihin en çok satan niş erkek parfümü unvanına sahiptir."
        },
        "vibe": {
            "summary": "Milyon dolarlık bir toplantıyı yeni kapatmış, ısmarlama takım elbiseli, karizmatik ve kendinden emin bir lider.",
            "mood": "Lider, Güçlü, Dinamik, Asil",
            "longevity": "8.9 / 10 (9-10 Saat)",
            "sillage": "9.0 / 10 (Farkedilir taze dumanlı iz)",
            "season": "4 Mevsim / İlkbahar & Sonbahar İdeal",
            "occasion": "İş Görüşmesi, CEO Masası, İmza Kokusu"
        },
        "notes": {
            "top": ["Taze Ananas", "Bergamot", "Siyah Frenk Üzümü", "Elma"],
            "heart": ["Huş Ağacı (Dumanlı)", "Paçuli", "Fas Yasemini", "Gül"],
            "base": ["Misk", "Meşe Yosunu", "Ambergris", "Vanilya"]
        },
        "prices": [
            {
                "store": "Parfüm Noktası",
                "price": 13900,
                "old_price": 15400,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.parfumnoktasi.com/creed-aventus-edp-100ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 14500,
                "old_price": 14900,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "4 Taksit",
                "shipping": "Hızlı Kargo",
                "link": "https://www.sephora.com.tr/p/aventus---eau-de-parfum-P2001.html"
            },
            {
                "store": "Beymen",
                "price": 14800,
                "old_price": 14800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "VIP Teslimat",
                "shipping": "Aynı Gün Teslim",
                "link": "https://www.beymen.com/tr/p_creed-aventus-edp-100ml_312456"
            },
            {
                "store": "Boyner",
                "price": 14950,
                "old_price": 14950,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Vade Farksız 3 Taksit",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/creed-aventus-edp-100ml"
            },
            {
                "store": "Sevil Parfümeri",
                "price": 15200,
                "old_price": 15200,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "6 Taksit",
                "shipping": "Kargo Bedava",
                "link": "https://www.sevil.com.tr/creed-aventus-edp-100ml"
            }
        ]
    },
    {
        "id": "tom-ford-tobacco-vanille",
        "name": "Tobacco Vanille",
        "brand": "Tom Ford",
        "concentration": "Eau de Parfum",
        "gender": "Unisex",
        "category": "Niş / Baharatlı Oryantal",
        "family": "Tütün / Tatlı Baharat",
        "image": "https://fimgs.net/mdimg/perfume/375x500.1825.jpg",
        "year": 2007,
        "perfumer": "Olivier Gillotin",
        "trivia": {
            "title": "İngiliz Centilmen Kulüpleri ve Satranç Taşı Şişesi",
            "text": "Tom Ford bu parfümü Londra'daki tarihi ve kapalı centilmen kulüplerine (gentlemen's clubs) olan hayranlığından yola çıkarak tasarladı. Şişesinin formu ise geleneksel bir satranç kalesi taşından esinlenilerek özel koyu kahverengi mimari camla şekillendirilmiştir.",
            "highlight": "Pipo tütününün kuru aroması ile Madagaskar vanilyasının asil buluşması."
        },
        "vibe": {
            "summary": "Ağır meşe kaplı bir kütüphanede, chesterfield deri koltukta tüten pipo tütünü ve vanilyalı sıcak içecek.",
            "mood": "Aristokrat, Sıcak, Zengin, Güven Verici",
            "longevity": "9.5 / 10 (14+ Saat)",
            "sillage": "9.3 / 10 (Kıyafetlerde günlerce kalan sıcaklık)",
            "season": "Kış - Sonbahar",
            "occasion": "Kış Tatilleri, Akşam Yemeği, Kar Manzarası"
        },
        "notes": {
            "top": ["Tütün Yaprağı", "Zencefil", "Baharat Notaları"],
            "heart": ["Tonka Fasulyesi", "Kakao", "Vanilya", "Tütün Çiçeği"],
            "base": ["Kuru Meyve Akorları", "Zengin Odunsu Notalar"]
        },
        "prices": [
            {
                "store": "Boyner",
                "price": 12200,
                "old_price": 13100,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "4 Taksit",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/tom-ford-tobacco-vanille-edp-50ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 12800,
                "old_price": 12800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Teslim",
                "link": "https://www.sephora.com.tr/p/tobacco-vanille---eau-de-parfum-P55201.html"
            },
            {
                "store": "Beymen",
                "price": 12950,
                "old_price": 12950,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club Puan",
                "shipping": "VIP Kurye",
                "link": "https://www.beymen.com/tr/p_tom-ford-tobacco-vanille-edp-50ml_120445"
            },
            {
                "store": "Sevil Parfümeri",
                "price": 13100,
                "old_price": 13100,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "6 Taksit",
                "shipping": "Kargo Bedava",
                "link": "https://www.sevil.com.tr/tom-ford-tobacco-vanille-edp-50ml"
            }
        ]
    },
    {
        "id": "dior-sauvage-elixir",
        "name": "Sauvage Elixir",
        "brand": "Dior",
        "concentration": "Parfum / Elixir",
        "gender": "Erkek",
        "category": "Designer Lüks / Baharatlı Odunsu",
        "family": "Taze Baharat / Lavanta / Likör",
        "image": "https://fimgs.net/mdimg/perfume/375x500.68415.jpg",
        "year": 2021,
        "perfumer": "François Demachy",
        "trivia": {
            "title": "Gece Göğünün Laciverti & François Demachy'nin Jübilesi",
            "text": "Sauvage Elixir, efsanevi parfümör François Demachy'nin Dior moda evinden emekli olmadan önce yarattığı son başyapıttır. Sauvage DNA'sını konsantre bir gece iksirine dönüştürmek için gece gökyüzünün en derin lacivert tonunu yansıtan minik ama aşırı ağır özel cam şişe geliştirilmiştir.",
            "highlight": "Geleneksel Sauvage ferahlığını yoğun meyan kökü, tarçın ve Fransız lavantası likörüyle harmanlar."
        },
        "vibe": {
            "summary": "Dolunay altındaki kızıl çöl gecesinde, kamp ateşi kıvılcımları ve rüzgarın taşıdığı manyetik karanlık baharatlar.",
            "mood": "Manyetik, Maskülen, Derin, Yoğun",
            "longevity": "9.8 / 10 (Ten üzerinde 24 saat kalıcı)",
            "sillage": "9.6 / 10 (2 fıs tüm odayı kaplar)",
            "season": "Sonbahar - Kış - Serin İlkbahar",
            "occasion": "Özel Gece Çıkışları, Kulüp, Soğuk Akşamlar"
        },
        "notes": {
            "top": ["Seylan Tarçını", "Muskat (Küçük Hindistan Cevizi)", "Kakule", "Greyfurt"],
            "heart": ["Özel Nyons Lavantası"],
            "base": ["Meyan Kökü", "Sandal Ağacı", "Amber", "Haiti Vetiveri"]
        },
        "prices": [
            {
                "store": "Boyner",
                "price": 7450,
                "old_price": 8200,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "Hopi İndirimiyle",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/dior-sauvage-elixir-parfum-60ml"
            },
            {
                "store": "Sevil Parfümeri",
                "price": 7800,
                "old_price": 7800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "6 Taksit",
                "shipping": "Hızlı Kargo",
                "link": "https://www.sevil.com.tr/dior-sauvage-elixir-60ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 7950,
                "old_price": 7950,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Teslimat",
                "link": "https://www.sephora.com.tr/p/sauvage-elixir---parfum-P10017126.html"
            },
            {
                "store": "Beymen",
                "price": 8100,
                "old_price": 8100,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club",
                "shipping": "Özel Paketleme",
                "link": "https://www.beymen.com/tr/p_dior-sauvage-elixir-60ml_998124"
            }
        ]
    },
    {
        "id": "le-labo-santal-33",
        "name": "Santal 33",
        "brand": "Le Labo",
        "concentration": "Eau de Parfum",
        "gender": "Unisex",
        "category": "Niş / Odunsu Aromatik",
        "family": "Sandal Ağacı / Deri / İris",
        "image": "https://fimgs.net/mdimg/perfume/375x500.12201.jpg",
        "year": 2011,
        "perfumer": "Frank Voelkl",
        "trivia": {
            "title": "Amerikan Marlboro Man Miti ve Eczane Şişesi",
            "text": "Santal 33, Amerikan Vahşi Batı efsanesinden ve atının üzerinde uçsuz bucaksız kanyonlara bakan özgür kovboy imajından ilham almıştır. İsmindeki '33' rakamı, formülünde kullanılan tam 33 bileşeni temsil eder. Şişesi ise 19. yüzyıl vintage New York eczacı şişeleri tarzında hazırlanır ve alıcının adıyla kişiselleştirilir.",
            "highlight": "New York ve Londra moda çevrelerinin en çok koklanan ikonik kült parfümü."
        },
        "vibe": {
            "summary": "SoHo sanat galerisi, minimalist ahşap mobilyalar, şık deri ceket, kahve aroması ve entelektüel sohbetler.",
            "mood": "Entelektüel, Bohem, Minimalist, Karizmatik",
            "longevity": "9.1 / 10 (11 Saat)",
            "sillage": "8.8 / 10 (Zarif ve farkedilir)",
            "season": "İlkbahar - Sonbahar - Kış",
            "occasion": "Tasarım Ofisi, Sanat Etkinlikleri, Şık Kafeler"
        },
        "notes": {
            "top": ["Kakule", "Menekşe Akoru"],
            "heart": ["İris", "Papirüs Bitkisi", "Sedir Ağacı"],
            "base": ["Avustralya Sandal Ağacı", "Deri Akoru", "Kehribar"]
        },
        "prices": [
            {
                "store": "Parfüm Noktası",
                "price": 9950,
                "old_price": 11200,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Sigortalı Kargo",
                "link": "https://www.parfumnoktasi.com/le-labo-santal-33-edp-100ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 10900,
                "old_price": 10900,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Teslim",
                "link": "https://www.sephora.com.tr/p/santal-33-edp-100ml"
            },
            {
                "store": "Beymen",
                "price": 11200,
                "old_price": 11200,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Ayrıcalıkları",
                "shipping": "Hızlı Kurye",
                "link": "https://www.beymen.com/tr/p_le-labo-santal-33-100ml_441923"
            },
            {
                "store": "Boyner",
                "price": 11400,
                "old_price": 11400,
                "currency": "₺",
                "in_stock": False,
                "is_lowest": False,
                "installment": "Tükendi",
                "shipping": "Stok Bekleniyor",
                "link": "https://www.boyner.com.tr/le-labo-santal-33"
            }
        ]
    },
    {
        "id": "nishane-hacivat",
        "name": "Hacivat",
        "brand": "Nishane Istanbul",
        "concentration": "Extrait de Parfum",
        "gender": "Unisex",
        "category": "Niş / Şipre Meyveli",
        "family": "Ananas / Narenciye / Meşe Yosunu",
        "image": "https://fimgs.net/mdimg/perfume/375x500.44174.jpg",
        "year": 2017,
        "perfumer": "Jorge Lee",
        "trivia": {
            "title": "Geleneksel Türk Gölge Oyunu & Hacivat Çelebi",
            "text": "İstanbul kökenli dünyaca ünlü lüks niş parfüm evi Nishane'nin 'Gölge Oyunu' üçlemesinin baş tacıdır. Osmanlı döneminin zeki, nazik, sanatsever ve kültürlü karakteri Hacivat Çelebi'ye adanmıştır. Şişesindeki altın rengi gravürler Türk saray hat sanatından izler taşır.",
            "highlight": "Türkiye'den çıkıp dünyanın en iyi parfümleri listelerine 1 numaradan giren milli gururumuz."
        },
        "vibe": {
            "summary": "Boğaz'da serin bir rüzgar, taze sulu ananas dilimleri ve asil Akdeniz meşeleri. Sabah enerjisiyle başlayıp geceye kadar dinmeyen ışıltı.",
            "mood": "Asil, Canlandırıcı, Karizmatik, Akılda Kalıcı",
            "longevity": "9.6 / 10 (Extrait konsantrasyonuyla 14+ Saat)",
            "sillage": "9.4 / 10 (Arkada devasa bir imza kokusu bırakır)",
            "season": "İlkbahar - Yaz - Sonbahar (Her Mevsim)",
            "occasion": "Yaz Davetleri, Özel Toplantılar, Günlük Lüks"
        },
        "notes": {
            "top": ["Sulu Ananas", "Bergamot", "Greyfurt"],
            "heart": ["Yasemin", "Paçuli", "Sedir Ağacı"],
            "base": ["Şeffaf Meşe Yosunu", "Kuru Odunsu Notalar"]
        },
        "prices": [
            {
                "store": "Parfüm Noktası",
                "price": 8700,
                "old_price": 9900,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "3 Taksit",
                "shipping": "Aynı Gün Kargo",
                "link": "https://www.parfumnoktasi.com/nishane-hacivat-extrait-100ml"
            },
            {
                "store": "Boyner",
                "price": 9400,
                "old_price": 9400,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Hopi Kampanyası",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/nishane-hacivat-extrait-100ml"
            },
            {
                "store": "Beymen",
                "price": 9600,
                "old_price": 9600,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club Puan",
                "shipping": "Hızlı Kurye",
                "link": "https://www.beymen.com/tr/p_nishane-hacivat-extrait-100ml_552194"
            },
            {
                "store": "Sephora Türkiye",
                "price": 9800,
                "old_price": 9800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Teslim",
                "link": "https://www.sephora.com.tr/p/hacivat-extrait-100ml"
            }
        ]
    },
    {
        "id": "replica-by-the-fireplace",
        "name": "By the Fireplace",
        "brand": "Maison Margiela",
        "concentration": "Eau de Toilette",
        "gender": "Unisex",
        "category": "Niş / Sıcak Odunsu",
        "family": "Kestane / Duman / Vanilya",
        "image": "https://fimgs.net/mdimg/perfume/375x500.31623.jpg",
        "year": 2015,
        "perfumer": "Marie Salamagne",
        "trivia": {
            "title": "1971 Chamonix Kış Tatili ve Daktilo Etiketi",
            "text": "Maison Margiela'nın Replica serisi, insanın hayatındaki unutulmaz anı ve mekanları yeniden canlandırmak için tasarlanmıştır. Bu parfümün pamuklu kumaş etiketinde 'Chamonix, 1971' yazar; Fransa Alpleri'nde karlar altındaki ahşap bir dağ evinde şöminede kestane közleme anını simgeler.",
            "highlight": "Kapağı olmayan eczacı şişesi ve pamuklu daktilo etiketiyle tam bir tasarım harikası."
        },
        "vibe": {
            "summary": "Dışarıda fırtına ve kar yağarken, ahşap dağ evinde çıtırdayan şömine ateşi, fırında közlenen tatlı kestaneler ve sıcacık kaşmir battaniye.",
            "mood": "Nostaljik, Huzurlu, Sıcacık, Samimi",
            "longevity": "8.7 / 10 (8-10 Saat)",
            "sillage": "8.5 / 10 (Sıcak samimi çember)",
            "season": "Kış - Sonbahar",
            "occasion": "Şömine Başı, Kar Tatili, Pazar Günleri"
        },
        "notes": {
            "top": ["Karanfil", "Pembe Biber", "Portakal Çiçeği"],
            "heart": ["Kestane Akoru", "Guaiac Ağacı", "Ardıç"],
            "base": ["Bourbon Vanilya", "Peru Balsamı", "Kaşmiran"]
        },
        "prices": [
            {
                "store": "Boyner",
                "price": 5400,
                "old_price": 5900,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "Hopi İndirimi",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/maison-margiela-by-the-fireplace-100ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 5650,
                "old_price": 5650,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Hızlı Kargo",
                "link": "https://www.sephora.com.tr/p/replica-by-the-fireplace-100ml"
            },
            {
                "store": "Sevil Parfümeri",
                "price": 5700,
                "old_price": 5700,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "6 Taksit",
                "shipping": "Ücretsiz Teslim",
                "link": "https://www.sevil.com.tr/replica-by-the-fireplace"
            },
            {
                "store": "Beymen",
                "price": 5800,
                "old_price": 5800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club",
                "shipping": "Özel Kurye",
                "link": "https://www.beymen.com/tr/p_maison-margiela-fireplace-100ml_87123"
            }
        ]
    },
    {
        "id": "xerjoff-naxos",
        "name": "Naxos",
        "brand": "Xerjoff",
        "concentration": "Eau de Parfum",
        "gender": "Unisex",
        "category": "Niş / Aromatik Baharatlı",
        "family": "Bal / Tütün / Lavanta",
        "image": "https://fimgs.net/mdimg/perfume/375x500.30529.jpg",
        "year": 2015,
        "perfumer": "Chris Maurice",
        "trivia": {
            "title": "İtalya Birliği 1861 Koleksiyonu ve Sicilya Mirası",
            "text": "Naxos, İtalya'nın birleşmesinin 150. yılı anısına yaratılan prestijli 'Xerjoff 1861' koleksiyonunun en parlayan yıldızıdır. Sicilya adasının Akdeniz güneşi, bin yıllık bal üretimi ve tarihi tütün ticaretinin bereketini İtalyan kuyumculuk zarafetiyle işlenmiş altın kaplama bir şişede yaşatır.",
            "highlight": "Hakiki Akdeniz lavantası ile tatlı tütün ve organik balın muhteşem harmonisi."
        },
        "vibe": {
            "summary": "Sicilya kıyılarında gün batımı, altın sarısı bal petekleri, taze lavanta tarlaları ve puro dumanının yarattığı soylu bir İtalyan rüyası.",
            "mood": "Aristokrat, Sıcak, Büyüleyici, Nezaket Dolu",
            "longevity": "9.5 / 10 (12+ Saat)",
            "sillage": "9.2 / 10 (Görkemli ve zarif iz)",
            "season": "Sonbahar - Kış - İlkbahar",
            "occasion": "Lüks Restoranlar, Tiyatro, Gala Geceleri"
        },
        "notes": {
            "top": ["Bergamot", "Limon", "Akdeniz Lavantası"],
            "heart": ["Organik Bal", "Tarçın", "Kaşmiran", "Yasemin Sambac"],
            "base": ["Tütün Yaprağı", "Tonka Fasulyesi", "Bourbon Vanilya"]
        },
        "prices": [
            {
                "store": "Parfüm Noktası",
                "price": 10400,
                "old_price": 11900,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Sigortalı Kargo",
                "link": "https://www.parfumnoktasi.com/xerjoff-naxos-edp-100ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 11500,
                "old_price": 11500,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Teslim",
                "link": "https://www.sephora.com.tr/p/naxos-100ml"
            },
            {
                "store": "Beymen",
                "price": 11800,
                "old_price": 11800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club",
                "shipping": "Hızlı Kurye",
                "link": "https://www.beymen.com/tr/p_xerjoff-naxos-100ml_98451"
            },
            {
                "store": "Boyner",
                "price": 11900,
                "old_price": 11900,
                "currency": "₺",
                "in_stock": False,
                "is_lowest": False,
                "installment": "Tükendi",
                "shipping": "Stok Bekleniyor",
                "link": "https://www.boyner.com.tr/xerjoff-naxos"
            }
        ]
    },
    {
        "id": "parfums-de-marly-layton",
        "name": "Layton",
        "brand": "Parfums de Marly",
        "concentration": "Eau de Parfum",
        "gender": "Unisex / Erkek Ağırlıklı",
        "category": "Niş / Oryantal Çiçeksi",
        "family": "Vanilyalı Elma / Baharat",
        "image": "https://fimgs.net/mdimg/perfume/375x500.39314.jpg",
        "year": 2016,
        "perfumer": "Hamid Merati-Kashani",
        "trivia": {
            "title": "Fransa Kralı 15. Louis ve Château de Marly Şenlikleri",
            "text": "Parfums de Marly, 18. yüzyılda koku sanatının zirvesi sayılan Fransa Kralı 15. Louis'nin 'La Cour Parfumée' (Kokulu Saray) sarayından ve safkan at sevgisinden doğmuştur. Şişedeki şahlanan kabartma atlar, Kraliyet Harası'ndaki efsanevi safkanları onurlandırır.",
            "highlight": "Elmalı tart ve vanilyayı kraliyet lavantasıyla buluşturan övgü mıknatısı."
        },
        "vibe": {
            "summary": "Mavi kadife ceket, kışlık şık bir davet salonu, tarçınlı sıcak elmalı tatlı ve lüks vanilya aurası. Herkesin 'Ney kokuyorsun?' diyeceği büyü.",
            "mood": "Çekici, Şehvetli, Asil, Gurme",
            "longevity": "9.3 / 10 (11+ Saat)",
            "sillage": "9.1 / 10 (Güçlü yayılım)",
            "season": "Sonbahar - Kış - Serin İlkbahar",
            "occasion": "Randevular, Akşam Partileri, Şık Yemekler"
        },
        "notes": {
            "top": ["Çıtır Elma", "Bergamot", "Lavanta", "Mandalina"],
            "heart": ["Yasemin", "Menekşe", "Sardunya"],
            "base": ["Vanilya", "Kakule", "Sandal Ağacı", "Biber", "Paçuli"]
        },
        "prices": [
            {
                "store": "Parfüm Noktası",
                "price": 10900,
                "old_price": 12500,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.parfumnoktasi.com/pdm-layton-edp-125ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 12100,
                "old_price": 12100,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Teslimat",
                "link": "https://www.sephora.com.tr/p/layton-edp-125ml"
            },
            {
                "store": "Beymen",
                "price": 12300,
                "old_price": 12300,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club",
                "shipping": "Aynı Gün Teslim",
                "link": "https://www.beymen.com/tr/p_pdm-layton-125ml_44912"
            },
            {
                "store": "Boyner",
                "price": 12500,
                "old_price": 12500,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Hopi Puan",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/pdm-layton-edp"
            }
        ]
    },
    {
        "id": "chanel-bleu-de-chanel",
        "name": "Bleu de Chanel",
        "brand": "Chanel Paris",
        "concentration": "Parfum",
        "gender": "Erkek",
        "category": "Designer Lüks / Odunsu Aromatik",
        "family": "Narenciye / Sedir / Sandal Ağacı",
        "image": "https://fimgs.net/mdimg/perfume/375x500.49912.jpg",
        "year": 2018,
        "perfumer": "Olivier Polge",
        "trivia": {
            "title": "Manyetik Kapak ve Derin Gece Mavisi",
            "text": "Bleu de Chanel, özgürlüğünü kendi tanımlayan modern erkeğin manifestosudur. Güneş ışığında kobalt mavisi parlayan, loş ortamda ise siyah gibi görünen şişesi manyetik bir kapağa sahiptir; kapak çevrildiğinde bile Chanel logosu her zaman kusursuzca düz hizalanır.",
            "highlight": "Yeni Kaledonya sandal ağacı ile narenciyenin zamansız centilmen buluşması."
        },
        "vibe": {
            "summary": "Kusursuz ütülenmiş beyaz gömlek, lüks bir saat, Boğaz manzaralı akşam iş yemeği ve temiz, güven veren maskülen bir zarafet.",
            "mood": "Centilmen, Temiz, Prestijli, Çekici",
            "longevity": "9.0 / 10 (10 Saat)",
            "sillage": "8.7 / 10 (Zarif ve saygın)",
            "season": "4 Mevsim",
            "occasion": "Ofis, Toplantı, Özel Yemekler, İmza Kokusu"
        },
        "notes": {
            "top": ["Limon Kabuğu Esansı", "Bergamot", "Taze Nane", "Artemisia"],
            "heart": ["Lavanta", "Sardunya", "Yeşil Notalar", "Ananas"],
            "base": ["Yeni Kaledonya Sandal Ağacı", "Sedir", "Amber Ağacı", "Tonka"]
        },
        "prices": [
            {
                "store": "Sephora Türkiye",
                "price": 6950,
                "old_price": 7500,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.sephora.com.tr/p/bleu-de-chanel-parfum-100ml"
            },
            {
                "store": "Boyner",
                "price": 7100,
                "old_price": 7100,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Hopi Avantajı",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/chanel-bleu-de-chanel-parfum-100ml"
            },
            {
                "store": "Sevil Parfümeri",
                "price": 7200,
                "old_price": 7200,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "6 Taksit",
                "shipping": "Hızlı Kargo",
                "link": "https://www.sevil.com.tr/chanel-bleu-de-chanel-parfum-100ml"
            },
            {
                "store": "Beymen",
                "price": 7350,
                "old_price": 7350,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club",
                "shipping": "VIP Teslimat",
                "link": "https://www.beymen.com/tr/p_chanel-bleu-de-chanel-parfum_128941"
            }
        ]
    },
    {
        "id": "ysl-libre-le-parfum",
        "name": "Libre Le Parfum",
        "brand": "Yves Saint Laurent",
        "concentration": "Parfum",
        "gender": "Kadın / Unisex",
        "category": "Designer Lüks / Baharatlı Çiçeksi",
        "family": "Safran / Lavanta / Portakal Çiçeği / Bal",
        "image": "https://fimgs.net/mdimg/perfume/375x500.75883.jpg",
        "year": 2022,
        "perfumer": "Anne Flipo & Carlos Benaïm",
        "trivia": {
            "title": "Fas Ourika Bahçeleri Safranı ve Altın Cassandra Logosu",
            "text": "Libre serisinin en yoğun ve ateşli üyesidir. Yves Saint Laurent'in Fas Atlas Dağları eteklerindeki Ourika Topluluk Bahçeleri'nde yerel kadınlar tarafından elle toplanan nadide kırmızı safran çiçeğiyle harmanlanmıştır. Şişesindeki altın YSL Cassandra logosu camın kıvrımına göre eğilerek haute couture bir mücevhere dönüştürülmüştür.",
            "highlight": "Kırmızı safran ve balın sıcaklığıyla alevlenen ikonik Fransız lavantası."
        },
        "vibe": {
            "summary": "Sonbahar esintisinde sıcak altın rengi ışıklar, ipek elbise, baharatlı bal ve özgür kadının tavizsiz gücü.",
            "mood": "Özgür, Tutkulu, Parlak, Sıcak",
            "longevity": "9.4 / 10 (11 Saat)",
            "sillage": "9.0 / 10 (Göz kamaştırıcı yayılım)",
            "season": "Sonbahar - Kış",
            "occasion": "Özel Davetler, Akşam Yemekleri, Gece Kulübü"
        },
        "notes": {
            "top": ["Zencefil", "Fas Safranı", "Mandalina", "Bergamot"],
            "heart": ["Portakal Çiçeği", "Fransız Lavantası"],
            "base": ["Bourbon Vanilya", "Organik Bal", "Tonka Fasulyesi", "Vetiver"]
        },
        "prices": [
            {
                "store": "Boyner",
                "price": 6100,
                "old_price": 6800,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": True,
                "installment": "Hopi İndirimi",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.boyner.com.tr/ysl-libre-le-parfum-50ml"
            },
            {
                "store": "Sephora Türkiye",
                "price": 6350,
                "old_price": 6350,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "3 Taksit",
                "shipping": "Ücretsiz Kargo",
                "link": "https://www.sephora.com.tr/p/libre-le-parfum-50ml"
            },
            {
                "store": "Sevil Parfümeri",
                "price": 6400,
                "old_price": 6400,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "6 Taksit",
                "shipping": "Hızlı Kargo",
                "link": "https://www.sevil.com.tr/ysl-libre-le-parfum"
            },
            {
                "store": "Beymen",
                "price": 6500,
                "old_price": 6500,
                "currency": "₺",
                "in_stock": True,
                "is_lowest": False,
                "installment": "Beymen Club",
                "shipping": "Özel Kurye",
                "link": "https://www.beymen.com/tr/p_ysl-libre-le-parfum_912384"
            }
        ]
    }
]

class PerfumeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/perfumes":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(PERFUMES_DATA, ensure_ascii=False).encode("utf-8"))
            return

        if path.startswith("/api/perfumes/"):
            perfume_id = path.split("/api/perfumes/")[1].strip("/")
            perfume = next((p for p in PERFUMES_DATA if p["id"] == perfume_id), None)
            if perfume:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(perfume, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Parfüm bulunamadı"}).encode("utf-8"))
            return

        if path == "/api/stores":
            stores = [
                {"name": "Beymen", "logo": "🛍️", "domain": "beymen.com", "badge": "Lüks Niş Distribütör"},
                {"name": "Sephora Türkiye", "logo": "🖤", "domain": "sephora.com.tr", "badge": "Resmi Distribütör"},
                {"name": "Boyner", "logo": "🟡", "domain": "boyner.com.tr", "badge": "Hopi / Taksit Avantajı"},
                {"name": "Sevil Parfümeri", "logo": "✨", "domain": "sevil.com.tr", "badge": "Köklü Parfümeri"},
                {"name": "Parfüm Noktası", "logo": "💎", "domain": "parfumnoktasi.com", "badge": "En İyi Fiyat Garantisi"}
            ]
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(stores, ensure_ascii=False).encode("utf-8"))
            return

        if path == "/api/search":
            query_params = urllib.parse.parse_qs(parsed.query)
            q = query_params.get("q", [""])[0].lower().strip()
            category = query_params.get("category", [""])[0].lower().strip()

            filtered = PERFUMES_DATA
            if q:
                filtered = [
                    p for p in filtered
                    if q in p["name"].lower() or q in p["brand"].lower() or any(q in n.lower() for n in p["notes"]["top"] + p["notes"]["heart"] + p["notes"]["base"]) or q in p["vibe"]["summary"].lower()
                ]
            if category and category != "tümü":
                filtered = [p for p in filtered if category in p["category"].lower() or category in p["family"].lower()]

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(filtered, ensure_ascii=False).encode("utf-8"))
            return

        # Fallback to standard static file serving (index.html, styles.css, app.js)
        return super().do_GET()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PerfumeRequestHandler) as httpd:
        print(f"======================================================")
        print(f" ✨ SILLAGE / AURA PARFÜM SUNUCUSU ÇALIŞIYOR!")
        print(f" 🌐 Localhost adresi: http://localhost:{PORT}")
        print(f" 💻 Safari / MacBook Uyumlu Açık & Liquid Glass Tema")
        print(f" 📡 Canlı API Endpoint: http://localhost:{PORT}/api/perfumes")
        print(f"======================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu kapatıldı.")

if __name__ == "__main__":
    run_server()
