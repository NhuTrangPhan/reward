# Phan tich Product Manager - Reward v2

## Verdict Tong quan

**EXECUTION-ONLY MODE (3.2/10)** — Team Reward v2 dang ship nhieu feature ky thuat (11 feature hoan thanh), nhung thieu su lua chon uu tien dua tren user value va business outcome. Nguy co cao: ship nhieu, adopt thap, rework nang khi UI dinh hinh.

---

## User Value Assessment

### Ai dang duoc loi?

Team da tao value cho 3 nhom user chinh:

1. **End User (Miniapp)** — API day du de xem diem, doi qua, quan ly voucher. Value hien tai: 0 (pending UI).

2. **Admin Shop (Web)** — API cho cai dat API Key, config doi diem. Value hien tai: 0 (pending UI).

3. **Backend/System** — API backend cho payment (3-mode), retry worker, loyalty integration xong. Value: Chua ro (no metric).

### Value cao vs thap o dau?

**Value CAO (High):**
- API danh sach qua + filter (high frequency, core use case)
- API doi qua (core transaction, drive redemption)
- Luong tien 3-mode (flexibility, critical for business model)
- GotIt integration (mo vendor moi, expansion)
- CNV Loyalty sync (core flow)

**Value MEDIUM:**
- Urbox sync workers, API lich su, Self-Healing Worker

**Value CHUA RO:**
- Luong doi soat (chua implement), Webhook routing (ZNS bi loi)

---

## UX Gaps Nghiem Trong

### 1. CRITICAL: Miniapp UI chua chot

**Risk:** EXTREME - API xong nhung UI chua start. Neu UX dinh hinh khong match API response format, rework 1-2 tuan.

### 2. CRITICAL: Web Admin UI chua chot

**Risk:** HIGH - API config xong nhung Admin chua biet UI nhin nhu nao, co validation gi.

### 3. CRITICAL: CRM UI chua chot

**Risk:** HIGH - Report metric chon chua ro, filter logic chua define.

### 4. MEDIUM: ZNS Voucher Issuing bi loi

**Risk:** MEDIUM - ZNS la preferred channel nhung dang bi loi. User chi nhan Email/SMS → lower engagement.

### 5. MEDIUM: Luong doi soat chua implement

**Risk:** MEDIUM - Finance se phai xu ly manual → high ops cost.

---

## Alignment voi Business Goal

**PROBLEM: Khong ro North Star Metric**

Team dang build theo tech roadmap (Urbox → GotIt → APIs), khong ro product roadmap (user nao duoc loi, measure success bang gi).

### Feature-Goal Alignment

**Neu goal = Tang Redemption Rate:**
- OK Urbox / GotIt sync → Them qua
- OK 3-mode payment → Giam cost
- Canh bao API + miniapp UX → Core flow, nhung UX chua
- Canh bao ZNS loi → Notification channel yeu

---

## Product Thinking Score

| Truc | Score | Reasoning |
|------|-------|-----------|
| User Focus | 5/10 | Co ten user nhung chua ro pain point |
| Outcome Orientation | 3/10 | Ship 11 feature, khong co metric |
| Prioritization | 4/10 | Uu tien theo vendor, khong theo user impact |
| UX Maturity | 2/10 | BE xong roi UI start = extreme risk |
| Data-Informed | 2/10 | Zero metric |
| Business Alignment | 3/10 | Build theo tech roadmap |

**Trung binh: 3.2/10 → EXECUTION-ONLY**

---

## 3 Recommendation Uu Tien (1 sprint)

### 1. Chot UI Miniapp NGAY (Deadline T3 tuan sau)

API miniapp hoan toan xong. Neu UI dinh hinh sai, rework 1-2 tuan.

**Concrete:** Lock design tren list qua, chi tiet qua, flow doi qua, voucher detail.

**Owner:** Product Manager + Designer

### 2. Dinh nghia North Star Metric & Success Metric

11 feature ship, 0 metric = team khong biet optimize huong nao.

**Concrete:** Viet doc "Reward v2 Success Metrics" voi metric cho tung feature.

**Owner:** Product Manager + Analytics team

### 3. Design → Dev Sync Session truoc UI Start

Hien tai: BE xong → UI start = mismatch risk cao.

**Concrete:** Setup weekly sync meeting, Design + Dev overlap 2-3 ngay khi BE xong.

**Owner:** Product Manager (facilitate)

---

## Caveats & Gioi han

Phan tich nay dua tren 1 bao cao dev progress, khong day du.

**Bo sung de hoan chinh:**
1. Snapshot PRD + change requests
2. User research findings
3. Proposed metric dashboard
4. Product roadmap 1-2 quy
5. Blocker root cause analysis

---

## Summary: Feature Inventory

| Feature | User | Value | Status | Metric |
|---------|------|-------|--------|--------|
| Urbox Sync | Admin | Medium | OK | Khong |
| GotIt Integration | Admin | High | OK | Khong |
| API List/Redeem/Voucher | End User | High | OK | Khong |
| API Config | Admin | High | OK | Khong |
| Webhook & Issuing | Admin | High | In Progress | Khong |
| 3-Mode Payment | Admin/Finance | High | OK | Khong |
| Self-Healing Worker | System | Medium | OK | Khong |
| CNV Loyalty | System | High | OK | Khong |

---

## Hoc hoi chinh

1. **Ship ≠ Success:** 11 feature xong nhung 0 metric
2. **UX khong phai "trang tri":** BE xong roi UI → rework risk cao
3. **Business goal must come first:** Tech roadmap ≠ product roadmap
4. **Execution-only mode:** Dev lam theo scope → khong pro-active

**Recommendation:** Chuyen sang Feature-aware mode (5-7/10) bang cach: chot UI, dinh metric, sync UX-BE som.

