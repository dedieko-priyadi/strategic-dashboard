# BTD Analytics Dashboard — Arsitektur Kerja Ekosistem UGM

**Repo payung**: https://github.com/dedieko-priyadi/strategic-dashboard
**Tanggal**: 2026-08-07 | **Status**: LIVE

## 🏛️ Visi

Satu **main dashboard** yang menyintesis analytics dari SEMUA dataset BTD UGM — dengan
sub-menu per dataset dan cross-domain analytics. Ini adalah **payung besar** project
dashboard analytics BTD.

## 📊 Live URL

| Dashboard | Public URL |
|---|---|
| **Strategic (PAYUNG)** | https://nuc-nuc7i5bnh-1.tail758353.ts.net/strategic/ |
| EA Decision | https://nuc-nuc7i5bnh-1.tail758353.ts.net/ea-decision/ |
| DSH Analytics | https://nuc-nuc7i5bnh-1.tail758353.ts.net/dsh-analytics/ |
| 9router | https://nuc-nuc7i5bnh-1.tail758353.ts.net/9router-dash/ |
| Qdrant | https://nuc-nuc7i5bnh-1.tail758353.ts.net/qdrant-dash/ |
| Wekan | https://nuc-nuc7i5bnh-1.tail758353.ts.net/wekan-dash/ |
| Charts Admin | https://nuc-nuc7i5bnh-1.tail758353.ts.net/charts-admin/ |

---

# 📐 ARSITEKTUR KERJA — 7 LAYER

```
┌─────────────────────────────────────────────────────┐
│ L7 INFRASTRUKTUR: server, Docker, Tailscale, Git,   │
│    Nextcloud, NAS                                   │
├─────────────────────────────────────────────────────┤
│ L6 KNOWLEDGE: BookStack, ea-ugm-explorer,           │
│    shared-skills, ugm-strategic-analysis            │
├─────────────────────────────────────────────────────┤
│ L5 DASHBOARD: strategic (payung) + 8 per-dataset    │
├─────────────────────────────────────────────────────┤
│ L4 MCP: ugmcore, dsh, 9router, planka, wekan,       │
│    regulasi — jembatan Hermes → data                │
├─────────────────────────────────────────────────────┤
│ L3 CHATBOT/AI: ea-chatbot, dsh-chatbot, dsh-aitool, │
│    ugmcore-ai, LISA, openbtd                        │
├─────────────────────────────────────────────────────┤
│ L2 PLATFORM/WEB: dsh-ugm, ugmcore_main, planka,     │
│    n8n, snapotter, sistemantrian, docuseal          │
├─────────────────────────────────────────────────────┤
│ L1 DATA: eaugm_2025, ugm_dsh, 9router, Qdrant,      │
│    Wekan, charts.db                                 │
└─────────────────────────────────────────────────────┘
```

---

# L1 — SUMBER DATA

Semua data diakses **read-only**, disimpan di **charts.db** (collection engine) via collector cron.

| Dataset | Lokasi | Isi | Kredensial |
|---|---|---|---|
| **EA** | SQL Server `eaugm_2025` @ 10.17.104.247 | 132.183 elemen, 6.151 diagram, 2.604 risiko, 47.925 proses, 481 unit | sa / EA_SQL_PASS (config) |
| **DSH** | MySQL `ugm_dsh` @ 10.17.104.219 (tunnel 13307) | search_history 3.812, ai_logs 2.362, Q&A 338, feedback 41, index 89.774 | hermes_ro / H3rm3sR0#2024 |
| **9router** | SQLite `data.sqlite` @ PC-AMD7900X 10.15.17.190 | usage_history 30K, api_keys 24, cost per model | SSH dedie |
| **Qdrant** | localhost :8599 (NUC) | ea_elements 17K vectors, dsh_search | API lokal |
| **Wekan** | Wekan API | board/cards project | token MCP |
| **Planka** | Planka API 127.0.0.1:13370 | kanban project | MCP planka |

**PITFALL KRITIS**: DSH = `ugm_dsh` BUKAN `store_ai`! EA = `eaugm_2025`. Jangan tertukar.

## Collector → charts.db (pipeline)

| Collector | Sumber | Cron | Tabel di charts.db |
|---|---|---|---|
| `collect_ea_ugm.py` | SQL Server EA | 04:00 harian | r9_ea_packages, r9_ea_elements (132K), r9_ea_connectors (94K), r9_ea_diagrams (6.151), r9_ea_diagram_objects |
| `collect_dsh.py` | MySQL ugm_dsh | 04:30 harian | r9_dsh_search_history, r9_dsh_ai_logs, r9_dsh_qa_knowledge, r9_dsh_ai_feedback, r9_dsh_ai_conversations, r9_dsh_ai_analytics, r9_dsh_popular, r9_dsh_entity_trends, r9_dsh_facilities |
| `collect_9router_detail.py` | SQLite 9router | tiap jam | r9_usage_history, r9_api_keys |

Semua dashboard baca charts.db **read-only** (volume mount `:ro`).

---

# L2 — PLATFORM & WEB

| Project | Fungsi | Port | Repo |
|---|---|---|---|
| **dsh-ugm** | Web DSH asli (PHP, 89.740 entitas) | :8585 /dsh/ | dsh-ugm |
| **ugmcore_main** | Web EA UGM | :8580 | ugmcore_main |
| **planka** | Kanban modern | 13370/13371 /planka/ | planka |
| **n8n** | Workflow automation | :8550/8551 | n8n-magang |
| **snapotter** | Transcribe audio/video | 13490 /snapotter/ | snapotter |
| **sistemantrian** | Antrian layanan | :8570 | sistemantrian-ugm |
| **docuseal** | Digital signature | :3000 | docuseal |
| **bookstack** | Knowledge base docs | :8603 | bookstack-btd |
| **openbtd** | PoC chatbot publik BTD | :8600 | openbtd |

---

# L3 — CHATBOT & AI

| Project | Fungsi | Kanal | Repo |
|---|---|---|---|
| **ea-chatbot** | Chatbot EA (Hermes profile, MCP-only) | Telegram @ugm_dsh_bot | ea-chatbot |
| **ea-chat-ui** | Web UI chatbot EA | :3000 | ea-chat-ui |
| **dsh-chatbot** | Chatbot DSH | :8516 | dsh-chatbot |
| **dsh-aitool** | AI tool (chat + generator berita) | :8590 | dsh-aitool |
| **ugmcore-ai/api** | AI query EA (query-ai.ps1) | :8580 | ugmcore-ai |
| **LISA-UGM** | AI asisten (legacy) | — | LISA-UGM |

**Pola**: Hermes profile + Telegram, public bot = toolsets mcp-only + branding hidden + TELEGRAM_HOME_CHANNEL.

---

# L4 — MCP SERVERS (jembatan Hermes → data)

| MCP | Tools | Data | Lokasi config |
|---|---|---|---|
| **ugmcore** | 11: test, summary, search, detail, proses-bisnis, aplikasi, search_qdrant, regulasi, dsh | EA eaugm_2025 | mcp_servers (command) |
| **dsh** | 7: facilities, news, faq, academic, publications, stats | DSH ugm_dsh | mcp.servers (URL) |
| **9router** | 6: health, keys, usage, settings | 9router API | mcp.servers |
| **planka** | 13: project, board, list, card, user, member | Planka API | mcp_servers (command, mcp 1.x) |
| **wekan** | 21: board, card, checklist, member, label | Wekan API | mcp_servers (command) |
| **regulasi** | search_regulations | Qdrant regulasi | mcp_servers (command) |

**Config**: `mcp.servers` (URL-based) vs `mcp_servers` top-level (command-based stdio).
**Pitfall**: mcp package == 1.x utk FastMCP (2.0 tidak punya mcp.server.fastmcp).

---

# L5 — DASHBOARD ANALYTICS

| Dashboard | Port | Subpath | Dataset | Repo |
|---|---|---|---|---|
| **strategic (PAYUNG)** | 8542 | /strategic/ | semua + cross-domain | strategic-dashboard |
| ea-decision | 8540 | /ea-decision/ | EA | ea-decision-dashboard |
| dsh-analytics | 8541 | /dsh-analytics/ | DSH | dsh-analytics-dashboard |
| 9router | 8527 | /9router-dash/ | 9router | 9router-dashboard |
| qdrant | 8529 | /qdrant-dash/ | Qdrant | qdrant-dashboard |
| wekan | 8532 | /wekan-dash/ | Wekan | wekan-dashboard |
| charts-admin | 8533 | /charts-admin/ | collection engine | collection-engine |
| ea-dash (legacy) | 8531 | /ea-dash/ | EA lama | ea-dashboard |
| dsh-dash (legacy) | 8528 | /dsh-dash/ | DSH lama | dsh-dashboard |

## Strategic Dashboard — 5 Tab (payung)

1. **Executive Overview** — narasi sintesis: KPI inti + 3 gap auto-deteksi + sinyal + rekomendasi
2. **Proses Bisnis (EA)** — kematangan unit, risk map, KPI coverage
3. **Kebutuhan Publik (DSH)** — top query, feedback, Q&A
4. **Cross-Domain** — EA layanan × DSH service × query publik
5. **Konteks Pendukung** — biaya AI 9router (sekunder)

---

# L6 — KNOWLEDGE & DOKUMENTASI

| Project | Isi | Repo |
|---|---|---|
| **ea-ugm-explorer** | 6.151 diagram → markdown 28MB + SVG 78MB | ea-ugm-explorer |
| **ugm-strategic-analysis** | konsep (KONSEP-STRATEGIS.md), analisis (6 temuan, 7 rekomendasi) | ugm-strategic-analysis |
| **bookstack-btd** | knowledge base tim BTD | bookstack-btd |
| **shared-skills / hermes-skills** | katalog 121 skill via NAS | shared-skills |
| **collection-engine** | charts.db + collector + admin panel | collection-engine |

---

# L7 — INFRASTRUKTUR

| Host | IP | Peran |
|---|---|---|
| **NUC** (def) | 10.14.7.239 | host utama: dashboard, MCP, collector, gateway Hermes |
| **PC-MONITOR** (w1) | 10.14.7.240 | worker, Nextcloud :18080, Immich |
| **PC-AMD7900X** (w2) | 10.15.17.190 | worker, 9router gateway, provider LLM |
| **NAS Synology** | 10.15.17.194 | shared storage btdstorage |

- **Docker NUC**: 76+ container, bridge /24 (ipam), `sg docker -c`, port bind 0.0.0.0
- **Tailscale Funnel**: `sudo tailscale funnel --bg --set-path /<sub>/ http://localhost:<port>/<sub>/`
- **Git**: 47 repo @ dedieko-priyadi; GIT RULES (logbook commit ber-timestamp, laporan wajib URL)
- **Nextcloud**: :18080, share link baru setiap kali
- **Cron**: Hermes cron collector + hgr restart gateway (system crontab)

---

# 🧠 SKILL TERKAIT

| Skill | Fungsi |
|---|---|
| **ugm-btd-ecosystem** | MASTER — peta 7 layer seluruh ekosistem |
| **btd-analytics-dashboard** | detail dashboard (port, pipeline, deploy pola) |
| **ugm-enterprise-architecture** | EA query & ekstraksi (3 jalur) |
| **dsh-ugm-platform** | DSH platform + peta 9 project + wajah publik |
| **collection-engine** | pipeline charts.db |
| **9router-monitor** | monitoring 9router |
| **server-operations** | akses 3 server + NAS |
| **docker-container-audit** | audit container |
| **tailscale-management** | funnel & publikasi |
| **nextcloud-share** | file sharing |
| **hermes-telegram-chatbot** | pola chatbot Telegram |

---

# 🔗 ALUR KERJA (saling melengkapi)

```
1. Data EA (eaugm_2025) → MCP ugmcore → ea-decision-dashboard + strategic
2. Data DSH (ugm_dsh) → MCP dsh → dsh-analytics-dashboard + strategic
3. EA × DSH → strategic Cross-Domain (gap proses vs kebutuhan publik)
4. Chatbot (ea-chatbot) → MCP ugmcore → jawab pertanyaan EA
5. Biaya AI (9router) → konteks evaluasi chatbot
6. Knowledge (bookstack) → dokumentasi semua project
7. Kanban (planka/wekan) → pelacakan project tim
```

---

# 🚀 DEPLOY POLA (dashboard baru)

```bash
mkdir ~/<name>-dashboard && cd ~/<name>-dashboard
# Dockerfile: streamlit --server.port=X --server.baseUrlPath=/<subpath>
# compose: port 0.0.0.0, volume charts.db:ro, network /24
sg docker -c "docker compose up -d --build"
# user eksekusi (bubble terpisah):
sudo tailscale funnel --bg --set-path /<subpath>/ http://localhost:PORT/<subpath>/
# verify: curl funnel 200 → browser DOM → deploy-verify → commit + laporan
```

---

# 📝 GIT RULES (wajib)

1. **Deploy** → project git baru: laporan-deploy-<tanggal>.md + README + URL lokal + funnel
2. **LOG BOOK**: tiap attempt/iterasi WAJIB commit ber-timestamp + deskripsi — git = laporan tak langsung + logbook
3. **Push** + lapor nama project + link
4. Laporan akhir WAJIB cantum URL git
5. README English, update langsung setelah fix (tanpa nunggu arahan)
