# Báo cáo tiến độ dự án Reward v2

## Đã hoàn thành

### 30/3 - 3/4
- Hoàn thành phát triển worker đồng bộ quà tặng từ Urbox (Tạo mới quà tặng, Cập nhật Giá & Stock) — Urbox không support API nên setup 1 ngày 1 lần
- Hoàn thành phát triển worker đồng bộ brand từ Urbox
- API chi tiết quà (Urbox)
- API Integration Hub (CRUD connection)
- API Toggle RewardBrand, RewardCategory ON/OFF

### 6/4 - 10/4
- Phân tích tài liệu kỹ thuật với GotIt, đánh giá các API đã cung cấp so với nghiệp vụ hiện tại
- Test sơ bộ trên môi trường stg của GotIt
- Auto-Sync worker GotIt (category, brand, product, mapping brand-category)
- API danh sách quà + filter + pagination (hoàn thiện)
- API đổi quà — có RedeemService + strategy riêng cho từng vendor (UrboxRedeemStrategy, GotItRedeemStrategy)
- API lịch sử đổi quà (/account/redemption-orders/history)
- API giỏ quà / voucher user (/user/vouchers, /user/vouchers/{id})
- API cài đặt API Key, Cài đặt đổi điểm

### 13/4 - 17/4
- Trao đổi với GotIt và đã nhận các thông tin sandbox chính thức: cặp publickey, API, quy trình webhook. Đã test thành công Phát hành voucher, inquiry voucher
- Kênh gửi voucher: worker gửi thủ công Email/SMS/ZNS (đang bị lỗi ZNS)
- Phát triển module webhook API
- Luồng tiền đổi quà: support 3 mode ký quỹ / công nợ / hybrid, retry framework cho critical failures, idempotency key chống double-click
- Phát triển 4.6 Self-Healing Worker — quét đơn PENDING quá timeout → retry/inquiry
- Integration CNV Loyalty: check điểm, cộng/trừ điểm, refund khi đổi quà thất bại
- API miniapp: xem điểm, đổi quà, list/chi tiết voucher, list quà đổi được

## Block

- GotIt: Yêu cầu cung cấp OAuth2 → Họ chưa phản hồi
- Nghiệp vụ ký quỹ: Dev đã tự quyết support 3 mode ký quỹ / công nợ / hybrid → Sẽ đổi khi nghiệp vụ chốt
- UI: Hiện tại chưa chốt UI web admin, miniapp, CRM
- Luồng đối soát: chưa có
