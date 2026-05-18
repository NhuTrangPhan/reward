# Phân tích Tech Lead - Dự án Reward v2
**Ngày đánh giá:** 21/04/2026  
**Dựa trên:** Báo cáo tiến độ 30/3 - 17/4

---

## Kết luận tổng quan

**Trình độ team: Mid-Senior, xu hướng Senior**

Team Reward v2 cho thấy suy nghĩ kiến trúc solid với strategy pattern, distributed systems awareness (idempotency, retry), và self-healing logic. Tuy nhiên, báo cáo thiếu hoàn toàn reference tới testing, monitoring, hay observability — đây là red flag lớn cho hệ thống xử lý tiền.

---

## Điểm mạnh rõ rệt

### 1. Kiến trúc multi-vendor với Strategy Pattern (Architecture: 8/10)

Team đã thiết kế hệ thống redemption cho phép mỗi vendor (Urbox, GotIt) có RedeemStrategy riêng. Thay vì hardcode vendor-specific logic vào core, họ tách biệt nó. Khi vendor mới vào, không cần sửa payment engine, chỉ thêm strategy mới. Đây là dấu hiệu Mid-Senior: hiểu tradeoff giữa abstraction vs complexity.

**Evidence:** "API đổi quà — có RedeemService + strategy riêng cho từng vendor (UrboxRedeemStrategy, GotItRedeemStrategy)"

### 2. Distributed systems thinking: Idempotency & Retry Framework (System Design: 8/10)

Payment systems dễ bị double-click (user click button 2x, lỡ submit 2 request). Team dùng idempotency key để chống. Thêm vào đó, họ có retry framework cho critical failures. Đây không phải basic CRUD — đây là thinking của production engineer. Không mỗi junior team nào suy nghĩ chi tiết tới mức này.

**Evidence:** "idempotency key chống double-click" + "retry framework cho critical failures"

### 3. Self-healing mindset: Tự detect & fix errors

Bằng cách scan PENDING orders quá timeout rồi retry/inquiry, team xây dựng observability vào hệ thống từ design. Không chỉ "code đúng", mà phải "tự lại khi lỗi". Self-Healing Worker là advanced pattern.

**Evidence:** "Self-Healing Worker — quét đơn PENDING quá timeout → retry/inquiry"

### 4. Domain depth: Fintech multi-mode (Domain Depth: 7/10)

Support 3 mode ký quỹ / công nợ / hybrid cho thấy team hiểu fintech logic. Không phải mỗi dev nào có thể code payment system — cần understand risk, compliance, reconciliation. Báo cáo còn mention integration với CNV Loyalty (check/add/subtract points, refund). Đây là business logic complexity.

**Evidence:** "support 3 mode ký quỹ / công nợ / hybrid" + "Integration CNV Loyalty: check điểm, cộng/trừ điểm, refund"

---

## Điểm yếu & Rủi ro

### Critical Gap #1: Không có Test Strategy

Báo cáo hoàn toàn không nhắc tới unit test, integration test, end-to-end test, hay QA process. Đây là red flag — hệ thống xử lý tiền thật, nên mỗi bug có thể làm user mất tiền hoặc business mất trust. Không test = high risk.

**Risk:** Production bug có thể cost cao. Khi team thêm feature mới, không có test coverage để catch regression.

**What's missing:** Test strategy, coverage target, QA checklist, staging validation.

### Critical Gap #2: Không có Observability (Monitoring/Logging/Metrics)

Self-healing worker và retry framework là tốt, nhưng nếu không có log/metric, team sẽ biết error xảy ra bao giờ? Khi nào redemption failure rate tăng từ 0.1% lên 2%? Qua user complaining hay proactive alerting?

**Risk:** Blind production environment. Nếu vendor API down, team sẽ biết muộn.

**What's missing:** Logging (each redemption attempt), metrics (success/failure rate per vendor), alerting (notify team if rate > threshold).

### High Gap #3: ZNS Channel Error — chưa xử lý

Báo cáo mention "Kênh gửi voucher: worker gửi thủ công Email/SMS/ZNS (đang bị lỗi ZNS)" — nhưng không rõ root cause hay fallback strategy. User không nhận voucher via ZNS? Có auto-retry hay fallback to SMS?

**Risk:** Incomplete feature, user experience degrade.

**What's missing:** Error handling, fallback logic, retry policy, root cause analysis.

### High Gap #4: Manual & Limited Automation

"Urbox không support API nên setup 1 ngày 1 lần" — manual sync là operational burden. Người setup quên → vendor data stale. Thêm vào đó, không có CI/CD pipeline mentioned.

**Risk:** Human error, downtime, inconsistent deployment.

**What's missing:** Automated deployment, pre-deploy testing, rollback plan, infrastructure-as-code.

### Medium Gap #5: Chưa sync nghiệp vụ với dev

"Dev đã tự quyết support 3 mode ký quỹ / công nợ / hybrid → Sẽ đổi khi nghiệp vụ chốt" — architecture decision được dev make, không PM/PO sign-off. Có thể OK (ownership tốt), hoặc có thể sẽ rework sau (over-engineering).

**Risk:** Waste effort nếu business chọn mode khác.

**What's missing:** Design review, stakeholder alignment, ADR (Architecture Decision Record).

---

## Điểm số theo khung

Technical Execution: **7/10** — Ship nhanh, nhưng không biết code quality vì không test.  
System Design: **8/10** — Strategy pattern, multi-vendor, idempotency → solid foundation.  
Domain Depth: **7/10** — Fintech logic, reconciliation, vendor integration → team hiểu business.  
Testing & Quality: **3/10** — Red flag, không nhắc test hoàn toàn.  
Communication: **7/10** — Báo cáo rõ feature/blocker, nhưng thiếu architectural rationale.  
Ownership & Initiative: **7/10** — Tự design, tự build workaround, nhưng cần sync sớm hơn.

---

## Next step cụ thể

1. **P0 (This sprint):** Implement test strategy. Unit test cho mỗi RedeemStrategy, integration test cho escrow/payable/hybrid mode, end-to-end test cho redemption flow. Target: 70%+ coverage.

2. **P0 (This sprint):** Setup observability. Add logging cho mỗi redemption attempt, metrics (success rate, latency per vendor), alert nếu failure rate > 5%.

3. **P1 (Next sprint):** Fix ZNS + add fallback. Investigate error root cause, implement auto-fallback: ZNS fail → retry → SMS → Email.

4. **P1 (Next sprint):** Automate Urbox sync. Script để daily sync, add error notification, CI/CD pipeline để deploy worker changes safely.

5. **P2 (Sprint after):** Architecture review + ADR. Formal review với PM/PO/Architecture team, document 3-mode escrow decision, confirm no rework expected.

---

## Caveats & Limitations

- **Sample quá nhỏ:** 1 báo cáo ~2 tuần không đủ để kết luận chắc. Có thể team có test nhưng quên ghi, hay đang trong sprint high-pressure nên skip tạm.
- **Context incomplete:** Không biết deadline, team size, onboarding status. Có thể ảnh hưởng evaluation.
- **Báo cáo có thể incomplete:** Team có thể có monitoring setup nhưng chưa mention. Cần verify trực tiếp.
- **Dùng để improve, không phải punish:** Đánh giá này là để team aware gap, không để blame. Action plan cần collaborative.

---

## Kết luận cuối

Team Reward v2 có foundation tốt (kiến trúc solid, distributed systems thinking). Nếu họ implement test + observability trong 2 sprint, họ ready để move to Senior level. Nếu skip, technical debt sẽ accumulate và risk sẽ cao khi scale.

**Ưu tiên:** Testing → Observability → Automation → Architecture review. Thực hiện theo thứ tự này sẽ maximize quality & team growth.
