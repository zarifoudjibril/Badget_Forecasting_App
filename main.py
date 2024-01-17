import pandas as pd
from pyweb import pydom
from pyodide.http import open_url
from pyscript import display, when
from js import console
# from pyscript import window, document

# csv file of sequencing
url = "https://raw.githubusercontent.com/zarifoudjibril/essai/main/investment_50.csv"
df = pd.read_csv(open_url(url))

av_read_cost = 139000
s = df['Country'][df['Investment Phase'] != 7].count()

# ASSUMPTIONS
aocp = 0.75  # additional output cost
yo = 3.5  # years operating
ipoto = 0.5  # percentage of time operating for improved stations
npoto = 0.3  # percentage of time operating for newly installed stations
iep = 0.07  # percentage for ie
tfp = 0.01  # percentage for trustee fee
budget_six = 30543829  # (all six 1st batch country badget)
budget_five = budget_six - 2168056  # (South Sudan budget)


def loadFromURL(event):
    # geting values from select

    # South Sudan Case
    if pydom['select'].value == ['7']:
        n = df['Country'][df['Country'] ==
                          'South Sudan'].count()
        si = df['Gap(improve)'][df['Country']
                                == 'South Sudan'].sum()
        sn = df['Gap(new)'][df['Country'] ==
                            'South Sudan'].sum()
        ui = df['Gap(improve)_u'][df['Country']
                                  == 'South Sudan'].sum()
        un = df['Gap(new)_u'][df['Country'] ==
                              'South Sudan'].sum()
        df_selected = df[['Country',
                          'Gap(total)', 'Gap(improve)', 'Gap(new)', 'Gap(total)_u','Gap(improve)_u', 'Gap(new)_u']][df['Country'] ==
                                                                                       'South Sudan']

        display(df_selected, target="#inputs", append=False)
    # First Batch except South Sudan
    elif pydom['select'].value == ['1']:
        n = df['Country'][df['Investment Phase'] ==
                          int(pydom['select'].value[0])].count() - 1
        si = df['Gap(improve)'][df['Investment Phase']
                                == int(pydom['select'].value[0])].sum()-2
        sn = df['Gap(new)'][df['Investment Phase'] ==
                            int(pydom['select'].value[0])].sum()-14
        ui = df['Gap(improve)_u'][df['Investment Phase']
                                  == int(pydom['select'].value[0])].sum()-0
        un = df['Gap(new)_u'][df['Investment Phase'] ==
                              int(pydom['select'].value[0])].sum()-3
        df_selected = df[['Country',
                          'Gap(total)', 'Gap(improve)', 'Gap(new)', 'Gap(total)_u','Gap(improve)_u', 'Gap(new)_u']][(df['Investment Phase'] ==
                                                                                       int(pydom['select'].value[0])) & (df['Country'] !=
                                                                                                                         'South Sudan')]
        

        display(df_selected, target="#inputs", append=False)
        pydom["#inputs_surface_total"].html = f"Total Surface Gap (total): {df['Gap(total)'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()-16}"
        pydom["#inputs_surface_improve"].html = f"Total Surface Gap(improve): {df['Gap(improve)'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()-2}"
        pydom["#inputs_surface_new"].html = f"Total Surface Gap(new): {df['Gap(new)'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()-14}"
        pydom["#inputs_upper_total"].html = f"Total Upper-air Gap (total): {df['Gap(total)_u'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()-3}"
        pydom["#inputs_upper_improve"].html = f"Total Upper-air Gap (improve): {df['Gap(improve)_u'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()-0}"
        pydom["#inputs_upper_new"].html = f"Total Upper-air Gap (new): {df['Gap(new)_u'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()-3}"
        
        # print(n, si, sn, ui, un)
    else:
        n = df['Country'][df['Investment Phase'] ==
                          int(pydom['select'].value[0])].count()
        si = df['Gap(improve)'][df['Investment Phase']
                                == int(pydom['select'].value[0])].sum()
        sn = df['Gap(new)'][df['Investment Phase'] ==
                            int(pydom['select'].value[0])].sum()
        ui = df['Gap(improve)_u'][df['Investment Phase']
                                  == int(pydom['select'].value[0])].sum()
        un = df['Gap(new)_u'][df['Investment Phase'] ==
                              int(pydom['select'].value[0])].sum()
        df_selected = df[['Country',
                          'Gap(total)', 'Gap(improve)', 'Gap(new)', 'Gap(total)_u','Gap(improve)_u', 'Gap(new)_u']][df['Investment Phase'] ==
                                                                                       int(pydom['select'].value[0])]
        
        display(df_selected, target="#inputs", append=False)
        pydom["#inputs_surface_total"].html = f"Total Surface Gap (total): {df['Gap(total)'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()}"
        pydom["#inputs_surface_improve"].html = f"Total Surface Gap(improve): {df['Gap(improve)'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()}"
        pydom["#inputs_surface_new"].html = f"Total Surface Gap(new): {df['Gap(new)'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()}"
        pydom["#inputs_upper_total"].html = f"Total Upper-air Gap (total): {df['Gap(total)_u'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()}"
        pydom["#inputs_upper_improve"].html = f"Total Upper-air Gap (improve): {df['Gap(improve)_u'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()}"
        pydom["#inputs_upper_new"].html = f"Total Upper-air Gap (new): {df['Gap(new)_u'][df['Investment Phase'] == int(pydom['select'].value[0])].sum()}"
       

# Mic

    # READINESS
    rpc = n * av_read_cost  # readiness peer advisor cost

    # INVESTMENT
    ipc = 3*rpc  # investment peer advisor cost
    ic = 1000*(35*si + 70*sn + 250*ui + 750*un)
    aoc = ic * aocp
    om = yo*1000*(5*(si*ipoto+sn*npoto)+260*(ui * ipoto + un * npoto))  # O&M

    # OVERHEADS
    soff = 3_000_000/s + (6_000_000/s)*n  # SOFF secretariat cost
    iec = (ic + aoc + om)*iep
    tf = (rpc + ipc + ic + aoc + om + soff + iec) * tfp  # trustee fee

    # TOTAL
    total_cost = rpc + ipc + ic + aoc + om + soff + iec + tf  # total cost
    total_cost_wr = ipc + ic + aoc + om + soff + iec + tf  # total cost without readiness

    pydom["#rpc-value"].html = int(rpc)
    pydom["#ipc-value"].html = int(ipc)
    pydom["#ic-value"].html = int(ic)
    pydom["#aoc-value"].html = int(aoc)
    pydom["#om-value"].html = int(om)
    pydom["#soff-value"].html = int(soff)
    pydom["#iec-value"].html = int(iec)
    pydom["#tf-value"].html = int(tf)
    pydom["#total-cost-value"].html = int(total_cost_wr)

    # Displaying hidden elements
    pydom["#note"].html = ""
    pydom["div#resp"].style["display"] = "flex"
    pydom["#avg"].style["display"] = "block"
    pydom["#finals"].style["display"] = "block"
    pydom["#grands"].style["display"] = "block"
    pydom["#future-expenses"].style["display"] = "block"
    pydom['#inputs'].style["display"] = "block"
    pydom["#title-gbon"].style["display"] = "block"
    pydom["#gbon"].style["display"] = "flex"

    # Header Message
    if pydom['select'].value[0] == "1":
        pydom["#note"].html = pydom['select'].value[0] + \
            "st Batch Budget Estimation - South Sudan Excluded (All values in USD)"
    elif pydom['select'].value[0] == "2":
        pydom["#note"].html = pydom['select'].value[0] + \
            "nd Batch Budget Estimation (All values in USD)"
    elif pydom['select'].value[0] == "3":
        pydom["#note"].html = pydom['select'].value[0] + \
            "rd Batch Budget Estimation (All values in USD)"
    elif pydom['select'].value[0] == "7":
        pydom["#note"].html = "South Sudan Batch Budget Estimation (All values in USD)"
    else:
        pydom["#note"].html = pydom['select'].value[0] + \
            "th Batch Budget Estimation (All values in USD)"

    # display(None, target="note", append="True")

    # 1st batch

    # total cost

    if pydom['select'].value == ['1']:
        total_cost_first = budget_five + av_read_cost * n
        total_cost_first_wr = budget_five
        # display(n)
    else:
        total_cost_first = (budget_five/5 + av_read_cost) * n
        total_cost_first_wr = (budget_five/5) * n
        # display(n)
    pydom["#total-cost1-value"].html = int(total_cost_first_wr)
    avg = (total_cost_wr+total_cost_first_wr)/2
    pydom["#avg-total-cost-value"].html = int(avg)

    if pydom['select'].value == ['1']:
        pydom['#actual-total-cost-value'].html = total_cost_first_wr
        pydom['#difference-value'].html = int(avg - total_cost_first_wr)
        total_cost_first_wr = budget_five
        if avg > total_cost_first_wr:
            pydom['#avg tr:nth-last-child(1)'].style["background-color"] = '#018c85'
        else:
            pydom['#avg tr:nth-last-child(1)'].style["background-color"] = '#D9654C'
    else:
        pydom['#actual-total-cost-value'].html = ""
        pydom['#difference-value'].html = ""

    # ALL_MIC
    # 7 Sudan
    n7 = df['Country'][df['Country'] ==
                       'South Sudan'].count()
    si7 = df['Gap(improve)'][df['Country']
                             == 'South Sudan'].sum()
    sn7 = df['Gap(new)'][df['Country'] ==
                         'South Sudan'].sum()
    ui7 = df['Gap(improve)_u'][df['Country']
                               == 'South Sudan'].sum()
    un7 = df['Gap(new)_u'][df['Country'] ==
                           'South Sudan'].sum()
    # READINESS
    rpc = n7 * av_read_cost  # readiness peer advisor cost
    # INVESTMENT
    ipc = 3*rpc  # investment peer advisor cost
    ic = 1000*(35*si7 + 70*sn7 + 250*ui7 + 750*un7)
    aoc = ic * aocp
    om = yo*1000*(5*(si7*ipoto+sn7*npoto)+260 *
                  (ui7 * ipoto + un7 * npoto))  # O&M
    # OVERHEADS
    soff = 3_000_000/s + (6_000_000/s)*n7  # SOFF secretariat cost
    iec = (ic + aoc + om)*iep
    tf = (rpc + ipc + ic + aoc + om + soff + iec) * tfp  # trustee fee
    # TOTAL
    total_cost7 = rpc + ipc + ic + aoc + om + soff + iec + tf  # total cost
    total_cost_first7 = (budget_five/5 + av_read_cost) * n7

    # 1 except South Sudan
    n1 = df['Country'][df['Investment Phase'] ==
                       1].count() - 1
    si1 = df['Gap(improve)'][df['Investment Phase']
                             == 1].sum()-2
    sn1 = df['Gap(new)'][df['Investment Phase'] ==
                         1].sum()-14
    ui1 = df['Gap(improve)_u'][df['Investment Phase']
                               == 1].sum()-0
    un1 = df['Gap(new)_u'][df['Investment Phase'] ==
                           1].sum()-3
    # READINESS
    rpc = n1 * av_read_cost  # readiness peer advisor cost
    # INVESTMENT
    ipc = 3*rpc  # investment peer advisor cost
    ic = 1000*(35*si1 + 70*sn1 + 250*ui1 + 750*un1)
    aoc = ic * aocp
    om = yo*1000*(5*(si1*ipoto+sn1*npoto)+260 *
                  (ui1 * ipoto + un1 * npoto))  # O&M
    # OVERHEADS
    soff = 3_000_000/s + (6_000_000/s)*n1  # SOFF secretariat cost
    iec = (ic + aoc + om)*iep
    tf = (rpc + ipc + ic + aoc + om + soff + iec) * tfp  # trustee fee
    # TOTAL
    total_cost1 = rpc + ipc + ic + aoc + om + soff + iec + tf  # total cost
    total_cost_first1 = budget_five + av_read_cost * n1
    # 2,3,4,5,6
    lis_t = [2, 3, 4, 5, 6]
    lis_tt = []
    lis_tt2 = []
    for i in lis_t:
        ni = df['Country'][df['Investment Phase'] ==
                           i].count()
        sii = df['Gap(improve)'][df['Investment Phase']
                                 == i].sum()
        sni = df['Gap(new)'][df['Investment Phase'] ==
                             i].sum()
        uii = df['Gap(improve)_u'][df['Investment Phase']
                                   == i].sum()
        uni = df['Gap(new)_u'][df['Investment Phase'] ==
                               i].sum()
        # READINESS
        rpc = ni * av_read_cost  # readiness peer advisor cost
        # INVESTMENT
        ipc = 3*rpc  # investment peer advisor cost
        ic = 1000*(35*sii + 70*sni + 250*uii + 750*uni)
        aoc = ic * aocp
        om = yo*1000*(5*(sii*ipoto+sni*npoto)+260 *
                      (uii * ipoto + uni * npoto))  # O&M
        # OVERHEADS
        soff = 3_000_000/s + (6_000_000/s)*ni  # SOFF secretariat cost
        iec = (ic + aoc + om)*iep
        tf = (rpc + ipc + ic + aoc + om + soff + iec) * tfp  # trustee fee
        # TOTAL
        total_costi = rpc + ipc + ic + aoc + om + soff + iec + tf  # total cost
        total_cost_firsti = (budget_five/5 + av_read_cost) * ni
        lis_tt.append(total_costi)
        lis_tt2.append(total_cost_firsti)
        # display(total_cost_firsti, ni)
    lis_tt.extend([total_cost1, total_cost7])
    lis_tt2.extend([total_cost_first1, total_cost_first7])
    # display(lis_tt, lis_tt2)
    mic_final = sum(lis_tt)
    first_final = sum(lis_tt2)
    pydom['#final-cost-value-mic'].html = int(mic_final)
    pydom['#final-cost-value-first'].html = int(first_final)
    avg_final = (mic_final+first_final)/2
    pydom['#final-cost-value-avg'].html = int(avg_final)

    # Grand Total
    gr_mic = mic_final + av_read_cost * (61-s+14)
    gr_first = first_final + av_read_cost * (61-s+14)
    gr_avg = (gr_first + gr_mic)/2
    pydom['#final-cost-value-mic-gr'].html = int(gr_mic)
    pydom['#final-cost-value-first-gr'].html = int(gr_first)
    pydom['#final-cost-value-avg-gr'].html = int(gr_avg)

    # Future Expenses
    f_mic = mic_final + av_read_cost * (61 - s - 45+14)
    f_first = first_final + av_read_cost * (61 - s - 45+14)
    f_avg = (f_first + f_mic)/2
    pydom['#fcost-mic-value'].html = int(f_mic)
    pydom['#fcost-first-value'].html = int(f_first)
    pydom['#fcost-avg-value'].html = int(f_avg)
