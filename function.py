import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec

def creazione_grafico(serie, df_soglie, id_check, serie_test,ord_type, df_actual_thresholds, percentile_distr_high, percentile_distr_high_perc, percentile_distr_low_perc):
    for j in serie.COMPANY_CODE.unique():
        for i in serie.NF_KEY.unique():
            df = serie[(serie["COMPANY_CODE"] == j) & (serie["NF_KEY"] == i) & (serie["NF_KEY"] != "AG")]
            # print(df)
            df_2 = df_soglie[(df_soglie["CC"] == j) & (df_soglie["metallo"] == i)]
            df_3 = df_actual_thresholds[
                (df_actual_thresholds["COMPANY_CODE"] == j) & (df_actual_thresholds["METAL"] == i) & (
                            df_actual_thresholds["CHECK_ID"] == id_check) & (df_actual_thresholds["ACTIVE"] == 1)]
            df_4 = serie_test[(serie_test["COMPANY_CODE"] == j) & (serie_test["NF_KEY"] == i)]
            if len(df_3) != 0:
                # print(df)
                if id_check in [2, 5, 7, 10, 13, 20, 21, 22]:
                    vett_medie = pd.DataFrame(df.groupby("WORKED_DATE")["DAILY_QTY"].mean()).reset_index()
                    # print(vett_medie)
                if id_check in [17, 18]:
                    vett_medie = pd.DataFrame(df.groupby("WORKED_DATE")["RATIO"].mean()).reset_index()
                if id_check in [1, 3, 6, 8, 12, 15, 16]:
                    vett_medie = np.array([])
                if len(df) != 0:
                    fig = plt.figure(figsize=(10, 6))
                    spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[3, 1], wspace=0.05, hspace=0.0)
                    plt.style.use('seaborn')
                    ax0 = fig.add_subplot(spec[0])
                    if id_check in [17, 18]:
                        ax0.plot_date(df.WORKED_DATE, df.RATIO, ms=6)
                        if len(vett_medie) != 0:
                            ax0.plot_date(vett_medie.WORKED_DATE, vett_medie.RATIO, ls='-', color='darkblue',
                                          marker=False, lw=2.5, alpha=0.7)
                    else:
                        ax0.plot_date(df.WORKED_DATE, df.DAILY_QTY, ms=6)
                        if len(vett_medie) != 0:
                            ax0.plot_date(vett_medie.WORKED_DATE, vett_medie.DAILY_QTY, ls='-', color='darkblue',
                                          marker=False, lw=2.5, alpha=0.7)
                    # ax0.axhline(df_2["soglia"].iloc[0], color='red', label="ML threshold (0.99)", alpha=0.5, lw=1.5)
                    ax0.axhline(df_3["THRESHOLD"].iloc[0] * 1000, color='green', label="MM threshold", alpha=0.5,
                                lw=2.5)
                    # ax0.axhline(df.DAILY_QTY.quantile(0.75) + 1.5*(df.DAILY_QTY.quantile(0.75) - df.DAILY_QTY.quantile(0.25)), color='black', label="ML threshold (Q3+1.5*IQR)", alpha=0.5, lw=2.5)
                    if id_check in [1, 2, 5, 6, 7, 10, 12, 13, 15, 20, 21, 22]:
                        ax0.axhline(df.DAILY_QTY.quantile(percentile_distr_high), color='black', label="ML threshold",
                                    alpha=0.5, lw=2.5)
                    if id_check in [17, 18]:
                        ax0.axhline(df.RATIO.quantile(percentile_distr_high), color='black', label="ML threshold",
                                    alpha=0.5, lw=2.5)
                    if id_check in [3, 8, 16]:
                        ax0.axhline(df_2["soglia"].iloc[0], color='black', label="ML threshold", alpha=0.5, lw=2.5)
                        # ax0.axhline(df.DAILY_QTY.quantile(percentile_distr_low), color='black', label="ML threshold", alpha=0.5, lw=2.5)
                    ax0.set_title(
                        ord_type + ' Orders check_id:' + str(id_check) + ' - Time Series last six months\nLE: ' + str(
                            j) + ' Metallo: ' + str(i))
                    ax0.tick_params(axis='y', labelsize=13)
                    ax0.legend(loc=0)
                    plt.xticks(rotation=45)

                    ax1 = fig.add_subplot(spec[1])
                    if id_check in [1, 2, 5, 6, 7, 10, 12, 13, 15, 20, 21, 22]:
                        ax1 = sns.boxplot(x="NF_KEY", y="DAILY_QTY", data=df, flierprops={'markersize': 0},
                                          color="orange", whis=[0, percentile_distr_high_perc])
                    if id_check in [17, 18]:
                        ax1 = sns.boxplot(x="NF_KEY", y="RATIO", data=df, flierprops={'markersize': 0}, color="orange",
                                          whis=[0, percentile_distr_high_perc])
                    if id_check in [3, 8, 16]:
                        ax1 = sns.boxplot(x="NF_KEY", y="DAILY_QTY", data=df, flierprops={'markersize': 0},
                                          color="orange", whis=[percentile_distr_low_perc, 100])
                        # ax1 = sns.boxplot(x="NF_KEY", y="DAILY_QTY", data=df, flierprops={'markersize':0}, color="orange", whis = [,100])
                    ax1.axhline(df_3["THRESHOLD"].iloc[0] * 1000, color='green', alpha=0.5, lw=2.5)
                    # ax1.axhline(df.DAILY_QTY.quantile(0.75) + 1.5*(df.DAILY_QTY.quantile(0.75) - df.DAILY_QTY.quantile(0.25)), color='red', alpha=0.5, lw=1.5)
                    ax1.set_title(
                        ord_type + ' Orders check_id:' + str(id_check) + '\nLE:' + str(j) + ' Metallo:' + str(i))
                    plt.yticks([])
                    if len(df_4) != 0:
                        #df_4["WORKED_DATE"] = df_4["WORKED_DATE"].dt.date
                        df_4["WORKED_DATE"] = pd.to_datetime(df_4["WORKED_DATE"])
                        df_4["WORKED_DATE"] = df_4["WORKED_DATE"].dt.date

                        if id_check in [1, 2, 3, 5, 6, 7, 8, 10, 12, 13, 15, 16, 20, 21, 22]:
                            ax1 = sns.stripplot(y='DAILY_QTY', data=df_4, size=6)
                        else:
                            ax1 = sns.stripplot(y='RATIO', data=df_4, size=6)
                    plt.ylabel("")
                    plt.grid(True)
                    lim1 = ax0.get_ylim()
                    lim2 = ax1.get_ylim()
                    if lim1[0] < lim2[0]:
                        lim_inf = lim1[0]
                    else:
                        lim_inf = lim2[0]
                    if lim1[1] > lim2[1]:
                        lim_sup = lim1[1]
                    else:
                        lim_sup = lim2[1]
                    ax0.set_ylim([lim_inf, lim_sup])
                    ax1.set_ylim([lim_inf, lim_sup])
                    plt.savefig(os.path.join(root_path, path_grafici) + today.strftime('%Y%m%d') + '/check_' + str(
                        id_check) + '/' + ord_type + '_orders_LE_' + str(j) + '_Met_' + str(
                        i))  # Purchase Orders LE:0435 Metallo:CU
                    # plt.show()