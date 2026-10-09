#!/usr/bin/env python3
"""
Sinh tài liệu "CNV Reward V2 — Tổng quan tính năng sản phẩm" (HTML + PDF).

Nguồn duy nhất: sửa THEMES bên dưới rồi chạy lại. Số thứ tự 1..N và "Trang x/y" tự đếm.

Chạy:
  DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib /tmp/wp-venv/bin/python generate_tinh_nang_san_pham.py

(venv: /usr/bin/python3 -m venv /tmp/wp-venv && /tmp/wp-venv/bin/pip install weasyprint;
 font: brew install --cask font-dejavu — bắt buộc, PDF đã gửi khách dùng DejaVu Sans)

Output:
  - cowork/html/CNV_Reward_V2_Tinh_nang_san_pham.html   (HTML source, giữ lại)
  - reward-claude/CNV_Reward_V2_Tinh_nang_san_pham.pdf   (bản gửi khách)
"""
import html
import os

UPDATED = "07/10/2026"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(HERE, "CNV_Reward_V2_Tinh_nang_san_pham.html")
OUT_PDF = os.path.join(HERE, "..", "..", "cnv", "projects", "reward-claude",
                       "CNV_Reward_V2_Tinh_nang_san_pham.pdf")
OUT_PDF = os.path.normpath(os.path.join(os.path.expanduser("~"),
                                        "cnv/projects/reward-claude/CNV_Reward_V2_Tinh_nang_san_pham.pdf"))

NEW = "MỚI"
UPD = "MỞ RỘNG"

INTRO = (
    "Tài liệu tổng hợp các tính năng của nền tảng CNV Reward V2, phân theo nhóm. Mỗi tính năng nêu rõ "
    "người dùng làm được gì và lợi ích mang lại. Các mục gắn nhãn <b>Mới</b> / <b>Mở rộng</b> là tính năng "
    "cập nhật ở đợt gần đây. Hệ thống kết nối hai đối tác cung cấp quà là <b>GotIt</b> và <b>UrBox</b>: "
    "tính năng <b>không ghi chú đối tác</b> áp dụng chung cho cả hai; tính năng chỉ một đối tác hỗ trợ được "
    "gắn nhãn <span class=\"vendor\">GotIt</span> hoặc <span class=\"vendor\">UrBox</span>. Bản cập nhật này "
    "bổ sung tích hợp UrBox (kết nối, kho quà e-voucher/combo/quà vật lý, giao hàng tận nơi) và gom các tính "
    "năng dùng chung của hai đối tác về một mục."
)

GOTIT = "GotIt"
URBOX = "UrBox"

# Mỗi theme: title, col (tiêu đề cột 3), intro (tuỳ chọn), highlights (tuỳ chọn), badge (tuỳ chọn),
# features: (tên, badge|None, làm gì, lợi ích[, vendor]) — vendor None = cả GotIt lẫn UrBox.
THEMES = [
    {
        "title": "Theme 1 — Kết nối & Cấu hình Vendor",
        "col": "KHÁCH LÀM GÌ",
        "features": [
            ("Kết nối đối tác cung cấp quà", None,
             "Kết nối nhiều đối tác cùng lúc (GotIt, UrBox), xem trạng thái cài đặt & thống kê (số quà, "
             "tình trạng) từng kết nối; tạm dừng để chỉnh sửa rồi bật lại.",
             "Một nơi quản lý multi-vendor, đỡ phân mảnh dữ liệu."),
            ("Cấu hình credential theo đối tác", UPD,
             "Tự thêm / sửa / xoá credential của chính mình, bật-tắt theo trạng thái; credential mã hoá "
             "AES-256 riêng theo account và được <b>xác minh với đối tác ngay lúc lưu</b> — sai thì chặn, "
             "không lưu key hỏng. <b>GotIt</b>: API key + cặp public/private key RSA + webhook secret (có "
             "versioning khi đổi key). <b>UrBox</b>: App ID + Secret Key + Campaign Code, request đổi quà "
             "được CNV ký RSA theo chuẩn UrBox.",
             "Tự chủ hoàn toàn, không phải chờ CNV ops khi đổi key; phát hiện key sai ngay lúc cấu hình "
             "thay vì lúc khách đang đổi quà."),
            ("Quản lý kênh gửi voucher", None,
             "Chọn kênh giao voucher tới user: Email (kèm mã QR ngay trong email) hoặc ZNS (Zalo). "
             "Mặc định Email.",
             "Linh hoạt theo tập khách hàng mục tiêu; email có sẵn QR để user quét dùng ngay."),
        ],
    },
    {
        "title": "Theme 2 — Catalog & Pricing",
        "col": "KHÁCH LÀM GÌ",
        "features": [
            ("Quản lý brand", None,
             "Bật/tắt thương hiệu, override riêng theo từng vendor, thao tác hàng loạt (bulk) hoặc theo "
             "category.",
             "Chọn đúng brand phù hợp tập khách của mình."),
            ("Quản lý category", None,
             "Bật/tắt danh mục, kéo-thả sắp xếp thứ tự hiển thị, đặt tên/ảnh hiển thị tuỳ biến "
             "(display override).",
             "Tuỳ biến trải nghiệm catalog cho end-user của khách."),
            ("Cấu hình riêng theo đối tác", NEW,
             "Mỗi đối tác có bộ danh mục/thương hiệu riêng để tick bật/tắt; chọn chế độ <b>dùng chung</b> "
             "hay <b>tuỳ chỉnh riêng</b> ghi đè cấu hình chung cho từng đối tác. Sau mỗi lượt đồng bộ, "
             "danh mục/thương hiệu không còn quà tự tắt riêng cho account đó.",
             "Mỗi đối tác hiển thị đúng những gì account thật sự có hàng; không lẫn cấu hình giữa các "
             "đối tác."),
            ("Tỷ giá quy đổi điểm", None,
             "Đặt tỷ lệ quy đổi điểm → VND.",
             "Tự quyết economics của chương trình loyalty."),
            ("Xem kho reward", UPD,
             "Duyệt catalog phân trang, tìm theo từ khoá, lọc theo tình trạng kho; xem thống kê kho "
             "(metric + breakdown). Gộp quà của mọi đối tác về một chỗ hoặc xem riêng theo từng đối tác; "
             "<b>lọc theo loại quà</b>: voucher, combo, quà vật lý.",
             "Nhìn rõ kho hàng khả dụng và sức khoẻ tồn kho theo từng đối tác và loại quà."),
            ("Đồng bộ kho từ đối tác", UPD,
             "Tự kích hoạt đồng bộ mới theo credential của mình; theo dõi tiến độ & huỷ giữa chừng được. "
             "Kéo về cả e-voucher, combo và quà vật lý; quà bị đối tác gỡ tự ẩn khỏi cửa hàng; thương "
             "hiệu chưa có trong danh mục đối tác được tạo tự động từ tên trong quà thay vì dồn vào nhóm "
             "“Khác”.",
             "Cập nhật ngay khi đối tác có hàng mới, không chờ lịch nền; kho đầy đủ mọi loại quà mà "
             "không cần thao tác riêng."),
            ("Cập nhật giá & tồn kho theo thời gian thực", NEW,
             "Mỗi lần mở chi tiết một quà, hệ thống hỏi UrBox giá và số lượng hiện tại, cập nhật ngay "
             "nếu lệch so với dữ liệu đã đồng bộ; quà hết hàng chuyển trạng thái hết tức thì.",
             "Khách không đổi phải quà đã hết hàng hay giá cũ; số điểm trừ luôn đúng với giá hiện hành.",
             URBOX),
            ("Cấu hình hạn mức đổi", None,
             "Giới hạn số lượt đổi trên mỗi user cho từng item.",
             "Chống lạm dụng, kiểm soát ngân sách."),
        ],
    },
    {
        "title": "Theme 3 — Đổi quà cho End-user",
        "col": "USER CUỐI LÀM GÌ",
        "features": [
            ("Đổi điểm lấy voucher", UPD,
             "Chọn quà + số lượng → nhận voucher tự động, đủ mã, QR, PIN/serial và link sử dụng theo "
             "từng đối tác. Hỗ trợ chống trùng đơn (Idempotency-Key). Voucher <b>vô thời hạn</b> được giữ "
             "đúng là vô thời hạn, không bị gán hạn mặc định.",
             "Trải nghiệm tức thì, không chờ xử lý thủ công; khách không mất quyền dùng voucher còn "
             "nguyên giá trị."),
            ("Xem voucher của tôi", None,
             "Duyệt voucher (còn hạn / đã dùng / hết hạn) + xem chi tiết (mã, điểm đã dùng, trạng thái "
             "từ đối tác).",
             "Self-service, không cần liên hệ CSKH."),
            ("Đánh dấu voucher đã/chưa dùng", UPD,
             "User tự bật/tắt trạng thái “đã sử dụng” cho voucher của mình với các voucher đối tác không "
             "báo lại trạng thái sử dụng: thương hiệu dùng link đổi quà của GotIt và mọi voucher UrBox.",
             "Tự quản lý voucher gọn gàng; trạng thái thủ công của user được tôn trọng, đối tác không "
             "ghi đè."),
            ("Voucher combo", NEW,
             "Combo gồm nhiều quà con được gom thành <b>một voucher</b> kèm trang gộp của UrBox; từng mã "
             "con có tên quà, mã/QR/PIN riêng và có thể đánh dấu đã dùng <b>riêng từng mã con</b>; voucher "
             "chỉ chuyển “đã dùng” khi mọi mã con đã dùng và chỉ hết hạn khi mã con cuối cùng hết hạn.",
             "Mở bán được các gói combo; khách dùng dần từng phần mà không mất dấu phần còn lại.",
             URBOX),
            ("Duyệt kho quà", None,
             "Lọc theo brand / category / giá; tìm theo từ khoá.",
             "Khám phá quà phù hợp dễ dàng."),
            ("Xem danh mục, thương hiệu & điểm áp dụng", UPD,
             "Xem danh mục đang bật, danh sách brand; xem cửa hàng / điểm áp dụng của quà theo "
             "TP/quận, kèm toạ độ để hiển thị bản đồ (GotIt theo cửa hàng của sản phẩm, UrBox theo điểm "
             "áp dụng của quà).",
             "Điều hướng dễ, tìm brand quen thuộc, biết dùng được ở đâu."),
            ("Lọc thương hiệu theo kênh sử dụng", None,
             "Lọc danh sách thương hiệu theo phương thức sử dụng quà: voucher điện tử, nạp thẻ điện "
             "thoại, hay đổi qua trang đối tác (webview).",
             "Tìm đúng loại quà theo nhu cầu nhanh hơn, không phải lướt toàn bộ danh sách.",
             GOTIT),
            ("Gợi ý quà cá nhân hoá", None,
             "Sắp xếp danh sách quà theo “đề xuất” (recommended) dựa trên bộ máy xếp hạng cá nhân hoá "
             "theo hành vi & sở thích của user (có điểm ưu tiên riêng cho thương hiệu/danh mục); hoạt "
             "động ổn định cả với user chưa có lịch sử.",
             "Tăng tỉ lệ đổi quà nhờ đưa quà phù hợp lên đầu; user mới cũng có gợi ý hợp lý ngay từ đầu."),
            ("Tìm kiếm theo từ khoá brand & category", None,
             "Gõ từ khoá để tìm quà/voucher — hệ thống khớp theo cả tên thương hiệu và tên danh mục theo "
             "ngữ nghĩa (vd gõ “cà phê” ra toàn bộ quà thuộc thương hiệu Highlands và danh mục cafe & "
             "bánh).",
             "Tìm đúng quà mong muốn nhanh, kể cả khi user chỉ nhớ tên brand hoặc loại quà."),
            ("Đổi quà trên Zalo Mini App", UPD,
             "User xem danh sách ưu đãi, chi tiết ưu đãi + cửa hàng áp dụng, đổi điểm và xem voucher ngay "
             "trong Zalo Mini App. Thẻ quà, voucher và đơn hàng hiển thị nhãn <b>“Cung cấp bởi”</b> kèm "
             "logo đối tác.",
             "Tiếp cận user ngay trên Zalo, không cần cài app riêng — tăng tỉ lệ tham gia; khách biết rõ "
             "quà đến từ đối tác nào."),
            ("Đổi quà qua trang đối tác (Webview)", None,
             "Với một số thương hiệu yêu cầu đổi quà trên trang riêng, user đổi ngay trong ứng dụng qua "
             "webview nhúng — không phải thoát ra trình duyệt ngoài.",
             "Trải nghiệm liền mạch, giữ user trong app; mở rộng hỗ trợ các thương hiệu có quy trình đổi "
             "quà riêng.",
             GOTIT),
        ],
    },
    {
        "title": "Theme 4 — Vận hành & Insights",
        "col": "KHÁCH LÀM GÌ",
        "features": [
            ("Lịch sử đổi quà", None,
             "Tra cứu toàn bộ đơn (theo đơn hoặc theo từng voucher), lọc theo thời gian / trạng thái / "
             "brand; xem chi tiết khách (lifetime spend, đơn gần nhất).",
             "Truy vết & đối soát nội bộ đầy đủ."),
            ("Thống kê đổi quà", None,
             "KPI tổng quan (4 thẻ), biểu đồ phễu (funnel), timeseries theo ngày, top quà, breakdown theo "
             "category/brand/vendor, heatmap khung giờ vàng, top khách hàng (Super Redeemers), quà ế "
             "(dead items), so sánh hiệu quả từng quà.",
             "Insight sâu để tối ưu chương trình, không chỉ con số tổng."),
            ("Quản lý voucher cấp Account", None,
             "Account xem toàn bộ voucher đã phát cho mọi user, có chi tiết & summary (đang hoạt động, "
             "sắp hết hạn trong 7/30 ngày).",
             "Bức tranh toàn cảnh voucher của cả chương trình (khác với “voucher của tôi” phía user)."),
            ("Thời hạn voucher & cảnh báo hết hạn", None,
             "Cấu hình thời hạn hiệu lực voucher (mặc định 12 tháng, tối đa 12 tháng); dashboard hiển "
             "thị số voucher sắp hết hạn 7/30 ngày.",
             "Chủ động kiểm soát vòng đời voucher.",
             GOTIT),
            ("Đối soát (Reconciliation)", None,
             "Tự upload report đối tác (.xlsx), hệ thống dò lệch (discrepancy), phân loại theo mức độ, xử "
             "lý từng dòng (duyệt/từ chối), resolve “ghost”, export kết quả. Có template mẫu để tải.",
             "Đảm bảo dữ liệu khớp với đối tác, minh bạch tài chính.",
             GOTIT),
            ("Xuất báo cáo & dữ liệu", None,
             "Xuất báo cáo tổng quan Excel 9 sheet (ví, voucher, đổi quà, heatmap, insight, biểu đồ "
             "phễu); xuất CSV lịch sử giao dịch; export dữ liệu đối soát.",
             "Mang số liệu ra ngoài để báo cáo nội bộ / lưu trữ."),
        ],
    },
    {
        "title": "Theme 5 — Tự động hoá & Nền tảng tin cậy (chạy nền)",
        "col": "HỆ THỐNG LÀM GÌ",
        "features": [
            ("Tự động đồng bộ catalog từ đối tác", UPD,
             "Tiến trình nền tự nạp danh mục/thương hiệu gộp từ mọi kết nối đang hoạt động, rồi tự kéo "
             "kho quà về cho toàn bộ account đang kết nối đối tác đó (không cần khách bấm tay); account "
             "vừa kết nối được kéo quà ngay.",
             "Catalog luôn cập nhật hàng mới/giá mới mà khách không phải thao tác, cho mọi đối tác."),
            ("Tự rà soát quà & danh mục/thương hiệu rỗng", UPD,
             "Worker tự quét dữ liệu quà theo danh mục và thương hiệu; tự ẩn danh mục/thương hiệu khi "
             "không còn quà khả dụng và tự hiển thị lại khi có quà trở lại, theo từng account. Có bộ chốt "
             "an toàn: lượt đồng bộ lỗi một phần thì <b>không</b> dọn kho cũ.",
             "Tránh để user thấy danh mục/thương hiệu trống rỗng — trải nghiệm sạch, chuyên nghiệp; một "
             "lượt đồng bộ chập chờn không làm biến mất kho quà."),
            ("Tự đồng bộ trạng thái voucher qua webhook", None,
             "Nhận webhook từ GotIt và tự cập nhật trạng thái voucher (đã dùng / hết hạn / huỷ / tách). "
             "UrBox không có cơ chế báo lại — user tự đánh dấu (xem Theme 3).",
             "Voucher của user luôn phản ánh đúng thực tế mà không cần thao tác thủ công.",
             GOTIT),
            ("Tự phục hồi đơn kẹt", UPD,
             "Mỗi 5 phút quét các đơn PENDING, hỏi lại đối tác theo cách phù hợp (UrBox: gửi lại cùng mã "
             "giao dịch, idempotent; GotIt: tra trạng thái giao dịch) và kiểm tra đơn có tồn tại phía đối "
             "tác trước khi kết luận → tự hoàn tất hoặc hoàn điểm. Đơn hỏi mãi không rõ kết quả → "
             "<b>treo chờ người kiểm</b>, không tự hoàn điểm theo đồng hồ.",
             "Đơn lỗi mạng/đối tác không bị “treo” và không mất điểm của user; không huỷ oan đơn mà "
             "đối tác đã phát mã — giảm ticket CSKH và tranh chấp đối soát."),
            ("Chống trùng đơn (Idempotency)", None,
             "Lưu khoá chống trùng cho mỗi yêu cầu đổi quà (TTL 24h), tự dọn định kỳ.",
             "Bấm nhiều lần / lỗi mạng cũng không tạo đơn trùng, không trừ điểm 2 lần."),
            ("Tích hợp điểm CNV Loyalty", None,
             "Khi đổi quà, hệ thống giữ điểm (hold) → chỉ trừ thật (accept) khi voucher phát thành công, "
             "ngược lại hoàn điểm (deny).",
             "Điểm của user chỉ bị trừ khi đổi thành công — công bằng, minh bạch, ít khiếu nại."),
            ("Công cụ xử lý đơn cho đội vận hành CNV", NEW,
             "Trên CRM nội bộ, người trực tra cứu đơn của mọi đối tác (kể cả đơn quà vật lý), chốt đơn "
             "đang chờ theo đúng kết quả đối tác trả về (bắt buộc ký RSA, ghi nhật ký), chạy lại tác vụ "
             "hoàn/trừ điểm bị lỗi và xử lý hàng loạt.",
             "Ticket của khách được xử lý ngay, không chờ nhịp worker; không can thiệp tay vào dữ liệu."),
        ],
    },
    {
        "title": "Theme 6 — Quà vật lý (Physical Gift)",
        "col": "AI & LÀM GÌ",
        "badge": UPD,
        "break": True,
        "intro": (
            "Quà vật lý cho phép người dùng đổi điểm lấy <b>sản phẩm thật</b> (điện thoại, đồ gia dụng, phụ "
            "kiện…) và được giao tận nơi đến địa chỉ đăng ký. Khác với e-voucher, quà vật lý có thêm bước "
            "nhập địa chỉ nhận hàng và theo dõi trạng thái giao hàng. Nguồn quà từ cả hai đối tác: <b>GotIt</b> "
            "(theo từng chương trình/campaign, nhiều thương hiệu như Aukey, Philips, Starbucks, Thế Giới Di "
            "Động…) và <b>UrBox</b> (quà vật lý nằm chung kho với e-voucher). Trải nghiệm của khách và cách "
            "vận hành là một, bất kể quà đến từ đối tác nào."
        ),
        "highlights": [
            "Kết nối kho quà vật lý của cả hai đối tác: GotIt theo campaign (hỗ trợ sản phẩm gắn thương "
            "hiệu riêng của doanh nghiệp), UrBox đồng bộ chung với kho e-voucher.",
            "Khách đổi điểm ngay trên Zalo Mini App, nhập địa chỉ nhận hàng và được giao tận nơi qua đối "
            "tác vận chuyển — cùng một trải nghiệm cho cả hai đối tác.",
            "Theo dõi hành trình đơn hàng xuyên suốt: Đang xử lý → Đang giao → Đã giao, cập nhật trực "
            "tiếp trên Mini App; theo dõi được từng kiện hàng trong đơn để hỗ trợ khi khách phản hồi.",
            "Bảo mật dữ liệu cá nhân: có màn hình xin đồng ý chia sẻ thông tin trước khi khách nhập địa "
            "chỉ, tuân thủ Nghị định 13/2023 về bảo vệ dữ liệu cá nhân.",
            "Tự động đồng bộ danh mục quà & tồn kho; bộ địa giới hành chính chuẩn 2 cấp (tỉnh/phường sau "
            "sáp nhập) dùng chung, tự ánh xạ sang mã khu vực của từng đối tác.",
            "Vận hành tin cậy: chống phát sinh đơn trùng, đảm bảo điểm chỉ trừ khi đơn được tạo thành "
            "công, tự động dò soát và phục hồi các giao dịch còn treo.",
            "Hỗ trợ đối soát với đối tác theo từng chương trình, phục vụ vận hành và nghiệp vụ kế toán.",
        ],
        "features": [
            ("Kết nối kho quà vật lý của đối tác", UPD,
             "<b>Quản trị viên:</b> <b>GotIt</b> — nhập Campaign ID (GotIt cấp qua email) → Thêm campaign → "
             "Đồng bộ quà vật lý; hỗ trợ sản phẩm gắn thương hiệu riêng của doanh nghiệp theo từng chương "
             "trình. <b>UrBox</b> — không cần campaign riêng, quà vật lý về cùng lượt đồng bộ với e-voucher "
             "và combo. Quà vật lý tự gắn nhãn “Giao tận nơi” và lọc được theo loại.",
             "Mở rộng kho thưởng sang sản phẩm thật từ hai nguồn; chủ động tổ chức quà theo chương trình "
             "mà không thêm thao tác vận hành."),
            ("Đổi điểm lấy quà vật lý trên Zalo Mini App", UPD,
             "<b>User cuối:</b> Chọn quà gắn nhãn “Giao tận nơi” (icon xe tải xanh), chọn số lượng, đổi "
             "điểm ngay trên Zalo Mini App rồi nhập/chọn địa chỉ nhận hàng để được giao tận nơi qua đối tác "
             "vận chuyển — cùng một luồng cho quà của mọi đối tác.",
             "Đổi quà thật liền mạch ngay trên Zalo, không cần app riêng; nhận hàng tận nơi."),
            ("Đặt đơn giao hàng với đối tác", NEW,
             "<b>Hệ thống:</b> Gửi thẳng địa chỉ nhận hàng (tỉnh/phường 2 cấp, địa chỉ chi tiết, người "
             "nhận, số điện thoại, ghi chú) sang đối tác khi tạo đơn; mỗi đơn vị quà là một kiện riêng có "
             "serial. Kiểm tra tồn kho, khu vực đối tác có giao và credential <b>trước khi giữ điểm</b>.",
             "Khách không bị giữ điểm cho đơn chắc chắn không tạo được; mỗi kiện có dấu vết riêng để hỗ "
             "trợ."),
            ("Ngày giao dự kiến", NEW,
             "<b>User cuối:</b> Màn xác nhận đổi hiển thị khoảng ngày dự kiến nhận hàng, tính theo ngày "
             "làm việc — bỏ Thứ 7, Chủ nhật và các ngày lễ chính thức của Việt Nam (kể cả Tết, Giỗ Tổ theo "
             "âm lịch).",
             "Khách có kỳ vọng đúng về thời gian nhận hàng, giảm hỏi han CSKH."),
            ("Theo dõi hành trình đơn hàng", NEW,
             "<b>User cuối:</b> Theo dõi đơn xuyên suốt Đang xử lý → Đang giao → Đã giao, cập nhật trực "
             "tiếp trên Mini App; xem timeline theo mã vận chuyển và theo dõi từng kiện hàng trong đơn "
             "(mã …-01).",
             "Minh bạch trạng thái giao hàng; dễ tra cứu & hỗ trợ khi khách phản hồi về từng kiện."),
            ("Tự động cập nhật trạng thái giao hàng", NEW,
             "<b>Hệ thống:</b> Mỗi 2 giờ hỏi đối tác trạng thái từng kiện và quy về <b>một bộ trạng thái "
             "chung</b> (chờ xử lý, đang giao, đã giao, trả hàng, huỷ) dù quà đến từ GotIt hay UrBox; tự "
             "tổng hợp trạng thái cấp đơn (hoàn tất / giao một phần / thất bại); dừng theo dõi khi mọi kiện "
             "kết thúc.",
             "Khách và quản trị viên nhìn cùng một bộ trạng thái cho mọi đối tác."),
            ("Cập nhật trạng thái giao hàng tức thì", NEW,
             "<b>Đội vận hành CNV:</b> Trên CRM bấm hỏi đối tác ngay khi khách gọi (từng đơn hoặc hàng "
             "loạt tới 200 đơn), xem lịch sử đổi trạng thái của đơn; thao tác chỉ ghi trạng thái, không "
             "đụng điểm/tiền.",
             "Không phải chờ nhịp cập nhật 2 giờ khi khách hỏi “hàng tới đâu rồi”; phục vụ đối soát cuối "
             "tháng."),
            ("Đồng ý chia sẻ & bảo mật dữ liệu cá nhân", NEW,
             "<b>User cuối:</b> Xác nhận màn hình xin đồng ý chia sẻ thông tin trước khi nhập địa chỉ nhận "
             "hàng.",
             "Tuân thủ Nghị định 13/2023 về bảo vệ dữ liệu cá nhân; bảo vệ thông tin người nhận, tăng "
             "niềm tin."),
            ("Địa giới hành chính chuẩn dùng chung", UPD,
             "<b>Hệ thống:</b> Bộ địa giới hành chính 2 cấp (Tỉnh/Thành → Phường/Xã sau sáp nhập) dùng "
             "chung cho mọi đối tác, tự ánh xạ sang mã khu vực riêng của GotIt và UrBox (UrBox: 34 tỉnh, "
             "3.321 phường/xã); danh mục quà & tồn kho GotIt tự đồng bộ theo từng chương trình.",
             "Khách nhập địa chỉ một lần, giao được qua bất kỳ đối tác nào; catalog & tồn kho luôn đúng "
             "theo chương trình."),
            ("Vận hành tin cậy cho đơn quà vật lý", UPD,
             "<b>Hệ thống:</b> Chống phát sinh đơn trùng; chỉ trừ điểm khi đơn được tạo thành công; tự "
             "động dò soát và phục hồi các giao dịch còn treo; đơn chưa rõ kết quả được giữ cho worker xác "
             "minh lại với đối tác, chỉ hoàn điểm khi đối tác xác nhận đơn không tồn tại.",
             "Không trừ nhầm hay trừ 2 lần điểm; đơn lỗi không bị “treo”; không huỷ oan đơn đã được đối "
             "tác nhận — giảm khiếu nại & ticket CSKH."),
            ("Đối soát quà vật lý theo chương trình", NEW,
             "<b>Quản trị viên:</b> Đối soát với đối tác theo từng chương trình (campaign).",
             "Phục vụ vận hành & nghiệp vụ kế toán; minh bạch tài chính theo từng chương trình.",
             GOTIT),
        ],
    },
]

CSS = """
@page {
  size: A4;
  margin: 14mm 13mm 16mm 13mm;
  @bottom-center {
    content: "CNV Reward V2 — Tổng quan tính năng · Trang " counter(page) "/" counter(pages);
    font-family: "DejaVu Sans";
    font-size: 7.5pt;
    color: #7A8794;
  }
}
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans"; font-size: 8.6pt; color: #1F2A37; line-height: 1.38; margin: 0; }
b { font-weight: bold; }
.cover { border-left: 6px solid #F0A020; padding: 2px 0 2px 14px; margin-bottom: 12px; }
.cover h1 { font-size: 22pt; color: #0F3D6B; margin: 0 0 4px 0; font-weight: bold; letter-spacing: -0.2pt; }
.cover h2 { font-size: 12.5pt; color: #1F2A37; margin: 0 0 4px 0; font-weight: bold; }
.cover .meta { font-size: 8pt; color: #6B7A8A; }
.intro { font-size: 8.6pt; color: #2B3A4A; margin: 0 0 14px 0; }
.theme { margin-top: 10px; page-break-inside: auto; }
.theme.break { page-break-before: always; margin-top: 0; }
.theme-head {
  background: #0F3D6B; color: #fff; border-radius: 5px; padding: 7px 12px;
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 7px;
  page-break-after: avoid;
}
.theme-head .t { font-size: 11.5pt; font-weight: bold; }
.theme-head .r { white-space: nowrap; }
.pill {
  display: inline-block; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.55);
  color: #fff; border-radius: 10px; padding: 1px 9px; font-size: 7.5pt; font-weight: bold; margin-left: 6px;
}
.badge-h { display: inline-block; background: #F0A020; color: #0F3D6B; border-radius: 3px;
  padding: 1px 6px; font-size: 7pt; font-weight: bold; margin-left: 6px; }
.theme-intro { margin: 2px 0 8px 0; color: #2B3A4A; }
.hl { background: #F5F8FC; border: 1px solid #DBE6F2; border-radius: 5px; padding: 8px 12px 6px 12px; margin: 0 0 10px 0;
  page-break-inside: avoid; }
.hl .hl-t { color: #0F3D6B; font-weight: bold; font-size: 9pt; margin-bottom: 4px; }
.hl ul { margin: 0; padding-left: 14px; }
.hl li { margin: 0 0 3px 0; }
table { width: 100%; border-collapse: collapse; margin-bottom: 6px; }
thead { display: table-header-group; }
th { background: #E8EEF6; color: #0F3D6B; font-size: 7pt; font-weight: bold; text-align: left;
  padding: 6px 7px; letter-spacing: 0.3pt; border-bottom: 1px solid #C9D6E5; }
td { padding: 7px 7px; vertical-align: top; border-bottom: 1px solid #E6ECF3; }
tr { page-break-inside: avoid; }
td.no { width: 5%; color: #0F3D6B; font-weight: bold; }
td.name { width: 21%; font-weight: bold; color: #1F2A37; }
td.what { width: 42%; }
td.ben { width: 32%; color: #2B3A4A; }
.badge { display: inline-block; border-radius: 3px; padding: 0 5px; font-size: 6.5pt; font-weight: bold;
  margin-left: 4px; vertical-align: 1px; white-space: nowrap; }
.badge.new { background: #0F3D6B; color: #fff; }
.badge.upd { background: #F0A020; color: #0F3D6B; }
.vendor { display: inline-block; border: 1px solid #0F3D6B; color: #0F3D6B; border-radius: 3px;
  padding: 0 4px; font-size: 6.5pt; font-weight: bold; margin-left: 4px; vertical-align: 1px; white-space: nowrap; }
.foot-note { margin-top: 14px; font-size: 7.5pt; color: #7A8794; border-top: 1px solid #E6ECF3; padding-top: 6px; }
"""


def badge(b):
    if not b:
        return ""
    cls = "new" if b == NEW else "upd"
    return f' <span class="badge {cls}">{html.escape(b)}</span>'


def render():
    total = sum(len(t["features"]) for t in THEMES)
    parts = [f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8">
<title>CNV Reward V2 — Tổng quan tính năng sản phẩm</title>
<style>{CSS}</style></head><body>
<div class="cover">
  <h1>CNV Reward V2</h1>
  <h2>Tổng quan tính năng sản phẩm</h2>
  <div class="meta">Phạm vi: tính năng dành cho Khách hàng (Account) &amp; Người dùng cuối · Cập nhật: {UPDATED} · {total} tính năng</div>
</div>
<p class="intro">{INTRO}</p>
"""]
    n = 0
    for t in THEMES:
        cnt = len(t["features"])
        head_badge = f'<span class="badge-h">{html.escape(t["badge"])}</span>' if t.get("badge") else ""
        cls = "theme break" if t.get("break") else "theme"
        parts.append(f"""<div class="{cls}">
<div class="theme-head"><div class="t">{html.escape(t["title"])}</div>
<div class="r"><span class="pill">{cnt} tính năng</span>{head_badge}</div></div>
""")
        if t.get("intro"):
            parts.append(f'<p class="theme-intro">{t["intro"]}</p>')
        if t.get("highlights"):
            items = "".join(f"<li>{h}</li>" for h in t["highlights"])
            parts.append(f'<div class="hl"><div class="hl-t">★ Điểm nổi bật của tính năng Quà vật lý</div><ul>{items}</ul></div>')
        parts.append(f"""<table><thead><tr><th>#</th><th>TÍNH NĂNG</th><th>{html.escape(t["col"])}</th><th>LỢI ÍCH</th></tr></thead><tbody>""")
        for row in t["features"]:
            name, b, what, ben = row[:4]
            vendor = row[4] if len(row) > 4 else None
            vtag = f' <span class="vendor">{html.escape(vendor)}</span>' if vendor else ""
            n += 1
            parts.append(f'<tr><td class="no">{n}</td><td class="name">{html.escape(name)}{vtag}{badge(b)}</td>'
                         f'<td class="what">{what}</td><td class="ben">{ben}</td></tr>')
        parts.append("</tbody></table></div>")
    parts.append(f'<div class="foot-note">Tài liệu tổng quan tính năng CNV Reward V2 — cập nhật {UPDATED}. '
                 f'Nhãn <b>Mới</b> / <b>Mở rộng</b> đánh dấu các tính năng bổ sung hoặc thay đổi ở đợt cập nhật '
                 f'tháng 09–10/2026 (quà vật lý và tích hợp UrBox). Tính năng không ghi chú đối tác áp dụng chung cho '
                 f'cả GotIt và UrBox; nhãn <span class="vendor">GotIt</span> / <span class="vendor">UrBox</span> = chỉ đối tác đó hỗ trợ.</div>')
    parts.append("</body></html>")
    return "".join(parts)


def main():
    doc = render()
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(doc)
    from weasyprint import HTML
    HTML(string=doc, base_url=HERE).write_pdf(OUT_PDF)
    print("HTML:", OUT_HTML)
    print("PDF :", OUT_PDF)


if __name__ == "__main__":
    main()
