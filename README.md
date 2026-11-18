\# S3 Public Access Auditor



A Python tool that checks the S3 buckets in your AWS account for public access and reports the risky ones. It uses \*\*boto3\*\*, the AWS SDK for Python.



\## Features



\- Lists all S3 buckets in the account

\- Checks each bucket's \*\*Public Access Block\*\* settings

\- Checks whether the \*\*bucket policy\*\* allows public access

\- Checks whether the \*\*bucket ACL\*\* grants access to everyone

\- Prints the risky buckets and their reasons to the console

\- Saves the results to a JSON file

\- Unit tests that run without connecting to AWS



\## Risk Criteria



A bucket is marked as \*\*risky\*\* if at least one of the following is true:



| Check | Risk condition |

|-------|----------------|

| Public Access Block | Any of the four settings is off, or no settings exist at all |

| Bucket policy | The policy status reports `IsPublic: true` |

| Bucket ACL | A grant is given to `AllUsers` or `AuthenticatedUsers` |



A bucket with all four Public Access Block settings enabled, no public policy, and no public ACL grants is considered safe.



\## Requirements



\- Python 3.10 or newer

\- AWS CLI

\- An IAM user with S3 read permissions (`AmazonS3ReadOnlyAccess`)



\## Installation



1\. Install the required libraries:



```

py -m pip install boto3 pytest

```



2\. Configure your AWS credentials:



```

aws configure

```



The credentials are stored in your local AWS configuration folder, never in this project.



\## Usage



Run the audit from the project folder:



```

py src\\s3\_denetci.py

```



Custom output file:



```

py src\\s3\_denetci.py --cikti rapor.json

```



Example console output:



```

RİSKLİ: my-test-bucket

&#x20; - Public Access Block kapalı: BlockPublicAcls, IgnorePublicAcls

&#x20; - Bucket policy herkese açık

2 riskli bucket bulundu, 'riskli\_bucketlar.json' dosyasına yazıldı.

```



\## Running Tests



```

py -m pytest

```



The tests check the risk rules with sample data. They do not connect to AWS, so they run without any cost.



\## Error Handling



| Situation | Message |

|-----------|---------|

| No credentials configured | Suggests running `aws configure` |

| Missing S3 read permission | Suggests checking the IAM policy |

| Other AWS errors | Shows the AWS error code |



\## Security



\- Credentials are never written in the code or committed to Git.

\- `.gitignore` excludes JSON and CSV output files, `.env`, `credentials`, `\*.pem`, and `\*.tfstate`.

\- The tool only reads bucket settings. It does not change or delete anything.



\## Project Structure



```

s3-public-access-auditor/

├── README.md

├── .gitignore

├── src/

│   └── s3\_denetci.py

└── tests/

&#x20;   └── test\_s3\_denetci.py

```



\---



\# S3 Public Access Auditor (Türkçe)



Bu Python aracı, AWS hesabınızdaki S3 bucket'larını public erişim açısından kontrol eder ve riskli olanları raporlar. \*\*boto3\*\* kütüphanesini (Python için AWS SDK) kullanır.



\## Özellikler



\- Hesaptaki tüm S3 bucket'larını listeler

\- Her bucket'ın \*\*Public Access Block\*\* ayarlarını kontrol eder

\- \*\*Bucket policy\*\*'nin herkese açık erişime izin verip vermediğini kontrol eder

\- \*\*Bucket ACL\*\*'in herkese izin verip vermediğini kontrol eder

\- Riskli bucket'ları ve nedenlerini ekrana yazdırır

\- Sonuçları bir JSON dosyasına kaydeder

\- AWS'ye bağlanmadan çalışan birim testleri içerir



\## Risk Kriterleri



Bir bucket, aşağıdakilerden en az biri doğruysa \*\*riskli\*\* kabul edilir:



| Kontrol | Risk koşulu |

|---------|-------------|

| Public Access Block | Dört ayardan herhangi biri kapalıysa ya da hiç ayar yoksa |

| Bucket policy | Policy durumu `IsPublic: true` ise |

| Bucket ACL | Bir izin `AllUsers` ya da `AuthenticatedUsers` grubuna verilmişse |



Dört Public Access Block ayarı da açık, herkese açık policy yok ve herkese açık ACL izni yoksa bucket güvenli kabul edilir.



\## Gereksinimler



\- Python 3.10 veya üstü

\- AWS CLI

\- S3 okuma yetkisi olan bir IAM kullanıcısı (`AmazonS3ReadOnlyAccess`)



\## Kurulum



1\. Gerekli kütüphaneleri kurun:



```

py -m pip install boto3 pytest

```



2\. AWS kimlik bilgilerinizi yapılandırın:



```

aws configure

```



Bilgiler bilgisayarınızdaki AWS yapılandırma klasöründe saklanır, bu projede değil.



\## Kullanım



Denetimi proje klasöründen çalıştırın:



```

py src\\s3\_denetci.py

```



Farklı bir çıktı dosyası için:



```

py src\\s3\_denetci.py --cikti rapor.json

```



Örnek terminal çıktısı:



```

RİSKLİ: my-test-bucket

&#x20; - Public Access Block kapalı: BlockPublicAcls, IgnorePublicAcls

&#x20; - Bucket policy herkese açık

2 riskli bucket bulundu, 'riskli\_bucketlar.json' dosyasına yazıldı.

```



\## Testleri Çalıştırma



```

py -m pytest

```



Testler risk kurallarını örnek verilerle kontrol eder. AWS'ye bağlanmazlar, bu yüzden maliyet çıkarmazlar.



\## Hata Yönetimi



| Durum | Mesaj |

|-------|-------|

| Kimlik bilgisi yapılandırılmamış | `aws configure` çalıştırmayı önerir |

| S3 okuma yetkisi yok | IAM politikasını kontrol etmeyi önerir |

| Diğer AWS hataları | AWS hata kodunu gösterir |



\## Güvenlik



\- Kimlik bilgileri koda yazılmaz ve Git'e eklenmez.

\- `.gitignore`, JSON ve CSV çıktı dosyalarını, `.env`, `credentials`, `\*.pem` ve `\*.tfstate` dosyalarını dışarıda tutar.

\- Araç yalnızca bucket ayarlarını okur. Hiçbir şeyi değiştirmez ya da silmez.



\## Proje Yapısı



```

s3-public-access-auditor/

├── README.md

├── .gitignore

├── src/

│   └── s3\_denetci.py

└── tests/

&#x20;   └── test\_s3\_denetci.py

```

