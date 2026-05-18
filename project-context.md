# Project Context — rewards-v2
> AI: Đọc file này TRƯỚC KHI đọc code. File này là index giúp biết đi đâu tìm gì.
> Cập nhật lần cuối: 2026-04-17

---

## 1. Module Map

| Module | Package gốc | Chức năng |
|--------|-------------|-----------|
| `domain` | `com.cnv.rewards.domain` | Shared: ApiResponse, enums, DTOs, exceptions, models, utils |
| `jpa` | `com.cnv.rewards.jpa` | Entity + Repository + Service (DB layer). Mọi module khác chỉ được gọi JPA Service, KHÔNG gọi Repository |
| `urbox-integration` | `com.cnv.rewards.urbox_integration` | HTTP client gọi Urbox API (UrboxService). KHÔNG inject JPA dependencies |
| `gotit-integration` | `com.cnv.rewards.gotit_integration` | HTTP client gọi GotIt API (GotItService). KHÔNG inject JPA dependencies |
| `internal-api` | `com.cnv.rewards.internal_api` | REST API + Business logic, port 9090 |
| `worker-sync-urbox-*` | — | Cron job (CommandLineRunner) đồng bộ data Category/Brand/Reward từ Urbox |
| `worker-sync-gotit-*` | — | Cron job tách theo 4 phase: sync category, sync brand, sync category-brand mapping, sync product |
| `worker-recovery-pending-order` | — | Long-running pod với Spring `@Scheduled(fixedDelay=5m)`, recover order PENDING stuck do vendor timeout — retry vendor + resolve SUCCESS/FAILED |
| `worker-cleanup-idempotency-key` | — | One-shot CronJob (1 lần/ngày, K8s schedule), xóa idempotency key > TTL 24h khỏi bảng `idempotency_key` |

---

## 2. Entity → Mapping Method → Domain Model

Mỗi Entity đều `extends BaseEntity` (id, createdAt, updatedAt) và có method mapping sang domain model.

| Entity | Mapping Method | → Domain Model |
|--------|---------------|----------------|
| AccountEntity | toAccount() | Account |
| AccountConfigEntity | toAccountConfig() | AccountConfig |
| AccountBrandConfigEntity | toAccountBrandConfig() | AccountBrandConfig |
| AccountCategoryConfigEntity | toAccountCategoryConfig() | AccountCategoryConfig |
| AccountVendorApiKeyEntity | toAccountVendorApiKey() | AccountVendorApiKey |
| AccountVendorMappingEntity | toAccountVendorMapping() | AccountVendorMapping |
| RewardItemEntity | toRewardItem() | RewardItem |
| RewardBrandEntity | toRewardBrand() | RewardBrand |
| RewardCategoryEntity | toRewardCategory() | RewardCategory |
| RedemptionOrderEntity | toRedemptionOrder() | RedemptionOrder (+ pointsHoldId field cho recovery) |
| VoucherEntity | toVoucher() | Voucher |
| VendorEntity | toVendor() | Vendor |
| UserEntity | toUser() | User |
| UrBoxBrandEntity | toUrBoxBrand() | UrBoxBrand |
| UrBoxCategoryEntity | toUrBoxCategory() | UrBoxCategory |
| UrBoxOfficeEntity | toUrBoxOffice() | UrBoxOffice |
| UrBoxRewardItemEntity | toUrBoxRewardItem() | RewardItem |
| GotItBrandEntity | toGotItBrand() | GotItBrand |
| GotItCategoryEntity | toGotItCategory() | GotItCategory |
| GotItRewardItemEntity | toGotItRewardItem() | RewardItem |
| VendorCategoryMappingEntity | toProviderCategoryMapping() | ProviderCategoryMapping |
| VendorBrandMappingEntity | toProviderBrandMapping() | ProviderBrandMapping |
| CategoryBrandMappingEntity | — | — |
| AccountBalanceEntity | toAccountBalance() | AccountBalance |
| BalanceTransactionEntity | toBalanceTransaction() | BalanceTransaction |
| BalanceHoldEntity | toBalanceHold() | BalanceHold |
| TopUpRequestEntity | toTopUpRequest() | TopUpRequest |
| RecoveryTaskEntity | toRecoveryTask() | RecoveryTask |
| IdempotencyKeyEntity | — | — (internal-only, không expose) |

---

## 3. JPA Services

Các service trong `jpa/service/` — một số extends BaseService (có helper Specification/Filter), một số không.

| JPA Service | Extends BaseService | Chức năng chính |
|-------------|-------------------|----------------|
| AccountService | Không | CRUD Account |
| AccountConfigService | Không | Config per account |
| AccountBrandConfigService | **Có** | Enable/disable brand per account (có BaseObjectFilter) |
| AccountCategoryConfigService | **Có** | Enable/disable category per account (có BaseObjectFilter) |
| AccountVendorApiKeyService | Không | CRUD API key per account+vendor |
| AccountVendorMappingService | Không | Account ↔ Vendor mapping |
| RedemptionLogicService | Không | **Core**: createPendingOrder, finalizeSuccessOrder, markOrderFailed (tất cả @Transactional) |
| RedemptionOrderService | **Có** | Query orders (có BaseObjectFilter) |
| RewardItemService | **Có** | Query reward items (có BaseObjectFilter) |
| RewardBrandService | Không | CRUD brand |
| RewardCategoryService | Không | CRUD category |
| CategoryBrandMappingService | Không | RewardCategory ↔ RewardBrand mapping (many-to-many) |
| VoucherService | **Có** | Query vouchers (có BaseObjectFilter) |
| VendorService | Không | CRUD vendor |
| VendorListService | Không | Aggregated vendor list + installation status |
| VendorBrandMappingService | Không | Vendor ↔ Brand mapping |
| VendorCategoryMappingService | Không | Vendor ↔ Category mapping |
| UrBoxBrandService | Không | Mirror data |
| UrBoxCategoryService | Không | Mirror data |
| UrBoxRewardItemService | Không | Mirror data |
| GotItBrandService | Không | Mirror data |
| GotItCategoryService | Không | Mirror data |
| GotItRewardItemService | Không | Mirror data |
| UserService | Không | CRUD user |
| AccountBalanceService | **Có** | Balance per account (DEPOSIT/CREDIT) + pessimistic lock |
| BalanceTransactionService | **Có** | Sổ cái CRM (TOP_UP, PAYMENT, ADJUSTMENT) — append-only |
| BalanceHoldService | **Có** | Hold/capture/release tiền cho đổi quà + findByIdForUpdate |
| TopUpRequestService | **Có** | Yêu cầu nạp tiền — CRM admin tạo+duyệt |
| RecoveryTaskService | Không | CRUD RecoveryTask — retry critical failures (ACCEPT_POINTS/DENY_POINTS/CAPTURE_BALANCE/RELEASE_BALANCE) |
| IdempotencyKeyService | Không | CRUD IdempotencyKey + deleteOlderThan(cutoff) cho cleanup 24h |

### Admin services (internal-api, không phải JPA service)
Package `internal-api/service/admin/` — orchestrator cho CRM admin thao tác balance:

| Service | Trách nhiệm |
|---------|-------------|
| AccountBalanceAdminService | setMode (auto create/delete rows, validate balance empty khi xóa), updateCreditLimit, setPostpaidEnabled |
| TopUpAdminService | createPending (account-side), createAndApprove (CRM shortcut), approve (cộng DEPOSIT + ghi TOP_UP transaction), reject |
| PaymentAdminService | recordPayment (giảm CREDIT total + tăng available + ghi PAYMENT transaction, reject over-pay) |

---

## 4. Controller → Endpoint → Service (Consumer-based)

Tổ chức theo 3 nhóm consumer: `user/` (@CurrentUser), `account/` (@CurrentAccount), `crm_admin/` (không auth).

### 4.1 User — prefix `/user/`

| Controller | Base Path | Auth | Business Service |
|------------|-----------|------|-----------------|
| UserRedeemController | `/user/redeem` | @CurrentUser | **RedeemService** |
| UserVoucherController | `/user/vouchers` | @CurrentUser | VoucherService (jpa) |
| UserRewardItemController | `/user/reward-items` | @CurrentUser | RewardItemDetailService, RewardItemService (jpa) |

### 4.2 Account — prefix `/account/`

| Controller | Base Path | Auth | Business Service |
|------------|-----------|------|-----------------|
| AccountRewardItemController | `/account/reward-items` | @CurrentAccount | RewardItemDetailService, RewardItemService (jpa) |
| AccountVoucherController | `/account/vouchers` | @CurrentAccount | VoucherService (jpa) |
| AccountRedemptionOrderController | `/account/redemption-orders` | @CurrentAccount | RedemptionOrderService (jpa) |
| AccountVendorMappingController | `/account/vendor-mappings` | @CurrentAccount | VendorMappingConnectionService, VendorListService (jpa) |
| AccountAccountConfigController | `/account/account-configs` | @CurrentAccount | AccountConfigService (jpa) |
| AccountBrandConfigController | `/account/brand-configs` | @CurrentAccount | AccountBrandConfigService (jpa) |
| AccountCategoryConfigController | `/account/category-configs` | @CurrentAccount | AccountCategoryConfigService (jpa) |
| AccountApiKeyController | `/account/api-key` | @CurrentAccount | AccountVendorApiKeyService (jpa) |
| AccountPointExchangeConfigController | `/account/point-exchange-config` | @CurrentAccount | PointExchangeConfigService |

### 4.3 CRM Admin — prefix `/crm-admin/`

| Controller | Base Path | Auth | Business Service |
|------------|-----------|------|-----------------|
| CrmAdminAccountController | `/crm-admin/accounts` | — | AccountService (jpa) |
| CrmAdminInquiryController | `/crm-admin/inquiry` | — | OrderInquiryService |
| CrmAdminAccountBalanceController | `/crm-admin/accounts/{id}/balance` | — | AccountBalanceAdminService — GET balance/transactions/holds + PUT mode/credit-limit/postpaid |
| CrmAdminTopUpController | `/crm-admin/top-up-requests` | @CurrentAdminUserId | TopUpAdminService — create (+ autoApprove), approve, reject, list |
| CrmAdminPaymentController | `/crm-admin/payments` | @CurrentAdminUserId | PaymentAdminService — record payment cho CREDIT debt |
| AccountTopUpController | `/account/top-up-requests` | @CurrentAccount | TopUpAdminService.createPending — account tạo PENDING |

---

## 5. Design Patterns — Luồng chính

### Redeem Flow (Quan trọng nhất) — support 3 balance modes
```
RedeemController (@CurrentUser)
  → RedeemService (Orchestrator, KHÔNG @Transactional)
    → validateRequest + validateVendorConnection (dùng AccountVendorMappingService, KHÔNG repo)
    → VendorRedeemStrategyFactory.getStrategy(vendorCode) + strategy.generateTransactionId()
    → pointExchangeConfigService.calculatePointsForPrice() → pointsRequired
    → balanceCheckService.calculateSplit(account, totalCost) → BalanceSplit  [@Transactional nhỏ]
    → loyaltyPointsClient.getBalance() — pre-check đủ điểm (KHÔNG hold)
    → redemptionLogicService.createPendingOrder(..., depositAmount, creditAmount) [@Transactional]
      ↑ TẠO ORDER TRƯỚC: fail ở đây thì chưa hold gì, throw clean
    → loyaltyPointsClient.holdPoints(transactionId) → pointsHoldId
      ↑ fail → markOrderFailed + throw (chưa hold balance)
    → balanceCheckService.holdBalance(account, split, orderId) → List<holdIds> [@Transactional]
      ↑ fail → denyPointsSafely + markOrderFailed + throw
    → strategy.redeem(context) (ngoài transaction, gọi vendor)
    ├─ SUCCESS:
    │   → redemptionLogicService.finalizeSuccessOrder() [@Transactional, pessimistic lock reward]
    │   → loyaltyPointsClient.acceptHold(pointsHoldId) (critical log nếu fail)
    │   → balanceCheckService.captureOrder(orderId) [@Transactional, iterate all holds]
    └─ FAIL (LogicError / Exception / null result):
        → rollbackHolds(): denyPointsSafely + releaseBalanceOrderSafely + markOrderFailed
```

### Thứ tự trong Redeem Flow — vì sao
- **calculateSplit TRƯỚC createOrder**: split info (depositAmount/creditAmount) phải lưu vào order ngay lúc tạo để audit
- **createOrder TRƯỚC holdPoints**: nếu createOrder fail, chưa hold gì → throw clean, không cần rollback
- **holdPoints TRƯỚC holdBalance**: nếu hold points fail, chỉ cần markOrderFailed; ngược lại thì balance đã thay đổi rồi mới biết thiếu điểm
- **pre-check điểm** (getBalance) trước tất cả: fail fast khi rõ ràng thiếu điểm, không cần tạo order

### Strategy Pattern — 2 bộ Factory
1. **VendorRedeemStrategy** + VendorRedeemStrategyFactory
   - Interface: `supports(VendorCode)`, `validate(RedeemContext)`, `redeem(RedeemContext) → VoucherResult`
   - Implementations: `UrboxRedeemStrategy`, `GotItRedeemStrategy`
   - Vị trí: `internal-api/controller/redemption/strategy/`

2. **VendorDetailSyncStrategy** + VendorDetailSyncStrategyFactory
   - Interface: `supports(VendorCode)`, `syncDetail(RewardItemEntity, AccountEntity)`
   - Implementations: `UrboxDetailSyncStrategy`
   - Vị trí: `internal-api/service/vendor_sync/`
   - Dùng bởi: `RewardItemDetailService.getDetail()` — sync giá/stock từ vendor trước khi trả detail

### Sync Flow (Workers)
```
Worker (CommandLineRunner)
  → UrboxService.getXxx() [HTTP call]
  → Lưu vào Mirror table (UrBoxXxxEntity)
  → Transform → Business table (RewardXxxEntity)
  → Tạo mapping (VendorXxxMappingEntity)
```

### GotIt Sync Flow (many-to-many Brand-Category)
```
worker-sync-gotit-category
  → getCategories()
  → Sync GotItCategoryEntity + RewardCategoryEntity + VendorCategoryMappingEntity

worker-sync-gotit-brand
  → getBrands(page)
  → Sync GotItBrandEntity + RewardBrandEntity + VendorBrandMappingEntity

worker-sync-gotit-mapping
  → getBrandsByCategoryId(%s/categories/%s/brands)
  → Sync CategoryBrandMappingEntity (table: category_brand_mapping)

worker-sync-gotit-product
  → getProducts(page)
  → Sync GotItRewardItemEntity
```

### Auth Annotations
- `@CurrentAccount` → resolve từ header `X-Account-ID` → AccountEntity (resolver: CurrentAccountArgumentResolver)
- `@CurrentUser` → resolve từ header `X-User-ID` → UserEntity (resolver: CurrentUserArgumentResolver)
- `@CurrentAdminUserId` → resolve admin user ID của shop (dùng trong AccountVendorMappingController)
- OpenApiConfig tự detect 3 annotation này để thêm header vào Swagger

---

## 6. Enums (domain/enums/)

| Enum                       | Values |
|----------------------------|--------|
| VendorCode                 | URBOX, GOTIT, ... |
| VendorStatus               | ACTIVE, INACTIVE |
| AccountVendorApiKeyStatus  | ACTIVE, INACTIVE |
| AccountVendorMappingStatus | CONNECTED, DISCONNECTED, ... |
| RedemptionOrderStatus      | PENDING, SUCCESS, FAILED |
| VoucherUsageStatus         | ACTIVE, USED, EXPIRED, ... |
| ReconcileStatus            | PENDING, ... |
| VendorConnectionType       | CNV, PARTNER |
| VendorInstallationStatus   | INSTALLED, NOT_INSTALLED |
| UrBoxRewardItemType        | (mapping urbox gift types) |
| StatusCode                 | (API response codes) |
| AccountConfigKey           | (config key names) |
| BalanceType                | DEPOSIT, CREDIT (per-row trên `account_balance`) |
| AccountBalanceMode         | DEPOSIT, CREDIT, DEPOSIT_AND_CREDIT (suy ra từ tập row tồn tại — KHÔNG lưu column) |
| BalanceHoldStatus          | HOLDING, CAPTURED, RELEASED |
| BalanceTransactionType     | REDEMPTION, TOP_UP, PAYMENT, ADJUSTMENT |
| BalanceTransactionDirection | DEBIT_OUT, CREDIT_IN |
| BalanceRefType             | REDEMPTION_ORDER, TOP_UP_REQUEST, MANUAL |
| RecoveryResultType         | SUCCESS_WITH_VOUCHERS, DEFINITIVE_FAILURE, STILL_PENDING, TRANSIENT_ERROR |
| RecoveryTaskAction         | ACCEPT_POINTS, CAPTURE_BALANCE, RELEASE_BALANCE, DENY_POINTS |
| RecoveryTaskStatus         | PENDING, RETRYING, SUCCESS, FAILED_PERMANENT |

---

## 7. Exceptions (domain/exception/)

| Exception | Mục đích |
|-----------|---------|
| NotFoundException | Resource không tồn tại |
| LogicErrorException | Lỗi business logic (có code + message) |
| LogicErrorException | Lỗi khi redeem (có code + message) |

---

## 8. Urbox Integration (urbox-integration module)

- **UrboxService** — Client duy nhất gọi Urbox HTTP API
- **UrboxSignatureUtil** — Tạo chữ ký Private Key cho request
- **UrboxStatusCodeMapper** — Map mã lỗi Urbox → message (có overload `fromCode(int, String)`)
- DTOs: UrboxGiftItem, UrboxGiftDetail, UrboxRedeemVoucherRequest, UrboxCart, ...

---

## 9. GOTCHAS — Khi làm X, nhớ làm Y

### Thêm/sửa field trong Entity
- [ ] Entity phải extends `BaseEntity`
- [ ] Column dùng snake_case: `@Column(name = "xxx_yyy")`
- [ ] Chỉ dùng `@Getter`, `@Setter` — **KHÔNG dùng @Data**
- [ ] **Phải update mapping method** (`toXxx()`) trong entity — xem bảng ở section 2

### RewardBrand ↔ RewardCategory (many-to-many)
- [ ] Dùng bảng `category_brand_mapping` qua `CategoryBrandMappingEntity`
- [ ] Query brand theo category phải join qua `categoryBrandMappings`
- [ ] Với GotIt: chạy worker theo thứ tự `category` → `brand` → `mapping` → `product`

### Thêm JPA Service mới
- [ ] Nếu cần filter/query phức tạp → extends `BaseService` (có specificationsFromObjectFilter)
- [ ] Nếu service đơn giản → không cần extends BaseService
- [ ] Constructor injection thủ công, KHÔNG dùng @Autowired/@RequiredArgsConstructor

### Thêm Controller endpoint mới
- [ ] Response luôn wrap trong `ApiResponse<T>`
- [ ] Resource có owner → phải kiểm tra `@CurrentAccount` ownership
- [ ] Import class, KHÔNG dùng full-qualified name
- [ ] Nếu endpoint dùng `@CurrentUser` → kiểm tra `OpenApiConfig` đã config chưa

### Thêm vendor mới (integration)
- [ ] Tạo strategy implements `VendorRedeemStrategy` + đăng ký tự động qua Spring (List inject)
- [ ] Tạo strategy implements `VendorDetailSyncStrategy` + đăng ký tự động qua Spring
- [ ] Thêm enum value vào `VendorCode`
- [ ] Module integration KHÔNG được inject JPA dependencies

### Sửa redeem flow
- [ ] `RedeemService` là orchestrator — **KHÔNG có @Transactional**
- [ ] Gọi external API **TRƯỚC** hoặc **NGOÀI** @Transactional method
- [ ] Logic lock + save nằm trong `RedemptionLogicService` (có @Transactional + pessimistic lock)
- [ ] Retry logic: max 3 lần, chỉ retry timeout/network error, KHÔNG retry business error

### Transaction rule
- [ ] **KHÔNG gọi external API trong @Transactional** — làm cạn connection pool
- [ ] Scope transaction PHẢI nhỏ nhất có thể
- [ ] Pattern: API call → validate → rồi mới mở @Transactional để save

### Balance hold/capture/release (BalanceCheckService)
- [ ] Dùng `BalanceHoldService.findByIdForUpdate(holdId)` để load hold (có pessimistic lock) — KHÔNG dùng `findHoldingByRef(REDEMPTION_ORDER, holdId)` (sai: param 2 là refId/orderId, không phải holdId)
- [ ] Capture/Release **idempotent**: check `hold.status` đầu function, skip nếu đã CAPTURED/RELEASED; throw `INVALID_HOLD_STATE` nếu status lạ
- [ ] BalanceTransaction chỉ ghi ở **CAPTURE** (tiền thay đổi thật). KHÔNG ghi ở HOLD hay RELEASE
- [ ] DEPOSIT capture: `total -= amount`, direction = DEBIT_OUT
- [ ] CREDIT capture: `total += amount` (tăng nợ), direction = CREDIT_IN
- [ ] Release: chỉ đổi available/pending, `total` KHÔNG đổi (tiền chưa đi thật)
- [ ] Amount phải > 0 (validate trước khi hold) — throw `INVALID_AMOUNT`

### Phase 3-A — Safety & Reliability

#### A5: Amount guards trong RedeemService
- [ ] `validateRewardItemPrice`: reward price < 0 → `INVALID_REWARD_PRICE`
- [ ] `validateTotalCost`: < 0 → `INVALID_AMOUNT`; > `MAX_SAFE_AMOUNT` (10^15) → `AMOUNT_OVERFLOW`
- [ ] `toPointsLong`: wrap `longValueExact()` → `POINT_PRECISION_LOSS` thay vì silent truncate

#### A4: Vendor response validator (`VendorResultValidator`)
- [ ] Check `result.items.size() == quantity` → fail rollback nếu không khớp
- [ ] Check voucherCode non-blank cho mọi item
- [ ] faceValue tolerance = 1 VND → chỉ log warning, không throw hard
- [ ] Throw `LogicErrorException(VENDOR_INCONSISTENCY)` → trigger rollback flow

#### A1: Recovery job cho order PENDING stuck
- [ ] Module `worker-recovery-pending-order` — long-running pod với Spring `@Scheduled(fixedDelay, timeUnit=MINUTES)`. Config `rewards.recovery.sleep-minutes` (default 5) + `rewards.recovery.initial-delay-minutes` (default 1)
- [ ] `@EnableScheduling` trên `WorkerRecoveryPendingOrderApplication`
- [ ] `RedemptionRecoveryService.applySuccess()` phải: (1) validate voucher list qua `VendorResultValidator.validate(List<VoucherData>, qty, totalCost)` — fail thì treat DEFINITIVE_FAILURE; (2) finalize order; (3) capture balance, fail → `recoveryTaskScheduler.scheduleCaptureBalance()`; (4) schedule ACCEPT_POINTS task nếu `pointsHoldId != null`
- [ ] `RedemptionRecoveryService.applyFailure()` phải: (1) release balance, fail → `scheduleReleaseBalance()`; (2) markOrderFailed; (3) schedule DENY_POINTS task nếu `pointsHoldId != null`
- [ ] `RedemptionOrderEntity.pointsHoldId` — lưu loyalty hold ID để recovery biết accept/deny cái nào. Update qua `RedemptionLogicService.updatePointsHoldId(txnId, holdId)` NGAY sau `loyaltyPointsClient.holdPoints()` thành công trong RedeemService
- [ ] `VendorRecoveryStrategy` + Factory pattern như RedeemStrategy
- [ ] UrBox: `urboxService.redeemVoucher(sameTransactionId)` — idempotent
- [ ] GotIt: `gotItService.checkVoucherStatus(transactionRefId, 1, 100)`
- [ ] Error classification: UrBox code `408` và GotIt code `5000` → TRANSIENT; ResourceAccessException → TRANSIENT; khác → DEFINITIVE
- [ ] `STUCK_THRESHOLD` = 10 phút (chỉ recover sau PENDING 10 phút)
- [ ] `MAX_STUCK_DURATION` = 24h → escalate STILL_PENDING/TRANSIENT_ERROR thành FAILURE
- [ ] Recovery NOT handle loyalty accept/deny (cần user token) → để A3 RecoveryTask xử lý

#### A3: RecoveryTask framework cho critical failures
- [ ] Entity `RecoveryTaskEntity(order, action, payload, retry_count, max_retry=5, scheduled_at, status)`
- [ ] `RecoveryTaskScheduler` helper → dùng trong RedeemService khi acceptHold/captureOrder/releaseOrder/denyHold fail
- [ ] `RecoveryTaskExecutor` retry với exponential backoff: 30s → 2m → 10m → 1h → 6h → FAILED_PERMANENT
- [ ] Pessimistic lock `findByIdForUpdate` khi executor pick task
- [ ] RedeemService gọi `*OrScheduleRetry(...)` thay vì chỉ log — đảm bảo không mất tiền/điểm

#### A2: Idempotency key cho POST /user/redeem
- [ ] Header `Idempotency-Key: <uuid>` (optional, backward compat)
- [ ] Entity `IdempotencyKeyEntity(key, userId, endpoint, responseBody, responseStatus)` — unique (key, userId)
- [ ] Pattern: preHandle insert với responseBody=null, afterCompletion update status
- [ ] Key tồn tại + response != null → trả cached (stop controller)
- [ ] Key tồn tại + response == null → reject 409 `REQUEST_IN_PROGRESS`
- [ ] Cleanup: module `worker-cleanup-idempotency-key` (CronJob one-shot K8s), chạy 1 lần/ngày, xóa key > TTL 24h
- [ ] `IdempotencyKeyCleanupService.cleanup()` → trả số row deleted, throw nếu DB lỗi để K8s alert
- [ ] Config `rewards.idempotency.ttl-hours` (default 24)
- [ ] InternalApiApplication KHÔNG dùng `@EnableScheduling` (tách worker riêng)
- [ ] Chỉ apply interceptor cho `/user/redeem`, mở rộng khi thêm endpoint

### CRM Admin Balance Management (Phase 3-B)
- [ ] **Set balance mode**: `PUT /crm-admin/accounts/{id}/balance/mode` → auto tạo/xóa AccountBalance rows. Xóa row còn số dư (total != 0 || pending != 0) → throw `BALANCE_HAS_VALUE`
- [ ] **Top-up flow** 2 endpoint:
  - `POST /account/top-up-requests` (account-side, @CurrentAccount) — luôn PENDING, account tự tạo yêu cầu nạp tiền
  - `POST /crm-admin/top-up-requests` (CRM, @CurrentAdminUserId) — có flag `autoApprove=true` để shortcut 1 bước (CRM đã nhận tiền, tự ghi nhận)
  - `PUT /crm-admin/top-up-requests/{id}/approve` → cộng DEPOSIT.total + available + ghi `BalanceTransaction(TOP_UP, CREDIT_IN, ref=TOP_UP_REQUEST)`
  - `PUT /crm-admin/top-up-requests/{id}/reject` → mark REJECTED, không đụng balance
- [ ] **Payment**: `POST /crm-admin/payments` (1 bước, không request/approve) — giảm CREDIT.total + tăng available + ghi `BalanceTransaction(PAYMENT, DEBIT_OUT, ref=MANUAL)`. Reject over-pay (amount > total nợ)
- [ ] **Credit limit**: `PUT /crm-admin/accounts/{id}/balance/credit-limit` — reject nếu `newLimit < total + pending` (`CREDIT_LIMIT_TOO_LOW`)
- [ ] **Postpaid toggle**: `PUT /crm-admin/accounts/{id}/balance/postpaid-enabled` — runtime flag, không xóa CREDIT row (giữ số dư nợ cũ)
- [ ] Tất cả admin ops dùng pessimistic lock (`findByAccountIdAndTypeForUpdate`) để an toàn concurrent
- [ ] BalanceTransaction sinh ra ở admin ops: TOP_UP (CREDIT_IN), PAYMENT (DEBIT_OUT). Hold/capture/release redemption không duplicate ở đây

### Balance mode & split (Phase 2 — Hybrid)
- [ ] Mode suy ra từ rows tồn tại qua `AccountBalanceModeResolver.resolve(accountId)` — KHÔNG thêm column vào `AccountEntity`
- [ ] Trước khi hold: gọi `BalanceCheckService.calculateSplit(account, totalAmount)` → `BalanceSplit(depositAmount, creditAmount)`
- [ ] Hybrid split: ưu tiên dùng DEPOSIT trước, phần còn thiếu mới ghi CREDIT (`deposit = min(total, deposit.available)`, `credit = total - deposit`)
- [ ] CREDIT balance check: phải `isPostpaidEnabled == true` — throw `POSTPAID_DISABLED`
- [ ] CREDIT `available = credit_limit - total - pending` (đã tính sẵn trong row) — thiếu: `CREDIT_LIMIT_EXCEEDED`
- [ ] `holdBalance(account, BalanceSplit, orderId)` → `List<Long>` (1-2 holdIds). Deadlock prevention: lock DEPOSIT trước CREDIT
- [ ] `captureOrder(orderId)` / `releaseOrder(orderId)` — iterate TẤT CẢ hold HOLDING của order (hybrid có 2 hold)
- [ ] `RedemptionOrder.depositAmount` + `creditAmount` lưu split tại thời điểm tạo — null nếu = 0 (chuẩn hóa qua `normalizeAmount`)
- [ ] Legacy `holdBalance(account, amount, orderId)` chỉ dùng được cho mode DEPOSIT — mode khác throw `INVALID_HOLD_API`

### Domain models
- [ ] Domain models nằm ở `domain/model/` — dùng cho response ra ngoài
- [ ] Entity mapping method chuyển Entity → Domain Model
- [ ] DTOs cho request nằm trong `domain/dto/` hoặc trong chính controller package (request/)

### Build / Test
- [ ] Terminal KHÔNG có `mvn` CLI — **KHÔNG chạy mvn command**
- [ ] User tự chạy test trong IDE, AI chỉ cần viết code + test file
