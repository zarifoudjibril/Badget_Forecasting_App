import pandas as pd
from pyweb import pydom
from pyodide.http import open_url
from pyscript import display, when
from js import console
# from pyscript import window, document

# csv file of sequencing
url_c = "https://raw.githubusercontent.com/zarifoudjibril/Badget_Forecasting_App/main/149_investment_budget_gbon.csv"
df1 = pd.read_csv(open_url(url_c))
country_list = df1['Country'].to_list()

av_read_cost_c = 139000
s_c = 50

# ASSUMPTIONS
aocp_c = 0.75  # additional output cost
yo_c = 3.5  # years operating
ipoto_c = 0.5  # percentage of time operating for improved stations
npoto_c = 0.3  # percentage of time operating for newly installed stations
iep_c = 0.07  # percentage for ie
tfp_c = 0.01  # percentage for trustee fee
budget_six_c = 30543829  # (all six 1st batch country badget)
budget_five_c = budget_six_c - 2168056  # (South Sudan budget)


@when('click', '#btn-load-c')
def click_handler(event):
    pydom['body'].style['grid-template-rows'] = '1fr auto'
    # geting values from select
    console.log(country_list)
    # for country in country_list:
    country = pydom['#countries-c'].value[0]
    console.log(country)
    n_c = 1
    si_c = df1['Gap(improve)'][df1['Country']
                               == country].sum()
    sn_c = df1['Gap(new)'][df1['Country'] ==
                           country].sum()
    ui_c = df1['Gap(improve)_u'][df1['Country']
                                 == country].sum()
    un_c = df1['Gap(new)_u'][df1['Country'] ==
                             country].sum()
    df_selected_c = df1[['Country',
                         'Gap(improve)', 'Gap(new)', 'Gap(improve)_u', 'Gap(new)_u']][df1['Country'] ==
                                                                                      country]

    display(df_selected_c, target="#inputs-c", append=False)

    # Display gbon

    # pydom["#inputs_surface_total-c"].html = f"Surface {df1[['Gap(total)']][df1['Country'] == country].to_html(index=False)}"
    # pydom["#inputs_surface_improve-c"].html = f" - {df1[['Gap(improve)']][df1['Country'] == country].to_html(index=False)}"
    # pydom["#inputs_surface_new-c"].html = f" - {df1[['Gap(new)']][df1['Country'] == country].to_html(index=False)}"
    # pydom["#inputs_upper_total-c"].html = f"Upper-air {df1[['Gap(total)_u']][df1['Country'] == country].to_html(index=False)}"
    # pydom["#inputs_upper_improve-c"].html = f" - {df1[['Gap(improve)_u']][df1['Country'] == country].to_html(index=False)}"
    # pydom["#inputs_upper_new-c"].html = f" - {df1[['Gap(new)_u']][df1['Country'] == country].to_html(index=False)}"


# Mic

    # READINESS
    rpc_c = n_c * av_read_cost_c  # readiness peer advisor cost

    # INVESTMENT
    ipc_c = 3*rpc_c  # investment peer advisor cost
    ic_c = 1000*(35*si_c + 70*sn_c + 250*ui_c + 750*un_c)
    aoc_c = ic_c * aocp_c
    om_c = yo_c*1000*(5*(si_c*ipoto_c+sn_c*npoto_c)+260 *
                      (ui_c * ipoto_c + un_c * npoto_c))  # O&M

    # OVERHEADS
    soff_c = 3_000_000/s_c + (6_000_000/s_c)*n_c  # SOFF secretariat cost
    iec_c = (ic_c + aoc_c + om_c)*iep_c
    tf_c = (rpc_c + ipc_c + ic_c + aoc_c + om_c +
            soff_c + iec_c) * tfp_c  # trustee fee

    # TOTAL
    total_cost = rpc_c + ipc_c + ic_c + aoc_c + \
        om_c + soff_c + iec_c + tf_c  # total cost
    total_cost_wr_c = ipc_c + ic_c + aoc_c + om_c + \
        soff_c + iec_c + tf_c   # total cost without readiness

    pydom["#rpc-value-c"].html = int(rpc_c)
    pydom["#ipc-value-c"].html = int(ipc_c)
    pydom["#ic-value-c"].html = int(ic_c)
    pydom["#aoc-value-c"].html = int(aoc_c)
    pydom["#om-value-c"].html = int(om_c)
    pydom["#soff-value-c"].html = int(soff_c)
    pydom["#iec-value-c"].html = int(iec_c)
    pydom["#tf-value-c"].html = int(tf_c)
    pydom["#total-cost-value-c"].html = int(total_cost_wr_c)

    # Displaying hidden elements
    pydom["#note-c"].html = ""
    pydom["div#resp-c"].style["display"] = "flex"
    pydom['#inputs-c'].style["display"] = "block"
    pydom["#title-gbon-c"].style["display"] = "block"
    pydom["#gbon-c"].style["display"] = "flex"
    pydom["#note-c"].html = ""
    pydom["#avg-c"].style["display"] = "block"
    pydom["#per-country"].style["border-style"] = "solid"
    pydom["#per-country"].style["border-width"] = "2px"
    pydom["#per-country"].style["border-color"] = "#D9654C"
    pydom["#per-country"].style["padding"] = "10px"

    # Header Message
    pydom["#note-c"].html = pydom['#countries-c'].value[0] + \
        " Budget Estimation (USD)"


# Actual based on First Batch
    total_cost_first_wr_c = (total_cost_wr_c + 369786.42690992)/0.82842479
    # display(n)
    pydom["#total-cost1-value-c"].html = int(total_cost_first_wr_c)


# Actuals
    budget_act = df1['Investment_budget'][df1['Country'] == country].sum()
    if budget_act == 0:
        pydom["#actual-total-cost-value-c"].html = " "
        pydom["#difference-value-c"].html = " "
    else:
        pydom["#actual-total-cost-value-c"].html = budget_act
        pydom["#difference-value-c"].html = int(total_cost_first_wr_c- budget_act) 
        if total_cost_first_wr_c > budget_act:
            pydom['#avg-c tr:nth-last-child(1)'].style["background-color"] = '#018c85'
            pydom['#avg-c tr:nth-last-child(1)'].style["color"] = '#ffffff'
        else:
            pydom['#avg-c tr:nth-last-child(1)'].style["background-color"] = '#D9654C'
            pydom['#avg-c tr:nth-last-child(1)'].style["color"] = '#ffffff'
