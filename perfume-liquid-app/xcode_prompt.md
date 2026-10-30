# Sillage TR - Xcode AI İçin Kapsamlı Türkçe Geliştirme Promptu

Bu promptu Xcode AI (Apple Intelligence / Copilot / Cursor) ortamına doğrudan yapıştırarak eksiksiz, derlenebilir bir SwiftUI iOS ve macOS (Catalyst) uygulaması üretebilirsin.

---

```markdown
Sen kıdemli bir Apple platformları (iOS 18+, macOS 15+, SwiftUI 6, Swift 6) yazılım mimarısın. 
Bana "Sillage TR" adında, dünyaca ünlü ve Türkiye'de satılan bütün parfümleri içeren, şişe tarihçeleri ve anekdotları barındıran, koku "vibe" analizleri sunan ve Türkiye'deki mağazalar arasında yerel fiyat karşılaştırması yapan lüks bir mobil uygulama geliştireceksin.

### 1. UYGULAMA VİZYONU & TEMA (LIQUID GLASS & AYDINLIK KREM/BEYAZ)
- **Tasarım Dili:** Apple'ın en yeni Liquid Glass (Akışkan Cam) estetiği.
- **Renk Paleti:** Açık tema; saf beyaz ve sıcak fildişi/kremimsi arka planlar (`Color(hex: "FAF8F5")`, `Color(hex: "FFFDF9")`), şampanya altını vurgular (`Color(hex: "C5A059")`) ve derin sıcak antrasit tipografi (`Color(hex: "1C1917")`).
- **Cam Efektleri:** `.background(.ultraThinMaterial)`, `.glassBackgroundEffect()` (iOS 18+), kenarlarda ince beyaz parlama (`border(Color.white.opacity(0.85))`), yumuşak çok katmanlı gölgeler.
- **MacBook & iPad Uyumluluğu:** Uygulama `NavigationSplitView` ile hem iPhone hem de MacBook (Mac Catalyst / Designed for iPad) ekranlarında akıcı ve tam uyumlu çalışmalıdır.

---

### 2. TEMEL ÖZELLİKLER & GEREKSİNİMLER

#### A. Parfüm Ansiklopedisi & Görseller
- Gerçek online CDN'lerden çekilen yüksek çözünürlüklü parfüm şişesi görselleri (`AsyncImage` ile zarif shimmer/iskelet yükleme durumu).
- Koku piramidi: Üst Notalar (Top), Kalp Notalar (Heart), Dip Notalar (Base).
- Konsantrasyon (Extrait de Parfum, Eau de Parfum, Eau de Toilette) ve Cinsiyet rozetleri.

#### B. Şişe Tasarımı ve Tarihçe Anekdotları (Trivia & Lore)
- Her parfümün mutlaka özel bir tarihçe veya şişe tasarım hikayesi olmalıdır.
- **Örnek 1 (Kilian - Angels' Share):** Şişesinin ağır art-deco bir viski kadehini andırması; Kilian Hennessy'nin dünyaca ünlü Hennessy konyak hanedanlığının 8. kuşak doğrudan varisi olması ve meşe fıçılarda konyak yıllandırılırken havaya karışan %2'lik buhara 'Meleklerin Payı' (Angels' Share) denmesi hikayesi.
- **Örnek 2 (Maison Francis Kurkdjian - Baccarat Rouge 540):** 540 sayısının Baccarat kristaline imza kırmızılığını vermek için 24 ayar altın tozuyla 540°C fırında eritilmesinden gelmesi.
- **Örnek 3 (Creed - Aventus):** Şişesindeki şahlanan gümüş at ve binicinin İmparator Napolyon'un askeri zaferlerini simgelemesi.

#### C. Parfümün Vibe'ı ve Hissiyat Analizi
- **Vibe Özeti:** Kokunun kişiye ve ortama kattığı atmosfer (Örn: "Karlı bir kış gecesinde loş ışıklı gizli bir speakeasy caz barda, elde bir kadeh yıllanmış konyak ve sıcak tarçınlı elmalı turta hissi").
- **Metrikler:** Kalıcılık (Longevity) skoru, Yayılım / Silaj (Sillage) skoru, Mevsim tercihi (Kış, Sonbahar vb.), Kullanım Ortamı (Randevu, Ofis, Gece Kulübü, Gala).

#### D. Türkiye Yerel Fiyat Karşılaştırması (Online & Canlı)
- Türkiye'deki başlıca parfüm satıcılarının fiyatlarını anlık karşılaştır:
  - **Beymen** (Niş distribütör fiyatı & hızlı teslimat)
  - **Sephora Türkiye** (Resmi distribütör & mağaza teslim)
  - **Boyner** (Hopi paracık & taksit avantajı)
  - **Sevil Parfümeri** (Köklü parfümeri ağı)
  - **Parfüm Noktası** (En iyi fiyat garantisi & indirim)
- En ucuz mağazaya "En Avantajlı Fiyat" yeşil rozeti ekle.
- Mağazalar arasındaki fiyat farkını ve toplam tasarruf tutarını (Örn: "1.600 ₺ Tasarruf") hesapla.
- Her mağaza için `Link(destination:)` veya Safari In-App Browser (`SFSafariViewController`) ile doğrudan satın alma bağlantısı sağla.

---

### 3. TEKNİK MİMARİ & KOD YAPISI (SWIFTUI)

Lütfen aşağıdaki modülleri içeren eksiksiz Swift kodlarını oluştur:

#### 1. Veri Modelleri (`Models/Perfume.swift`):
```swift
import Foundation

struct Perfume: Identifiable, Codable, Hashable {
    let id: String
    let name: String
    let brand: String
    let concentration: String
    let category: String
    let family: String
    let imageURL: URL
    let year: Int
    let perfumer: String
    let trivia: PerfumeTrivia
    let vibe: PerfumeVibe
    let notes: FragrancePyramid
    let prices: [StorePrice]

    var lowestPrice: StorePrice? {
        prices.filter { $0.inStock }.min(by: { $0.price < $1.price })
    }
    
    var highestPrice: StorePrice? {
        prices.filter { $0.inStock }.max(by: { $0.price < $1.price })
    }
    
    var maxSavings: Double {
        guard let low = lowestPrice?.price, let high = highestPrice?.price, high > low else { return 0 }
        return high - low
    }
}

struct PerfumeTrivia: Codable, Hashable {
    let title: String
    let text: String
    let highlight: String
}

struct PerfumeVibe: Codable, Hashable {
    let summary: String
    let mood: String
    let longevity: String
    let sillage: String
    let season: String
    let occasion: String
}

struct FragrancePyramid: Codable, Hashable {
    let top: [String]
    let heart: [String]
    let base: [String]
}

struct StorePrice: Identifiable, Codable, Hashable {
    var id: String { storeName }
    let storeName: String
    let price: Double
    let oldPrice: Double?
    let currency: String
    let inStock: Bool
    let installmentInfo: String
    let shippingInfo: String
    let productURL: URL
}
```

#### 2. Liquid Glass Görünüm Değiştiricileri (`ViewModifiers/LiquidGlass.swift`):
- Krem zemin üzerinde akışkan cam kart stili:
```swift
struct LiquidGlassCardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .background(
                RoundedRectangle(cornerRadius: 24, style: .continuous)
                    .fill(Color.white.opacity(0.68))
                    .background(
                        RoundedRectangle(cornerRadius: 24, style: .continuous)
                            .fill(.ultraThinMaterial)
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 24, style: .continuous)
                    .stroke(
                        LinearGradient(
                            colors: [Color.white.opacity(0.95), Color.white.opacity(0.3)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1.2
                    )
            )
            .shadow(color: Color(red: 0.65, green: 0.58, blue: 0.50).opacity(0.12), radius: 18, x: 0, y: 8)
    }
}
```

#### 3. Ana Görünüm & SplitView (`Views/MainPerfumeCatalogView.swift`):
- MacBook ve iPad'de çift sütunlu `NavigationSplitView`.
- Arama Çubuğu (`.searchable`) ve Kategori Seçim Kapsülleri (Niş, Designer, Sıcak Gurme, Narenciye vb.).
- Detay Sayfası (`PerfumeDetailView.swift`):
  - Şişe görseli ve cam ışıltısı efekti.
  - "Şişe & Tarihçe Hikayesi (Trivia)" kutusu.
  - "Vibe & Aura" metreleri.
  - "Türkiye Mağazaları Canlı Karşılaştırma" listesi ve tek tıkla satın alma yönlendirmesi.

Lütfen bu yapıyı derlenebilir, modern Swift 6 kurallarına uygun ve Xcode Previews destekli olarak oluştur.
```
