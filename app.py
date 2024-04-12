import pandas as pd
import streamlit as st
from PIL import Image


from preprocess import load_inflation, load_salaries
from utils import plot_inflation, plot_salaries, plot_pct_change, find_corr


def process_main_page():
    show_main_page()
    process_side_bar_inputs()


def show_main_page():
    image = Image.open('data/img.png').resize((1000, 500))

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Demo Salary",
        page_icon=image,
    )

    st.write(
        """
        # Аналитика заработных плат с учётом инфляции
        Мы представляем анализ и сравнение реальных и номинальных зарплат в различных видах экономической деятельности.\n
        Вы можете выбрать как сами виды деятельности из списка, так и границы периода для анализа (его начало и конец).
        """
    )

    st.image(image)


def write_user_data(data):
    st.write("## Параметры запроса")

    if len(data['tps']) == 1:
        st.write("Пока не выбрано ни одного вида деятельности, будут отражены только средние значения.")
    else:
        st.write(f"Виды деятельности:    {', '.join(data['tps'][1:])}.")

    st.write(f"Анализируемый период: с {data['start']} года по {data['end']}.")


def write_analysis(salary_df, inflation_df, data):
    salary_df = salary_df.loc[data["tps"], list(map(str, range(data["start"], data["end"] + 1)))]
    inflation_df = inflation_df[range(data["start"], data["end"] + 1)]
    st.write("## Инфляция")
    st.write("Ниже представлена годовая инфляция для каждого года выбранного периода")
    st.pyplot(plot_inflation(inflation_df), use_container_width=False)

    st.write("## Влияние инфляции на рост заработных плат")
    st.write("""
        Для оценки влияния инфляции на изменение зарплат мы будем рассматривать относительное их изменение по сравнению 
        с предыдущим годом в процентах. Из-за этого инфляции 2000 года будет соответствовать это изменение за 2001 год, 
        инфляции 2001 - изменение за 2002 и так далее.\nГрафик ниже отражает распределение процента роста зарплат за 
        каждый год, поэтому данные на нём будут уточняться с ростом количества выбранных видов деятельности.
    """)
    st.pyplot(plot_pct_change(salary_df), use_container_width=False)

    st.write("## Поиск корреляций")
    st.write("""
        Уже можно заметить визуальное сходство усреднённого роста зарплаты и инфляции. 
        Чтобы численно определить выполнение этого сходства, мы посчитаем корреляцию между ростом для каждого 
        вида деятельности и инфляцией за предыдущий год.\nПодпись `средняя` задаёт показатели для усреднённой 
        заработной платы по всем видам деятельности.
    """)
    st.table(find_corr(salary_df, inflation_df))
    st.write("""
        Почти у всех видов деятельности прирост заработной платы имеет высокую корреляцию с инфляцией за 
        предыдущий год. Как и следовало ожидать, усреднённая зарплата имеет достаточно высокое значение коэффициента 
        корреляции, но не самый высокий средний прирост.
    """)

    st.write("## Уровень зарплат")
    st.write("""
        Здесь для каждого выбранного вида экономической деятельности показаны значения реальной и номинальной зарплаты. 
        Нормировка осуществляется на следующий год после конца периода с учётом годовой инфляции.\n
        График с подписью `средняя`, как и ранее, показывает динамику усреднённой заработной платы.
    """)
    st.pyplot(plot_salaries(salary_df, inflation_df), use_container_width=False)

    st.write("""
        Более полезным является график реальной зарплаты, поскольку он лучше отражает кризисы, которые выражаются в 
        заметных падениях. Номинальная же сумма не чувствительна к реальной стоимости валюты, поэтому полезна только 
        для сравнения заработных плат различных видов деятельности, но не для понимания их эффективной динамики.
    """)


def process_side_bar_inputs():
    salary_df = load_salaries()
    inflation_df = load_inflation()

    st.sidebar.header('Заданные пользователем параметры')
    data = sidebar_input_features(salary_df)

    write_user_data(data)

    write_analysis(salary_df, inflation_df, data)


def sidebar_input_features(salary_df):
    tp = st.sidebar.multiselect("Виды деятельности", tuple(salary_df.index)[1:])

    start_year = st.sidebar.slider("Начало периода", min_value=2000, max_value=2022, value=2000, step=1)
    end_year = st.sidebar.slider("Конец периода (включительно)", min_value=start_year + 1, max_value=2023, value=2023, step=1)

    data = {
        "tps": ["средняя"] + tp,
        "start": start_year,
        "end": end_year
    }

    return data


if __name__ == "__main__":
    process_main_page()
