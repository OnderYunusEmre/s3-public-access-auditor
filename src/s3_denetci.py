import argparse
import json

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# AWS'nin "herkes" ve "giriş yapmış herkes" gruplarını temsil eden adresler
ALL_USERS_URI = "http://acs.amazonaws.com/groups/global/AllUsers"
AUTH_USERS_URI = "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"

# Public Access Block'un dört ayarı
PAB_AYARLARI = [
    "BlockPublicAcls",
    "IgnorePublicAcls",
    "BlockPublicPolicy",
    "RestrictPublicBuckets",
]


def pab_kapali_ayarlar(pab_config):
    """Public Access Block'ta kapalı olan ayarların listesini döndürür."""
    if pab_config is None:
        return PAB_AYARLARI
    return [ayar for ayar in PAB_AYARLARI if not pab_config.get(ayar, False)]


def acl_herkese_acik_mi(grants):
    """ACL içinde herkese ya da giriş yapmış herkese verilmiş bir izin var mı?"""
    for grant in grants:
        uri = grant.get("Grantee", {}).get("URI", "")
        if uri in (ALL_USERS_URI, AUTH_USERS_URI):
            return True
    return False


def bucket_riskleri(pab_config, policy_herkese_acik, grants):
    """Bir bucket için risk nedenlerinin listesini döndürür. Boş liste = risk yok."""
    riskler = []

    kapali = pab_kapali_ayarlar(pab_config)
    if kapali:
        riskler.append("Public Access Block kapalı: " + ", ".join(kapali))

    if policy_herkese_acik:
        riskler.append("Bucket policy herkese açık")

    if acl_herkese_acik_mi(grants):
        riskler.append("ACL herkese açık izin içeriyor")

    return riskler


def bucket_bilgilerini_al(s3, isim):
    """AWS'den bir bucket'ın üç güvenlik bilgisini alır."""
    # 1. Public Access Block ayarları
    try:
        pab = s3.get_public_access_block(Bucket=isim)["PublicAccessBlockConfiguration"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration":
            pab = None  # Hiç ayarlanmamış, yani açık kabul ediyoruz
        else:
            raise

    # 2. Bucket policy herkese açık mı?
    try:
        policy_herkese_acik = s3.get_bucket_policy_status(Bucket=isim)["PolicyStatus"]["IsPublic"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
            policy_herkese_acik = False  # Policy yoksa herkese açık olamaz
        else:
            raise

    # 3. ACL izinleri
    grants = s3.get_bucket_acl(Bucket=isim)["Grants"]

    return pab, policy_herkese_acik, grants


def denetle():
    """Hesaptaki tüm bucket'ları tarar. (toplam, riskliler) döndürür."""
    s3 = boto3.client("s3")
    riskliler = []
    toplam = 0

    for bucket in s3.list_buckets()["Buckets"]:
        toplam += 1
        isim = bucket["Name"]
        pab, policy_herkese_acik, grants = bucket_bilgilerini_al(s3, isim)
        riskler = bucket_riskleri(pab, policy_herkese_acik, grants)
        if riskler:
            riskliler.append({"bucket": isim, "riskler": riskler})

    return toplam, riskliler


def main():
    parser = argparse.ArgumentParser(description="S3 public erişim denetçisi")
    parser.add_argument("--cikti", default="riskli_bucketlar.json", help="JSON çıktı dosyası")
    args = parser.parse_args()

    try:
        toplam, riskliler = denetle()
    except NoCredentialsError:
        print("Hata: AWS kimlik bilgisi bulunamadı. 'aws configure' ile yapılandırın.")
        return
    except ClientError as e:
        kod = e.response["Error"]["Code"]
        if kod in ("AccessDenied", "AccessDeniedException"):
            print("Hata: Bu kullanıcının S3 okuma yetkisi yok. IAM politikasını kontrol edin.")
        else:
            print(f"AWS hatası: {kod}")
        return

    for bucket in riskliler:
        print(f"RİSKLİ: {bucket['bucket']}")
        for risk in bucket["riskler"]:
            print(f"  - {risk}")

    with open(args.cikti, "w", encoding="utf-8") as f:
        json.dump(riskliler, f, ensure_ascii=False, indent=2)

    guvenli = toplam - len(riskliler)
    print(f"{toplam} bucket tarandı: {len(riskliler)} riskli, {guvenli} güvenli.")
    print(f"Sonuçlar '{args.cikti}' dosyasına yazıldı.")


if __name__ == "__main__":
    main()