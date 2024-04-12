import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_inflation(inflation_df):
    plt.close()
    plt.gcf().set_size_inches(5, 2)
    plt.title("Значения инфляции в %", fontsize=10)
    sns.barplot(inflation_df)
    plt.xticks(rotation=90, fontsize=6)
    plt.yticks(fontsize=6)
    return plt.gcf()


def plot_salaries(salary_df, inflation_df):
    plt.close()
    coef_arr = np.cumprod(1 + np.array(inflation_df)[::-1] / 100)[::-1]

    plt.gcf().set_size_inches(5, 4)

    plt.subplot(1, 2, 1)
    plt.title("Номинальные зарплаты", fontsize=8)
    sns.lineplot(salary_df.transpose())
    plt.xticks(rotation=90, fontsize=5)
    plt.yticks(fontsize=5)
    plt.legend(bbox_to_anchor=(1, 1.3), loc="lower right", fontsize="3")

    plt.subplot(1, 2, 2)
    plt.title("Реальные зарплаты", fontsize=8)
    sns.lineplot(salary_df.transpose() * coef_arr.reshape(-1, 1), legend=False)
    plt.xticks(rotation=90, fontsize=5)
    plt.yticks(fontsize=5)

    plt.tight_layout()
    return plt.gcf()


def plot_pct_change(salary_df):
    plt.close()
    plt.gcf().set_size_inches(6, 2)
    plt.title("Процент роста зарплат на 2001-2023 года (по отношению к предыдущему)", fontsize=8)
    sns.boxplot(salary_df.transpose().pct_change().iloc[1:].transpose() * 100)
    plt.xticks(rotation=90, fontsize=5)
    plt.yticks(fontsize=5)
    return plt.gcf()


def find_corr(salary_df, inflation_df):
    infl_arr = np.array(inflation_df)
    corr_df = pd.DataFrame(columns=["Вид деятельности", "Коэффициент корреляции с инфляцией", "Средний прирост за год"])

    for name, row in (salary_df.transpose().pct_change().iloc[1:].transpose() * 100).iterrows():
        coef = np.corrcoef(row, infl_arr[:-1])[0, 1]
        corr_df.loc[len(corr_df)] = [name, coef, np.mean(row)]

    corr_df.index = corr_df["Вид деятельности"]
    corr_df.drop(columns=["Вид деятельности"], inplace=True)

    return corr_df.sort_values(by="Средний прирост за год", ascending=False)
