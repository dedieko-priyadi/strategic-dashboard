# UGM Strategic Dashboard

Dashboard level pimpinan — **sintesis EA (blueprint) × DSH (realita)** untuk pengambilan keputusan.
9router/Qdrant = konteks pendukung (bukan fokus).

## URL
- **Public**: https://nuc-nuc7i5bnh-1.tail758353.ts.net/strategic/
- **Local**: http://127.0.0.1:8542/strategic/

## Konsep (lihat repo ugm-strategic-analysis/KONSEP-STRATEGIS.md)
- **INTI**: EA (proses bisnis, risiko, KPI) + DSH (kebutuhan publik, kualitas AI, KB)
- **Pendukung**: 9router (biaya), Qdrant (infra) — konteks saja
- **Overview = sintesis naratif**, bukan KPI berdampingan

## 5 Tab
1. **Executive Overview** — narasi terhubung: KPI inti + 3 gap auto-deteksi + sinyal + rekomendasi
2. **Proses Bisnis (EA)** — kematangan digital per unit, risk map, KPI coverage
3. **Kebutuhan Publik (DSH)** — top query, query populer, feedback, Q&A
4. **Cross-Domain** — EA layanan × DSH service × query publik (gap digitalisasi)
5. **Konteks Pendukung** — biaya AI 9router (sekunder)

## Data (charts.db)
| Sumber | Collector | Tabel |
|---|---|---|
| EA (SQL Server eaugm_2025) | collect_ea_ugm.py (cron 04:00) | r9_ea_* |
| DSH (MySQL ugm_dsh) | collect_dsh.py (cron 04:30) | r9_dsh_* |
| 9router (SQLite) | collect_9router_detail.py (cron tiap jam) | r9_usage_history |

## Insight terverifikasi (2026-08-07)
- 47.925 proses, 99,8% tanpa KPI
- 2.604 risiko, 2.106 (80,9%) tanpa mitigasi
- Layanan: EA 179 vs DSH 659 — gap arsitektur vs realita
- Service entity paling diklik publik (20 klik/30d)
- 144+ pencarian publik menyebut layanan

## Deploy
```bash
cd ~/strategic-dashboard
sg docker -c "docker compose up -d --build"
sudo tailscale funnel --bg --set-path /strategic/ http://localhost:8542/strategic/
```

## Repo
https://github.com/dedieko-priyadi/strategic-dashboard
