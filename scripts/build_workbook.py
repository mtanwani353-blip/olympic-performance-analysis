import pandas as pd, zipfile, uuid, html, re
U='/mnt/user-data/uploads/alltime_country_rankings__'
r=pd.read_csv(U+'alltime_country_rankings.csv'); a=pd.read_csv(U+'athletes.csv')
g=pd.read_csv(U+'games_summary.csv'); m=pd.read_csv(U+'medal_results.csv')
strip=lambda df: df.rename(columns=lambda c: re.sub(r'\s*\(.*?\)','',c).strip())
r,a,g,m=map(strip,(r,a,g,m))
for d in (a,m): d.rename(columns={'Total Medals':'Total Medals'},inplace=True)
m['Investment Score']=m['Sports Investment'].map({'Low':1,'Medium':2,'High':3})
g=g.rename(columns={'Host City':'Host City','Year':'Year'})
files={'country_rankings.csv':r,'athletes.csv':a,'games_summary.csv':g,'medal_results.csv':m}
for f,d in files.items(): d.to_csv('Data/'+f,index=False)

def dt(s):
    if pd.api.types.is_integer_dtype(s): return 'integer'
    if pd.api.types.is_float_dtype(s): return 'real'
    return 'string'
def rid(): return 'federated.'+uuid.uuid4().hex[:28]
E=lambda s: html.escape(str(s),quote=True)
DS={}
for key,(f,cap) in {'R':('country_rankings.csv','Country Rankings'),'A':('athletes.csv','Athletes'),
                    'G':('games_summary.csv','Games Summary'),'M':('medal_results.csv','Medal Results')}.items():
    DS[key]=dict(id=rid(),f=f,cap=cap,df=files[f])
from tableauhyperapi import HyperProcess,Telemetry,Connection,CreateMode,TableDefinition,SqlType,TableName,Inserter,SchemaName
import os
def make_hyper(f,df):
    p='Extracts/'+f.replace('.csv','.hyper')
    if os.path.exists(p): os.remove(p)
    with HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hp:
        with Connection(hp.endpoint,p,CreateMode.CREATE_AND_REPLACE) as c:
            c.catalog.create_schema('Extract')
            ty={'integer':SqlType.big_int(),'real':SqlType.double(),'string':SqlType.text()}
            td=TableDefinition(TableName('Extract','Extract'),[TableDefinition.Column(col,ty[dt(df[col])]) for col in df.columns])
            c.catalog.create_table(td)
            with Inserter(c,td) as ins:
                rows=[[None if pd.isna(v) else (v.item() if hasattr(v,'item') else v) for v in r] for r in df.itertuples(index=False)]
                ins.add_rows(rows); ins.execute()
    return p
def dsxml(k):
    d=DS[k]; nc='hyper.'+uuid.uuid4().hex[:28]
    make_hyper(d['f'],d['df'])
    path='Data/Extracts/'+d['f'].replace('.csv','.hyper')
    extra=''
    if k=='G': extra="<column datatype='integer' name='[Year]' role='dimension' type='ordinal' />"
    return f"""<datasource caption='{d['cap']}' inline='true' name='{d['id']}' version='18.1'>
<connection class='federated'><named-connections><named-connection caption='{d['cap']}' name='{nc}'><connection authentication='auth-none' class='hyper' dbname='{path}' default-settings='yes' sslmode='' username='' /></named-connection></named-connections>
<relation connection='{nc}' name='Extract' table='[Extract].[Extract]' type='table' /></connection>
{extra}<extract count='-1' enabled='true' units='records'><connection access_mode='readonly' authentication='auth-none' class='hyper' dbname='{path}' default-settings='yes' schema='Extract' sslmode='' tablename='Extract' update-time='2026-10-21T00:00:00.000' username=''><relation name='Extract' table='[Extract].[Extract]' type='table' /></connection></extract></datasource>"""

# helpers for worksheet
def dim(c): return f"<column datatype='string' name='[{c}]' role='dimension' type='nominal' />"
def meas(c,t='integer'): return f"<column datatype='{t}' name='[{c}]' role='measure' type='quantitative' />"
def inst_d(c): return f"<column-instance column='[{c}]' derivation='None' name='[none:{c}:nk]' pivot='key' type='nominal' />"
def inst_m(c,der): 
    tag={'Sum':'sum','Avg':'avg'}[der]
    return f"<column-instance column='[{c}]' derivation='{der}' name='[{tag}:{c}:qk]' pivot='key' type='quantitative' />"
def ref(k,c,kind,der=None):
    i=DS[k]['id']
    if kind=='d': return f"[{i}].[none:{c}:nk]"
    return f"[{i}].[{ {'Sum':'sum','Avg':'avg'}[der]}:{c}:qk]"
def sheet(name,k,deps,rows,cols,mark,enc='',view_extra='',filters='',title=None):
    i=DS[k]['id']
    t=f"<layout-options><title><formatted-text><run>{E(title or name)}</run></formatted-text></title></layout-options>"
    return f"""<worksheet name='{E(name)}'>{t}<table><view>
<datasources><datasource caption='{DS[k]['cap']}' name='{i}' /></datasources>
<datasource-dependencies datasource='{i}'>{deps}</datasource-dependencies>
{filters}{view_extra}<aggregation value='true' /></view><style />
<panes><pane><view><breakdown value='auto' /></view><mark class='{mark}' />{('<encodings>'+enc+'</encodings>') if enc else ''}</pane></panes>
<rows>{rows}</rows><cols>{cols}</cols></table></worksheet>"""
def sort(k,d,mm,der,shelf):
    return f"<sort class='computed' column='{ref(k,d,'d')}' direction='DESC' using='{ref(k,mm,'m',der)}' />"

S=[]
# 1 avg medals per athlete by sport category
S.append(sheet('Avg Medals per Athlete by Category','A',
  dim('Sport Category')+meas('Total Medals')+inst_d('Sport Category')+inst_m('Total Medals','Avg'),
  ref('A','Sport Category','d'),ref('A','Total Medals','m','Avg'),'Bar',
  f"<color column='{ref('A','Total Medals','m','Avg')}' />",sort('A','Sport Category','Total Medals','Avg','rows')))
# 2 top 20 countries
S.append(sheet('Global Performance by Country','R',
  dim('Country')+meas('Total Medals')+meas('Overall Rank')+inst_d('Country')+inst_m('Total Medals','Sum')
  +"<column-instance column='[Overall Rank]' derivation='None' name='[none:Overall Rank:qk]' pivot='key' type='quantitative' />",
  ref('R','Country','d'),ref('R','Total Medals','m','Sum'),'Bar',
  f"<color column='{ref('R','Total Medals','m','Sum')}' />",sort('R','Country','Total Medals','Sum','rows'),
  f"<filter class='quantitative' column='[{DS['R']['id']}].[none:Overall Rank:qk]' included-values='in-range'><min>1</min><max>20</max></filter>",
  title='Global Performance by Country (Top 20 by Overall Rank)'))
# 3 trend
S.append(sheet('Trend of Total Medals Awarded','G',
  "<column datatype='integer' name='[Year]' role='dimension' type='ordinal' />"+meas('Total Medals Awarded')
  +"<column-instance column='[Year]' derivation='None' name='[none:Year:ok]' pivot='key' type='ordinal' />"+inst_m('Total Medals Awarded','Sum'),
  f"[{DS['G']['id']}].[sum:Total Medals Awarded:qk]",f"[{DS['G']['id']}].[none:Year:ok]",'Line',
  f"<label column='[{DS['G']['id']}].[sum:Total Medals Awarded:qk]' />".replace("<label column","<text column")))
# 4 bubble
Mi=DS['M']['id']
S.append(sheet('Sports Investment vs Medal Performance','M',
  dim('Country')+dim('Region')+meas('Investment Score')+meas('Total Medals')+meas('Medal Efficiency Pct','real')
  +inst_d('Country')+inst_d('Region')+inst_m('Investment Score','Avg')+inst_m('Total Medals','Sum')+inst_m('Medal Efficiency Pct','Avg'),
  ref('M','Total Medals','m','Sum'),ref('M','Investment Score','m','Avg'),'Circle',
  f"<color column='{ref('M','Region','d')}' /><size column='{ref('M','Medal Efficiency Pct','m','Avg')}' /><lod column='{ref('M','Country','d')}' />"))
# 5 pie efficiency by region
S.append(sheet('Avg Medal Efficiency by Region','M',
  dim('Region')+meas('Medal Efficiency Pct','real')+inst_d('Region')+inst_m('Medal Efficiency Pct','Avg'),'','','Pie',
  f"<wedge-size column='{ref('M','Medal Efficiency Pct','m','Avg')}' /><color column='{ref('M','Region','d')}' /><text column='{ref('M','Medal Efficiency Pct','m','Avg')}' />"))
# 6 host nations
S.append(sheet('Medals Across Olympic Hosts','M',
  dim('Country')+dim('Host Advantage')+meas('Total Medals')+inst_d('Country')+inst_d('Host Advantage')+inst_m('Total Medals','Sum'),
  ref('M','Country','d'),ref('M','Total Medals','m','Sum'),'Bar',
  f"<color column='{ref('M','Total Medals','m','Sum')}' />",sort('M','Country','Total Medals','Sum','rows'),
  f"<filter class='categorical' column='{ref('M','Host Advantage','d')}'><groupfilter function='member' level='[none:Host Advantage:nk]' member='&quot;Host Nation&quot;' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate' /></filter>",
  title='Medal Totals of Host Nations (host-edition rows)'))
# 7 medal distribution by region
S.append(sheet('Medal Distribution by Region','R',
  dim('Region')+meas('Total Medals')+inst_d('Region')+inst_m('Total Medals','Sum'),'','','Pie',
  f"<wedge-size column='{ref('R','Total Medals','m','Sum')}' /><color column='{ref('R','Region','d')}' /><text column='{ref('R','Total Medals','m','Sum')}' />"))

zid=[100]
def z(name,x,y,w,h):
    zid[0]+=1; return f"<zone h='{h}' id='{zid[0]}' name='{E(name)}' w='{w}' x='{x}' y='{y}' />"
def dash(name,zones,W=1400,H=900):
    zid[0]+=1
    return f"""<dashboard name='{E(name)}'><style /><size maxheight='{H}' maxwidth='{W}' minheight='{H}' minwidth='{W}' sizing-mode='fixed' />
<zones><zone h='100000' id='{zid[0]}' type-v2='layout-basic' w='100000' x='0' y='0'>{''.join(zones)}</zone></zones></dashboard>"""
D1=dash('Olympic Performance Dashboard',[z('Avg Medals per Athlete by Category',500,1000,48500,48000),z('Global Performance by Country',50000,1000,48500,48000),z('Trend of Total Medals Awarded',500,50000,98000,48500)])
D2=dash('Regional Efficiency Dashboard',[z('Sports Investment vs Medal Performance',500,1000,48500,48000),z('Avg Medal Efficiency by Region',50000,1000,48500,48000),z('Medals Across Olympic Hosts',500,50000,48500,48500),z('Medal Distribution by Region',50000,50000,48500,48500)])
NM=[re.search(r"<worksheet name='([^']+)'",x).group(1) for x in S]
def win(n): return "<window class='worksheet' name='"+n+"'><cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge><edge name='top'><strip size='2147483647'><card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip><strip size='31'><card type='title' /></strip></edge></cards></window>"
wins=''.join(win(n) for n in NM)
wins+=''.join(f"<window class='dashboard' name='{n}'><viewpoints /><active id='-1' /></window>" for n in ('Olympic Performance Dashboard','Regional Efficiency Dashboard'))
twb=f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2023.1.0 (20231.23.0316.1717)' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
<preferences><preference name='ui.encoding.shelf.height' value='24' /><preference name='ui.shelf.height' value='26' /></preferences>
<datasources>{''.join(dsxml(k) for k in DS)}</datasources>
<worksheets>{''.join(S)}</worksheets>
<dashboards>{D1}{D2}</dashboards>
<windows source-height='30'>{wins}</windows>
</workbook>"""
from xml.dom import minidom; minidom.parseString(twb.encode())  # well-formedness check
open('Olympic_Performance2.twb','w',encoding='utf-8').write(twb)
with zipfile.ZipFile('/mnt/user-data/outputs/Olympic_Performance_Analysis_Extracts.twbx','w',zipfile.ZIP_DEFLATED) as zf:
    zf.write('Olympic_Performance2.twb','Olympic_Performance.twb')
    for f in files: zf.write('Extracts/'+f.replace('.csv','.hyper'),'Data/Extracts/'+f.replace('.csv','.hyper'))
print('ok')
