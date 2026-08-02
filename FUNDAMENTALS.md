# 财务基本面数据 (Fundamentals)

`zzshare` 支持查询五张核心的基本面和财务数据表。数据均转换为标准的 **pandas DataFrame** 结构，方便进行量化分析。

---

## 💡 快速入门

```python
from zzshare.client import DataApi

# 初始化
api = DataApi(token="您的Token")

# 1. 查询日频估值数据
df_val = api.finance_valuation("2024-12-31")
print(df_val.head())

# 2. 查询季频财务指标数据
df_ind = api.finance_indicator("2024q4")  # 支持 '2024q4' 或 '2024-12-31' 格式
print(df_ind.head())
```

---

## 📊 接口、字段与公式详细说明

### 1. 估值日频表 (`finance_valuation`)

* **调用方式**：`api.finance_valuation(date_value)`
* **说明**：按交易日查询，`date_value` 传入交易日（如 `"2024-12-31"`）。

| 字段名 | 类型 | 含义说明 | 公式 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `code` | str | 股票代码 | - | 例如 `000001.SZ` |
| `trade_date` | str | 交易日期 | - | 格式为 `YYYY-MM-DD` |
| `capitalization` | float | 总股本（万股） | - | 公司的全部已发行的股份总数 |
| `circulating_cap` | float | 流通股本（万股） | - | 在证券交易所可以自由买卖的股份总数 |
| `market_cap` | float | 总市值（亿元） | $\text{股价} \times \text{总股本}$ | 反映企业整体规模与市值的绝对数值 |
| `circulating_market_cap` | float | 流通市值（亿元） | $\text{股价} \times \text{流通股本}$ | 反映市场上可实际变现交易的市值部分 |
| `turnover_ratio` | float | 换手率（%） | $\frac{\text{今日成交量}}{\text{流通股本}} \times 100\%$ | 衡量股票交易活跃度的核心指标 |
| `pe_ratio` | float | 市盈率（TTM） | $\frac{\text{当前总市值}}{\text{最近4个季度的归母净利润之和}}$ | 滚动市盈率，最常用的估值倍数 |
| `pe_ratio_lyr` | float | 市盈率（LYR） | $\frac{\text{当前总市值}}{\text{上一年度的归母净利润}}$ | 静态市盈率，基于上年度年报的静态估值 |
| `pb_ratio` | float | 市净率 | $\frac{\text{当前总市值}}{\text{最新报告期的归母股东权益(净资产)}}$ | 衡量股价相对于公司账面资产价值（净资产）的估值水平 |
| `ps_ratio` | float | 市销率 | $\frac{\text{当前总市值}}{\text{最近4个季度的营业收入之和}}$ | 适用于未盈利的高成长性企业估值 |
| `pcf_ratio` | float | 市现率 | $\frac{\text{当前总市值}}{\text{最近4个季度的经营活动现金流净额之和}}$ | 衡量市值与现金流健康度的比值 |

---

### 2. 财务指标季频表 (`finance_indicator`)

* **调用方式**：`api.finance_indicator(date_value)`
* **说明**：按报告期查询，`date_value` 可传季度简写（如 `"2024q4"`) 或具体期末日期（如 `"2024-12-31"`)。

| 字段名 | 类型 | 含义说明 | 公式 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `code` | str | 股票代码 | - | 例如 `000001.SZ` |
| `statDate` | str | 报表季度 | - | 格式为 `2024q4` 或报告期底 `2024-12-31` |
| `pubDate` | str | 财报发布日期 | - | 该季度财务报告向市场公开发布的实际日期，用于防范回测中的未来函数 |
| `eps` | float | 每股收益 | $\frac{\text{归属于母公司所有者的净利润}}{\text{期末总股本}}$ | 扣税后分配给普通股股东的每股利润额 |
| `adjusted_profit` | float | 扣除非经常性损益后的净利润 | - | 剔除非主营业务产生的偶然性收益后的净利润，更能反映公司核心主营的持续造血能力 |
| `operating_profit` | float | 经营活动净收益 | - | 扣除销售、管理、研发等期间费用后的企业日常经营活动所获得的营业利润 |
| `roe` | float | 净资产收益率 | $\frac{\text{净利润}}{\text{所有者权益(净资产)的均值}} \times 100\%$ | 衡量公司获利能力与资金使用效率的杜邦分析核心指标 |
| `inc_revenue_year_on_year` | float | 营业收入同比增长率 | $\frac{\text{本期营业收入} - \text{上年同期营业收入}}{\text{上年同期营业收入}} \times 100\%$ | 与上年同期相比，营业收入增长的比率，反映主打产品/业务扩张速度 |
| `inc_net_profit_year_on_year` | float | 净利润同比增长率 | $\frac{\text{本期归母净利润} - \text{上年同期归母净利润}}{\text{上年同期归母净利润}} \times 100\%$ | 与上年同期相比，归属于母公司所有者净利润的增长速度 |
| `inc_revenue_annual` | float | 营业收入环比增长率 | $\frac{\text{本期营业收入} - \text{上期营业收入}}{\text{上期营业收入}} \times 100\%$ | 相比上一季度增长的速度，用以评估企业短期增长势头 |
| `inc_net_profit_annual` | float | 净利润环比增长率 | $\frac{\text{本期归母净利润} - \text{上期归母净利润}}{\text{上期归母净利润}} \times 100\%$ | 相比上一季度归母净利润的增长速度，能够及时发现业绩拐点 |
| `net_profit_margin` | float | 销售净利率 | $\frac{\text{净利润}}{\text{营业总收入}} \times 100\%$ | 销售收入中能真正留存转化为最终收益的比例 |
| `gross_profit_margin` | float | 销售毛利率 | $\frac{\text{营业总收入} - \text{营业总成本}}{\text{营业总收入}} \times 100\%$ | 反映产品定价溢价能力与核心生产成本控制水平的关键门槛 |
| `operating_profit_to_total_profit` | float | 营业利润占总利润比例 | $\frac{\text{营业利润}}{\text{利润总额}} \times 100\%$ | 比例越高代表盈利中来自日常经营的越稳健，主营业务地位越突显 |
| `net_profit_to_total_profit` | float | 净利润占总利润比例 | $\frac{\text{净利润}}{\text{利润总额}} \times 100\%$ | 评估所得税、减值损失及非经常性支出的综合侵蚀或拉动效果 |
| `adjusted_profit_to_total_profit` | float | 扣除非经常性损益后的净利润占总利润比例 | $\frac{\text{扣非归母净利润}}{\text{利润总额}} \times 100\%$ | 用来评估核心经营性利润在企业最终获取总利润中的真实比重 |
| `net_profit_to_total_revenue` | float | 净利润占营业总收入比例 | $\frac{\text{净利润}}{\text{营业总收入}} \times 100\%$ | 营业收入最终产生净利润的转化比率 |
| `adjusted_profit_to_total_revenue` | float | 扣非净利润占营业总收入比例 | $\frac{\text{扣非归母净利润}}{\text{营业总收入}} \times 100\%$ | 主营业务核心盈利相对最终所带来的营收总额的比率，反映最纯粹的销售利润转化效率 |

---

### 3. 利润表季频表 (`finance_income`)

* **调用方式**：`api.finance_income(date_value)`

| 字段名 | 类型 | 含义说明 | 公式 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `code` | str | 股票代码 | - | 例如 `000001.SZ` |
| `statDate` | str | 报表季度 | - | 报告所属季度末日期 |
| `pubDate` | str | 财报发布日期 | - | 该报告实际向公开市场披露的日期 |
| `total_operating_revenue` | float | 营业总收入 | - | 包含公司销售商品、提供劳务、利息手续费及保费等业务所取得的全部收入 |
| `operating_revenue` | float | 营业收入 | - | 销售主打商品和直接提供劳务所取得的主营业务及其他业务收入 |
| `total_operating_cost` | float | 营业总成本 | - | 包含营业成本、税金、三项费用（销售、管理、财务）以及研发费用等的总流出 |
| `operating_cost` | float | 营业成本 | - | 与销售和生产商品直接挂钩并配比的直接成本（如原材料、生产折旧等） |
| `operating_tax` | float | 营业税金及附加 | - | 经营活动产生的附加税（如消费税、城建税、教育费附加） |
| `sale_expense` | float | 销售费用 | - | 为推销产品所支出的广告宣传、促销、销售网络搭建、人员工资、运输等费用 |
| `management_expense` | float | 管理费用 | - | 董事会、行政管理部门人员薪酬、办公折旧、管理开支等日常运营支出 |
| `research_expense` | float | 研发费用 | - | 进行新工艺、新产品或新技术开发研究而发生的总研发支出金额 |
| `financial_expense` | float | 财务费用 | - | 借款利息净收支、金融机构手续费、外汇折算产生的汇兑损失等筹资活动成本 |
| `asset_impairment_loss` | float | 资产减值损失 | - | 对存货跌价、坏账准备、固定资产以及商誉等提取的资产减值金 |
| `investment_income` | float | 投资收益 | - | 购买股票、短期理财或长期股权投资（联营/合营公司）所分回的盈利或红利 |
| `exchange_income` | float | 汇兑收益 | - | 外汇市场汇率变动导致外币资产产生折算利得的盈余部分 |
| `operating_profit` | float | 营业利润 | $\text{营业收入} - \text{营业成本} - \text{税金} - \text{费用} - \text{减值} + \text{投资收益}$ | 扣除一切直接与间接经营成本后的核心营业利润金额 |
| `non_operating_income` | float | 营业外收入 | - | 与生产经营无直接关联的利得，如政府补助、接受捐赠、处置废旧资产收益 |
| `non_operating_expense` | float | 营业外支出 | - | 与生产经营无直接关联的损失，如违约罚款、公益捐赠、自然灾害资产报废损失 |
| `total_profit` | float | 利润总额 | $\text{营业利润} + \text{营业外收入} - \text{营业外支出}$ | 息税前全部总利润金额 |
| `income_tax` | float | 所得税费用 | - | 按照适用税率和税收法规应向税务局缴纳的企业所得税 |
| `unconfirmed_investment_loss` | float | 未确认的投资损失 | - | 控股子公司超额亏损中，依约本应由少数股东分担但由于合同约定未予确认的超额亏损 |
| `net_profit` | float | 净利润(含少数股东损益) | $\text{利润总额} - \text{所得税费用}$ | 合并利润表中的税后总利润额 |
| `np_parent_company_owners` | float | 净利润(不含少数股东损益) | $\text{净利润} - \text{少数股东损益}$ | 扣除子公司中其他小股东应得的利润后，真正属于母公司股东的归母净利润 |
| `minority_interest` | float | 少数股东损益 | - | 合并报表非全资子公司中由非母公司所占持股比例对应的本期盈亏金额 |
| `deduct_parent_net_profit` | float | 扣除非经常性损益后的净利润 | $\text{归母净利润} - \text{非经常性损益}$ | 扣除政府补贴、卖房投资等偶发收益后，主营业务核心获利能力的归母净利润 |
| `deduct_minority_profit` | float | 扣除非经常性损益后的净利润(少数股东损益) | - | 少数股东损益中剔除掉非经常性损益项目后的余额 |

---

### 4. 资产负债表季频表 (`finance_balance`)

* **调用方式**：`api.finance_balance(date_value)`

| 字段名 | 类型 | 含义说明 | 公式 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `code` | str | 股票代码 | - | 例如 `000001.SZ` |
| `statDate` | str | 报表季度 | - | 资产负债表静态财务状况的编制截止报告期 |
| `pubDate` | str | 财报发布日期 | - | 该报告实际向公开市场披露的日期 |
| `cash_equivalents` | float | 货币资金 | - | 可以随时用于支付的存款、现金及高流动性的短期有价证券（现金等价物） |
| `settlement_provisions` | float | 结算备付金 | - | 金融机构或企业专门存入中登公司用以证券或期货等品种买卖清算结算的资金 |
| `trading_financial_assets` | float | 交易性金融资产 | - | 持有期较短（如不超过一年）以赚取交易价差为主要目的的证券或金融投资 |
| `derivative_financial_assets` | float | 衍生金融资产 | - | 签订的期权、远期、利率/货币互换合同在期末呈现正向公允价值部分的衍生资产 |
| `accounts_receivable` | float | 应收账款 | - | 因销售货物、提供劳务应收尚未收到买方的销售欠款 |
| `other_receivables` | float | 其他应收款 | - | 除应收账款、应收票据等常规经营应收款项外的各种暂付、垫付的款项 |
| `prepayments` | float | 预付款项 | - | 依据合同条款，在接受货物之前提前支付给供应商的预付定金或预付货款 |
| `premium_receivables` | float | 应收保费 | - | 保险公司应收而尚未收到的各保单项下的未缴保险费 |
| `sub_receivables` | float | 应收代位追偿款 | - | 保险公司在向被保险人理赔赔付后，依法应向责任方或第三方追偿的应收款项 |
| `reinsurance_receivables` | float | 应收分保账款 | - | 分保分出人与分保分入人再保险业务清算中产生的往来未结算应收款 |
| `reinsurance_contract_reserve_receivables` | float | 应收分保合同准备金 | - | 因分出再保险业务而在分入人处计提并可随时摊回或应收的分保准备金存入款 |
| `interest_receivable` | float | 应收利息 | - | 持有债券或存款产生的已到期但尚未收到的利息 |
| `dividend_receivable` | float | 应收股利 | - | 被投资公司已宣告发放但尚未实际支付至本账户的派息红利 |
| `inventory` | float | 存货 | - | 存放在仓库准备用于销售的库存商品，或用于后续生产的原材料和在制品 |
| `contract_assets` | float | 合同资产 | - | 已转让商品或完成劳务但无条件收款权利尚未确立（如需等其他履约条件）的收款资产 |
| `non_current_asset_due_within_one_year` | float | 一年内到期的非流动资产 | - | 长期债权投资或应收款等非流动资产中，将在一年内到期并变现的部分 |
| `other_current_assets` | float | 其他流动资产 | - | 其他无法单独归类但预期一年内可以变现或抵扣的资产（如待抵扣增值税留抵） |
| `total_current_assets` | float | 流动资产合计 | $\text{货币资金} + \text{交易性金融资产} + \text{应收款} + \text{存货} + \dots$ | 企业中可以在一年或一个常规营业周期内变现或被消耗的全部资产总额 |
| `non_current_debt_investment` | float | 非流动资产-债权投资 | - | 打算长期（持有一年以上直至到期）持有的债权类金融工具投资 |
| `other_non_current_financial_assets` | float | 其他非流动金融资产 | - | 企业持有的变现期超过一年且不构成控制或重大影响的股权或债务性金融投资 |
| `long_term_equity_investment` | float | 长期股权投资 | - | 对联营、合营企业及可施加重大控制的子公司持有的长期股权资本投资 |
| `other_non_current_equity_investment` | float | 其他权益工具投资 | - | 企业出于战略目的持有的、指定为以公允价值计量且其变动计入其他综合收益的非交易性权益投资 |
| `other_non_current_receivables` | float | 其他非流动资产-其他应收款 | - | 无法在一年内收回或结算的非流动性其他应收往来款项 |
| `investment_property` | float | 投资性房地产 | - | 为赚取未来租金收入或资本溢价增值而专门持有的土地使用权和厂房建筑物 |
| `fixed_assets` | float | 固定资产 | - | 厂房、建筑物、运输车辆、机器设备等使用年限超一年且单价较高的有形资产 |
| `construction_in_progress` | float | 在建工程 | - | 尚处于设计、施工、安装调试阶段的、未办理竣工决算的固定资产工程支出成本 |
| `using_assets` | float | 使用权资产 | - | 新租赁准则下，承租人依据租赁合同取得并在租赁期内占有和使用租赁标的物的权利资产 |
| `intangible_assets` | float | 无形资产 | - | 专利权、商标权、非专利技术、土地使用权等无实物形态的长期性资产 |
| `development_expenditure` | float | 开发支出 | - | 研究开发项目中处于开发阶段、且符合资本化条件的累积研究费用开发支出 |
| `goodwill` | float | 商誉 | - | 溢价并购子公司时，合并溢价成本超过所获得的可辨认净资产公允价值部分的差额 |
| `long_term_deferred_expenses` | float | 长期待摊费用 | - | 已经发生但摊销期限在一年以上、应在未来各期分摊的费用（如租入房屋改良费） |
| `deferred_tax_assets` | float | 递延所得税资产 | - | 根据会计税收准则差异（如减值准备超支）未来可用于抵减所得税支出的可抵扣暂时性资产 |
| `other_non_current_assets` | float | 其他非流动资产 | - | 无法分摊或不属于以上各类项目的其他非流动长期资产 |
| `total_non_current_assets` | float | 非流动资产合计 | $\text{固定资产} + \text{无形资产} + \text{长期投资} + \text{在建工程} + \dots$ | 回收期或使用期限超过一年、以提供长期服务能力为目的的非流动资产总和 |
| `total_assets` | float | 资产总计 | $\text{流动资产合计} + \text{非流动资产合计}$ | 公司控制和拥有的全部资产价值的总和 |
| `short_term_loan` | float | 短期借款 | - | 向银行或其他金融机构借入的期限在一年以下的借款本金 |
| `trading_financial_liabilities` | float | 交易性金融负债 | - | 以短期内回购结算为目的而承担的负债（如融券卖空出借股票的结算义务） |
| `derivative_financial_liabilities` | float | 衍生金融负债 | - | 期末公允价值为负值的衍生品合约义务（如期权空头头寸） |
| `notes_payable` | float | 应付票据 | - | 采购材料或接受劳务开出并经商业或银行承兑的未到期应付汇票 |
| `accounts_payable` | float | 应付账款 | - | 因采购原材料、商品或接受劳务服务应支付给供货商的货款 |
| `advance_receipts` | float | 预收款项 | - | 预先收取的客户货款或订金，在对应货物交付或劳务完成前属于企业负债 |
| `contract_liabilities` | float | 合同负债 | - | 新收入准则下，已收或应收客户对价但有义务向客户转让商品的已确认负债 |
| `salaries_payable` | float | 应付职工薪酬 | - | 应当支付但尚未划转至员工账户的本期或历史累积的工资、社会保险、住房公积金等 |
| `taxes_payable` | float | 应交税费 | - | 应缴但尚未缴纳的各种税金（如增值税、企业所得税、印花税、城建税等） |
| `other_payables` | float | 其他应付款 | - | 除应付账款、应付票据、职工薪酬等核心科目之外的其他往来应付款 |
| `interest_payable` | float | 应付利息 | - | 计提但尚未到支付期限的债券利息或长期贷款利息 |
| `dividend_payable` | float | 应付股利 | - | 董事会或股东大会决议宣告分配但尚未派发现金的应付股利或红利 |
| `other_current_liabilities` | float | 其他流动负债 | - | 无法包含在以上流动科目中但需要在一年内偿还的短期债务 |
| `total_current_liability` | float | 流动负债合计 | $\text{短期借款} + \text{应付账款} + \text{合同负债} + \dots$ | 将在一年内或者一个常规营业周期内需优先以流动资产偿还的负债总额 |
| `long_term_loan` | float | 长期借款 | - | 向银行或金融机构借入的、偿还期限在一年以上的各项贷款本金 |
| `bonds_payable` | float | 应付债券 | - | 为筹集长期资本而向社会公开发行并应按期付息还本的公司债券负债 |
| `long_term_payable` | float | 长期应付款 | - | 具有融资性质的延期付款（如融资租赁购买资产应付的长期租金） |
| `estimated_liability` | float | 预计负债 | - | 因担保、未决诉讼、重组义务等或有事项产生，符合负债确认条件的潜在偿付义务 |
| `deferred_income` | float | 递延收益 | - | 收到并在以后期间计入收入的款项，通常为政府针对长期资产给予的非日常补贴 |
| `deferred_tax_liabilities` | float | 递延所得税负债 | - | 暂时性应纳税差异（如加速折旧）导致的将在未来期间多缴的所得税额 |
| `other_non_current_liabilities` | float | 其他非流动负债 | - | 无法列入上述长期科目的其他非流动负债 |
| `total_non_current_liability` | float | 非流动负债合计 | $\text{长期借款} + \text{应付债券} + \text{长期应付款} + \dots$ | 偿还期在一年以上的非流动性债务总额 |
| `total_liability` | float | 负债合计 | $\text{流动负债合计} + \text{非流动负债合计}$ | 公司所承担的全部外部债务的总额 |
| `paid_in_capital` | float | 实收资本(或股本) | - | 股东按公司章程规定实际投入并完成入账的资本或发行的普通股面值总额 |
| `capital_reserve` | float | 资本公积 | - | 股票发行溢价、其他股东权益变动等不计入股本但计入所有者权益的资本储备 |
| `treasury_stock` | float | 减:库存股 | - | 公司为注销或股权激励等目的购回并持有的自身股票在尚未处置前的抵减价值 |
| `surplus_reserve` | float | 盈余公积 | - | 公司按照国家法律规定，强制和任意从本期可分配净利润中计提的留存资金 |
| `statutory_welfare_reserve` | float | 一般风险准备 | - | 金融保险等特定行业企业按照国家规定，为了应对可能的潜在风险而提取的专用准备金 |
| `undistributed_profit` | float | 未分配利润 | - | 历年累积可分配而尚未进行分红派息的剩余净利润 |
| `minority_interest` | float | 少数股东权益 | - | 非全资子公司的净资产中，不属于母公司直接或间接持股比例占有的少数权益份额 |
| `owners_equity_including_minority_interest` | float | 所有者权益(含少数股东权益) | $\text{资产总计} - \text{负债合计}$ | 合并资产负债表中所有者权益的总额（即公司的全部净资产） |
| `total_owner_equities` | float | 所有者权益合计 | $\text{股本} + \text{资本公积} + \text{留存收益} - \text{库存股}$ | 合并资产负债表中属于母公司股东的权益总额（不含少数股东权益） |
| `total_liability_and_owner_equities` | float | 负债和所有者权益总计 | $\text{负债合计} + \text{所有者权益(含少数股东权益)}$ | 恒等于公司资产总计（代表资金来源的总规模） |

---

### 5. 现金流量表季频表 (`finance_cash_flow`)

* **调用方式** ：`api.finance_cash_flow(date_value)`

| 字段名 | 类型 | 含义说明 | 公式 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `code` | str | 股票代码 | - | 例如 `000001.SZ` |
| `statDate` | str | 报表季度 | - | 现金流量表所覆盖季度的期末日期 |
| `pubDate` | str | 财报发布日期 | - | 该报告实际向公开市场披露的日期 |
| `sale_goods_services` | float | 销售商品、提供劳务收到的现金 | - | 公司因日常经营销售产品或提供劳务取得的直接现金回笼流（含收到的增值税） |
| `net_operate_cash_inflows` | float | 经营活动现金流入小计 | - | 所有日常经营相关活动（销售、税费返还、收到其他往来）带来的现金流入总额 |
| `net_operate_cash_outflows` | float | 经营活动现金流出小计 | - | 所有日常经营相关活动（采购、付税、发工资、付其他往来）带来的现金流出总额 |
| `net_operate_cash_flow` | float | 经营活动产生的现金流量净额 | $\text{经营现金流入小计} - \text{经营现金流出小计}$ | 企业核心日常经营活动通过自我造血产生的真实净现金流量，反映利润含金量 |
| `buy_construct_long_term_assets` | float | 购建固定资产、无形资产和其他长期资产支付的现金 | - | 为扩充产能、研发升级所购买厂房、购入设备、无形资产等付出的现金（资本性支出资本） |
| `dispose_long_term_assets` | float | 处置固定资产、无形资产和其他长期资产收回的现金净额 | - | 处置或卖出公司厂房、旧设备、无形资产所回收并扣减相关费用的现金净额 |
| `net_invest_cash_inflows` | float | 投资活动现金流入小计 | - | 所有投资活动（收回投资本金、处置资产、取得红利派息）带来的现金流入总额 |
| `net_invest_cash_outflows` | float | 投资活动现金流出小计 | - | 所有投资活动（购建固定资产、买入理财、长期股权投资等）带来的现金流出总额 |
| `net_invest_cash_flow` | float | 投资活动产生的现金流量净额 | $\text{投资现金流入小计} - \text{投资现金流出小计}$ | 投资活动产生的净资金流动，通常成长期企业该值为负，表示在持续投入资金扩张 |
| `cash_dividend_internal` | float | 分配股利、利润或偿付利息支付的现金 | - | 支付贷款利息、派发公司普通股现金红利以及分红给少数股东所支付的现金 |
| `absorb_investment` | float | 吸收投资收到的现金 | - | 发行新股票、增发募资或子公司引入外部股权资本实际收到股东的现金 |
| `sub_loan_received` | float | 子公司吸收少数股东投资收到的现金 | - | 合并范围内子公司从非母公司股东处获得注资实际流入的现金 |
| `cash_received_borrower` | float | 取得借款收到的现金 | - | 获得银行贷款或向其他金融机构借入的短期/长期借款现金本金流入 |
| `net_finance_cash_inflows` | float | 筹资活动现金流入小计 | - | 所有的筹资活动（吸收股权资金、借债、发债）带来的现金流入总额 |
| `net_finance_cash_outflows` | float | 筹资活动现金流出小计 | - | 所有的筹资活动（还本、付息、派发现金股利）带来的现金流出总额 |
| `net_finance_cash_flow` | float | 筹资活动产生的现金流量净额 | $\text{筹资现金流入小计} - \text{筹资现金流出小计}$ | 筹资与融资活动对现金产生的净额，为负代表偿债及分红多于借入金额 |
| `exchange_rate_effect` | float | 汇率变动对现金的影响 | - | 外币现金及等价物在会计期末按最新汇率折算导致的现金账面价值损益的汇率影响金额 |
| `cash_and_equivalents_increase` | float | 现金及现金等价物净增加额 | $\text{经营净额} + \text{投资净额} + \text{筹资净额} + \text{汇率影响}$ | 本会计期间公司货币资金及等价物的最终净流入/流出差额 |
| `end_cash_balance` | float | 期末现金及现金等价物余额 | $\text{期初现金余额} + \text{现金等价物净增加额}$ | 本会计期末持有的随时可支取的货币现金及等价物余额（与资产负债表中现金资产核对） |
| `begin_cash_balance` | float | 期初现金及现金等价物余额 | - | 本会计期初账面上所持有的货币现金与随时可变现的现金等价物余额 |

---

## 🔬 高级查询接口（回测核心）

除了上述按表、按日期的基本查询外，`zzshare` 还提供以下 4 种高级查询模式，覆盖量化策略回测的全部核心场景。

---

### 6. Point-in-time 查询 (`finance_pit`)

* **调用方式**：`api.finance_pit(table, trade_date, codes=None, source="jq")`
* **回测核心**：给定交易日 D，返回每只股票在 D **之前最新已发布**的财务数据，严格防范未来函数（look-ahead bias）。

| 行为 | 说明 |
| :--- | :--- |
| **日频表** (valuation) | 直接返回 trade_date 当日的快照数据 |
| **季频表** (indicator/income/balance/cash_flow) | 查找 `pubDate <= trade_date` 的最新一期季报，模拟聚宽 `get_fundamentals(q, date=D)` |

```python
# 交易日 2024-06-03 的 PIT 估值快照（全市场）
df = api.finance_pit(table="valuation", trade_date="2024-06-03")

# 指定个股的 PIT 财务指标
df = api.finance_pit(table="indicator", trade_date="2024-06-03", codes="600519.SH,000001.SZ")
```

| 参数 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `table` | str | 是 | 表名: valuation / indicator / income / balance / cash_flow |
| `trade_date` | str | 是 | 交易日，如 2024-12-31 |
| `codes` | str | 否 | 股票代码，逗号分隔，如 600519.SH,000001.SZ |
| `source` | str | 否 | 数据源，默认 jq |

---

### 7. 日期区间查询 (`finance_range`)

* **调用方式**：`api.finance_range(table, start_date, end_date, codes=None, source="jq", limit=50000)`
* **说明**：返回指定日期范围内的财务数据，按日期降序排列。适合构建面板数据（panel data）或批量拉取历史数据。

```python
# 2024 全年的估值数据（降序）
df = api.finance_range(table="valuation", start_date="2024-01-01", end_date="2024-12-31")

# 指定个股 2022-2024 年的利润表
df = api.finance_range(table="income", start_date="2022q1", end_date="2024q4", codes="600519.SH")
```

| 参数 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `table` | str | 是 | 表名 |
| `start_date` | str | 是 | 起始日期/季度 |
| `end_date` | str | 是 | 结束日期/季度 |
| `codes` | str | 否 | 股票代码，逗号分隔 |
| `source` | str | 否 | 数据源，默认 jq |
| `limit` | int | 否 | 返回条数上限，默认 50000 |

---

### 8. 单股历史查询 (`finance_stock`)

* **调用方式**：`api.finance_stock(table, code, start_date=None, end_date=None, source="jq", limit=1000)`
* **说明**：返回指定单只股票的全部财务历史数据，按日期降序排列。适合个股深度分析。

```python
# 茅台的全部资产负债表历史
df = api.finance_stock(table="balance", code="600519.SH")

# 限制时间范围和条数
df = api.finance_stock(table="cash_flow", code="000001.SZ", start_date="2020-01-01", end_date="2024-12-31", limit=20)
```

| 参数 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `table` | str | 是 | 表名 |
| `code` | str | 是 | 股票代码，如 600519.SH |
| `start_date` | str | 否 | 起始日期 |
| `end_date` | str | 否 | 结束日期 |
| `source` | str | 否 | 数据源，默认 jq |
| `limit` | int | 否 | 返回条数上限，默认 1000 |

---

### 9. 最新数据快照 (`finance_latest`)

* **调用方式**：`api.finance_latest(table, codes=None, source="jq")`
* **说明**：获取最新的财务数据快照。日频表返回最新交易日数据，季频表返回每只股票最新一期季报。

```python
# 全市场最新的估值快照
df = api.finance_latest(table="valuation")

# 指定个股的最新财务指标
df = api.finance_latest(table="indicator", codes="600519.SH,000001.SZ")
```

| 参数 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `table` | str | 是 | 表名 |
| `codes` | str | 否 | 股票代码，逗号分隔 |
| `source` | str | 否 | 数据源，默认 jq |
