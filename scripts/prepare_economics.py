"""Freeze latest Wisconsin Schedule C observations with correct units/unknowns."""
import hashlib,json
from pathlib import Path
import openpyxl
CODES = ['236000','237000','238000','311000','321000','323000','423000','424000','425000','484000','493000','531000','532000','541100','541200','541300','541400','541500','541600','541700','541800','541900','561000','562000','611000','621000','624000','711000','713000','721000','722000','811000','812000']
root = Path(__file__).resolve().parents[1]
source = root / 'data' / 'economics_source.xlsx'
expected_source_hash = '5a674a1f96415c608581bdef01a0fa948415b9b72856de04b8712603dc4ae71f'
if hashlib.sha256(source.read_bytes()).hexdigest() != expected_source_hash:
    raise ValueError('IRS source workbook differs from the frozen 2023 source')
book=openpyxl.load_workbook(source,read_only=True,data_only=True)
records=[]
for row in book.active.values:
    if row[0] not in CODES or row[2]!='55000': continue
    def n(i): return row[i] if isinstance(row[i],(int,float)) else None
    filings,receipts,profit=n(4),n(5),n(11)
    record={'industry':row[0],'name':row[1],'filings':filings,'receipts':receipts,'net_profit':profit,
        'margin_pct':100*profit/receipts if profit is not None and receipts and receipts>0 else None,
        'receipts_per_filing':receipts/filings if receipts is not None and filings else None,
        'profit_per_filing':profit/filings if profit is not None and filings else None,
        'cogs':n(6),'gross_income':n(7),'depreciation':n(8),'expenses':n(9),'home_expenses':n(10)}
    assert (record['net_profit']==row[11]) if isinstance(row[11],(int,float)) else record['net_profit'] is None
    records.append(record)
result={'year':2023,'geography':'Wisconsin state (filing address; FIPS55000)','records':records,
    'source':{'name':'IRS Nonfarm Sole Proprietorships: Selected Items, by Industry and State, Tax Year2023',
        'url':'https://www.irs.gov/pub/irs-soi/23sp01st.xlsx',
        'landing_url':'https://www.irs.gov/statistics/soi-tax-stats-unincorporated-business-state-and-county-data',
        'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'units':'Dollars, not thousands of dollars; filing count is Number of Schedules C',
        'column_mapping':{'filings':'E: Number of Schedules C','receipts':'F: Gross receipts or sales minus returns and allowances (Schedule C line3)',
            'cogs':'G: Cost of goods sold(line4)','gross_income':'H: Gross income(line7)',
            'expenses':'J: Total expenses(line28)','home_expenses':'K: Expenses for business use of home(line30)','net_profit':'L: Net profit or(loss)(line31)'}},
    'limitations':['2023 tax-year observations published later; not live2026 market conditions',
        'Nonfarm sole proprietorship Schedule C data only; excludes partnerships, S corporations and C corporations',
        'Reported net profit includes losses and owner labor compensation; no separate owner wage is imputed',
        'Profit per filing is an aggregate-sums ratio, not median income, typical owner salary, personal take-home, investment return or success probability',
        'One tax return can include multiple Schedules C; counts are not unique people',
        'State uses tax-filing address, which can differ from business operating location',
        'Originally filed uncorrected administrative records; suppressed values remain null',
        'Broad industry categories combine different businesses and business models',
        'No willingness-to-pay, customer-pain, owner-wealth, acquisition-cost or personal-outcome labels exist here',
        'COGS(line4) is already deducted in grossincome(line7); totalexpenses(line28) and homeofficeexpense(line30) are later separate deductions. Do not subtract COGS twice',
        'Gross income can include otherincome, so reported profit/sales need not equal one minus the displayed expense ratios. This is not a complete individual-company P&L']}
(root/'data'/'economics.json').write_text(json.dumps(result,indent=2)+'\n')
print('Snapshot:',len(records),'Wisconsin industry groups')
