from src.s3_denetci import (
    ALL_USERS_URI,
    acl_herkese_acik_mi,
    bucket_riskleri,
    pab_kapali_ayarlar,
)

TUM_AYARLAR_ACIK = {
    "BlockPublicAcls": True,
    "IgnorePublicAcls": True,
    "BlockPublicPolicy": True,
    "RestrictPublicBuckets": True,
}


def test_guvenli_bucket_risk_yok():
    assert bucket_riskleri(TUM_AYARLAR_ACIK, False, []) == []


def test_public_access_block_hic_yoksa_risk():
    riskler = bucket_riskleri(None, False, [])
    assert any("Public Access Block kapalı" in r for r in riskler)


def test_bir_ayar_kapaliysa_o_ayar_listelenir():
    ayarlar = dict(TUM_AYARLAR_ACIK, BlockPublicAcls=False)
    assert pab_kapali_ayarlar(ayarlar) == ["BlockPublicAcls"]


def test_policy_herkese_aciksa_risk():
    riskler = bucket_riskleri(TUM_AYARLAR_ACIK, True, [])
    assert "Bucket policy herkese açık" in riskler


def test_acl_herkese_acikse_risk():
    grants = [{"Grantee": {"URI": ALL_USERS_URI}, "Permission": "READ"}]
    assert acl_herkese_acik_mi(grants)


def test_acl_sadece_sahibe_aitse_risk_yok():
    grants = [{"Grantee": {"ID": "sahip-kimligi"}, "Permission": "FULL_CONTROL"}]
    assert not acl_herkese_acik_mi(grants)