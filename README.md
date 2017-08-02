# tr-preprocessing
Türkçe metinler için metin ön işleme kütüphanesi; küçük harfe dönüştürme, şapkalı karakterleri eşleniği il değiştirme, stopwords'leri çıkarma, noktalama işaretlerini kaldırma, stopwords'ün geçerliliğini kontrol etme, klasör altındaki birden çok dosyayı birleştirip aynı anda işleme, rakamları, boşlukşarı, yeni satırları kaldırma yada olduğu gibi bıırakma gibi metin işleme de ihtiyaç duyulan işlemleri  yapılabileceği python kütüphanesi.

Genelde makine öğrenmesi çalışmalarında veriler toplandıktan sonra çalışma öncesinde ön işleme tabi tutulurlar. Bu işlemde Türkçe karakterler ile ilgili problemler yaşanabilmektedir. Geliştirilen kütüphanede tüm işlemleri tek bir kütüphane altında toplanmıştır.

## Stopword'lerin değerlendirilmesi

Genel de makine öğrenmesi yöntemlerinde dilde çokça bulunan kelime ve bağlaçlar zaman zaman öğrenme başarımını düşürmektedir. Bu amaçla bazı çalışmalarda bu kelimeler dökümanda çıkarılmaktadır. Bu amaçla geliştirilmiş Türkçe için birden fazla stopword listesi bulanabilir. Bununla birlikte geliştirilen kütüphanede bu stopword listelerinde kelimelerin gerçekten stopword olup olnmadığını kontrol etmektedir. Kontrol işlemini dökümanda geçen kelimelerin frekans değerleri hesaplayarak yapar. Hesapladığı frekans değerlerinden parametre olarak belirtilen yüzde kadarını büyükten küçüğe alır ve ilgili stopwordlerin bu liste de olup olmadığını kontrol eder. Eğer değilse stopwrod dışında tutulur. Bu özellik seçmelidir. İstenilse devre dışı bırakılabilir. Yüzdelik değer için varsayılan parametre %10 olarak kullanılmıştır. Bunun için yapılmış bir çalışma yoktur. Sezgisel olarak belirlenmiştir.

