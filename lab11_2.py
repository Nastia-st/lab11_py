import pandas as pd
import matplotlib.pyplot as plt

print("1. Завантаження та підготовка даних")
try:
    df = pd.read_csv('comptagevelo2017.csv')
except FileNotFoundError:
    print("Помилка: Файл 'comptagevelo2017.csv' не знайдено. Будь ласка, завантажте його.")
    exit()

#Приведення колонки дати до типу datetime та встановлення як індексу
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df = df.set_index('Date')
elif 'Date_Hour' in df.columns:
    df['Date'] = pd.to_datetime(df['Date_Hour'], dayfirst=True)
    df = df.set_index('Date')
    df = df.drop(columns=['Date_Hour'])

# Видалення допоміжних колонок, які не є лічильниками
cols_to_drop = [col for col in ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2'] if col in df.columns]
df = df.drop(columns=cols_to_drop, errors='ignore')

print("\n2. Перевірка характеристик датафрейму")
print("\ndf.head()")
print(df.head())
print("\ndf.info()")
df.info()
print("\ndf.describe()")
print(df.describe())

# Визначаємо колонки-лічильники
count_columns = df.columns

total_cyclists_year = df[count_columns].sum().sum()
print(f"\n3. Загальна кількість велосипедистів за 2017 рік: {total_cyclists_year:,.0f}")
total_cyclists_by_path = df[count_columns].sum().sort_values(ascending=False)
print("\n4. Загальна кількість велосипедистів на кожній велодоріжці за 2017 рік")
print(total_cyclists_by_path.to_string())

# Обираємо три найбільш завантажені велодоріжки
if len(count_columns) >= 3:
    selected_paths = total_cyclists_by_path.head(3).index.tolist()
else:
    selected_paths = count_columns.tolist()
df_monthly = df[selected_paths].resample('MS').sum() # Групування даних за місяцями

print("\n5. Найбільш популярний місяць на обраних велодоріжках")
for path in selected_paths:
    max_month_index = df_monthly[path].idxmax()
    max_month_name = max_month_index.strftime('%B')
    max_count = df_monthly[path].max()
    print(f"Дорожка '{path}': Найбільш популярний місяць — {max_month_name} ({max_count:,.0f} велосипедистів)")

# Побудова графіка завантаженості
path_for_plot = selected_paths[0]
plt.figure(figsize=(10, 6))
df_monthly[path_for_plot].plot(kind='bar', color='darkgreen')
plt.title(f'Завантаженість велодоріжки "{path_for_plot}" по місяцях (2017)', fontsize=14)
plt.xlabel('Місяць', fontsize=12)
plt.ylabel('Кількість велосипедистів', fontsize=12)
# Встановлюємо мітки як назви місяців
plt.xticks(ticks=range(len(df_monthly)), labels=df_monthly.index.strftime('%B'), rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
print(f"\n6. Графік завантаженості велодоріжки '{path_for_plot}' побудовано.")
plt.show()