#!/usr/bin/env python
#
# Türkçe dökümanlar için çalışma öncesi dökümanı işlenecek hale getirir.
#   Döküman listesinin birleştirilmesi, noktalama işaretlerinin kaldırılması,istenmeyen karakterlerin dökümandan silinmesi,
#   Türkçe de kullanılan şapkalı karakterlerin karlığı ile değiştirilmesi, stopwordlerin ve stemwordlerin filtrelenmesi
#   gibi işlemleri gerçekleştirir. Hazırlanan kütüphane özellikle Türkçe dildeki dökümanlara yönelik hazırlanmıştır.
#   Özellikle Türkçe dökümanların ön işlem süreçlerindeki problemlerin çözülmesi hedeflenmiştir.
#
# Author: Necmettin Çarkacı
#
# E-mail: necmettin [ . ] carkaci [ @ ] gmail [ . ] com
#
# Usage : preprocessing.py dataset
#   dataset : file or directory


import os # To walk directory
import sys # To get parameter from command line


def mergeFiles(dirname, ext='.txt'):
    '''
        Verilen klasör içindeki dosyaları ardı ardına birleştirerek tek bir dosya haline getirir.

        @param  string dirname  : Klasör adı
        @param  string ext      : Klasör içinde birleştirilmesi istenen dosyaların uzantısı örn: .txt
        @result string          : Birleştirme sonucu elde edilen dosyanın adı
    '''

    print('Dosyaları birleştiriyor ...')
    filename = dirname + '_dataset.txt'
    with open(filename, 'w') as output_file:
        for root, dirs, files in os.walk(dirname):
            for file in files:
                if file.endswith(ext):
                    with open(os.path.join(root, file), 'r') as input_file:
                        content = input_file.read()
                    output_file.write(content)

    return filename



def getCharset(text):
    '''
        text içinde kullanılan tekil karakter listesi geri döndürür.

        @param  string text : Döküman içeriği
        @return list        : Karakter listesi
    '''

    # create mapping of unique chars to integers
    unique_chars = sorted(list(set(text)))
    print('Kullanılan karakterler : '+str(unique_chars))

    return unique_chars


def removePunction(text):
    '''
        Döküman içerisindeki noktalama işaretlerini kaldırır.

        @param  string text : Döküman içeriği
        @return string      : Noktalama işaretleri kaldırılmış text
    '''

    print ('Noktalama işaretlerini kaldırıyor ...')
    from string import punctuation
    text = ''.join([c for c in text if c not in punctuation])

    return text


def replaceChars(text):
    '''
        Döküman içerisinde şapkalı kararkterleri eşleniği ile değiştirir.

        @param  string  text        : Döküman içeriği
        @param  dict    char_dict   : Değişim yapılacak anahtar ve değer sözlüğü
        @return string              : Karakterleri değiştirilmiş döküman içeriği
    '''

    print('Şapkalı karakterleri eşleniği ile değiştiriyor ...')
    import re
    text = re.sub(r"Â", "A", text)
    text = re.sub(r"â", "a", text)
    text = re.sub(r"Î", "I", text)
    text = re.sub(r"î", "ı", text)
    text = re.sub(r"Û", "U", text)
    text = re.sub(r"û", "u", text)

    return text


def toLowercase(text):
    '''
        Dökümandaki tüm büyük harfleri küçük harf dönüştürür. Python lower() fonksiyonu I harfini
        i'ye dönüştürdüğü için bu işlem regex'le yapıldı. Diğer dönüşümler için python'un varsayılan
        lower() fonksiyonu kullanıldı.

        @param string text  : Döküman içeriği
        @return             : Tüm karakterleri küçük harfe dönüştürülmüş döküman içeriği
    '''

    print ('Tüm karakterler küçük harfe dönüştürülüyor ...')
    import re
    text = re.sub(r"I", "ı", text)
    text = text.lower()

    return text


def removeNewLine(text):
    '''
        Dökümanda bulunan yeni satırları kaldırır. Dökümanda yeni satırlar silindiğinde alt satırdaki kelimeler,
        üst satırdaki kelimelerle birleştiği için. Yeni satır silinmesi işlemi; yeni satırların önce çift boşluğa
        dönüştürülüp, daha sonra çift boşlukşların tek boşluğa dönüştürülmesiyle yapılır.

        @param string text  : Döküman içeriği
        @return             : Dökümanda bulunun yeni satırların kaldırılmış hali
    '''

    print('Dökümanda bulunan yeni satırları kaldırılıyor ...')
    import re
    text = re.sub(r"\n", "  ", text)
    text = re.sub(r"  ", " ", text)

    return text



def removeUndesiredCharsFromText(text,alfabe ='ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZabcçdefgğhıijklmnoöprsştuüvyz0123456789 '+'\n'):
    '''
        Döküman içinden alfabede olmayan karakterleri siler. Varsayılan alfabe Türkçe alfabedir.

        @param  string  text            : Döküman içeriği
        @param  string  alfabe          : Silinmeden kalması istenen karakter listesi
        @return string                  : İstenmeyen karakterlerin temizlendiği text dökümanı döndürür.
    '''

    print ('Belirtilen alfabede olmayan tüm karakterleri kaldırıyor ...')

    cleaned_text = ''
    for char in text:
        if char in alfabe:
            cleaned_text = cleaned_text + char

    return cleaned_text


def getStatistics(text):
    '''
        Döküman içindeki kelime ve karakterlere ait istatistiki bilgileri hesaplar.
        Hesaplanan veriler tekil ve toplam, karakter sayısı ile toplam ve tekil kelime sayısıdır.

        @param  string text : Döküman içeriği
        @return int         : Dökümandaki toplam karakter sayısı
        @return int         : Dökümandaki tekil karakter sayısı
        @return int         : Dökümandaki toplam kelime sayısı
        @return int         : Dökümandaki tekil karakter sayısı
    '''
    print ('Dökümana ait bazı istatistiki bilgiler hesaplanıyor ...')
    number_of_chars         = len(text)
    number_of_uniqueu_chars = len(set(text))
    word_list               = text.split()
    number_of_vocab         = len(word_list)
    unique_vocab            = sorted(list(set(word_list)))
    number_of_uniqueu_vocab = len(unique_vocab)

    print ("Dökümandaki toplam karakter sayısı : ", number_of_chars)
    print ("Dökümandaki tekil karakter sayısı : ", number_of_uniqueu_chars)
    print ("Dökümandaki toplam kelime sayısı : ", number_of_vocab)
    print ("Dökümandaki tekil kelime sayısı : ", number_of_uniqueu_vocab)

    return number_of_chars, number_of_uniqueu_chars, number_of_vocab, number_of_uniqueu_vocab



def getWordFrequency(text):
    '''
        Döküman içindeki kelimeler için kelime ve kelimeye ait terim frekans değerinden oluşan sözlük oluşturur.

        @param  string text : Döküman içeriği
        @return dict        : Kelime ve kelimeye ait terim frekans değeri içeren sözlük
    '''

    # Dökümandaki her kelimeyi listeye at
    text = text.split()

    # Değişkenleri başlat
    word_frequency_dict = {}

    # Kelimeler için terim frekans değeri hesapla
    for word in text:
        if word in word_frequency_dict.keys():
            word_frequency_dict[word] += 1
        else :
            word_frequency_dict[word] = 1

    # Terim frekans değeri sözlüğünü frekans değerine (value) göre sırala
    import operator
    ordered_word_frequency_dict = sorted(word_frequency_dict.items(), key=operator.itemgetter(1), reverse=True)

    return ordered_word_frequency_dict


def isStopword(stopword_canditate, text, percentage):
    '''
        Text içindeki tüm kelimelerin dökümanda kaç kez geçtiğini hesaplar. Daha sonra bu değerleri
        frekans değerine göre sıralar. Sıralanan bu kelimeler içinden frekans sıklığına göre belirtilen
        belirtilen yüzde kadarı alınır. Verilen stopword bu yüzdelik dilimdeki kelimeler içinde varsa stopword olarak değerlendirilir.

        @param  string  stopword    : Stopword olup olmadığı değerlendirilmek istenen kelime
        @param  string  text        : Döküman içeriği
        @param  int     percentage  : Stopword kontrolü için dökümanın içinde en sık geçen kelimelerin yüzde kaçına bakılacağı
        @return boolean             : Kelimenin stopword olup, olmadığı; stopword ise True, değilse False
    '''

    word_frequencies = getWordFrequency(text)

    # Stopword en sık geçen kelimeler listesinde belirtilen yüzdelik dilimde mi kontrol et.
    # Eğer bu yüzdelik dilimdeyse stopword olarak değerlendir.
    limit = int((len(word_frequencies) / 100) * percentage)  # %percentage'unu bul
    most_used_words = word_frequencies[0:limit]  # En sık kullanılan %percentage kelime.
    most_used_words = dict(most_used_words)

    if stopword_canditate in most_used_words.keys():
        return True
    else:
        return False


def isStopwordInFrequencyList(stopword_canditate, word_frequencies, percentage):
    '''
        Verilen stopword belirtilen yüzdelik dilimdeki kelimeler içinde varsa stopword olarak değerlendirilir.

        @param  string  stopword_canditate  : Stopword olup olmadığı değerlendirilmek istenen kelime
        @param  string  word_frequencies    : Dökümanda geçen kelimelerin terim frekans sözlüğü
        @param  int     percentage          : Stopword kontrolü için dökümanın içinde en sık geçen kelimelerin yüzde kaçına bakılacağı
        @return boolean                     : Kelimenin stopword olup, olmadığı; stopword ise True, değilse False
    '''

    # Stopword en sık geçen kelimeler listesinde belirtilen yüzdelik dilimde mi kontrol et.
    # Eğer bu yüzdelik dilimdeyse stopword olarak değerlendir.
    limit = int((len(word_frequencies) / 100) * percentage)  # %percentage'unu bul
    most_used_words = word_frequencies[0:limit]  # En sık kullanılan %percentage kelime.
    most_used_words = dict(most_used_words)

    if stopword_canditate in most_used_words.keys():
        return True
    else:
        return False


def filterStopwordsForFrequency(stopwordList, text, percentage=10):
    '''
        Stopword listesinde belirtilen kelimelerin gerçekten stopword olup olmadığını kontrol eder.
        Eğer kelimeler döküman içindeki frekansı, büyükten küçüğe doğru frekans değerine göre sıralanmış kelime listesinde
        yoksa stopword olarak değerlendirilen kelimenin değerli bir kelime olabileceğini düşünerek bu kelimeyi stopword
        listesinden çıkarır. Böylece filtrelenmiş yeni stopword listesini geri döndürür.

        @param  list    stopwordList    : Stopwordleri içeren liste.
        @param  string  text            : Döküman içeriği
        @param  int     percentage      : Stopword kontrolü için dökümanın içinde en sık geçen kelimelerin yüzde kaçına bakılacağı
        @return list                    : Filtrelenmiş stopword listesi
    '''

    print ('Stopword listesini filtreliyor ...')

    # Değişkenleri başlat
    validated_stopwords = []

    # Kelime sıklığı listesini oluştur
    word_frequencies = getWordFrequency(text)

    for stopword_canditate in stopwordList:
        if isStopwordInFrequencyList(stopword_canditate, word_frequencies, percentage):
            validated_stopwords.append(stopword_canditate)

    print('Stopword listesinden çıkarılan kelimeler : \n',(set(stopwordList) - set(validated_stopwords)))
    return validated_stopwords



def removeStopwords(text, stop_words_filename='', check_is_stopword = True, percentage=10):
    '''
        Verilen text içinde eğer stopwordsler en sık karakterlerin yer aldığı belirtilen yüzdelik dilimdeyse
        döküman içinden silinir.

        @param  string  text            : Döküman içeriği
        @param  string  text            : Stopwords dosya adı. Eğer boş bırakılırsa Türkçe için varsayılan stopwords dosyası kullanılacaktır.
        @param  boolean check_frequency : stopwordsler verilen döküman içinde en fazla kullanılan ilk 10.000 kelime arasında mı kontrol et.
                                            Varsayılan değer False.
        @return string                  : stop wrodsler temizlenmiş döküman içeriği
    '''

    print ('Stopwordleri kaldırıyor ...')

    if stop_words_filename == '':
        stop_words_filename = 'turkce-stop-words.txt'

    if  not os.path.exists(stop_words_filename):
        print('Belirtilen '+stop_words_filename+' isimli dosya bulunamadı. Stopwrodler temizlenemedi.')
        return text
    else:
        with open(stop_words_filename, 'r') as stopwords_file:
            stopwords = stopwords_file.read().split()

        if check_is_stopword :
            stopwords = filterStopwordsForFrequency(stopwords, text, percentage)

        text = text.split()
        text = [w for w in text if not w in stopwords]
        text = " ".join(item for item in text)

        return text



def wordsToStems(text):
    '''
        Dökümanda bulunan kelimeleri köklerine ayırır.

        # TODO: Zemberek projesi kullanılarak kelimeler kökleri çıkarılacak
    '''

    print ('Stemwordleri kaldırıyor \n TODO: Zemberek projesi kullanılarak kelimeler kökleri çıkarılacak')
    # TODO: Zemberek projesi kullanılarak kelimeler kökleri çıkarılacak

    return text


def turnTextToLine(text):
    '''
        Boşlukları ve yeni satırları kaldırarak dökümanı tek bir satıra dönüştürür.

        @param string text  : Döküman içeriği
        @return             : Tek satır halinde döküman içeriği
    '''

    text = text.split()
    text = " ".join(item for item in text)

    return text


def preprocessing(dataset,
                  stopwords_filename = '',
                  to_lowercase      = True,
                  replace_char      = True,
                  remove_punction   = True,
                  remove_stopwords  = False,
                  check_is_stopword = True,
                  word_to_stem      = False,
                  remove_digits     = False,
                  remove_space      = False,
                  remove_newline    = False,
                  text_to_line      = False,
                  print_statistics  = True):
    '''
        Verilen dosyayı kullanmadan önce ön işlemye tabi tutar. Dosya içindeki karakterleri hepsini küçük harf dönüştürür,
        noktalama işaretlerini kaldırır, şapkalı karakterleri eşlenikleriyle değiştirir, stopwords kaldırır,
        alfabe dışındaki, sayı, boşluk dışındaki karakterleri kaldırır. İlgili karaterlerin kaldırılması isteniyorsa
        fonksiyona ait varsayılan parametreler üzerinden değiştirilebilir.

        @param  string   dataset             : Verilerin bulunduğu veriseti. Eğer klasör ise klasör alındaki tüm dosyaları birleştirerek, tek bir veri seti dosyası
                                                oluşturup işler. Tek dosya ise onu veri dosyası olarak kullanır.
        @param  string   stopwords_filename  : Stopwords kelimelerinin olduğu dosya. Varsayılan dosya kullanılmak isteniyorsa parametre boş bırakılmalıdır.
        @param  boolean  to_lowercase        : Karakterlerin tümü küçük harfe dönüştürülsün mü? Varsayılan değer True
        @param  boolean  replace_char        : Şapkalı karakterler eşleneğine döünüştürülsün mü? Varsayılan değer True
        @param  boolean  remove_punction     : Noktalama işaretleri silinsin mi? Varsayılan değer True
        @param  boolean  remove_stopwords    : Stopwordsler silinsin mi? Varsayılan değer False
        @param  boolean  check_is_stopword   : Stopwordsler silinmeden önce en sık kullanılan 10.000 kelime içinde mi kontrol edilsin mi? Varsayılan değer True
        @param  boolean  word_to_stem        : Stemwordsler silinsin mi? Varsayılan değer False
        @param  boolean  remove_digits       : Rakamsal veriler silinsin mi? Varsayılan değer False
        @param  boolean  remove_space        : Boşluklar silinsin mi? Varsayılan değer False
        @param  boolean  remove_newline      : Alta satır geçişleri silinsi mi? Varsayılan değer False
        @param  boolean  remove_newline      : Döküman tek bir satıra dönüştürülsün mü? Varsayılan değer False
        @param  boolean  print_statistics    : Karakter, kelime sayısı gibi istatistiki veriler yazdırılsın mı? Varsayılan değer True
        @return string                       : Ön işlemden geçirilmiş döküman içeriğini geri döndürür. Aynı zamanda bu içeriği bir dosyaya yazarak kaydeder.
    '''

    # Dosya adı klasör ise belirtilen klasördeki tüm dosyaları birleştir
    if os.path.isdir(dataset):
        dataset_filename = mergeFiles(dataset)
    else :
        dataset_filename = dataset

    # Dosyanın içeriğini oku
    with open(dataset_filename,'r') as input_file:
        text = input_file.read()

    # Toplam kelime ve harf sayısını hesapla
    if print_statistics :
        print('\n Preprocessing öncesi istatistik')
        getStatistics(text)

    # Şapkalı harfleri şapkasızlarıyla değiştir
    if replace_char :
        text = replaceChars(text)

    # Hepsini küçük harfe dönüştür
    if to_lowercase:
        text = toLowercase(text)

    # Noktalamala işaretlerini dökümandan kaldır
    if remove_punction:
        text = removePunction(text)

    # Yeni satırları kaldırıyor
    if remove_newline:
        text = removeNewLine(text)

    # Text'den aşağıdaki karakterler dışındaki karakterleri temizle; boşluk, alfabe, sayı ve yeni satır kalsın.
    alfabe = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZabcçdefgğhıijklmnoöprsştuüvyz0123456789 '+'\n'
    text = removeUndesiredCharsFromText(text, alfabe)

    # Stop wordleri kaldır
    if remove_stopwords:
        text = removeStopwords(text, stopwords_filename, check_is_stopword)

    # Kelimelerin köklerini al
    if word_to_stem:
        text = wordsToStems(text)

    # Dökümanı tek satıra dönüştür
    if text_to_line:
        text = turnTextToLine(text)

    # Temizlenmiş dosyayı kaydet
    filename = 'cleaned_'+dataset_filename
    with open(filename,'w') as output_file:
        output_file.write(text)

    # Toplam kelime ve harf sayısını hesapla
    if print_statistics :
        print('\n Preprocessing sonrası istatistik')
        getStatistics(text)

    return text

if __name__ == '__main__':

    if len(sys.argv) > 1:
        dataset = sys.argv[1]
        preprocessing(dataset)
    else :
        print(' Usage : preprocessing.py dataset \n dataset : file or directory')


