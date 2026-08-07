"""UGM Strategic Dashboard — sintesis EA (blueprint) × DSH (realita) untuk pimpinan.
Data: charts.db (r9_ea_* + r9_dsh_* + r9_* 9router). 9router/Qdrant = konteks pendukung.
5 tab: Executive Overview, Proses Bisnis (EA), Kebutuhan Publik (DSH), Cross-Domain, Konteks."""
import streamlit as st, sqlite3, pandas as pd, plotly.express as px

st.set_page_config(page_title="UGM Strategic Analysis", layout="wide")
DB = "/app/charts.db"

@st.cache_data(ttl=3600)
def load():
    con = sqlite3.connect(DB)
    ea_el = pd.read_sql("SELECT Object_ID, Name, Stereotype, Status, Package_ID, Author FROM r9_ea_elements", con)
    ea_conn = pd.read_sql("SELECT Connector_ID, Connector_Type, Start_Object_ID, End_Object_ID FROM r9_ea_connectors", con)
    ea_pkg = pd.read_sql("SELECT Package_ID, Name FROM r9_ea_packages", con)
    ai = pd.read_sql("SELECT * FROM r9_dsh_ai_logs", con)
    sh = pd.read_sql("SELECT * FROM r9_dsh_search_history", con)
    qa = pd.read_sql("SELECT * FROM r9_dsh_qa_knowledge", con)
    fb = pd.read_sql("SELECT * FROM r9_dsh_ai_feedback", con)
    tr = pd.read_sql("SELECT * FROM r9_dsh_entity_trends", con)
    pop = pd.read_sql("SELECT * FROM r9_dsh_popular", con)
    con.close()
    return ea_el, ea_conn, ea_pkg, ai, sh, qa, fb, tr, pop

ea_el, ea_conn, ea_pkg, ai, sh, qa, fb, tr, pop = load()

st.title("🏛️ UGM Strategic Analysis — Proses Bisnis × Data Universitas")
st.caption("Sintesis EA (blueprint) × DSH (realita) — untuk pengambilan keputusan. 9router/Qdrant = konteks pendukung.")

tab = st.sidebar.radio("Menu", ["Executive Overview", "Proses Bisnis (EA)", "Kebutuhan Publik (DSH)", "Cross-Domain", "Konteks Pendukung"])

def merge_conn(stype, etype):
    s = ea_el[ea_el["Stereotype"] == stype]
    e = ea_el[ea_el["Stereotype"] == etype]
    m = ea_conn.merge(s[["Object_ID", "Name"]].rename(columns={"Object_ID": "Start_Object_ID", "Name": "src"}), on="Start_Object_ID", how="inner")
    return m.merge(e[["Object_ID", "Name"]].rename(columns={"Object_ID": "End_Object_ID", "Name": "dst"}), on="End_Object_ID", how="inner")

# ═══════════ EXECUTIVE OVERVIEW (SINTESIS) ═══════════
if tab == "Executive Overview":
    st.subheader("📌 Executive Overview — Narasi Terhubung")

    # KPI inti
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Proses (EA)", f"{len(ea_el[ea_el['Stereotype']=='Activity']):,}")
    c2.metric("Pencarian Publik (DSH)", f"{len(sh):,}")
    c3.metric("Layanan EA", f"{len(ea_el[ea_el['Stereotype'].isin(['Layanan','ApplicationService','ApplicationComponent'])]):,}")
    c4.metric("Layanan DSH", f"{int(tr[tr['entity_type']=='service']['total_items_created'].sum()) if not tr.empty else 0:,}")
    c5.metric("AI Query (DSH)", f"{len(ai):,}")

    # ── Gap utama (auto-computed) ──
    st.markdown("### 🔴 3 Gap Utama (auto-deteksi)")

    # Gap 1: proses tanpa KPI
    kpi_conn = merge_conn("Activity", "KPI")
    act_ids = set(ea_el[ea_el["Stereotype"] == "Activity"]["Object_ID"])
    kpi_linked = set(kpi_conn["Start_Object_ID"]) | set(kpi_conn["End_Object_ID"])
    gap_kpi = len(act_ids - kpi_linked)
    pct_kpi = gap_kpi / max(len(act_ids), 1) * 100
    g1 = st.columns([1, 5])
    g1[0].metric("Tanpa KPI", f"{gap_kpi:,} ({pct_kpi:.1f}%)")
    g1[1].info("**Gap 1 — Manajemen Kinerja**: hampir semua proses bisnis belum terhubung indikator kinerja (KPI). Basis: EA t_object.")

    # Gap 2: risiko tanpa mitigasi
    risks = ea_el[ea_el["Stereotype"] == "Risk"]
    mitig = merge_conn("Risk", "Mitigasi")
    mitig_ids = set(mitig["Start_Object_ID"]) | set(mitig["End_Object_ID"])
    unm = len(risks) - len(mitig_ids)
    g2 = st.columns([1, 5])
    g2[0].metric("Risiko Tanpa Mitigasi", f"{max(unm,0):,}")
    g2[1].warning("**Gap 2 — Manajemen Risiko**: mayoritas risiko belum punya mitigasi. Prioritas kontrol pada proses kritis (SNBT, layanan mahasiswa).")

    # Gap 3: kebutuhan publik vs KB
    n_layanan = len(sh[sh["query"].str.contains("layanan|simaster|portal|beasiswa|pendaftaran", case=False, na=False)])
    g3 = st.columns([1, 5])
    g3[0].metric("Query Layanan Publik", f"{n_layanan:,}")
    g3[1].warning("**Gap 3 — Kebutuhan vs Layanan**: permintaan publik (layanan/beasiswa/pendaftaran) harus dicek terhadap knowledge base & layanan digital yang ada di EA.")

    # ── Sinyal utama ──
    st.markdown("### 📡 Sinyal Utama")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("**Entity Paling Diklik (30d)**")
        if not tr.empty:
            agg = tr.groupby("entity_type")[["total_items_created", "clicked_items_30d"]].sum().reset_index()
            agg.columns = ["Entity", "Total", "Klik"]
            agg = agg[agg["Klik"] > 0].sort_values("Klik", ascending=False)
            st.dataframe(agg, use_container_width=True, hide_index=True)
    with col_r:
        st.markdown("**Feedback Negatif Teratas**")
        neg = fb[fb["rating"] < 0]
        if not neg.empty:
            st.dataframe(neg[["query", "feedback_text"]].rename(columns={"query": "Query", "feedback_text": "Keluhan"}),
                         use_container_width=True, hide_index=True)
        else:
            st.write("Tidak ada feedback negatif")

    st.markdown("### 🧭 Arah Rekomendasi")
    st.success("**Prioritas #1**: Perbaiki kualitas RAG chatbot (feedback negatif) + publikasikan (hanya 4 IP). "
               "**Prioritas #2**: Mitigasi risiko kritis + tetapkan KPI proses prioritas. "
               "**Prioritas #3**: Isi knowledge gap (beasiswa/bencana = topik populer).")

# ═══════════ PROSES BISNIS (EA) ═══════════
elif tab == "Proses Bisnis (EA)":
    st.subheader("⚙️ Proses Bisnis — EA")

    # Kematangan per unit (proses vs layanan per package)
    st.markdown("**Kematangan Digital per Unit** (proses vs layanan/aplikasi per package)")
    act = ea_el[ea_el["Stereotype"] == "Activity"]
    lay = ea_el[ea_el["Stereotype"].isin(["Layanan", "ApplicationService", "ApplicationComponent"])]
    pkg_n = ea_pkg.rename(columns={"Name": "Pkg"})
    a = act.groupby("Package_ID").size().rename("proses").reset_index()
    l = lay.groupby("Package_ID").size().rename("layanan").reset_index()
    m = a.merge(l, on="Package_ID", how="outer").fillna(0).merge(pkg_n, on="Package_ID", how="left")
    m = m[m["Pkg"].fillna("").str.contains("Fakultas|Direktorat|Biro|Sekolah", case=False, na=False)]
    m["rasio"] = (m["layanan"] / m["proses"].replace(0, 1) * 100).round(1)
    top = m.nlargest(12, "proses")[["Pkg", "proses", "layanan", "rasio"]]
    top.columns = ["Unit", "Proses", "Layanan", "Rasio %"]
    st.dataframe(top, use_container_width=True, hide_index=True)

    # Risk map
    st.markdown("**Risk Map — Proses Paling Berisiko**")
    rc = merge_conn("Activity", "Risk")
    if not rc.empty:
        rk = rc.groupby("src").size().sort_values(ascending=False).head(10).reset_index()
        rk.columns = ["Proses", "Risiko"]
        st.plotly_chart(px.bar(rk, x="Risiko", y="Proses", orientation="h", color="Risiko"), use_container_width=True)

    # KPI coverage
    st.markdown("**KPI Coverage**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Proses", f"{len(act):,}")
    kc = merge_conn("Activity", "KPI")
    linked = set(kc["Start_Object_ID"]) | set(kc["End_Object_ID"])
    c2.metric("Terhubung KPI", f"{len(linked):,} ({len(linked)/max(len(act),1)*100:.1f}%)")
    c3.metric("Tanpa KPI", f"{len(act)-len(linked):,}")

# ═══════════ KEBUTUHAN PUBLIK (DSH) ═══════════
elif tab == "Kebutuhan Publik (DSH)":
    st.subheader("📊 Kebutuhan Publik — DSH")

    st.markdown("**Top Query Chatbot (sinyal kebutuhan sivitas)**")
    top = ai["query"].value_counts().head(15).reset_index()
    top.columns = ["Query", "Jumlah"]
    st.dataframe(top, use_container_width=True, hide_index=True)

    st.markdown("**Query Populer Pencarian Web**")
    if not pop.empty:
        st.dataframe(pop.sort_values("search_count", ascending=False).head(15)
                     [["query", "search_count", "search_date"]]
                     .rename(columns={"query": "Query", "search_count": "Jumlah", "search_date": "Tanggal"}),
                     use_container_width=True, hide_index=True)

    st.markdown("**Knowledge Gaps & Feedback**")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Feedback Negatif**")
        neg = fb[fb["rating"] < 0]
        if not neg.empty:
            st.dataframe(neg[["query", "feedback_text"]], use_container_width=True, hide_index=True)
        else:
            st.write("Tidak ada")
    with c2:
        st.markdown("**Q&A Paling Dipakai**")
        if not qa.empty:
            st.dataframe(qa.nlargest(10, "use_count")[["query_original", "use_count"]]
                         .rename(columns={"query_original": "Pertanyaan", "use_count": "Dipakai"}),
                         use_container_width=True, hide_index=True)

# ═══════════ CROSS-DOMAIN ═══════════
elif tab == "Cross-Domain":
    st.subheader("🔗 Cross-Domain — EA (blueprint) × DSH (realita)")
    c1, c2, c3 = st.columns(3)
    ea_lay = ea_el[ea_el["Stereotype"].isin(["Layanan", "ApplicationService", "ApplicationComponent"])]
    dsh_serv = int(tr[tr["entity_type"] == "service"]["total_items_created"].sum()) if not tr.empty else 0
    n_q = len(sh[sh["query"].str.contains("layanan|simaster|portal|beasiswa", case=False, na=False)])
    c1.metric("EA: Layanan", f"{len(ea_lay):,}")
    c2.metric("DSH: Entity Service", f"{dsh_serv:,}")
    c3.metric("Query Layanan Publik", f"{n_q:,}")

    st.markdown("**Layanan EA per Unit**")
    if not ea_lay.empty:
        pkg_n = ea_pkg.rename(columns={"Name": "Pkg"})
        m2 = ea_lay.merge(pkg_n, on="Package_ID", how="left")
        t2 = m2["Pkg"].fillna("(tanpa package)").value_counts().head(12).reset_index()
        t2.columns = ["Unit", "Layanan"]
        st.plotly_chart(px.bar(t2, x="Layanan", y="Unit", orientation="h", color="Layanan"), use_container_width=True)

    st.markdown("**Insight**")
    st.info(f"**Service** paling diklik publik (30d) — kebutuhan layanan digital tertinggi. "
            f"EA memetakan {len(ea_lay):,} layanan, DSH punya {dsh_serv:,} entity service, "
            f"dan {n_q:,} pencarian publik menyebut layanan. Gap = peluang digitalisasi.")

# ═══════════ KONTEKS PENDUKUNG ═══════════
else:
    st.subheader("🧩 Konteks Pendukung — 9router (biaya AI) — SEKUNDER")
    st.caption("Data ini hanya konteks. Fokus analisis strategis = proses bisnis & data universitas (EA + DSH).")

    try:
        con = sqlite3.connect(DB)
        hist = pd.read_sql("SELECT model, SUM(prompt_tokens) p, SUM(completion_tokens) c, SUM(cost) cost, COUNT(*) n FROM r9_usage_history GROUP BY model ORDER BY cost DESC LIMIT 8", con)
        con.close()
        if not hist.empty:
            hist["total_tokens"] = hist["p"] + hist["c"]
            c1, c2 = st.columns(2)
            c1.metric("Total Request", f"{hist['n'].sum():,}")
            c2.metric("Total Cost", f"${hist['cost'].sum():,.0f}")
            st.dataframe(hist[["model", "n", "total_tokens", "cost"]]
                         .rename(columns={"model": "Model", "n": "Request", "total_tokens": "Token", "cost": "Cost ($)"}),
                         use_container_width=True, hide_index=True)
    except Exception as e:
        st.warning(f"Data 9router tidak tersedia: {e}")

st.caption("Data: charts.db — r9_ea_* (collect_ea_ugm.py), r9_dsh_* (collect_dsh.py), r9_* (collect_9router_detail.py)")
