# Arsitektur Dashboard BTD — Payung Besar (Master Concept)

**Tanggal**: 2026-08-07 | **Status**: DISETUJUI user — konsep payung dashboard BTD

## 1. Visi

**BTD MAIN DASHBOARD** = dashboard utama yang menampilkan analytics dari SEMUA dataset BTD.
Tiap dataset punya dashboard sendiri yang menjadi **sub-menu** di dashboard utama.

## 2. Struktur

```
BTD MAIN DASHBOARD (analytics seluruh dataset)
├── 📊 Overview — ringkasan sintesis semua dataset
├── 📂 Sub-menu per dataset (dashboard standalone per kategori)
│   ├── EA         → ea-decision-dashboard (:8540 /ea-decision/)
│   ├── DSH        → dsh-analytics-dashboard (:8541 /dsh-analytics/)
│   ├── 9router    → 9router-dashboard (:8527 /9router-dash/)
│   ├── Qdrant     → qdrant-dashboard (:8529 /qdrant-dash/)
│   ├── Wekan      → wekan-dashboard (:8532 /wekan-dash/)
│   ├── Charts     → charts-admin (:8533 /charts-admin/)
│   └── ...dsb
└── 🔗 CROSS-DOMAIN — sub-menu khusus
    └── menghubungkan SEMUA dataset → big picture relasi antar data
```

## 3. Prinsip Kerja (2 fase)

| Fase | Isi | Status |
|---|---|---|
| **Fase 1 (sekarang)** | Bangun tiap dashboard analytics per dataset TERPISAH — kelola pola pikir per dataset | EA ✅ DSH ✅ 9router ✅ lainnya menyusul |
| **Fase 2 (nanti)** | Main dashboard = Overview + Sub-menu menautkan semua + Cross-Domain analytics | ⏳ |

## 4. Posisi Project Ini

**`strategic-dashboard` (:8542 /strategic/)** = **CIKAL BAKAL BTD MAIN DASHBOARD** (payung besar):
- Tab **Executive Overview** = cikal bakal Overview main dashboard
- Tab **Cross-Domain EA×DSH** = cikal bakal sub-menu Cross-Domain (akan diperluas ke semua dataset)
- Tab per dataset (Proses Bisnis EA, Kebutuhan Publik DSH) = contoh pola sub-menu

## 5. Pemetaan Dashboard Existing

| Dataset | Dashboard | Port | Subpath | Status |
|---|---|---|---|---|
| EA | ea-decision-dashboard | 8540 | /ea-decision/ | ✅ |
| DSH | dsh-analytics-dashboard | 8541 | /dsh-analytics/ | ✅ |
| 9router | 9router-dashboard | 8527 | /9router-dash/ | ✅ |
| Qdrant | qdrant-dashboard | 8529 | /qdrant-dash/ | ✅ |
| Wekan | wekan-dashboard | 8532 | /wekan-dash/ | ✅ |
| Charts Admin | charts-admin | 8533 | /charts-admin/ | ✅ |
| **Main (payung)** | **strategic-dashboard** | **8542** | **/strategic/** | ✅ cikal bakal |

## 6. Referensi

- Repo main: https://github.com/dedieko-priyadi/strategic-dashboard
- Repo DSH analytics: https://github.com/dedieko-priyadi/dsh-analytics-dashboard
- Dokumen konsep analisis: https://github.com/dedieko-priyadi/ugm-strategic-analysis
