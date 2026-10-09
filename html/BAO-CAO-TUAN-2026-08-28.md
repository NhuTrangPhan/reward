# Báo cáo tuần 24–28/08/2026

**Người báo cáo:** Hải (haiht1) — **Dự án:** Reward V2 (rewards-v2, cdp-frontend, mini-app)

## Tóm tắt

Tuần này thay đổi một quyết định quan trọng trong luồng đổi quà: đơn hỏi nhà cung cấp mãi không rõ kết quả thì **treo chờ người kiểm** thay vì tự hoàn điểm cho khách sau 24 giờ. Cách cũ có thể huỷ oan đơn mà nhà cung cấp đã xuất mã — khách được hoàn điểm, mã thành mồ côi, công ty vẫn phải trả tiền. Đi kèm là bộ công cụ cho người trực xử lý các đơn treo đó ngay trên CRM.

Ngoài ra sửa một lỗi làm voucher vô thời hạn của UrBox bị đóng dấu hạn 30 ngày, và dọn nốt một bản sao mã voucher còn nằm trần trong cơ sở dữ liệu.

Phần bảo mật voucher làm hai tuần trước đã được duyệt và lên staging ngày 25/08.

## Công việc đã hoàn thành

**1. Đơn không rõ kết quả thì treo chờ người, thôi tự hoàn điểm theo đồng hồ (việc lớn nhất tuần)**

Trước đây đơn treo quá 24 giờ bị tự động chốt là thất bại và hoàn điểm cho khách. Vấn đề là "quá 24 giờ" không chứng minh được đơn hỏng: nhà cung cấp có thể chỉ đang chậm, hoặc chính worker của mình mới là thứ hỏng — pod chết, mất mạng, thiếu cấu hình khoá ký — trong khi đồng hồ vẫn chạy và số lần thật sự hỏi nhà cung cấp bằng không.

- **Ngưỡng nay đếm số lượt thật sự hỏi nhà cung cấp, không đếm giờ.** Hết lượt mà vẫn chưa có kết luận thì đơn chuyển sang trạng thái "chờ kiểm tra": giữ nguyên điểm và tiền đang giữ, chờ người kiểm hoặc đối soát cuối tháng. Nhà cung cấp trả lỗi dứt khoát thì vẫn hoàn điểm ngay như cũ.
- **Ba lối ra cho đơn treo, dùng được cho mọi loại đơn:** hỏi lại nhà cung cấp, đưa về hàng đợi (có bản xử lý hàng loạt, dùng khi nhà cung cấp sập vài giờ rồi sống lại), và chốt hỏng theo kết luận của người kiểm với lý do bắt buộc ghi rõ.
- **Ngưỡng hạ từ 24 xuống 12 lượt**, tương đương khoảng 1 giờ thay vì 4 giờ, để người trực biết có sự cố sớm hơn. Treo đơn không hoàn điểm và không mất mã bên nhà cung cấp nên việc hạ ngưỡng chỉ đổi thời điểm người vào nhìn, không đổi rủi ro tiền.
- **Hiển thị đúng ở cả ba phía:** mini-app vẫn giữ đơn trong danh sách đang xử lý nhưng bỏ câu hứa "ưu đãi sẽ xuất hiện sau ít phút" và ngừng gọi lại liên tục, vì đơn ở trạng thái này không còn tiến trình tự động nào; màn lịch sử đổi quà trên CRM có nhãn "Chờ kiểm tra" màu cảnh báo, thay vì vẽ như đơn đã thành công khiến người trực đóng đơn nhầm.
- **Bỏ hứa suông về hoàn điểm.** Đơn không có bản ghi giữ điểm thì không có gì để huỷ bên hệ thống loyalty, nên thông báo "điểm sẽ được hoàn tự động" là sai đúng vào nhóm đơn cần cứu nhất. Nay hệ thống cảnh báo rõ là phải xử lý tay.

**2. Công cụ cho người trực chốt đơn ngay trên CRM**

- Thêm chức năng chốt tay đơn đang chờ: hỏi lại nhà cung cấp và chốt đơn ngay, không phải đợi worker chạy vòng 5 phút. Dùng lại đúng luồng xử lý của worker chứ không viết luồng thứ hai, vì việc chốt đơn đụng cả voucher, số dư lẫn điểm khách — hai bản cài đặt song song sẽ trôi lệch nhau, mà lệch ở đây nghĩa là tiền. Có 5 điều kiện an toàn, khoá chống chạy đua với worker, bắt buộc ký RSA như các thao tác duyệt tiền khác, và ghi nhật ký ai bấm đơn nào kết quả ra sao.
- **Sửa một lỗi chỉ lộ ra khi chạy thật:** chốt tay đơn UrBox luôn ra kết quả thất bại, kể cả đơn mà nhà cung cấp đã phát mã. Nguyên nhân là thiếu một dòng cấu hình khoá ký ở phía CRM, khiến lỗi cấu hình của mình bị hệ thống diễn giải thành phán quyết "đơn hỏng" rồi hoàn điểm cho khách trong khi nhà cung cấp vẫn tính tiền. Kèm theo phát hiện nhật ký thao tác đang ghi lỗi im lặng nên không còn dấu vết ai bấm gì.
- Bổ sung tra cứu đơn quà vật lý GotIt trên màn tra cứu. Trước đây gọi nhầm sang đường tra voucher điện tử nên đơn vật lý luôn báo "mã giao dịch không hợp lệ", trông như đơn hỏng.

**3. Voucher vô thời hạn bị đóng dấu hạn 30 ngày**

UrBox báo voucher vô hạn bằng một quy ước riêng, nhưng tầng lưu trữ của mình hiểu nhầm thành "nhà cung cấp không cho biết hạn" nên tự gán mặc định 30 ngày. Hậu quả nhìn thấy ở phía khách: qua ngày thứ 31 voucher rơi vào mục "Hết hạn" và khách không dùng nữa, trong khi mã vẫn còn nguyên giá trị bên nhà cung cấp.

Kèm hai lỗi hiển thị liên quan: bộ lọc "Sắp hết hạn" đưa voucher vô thời hạn lên đầu danh sách, và mini-app bỏ trống dòng hạn sử dụng hoặc hiện câu cụt "có giá trị từ ngày ... đến —" ở màn đổi thành công.

**4. Dọn bản sao mã voucher còn nằm trần trong cơ sở dữ liệu**

Phát hiện cột lưu định danh voucher phía nhà cung cấp của GotIt thực chất đang chép nguyên văn mã voucher — 174 trên 174 dòng. Cột mã voucher đã được mã hoá, cột này thì không, nên mỗi dòng như vậy là một bản sao mã nằm trần ngay cạnh cột vừa mã hoá, làm việc mã hoá vô nghĩa với đúng những dòng đó. Nay hệ thống ghi đúng định danh do nhà cung cấp cấp; dữ liệu cũ dọn bằng một câu SQL khi deploy.

**5. Củng cố worker và bổ sung test**

- Làn quét đơn quà vật lý trước đây không có giới hạn số đơn mỗi lượt, tồn đọng lớn là kéo cả bảng vào bộ nhớ mỗi 5 phút và làm trễ luôn khâu xử lý điểm của các đơn khác. Đã thêm giới hạn và đẩy bộ lọc xuống tầng cơ sở dữ liệu — nếu chỉ thêm giới hạn mà vẫn lọc ở tầng ứng dụng thì lượt quét sẽ chạy không tải mà log vẫn báo đã lấy đủ.
- Bổ sung test cho những chỗ "hỏng thì im lặng" trước đây chưa ai canh, trong đó có hai hàng rào mà một chữ số gõ nhầm trong cấu hình là đủ để tắt toàn bộ cơ chế tự động cứu đơn mà không báo gì. Các test quan trọng đều được nghiệm bằng cách phá code để xác nhận test bắt được lỗi.

## Khối lượng và chất lượng

22 commit trên 3 repository, 58 file thay đổi, khoảng 4.300 dòng thêm và 1.100 dòng bớt. 15 lớp test được thêm mới hoặc cập nhật; bộ test của rewards-v2 hiện khoảng 1.790 ca. Hai lỗi nghiêm trọng tuần này được phát hiện khi chạy thật trên môi trường local chứ không phải từ test, nên đã bổ sung test khoá lại cả hai.

## Trạng thái triển khai

- **Đã lên staging:** phần bảo mật voucher (mã hoá mã voucher trong cơ sở dữ liệu), được duyệt và merge ngày 25/08.
- **Chờ lên staging:** ba nhánh của tuần này — đơn treo chờ kiểm, công cụ chốt đơn cho CRM, và dọn cột định danh voucher. Đã gộp vào nhánh chung chiều 28/08.

## Vướng mắc, cần lưu ý

- Phần đơn treo **phải deploy đồng thời rewards-v2, mini-app và CRM**. Nếu chỉ lên backend thì đơn ở trạng thái mới sẽ biến mất khỏi màn khách và bị CRM hiển thị như đơn đã thành công — người trực đọc xong đóng đơn nhầm.
- Dữ liệu voucher UrBox cũ đã bị gán sai hạn 30 ngày **chưa được xử lý**. Cần rà và sửa; bảng log chỉ giữ 90 ngày nên số đếm được sẽ là con số tối thiểu, có thể còn nhiều hơn.
- Việc dọn cột định danh voucher của dữ liệu cũ chạy bằng SQL tay lúc deploy, không gấp vì không chức năng nào đọc cột này.

## Kế hoạch tuần tới

1. Đưa ba nhánh còn lại lên staging và hỗ trợ deploy.
2. Rà soát và sửa dữ liệu voucher UrBox bị gán sai hạn sử dụng.
3. Theo dõi số đơn rơi vào trạng thái chờ kiểm sau khi lên staging, để điều chỉnh ngưỡng 12 lượt cho sát thực tế.
