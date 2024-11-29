import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os
import time
from pynput import keyboard
from tabulate import tabulate

key_timings = {
    'Key': [], 
    'Press_Time': [], 
    'Release_Time': [], 
    'Hold_Duration': [], 
    'Interval_Between_Keys': []
}

last_release_time = None

def on_press(key):
    global last_release_time
    try:
        key_str = str(key.char) 
    except AttributeError:
        key_str = str(key)  

    press_time = time.time() 
    key_timings['Key'].append(key_str) 
    key_timings['Press_Time'].append(press_time) 

    if last_release_time is not None:
        interval = press_time - last_release_time 
        key_timings['Interval_Between_Keys'].append(interval)

    else:
        key_timings['Interval_Between_Keys'].append(None)

def on_release(key):
    global last_release_time
    release_time = time.time()
    key_timings['Release_Time'].append(release_time) 

    if key_timings['Press_Time']:
        hold_duration = release_time - key_timings['Press_Time'][-1]
        key_timings['Hold_Duration'].append(hold_duration)

    else:
        key_timings['Hold_Duration'].append(None) 

    last_release_time = release_time 
    if key == keyboard.Key.esc: 
        return False



def save_key_sequence(file_path):
    """Зберігає послідовність натискань клавіш у текстовому файлі."""
    sequence = ''.join(key_timings['Key'])
    with open(file_path, 'w') as f:
        f.write(sequence) 

def collect_keystroke_data(file_path):
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    max_length = max(len(key_timings[key]) for key in key_timings)
    for key in key_timings:
        if len(key_timings[key]) < max_length:
            key_timings[key].extend([None] * (max_length - len(key_timings[key])))

    df = pd.DataFrame(key_timings)
    df['Interval_Between_Keys'] = df['Interval_Between_Keys'].fillna(0) 
    df.to_csv(file_path, index=False)

    sequence_file_path = os.path.splitext(file_path)[0] + "_key_sequence.txt"

    save_key_sequence(sequence_file_path)

    return file_path

def normalize_column_names(df):
    column_mapping = {
        'key': 'Key', 'press_time': 'Press_Time', 'release_time': 'Release_Time',
        'hold_duration': 'Hold_Duration', 'interval_between_keys': 'Interval_Between_Keys'
    }
    df = df.rename(columns=column_mapping)
    return df

def load_data(file_path):
    file_extension = os.path.splitext(file_path)[1].lower() 
    if file_extension == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    return normalize_column_names(df) 

def analyze_keyboard_biometrics(file_path):
    df = load_data(file_path)
    sns.set_theme() 

    fig = plt.figure(figsize=(20, 15)) 

    plt.subplot(2, 2, 1)
    sns.boxplot(data=df, x='Key', y='Hold_Duration', hue='Key', palette="viridis", legend=False)
    plt.title('Розподіл тривалості утримання клавіш')

    plt.subplot(2, 2, 2)
    plt.hist(df['Interval_Between_Keys'].dropna(), bins=30, color='skyblue', edgecolor='black')
    plt.title('Розподіл інтервалів між клавішами')

    pivot_df = df.pivot_table(index='Key', values='Hold_Duration', aggfunc=['mean', 'std']).round(3)

    if not pivot_df.empty:
        plt.subplot(2, 2, 3)
        sns.heatmap(pivot_df, annot=True, cmap='YlGnBu')
        plt.title('Теплова карта середньої тривалості утримання')

    plt.subplot(2, 2, 4)
    plt.scatter(df.index, df['Hold_Duration'], alpha=0.5, color='teal')
    plt.title('Патерн тривалості утримання протягом часу')

    plt.tight_layout() 
    output_dir = os.path.dirname(file_path)  
    output_path = os.path.join(output_dir, 'keyboard_biometrics_analysis.png')

    plt.savefig(output_path) 
    plt.close() 

    stats_df = pd.DataFrame()
    for key in df['Key'].unique():
        key_data = df[df['Key'] == key] 
        stats_dict = {
            'Клавіша': key,
            'Кількість натискань': len(key_data),
            'Середня тривалість утримання': key_data['Hold_Duration'].mean(),
            'СКВ тривалості': key_data['Hold_Duration'].std(),
            'Середній інтервал після': key_data['Interval_Between_Keys'].mean(),
            'СКВ інтервалу': key_data['Interval_Between_Keys'].std()
        }
        stats_df = pd.concat([stats_df, pd.DataFrame([stats_dict])], ignore_index=True) 

    metrics = {
        'Загальна швидкість друку (символів/сек)': len(df) / (df['Press_Time'].max() - df['Press_Time'].min()),
        'Середня тривалість утримання (сек)': df['Hold_Duration'].mean(),
        'Середній інтервал між клавішами (сек)': df['Interval_Between_Keys'].mean(),
        'Варіація тривалості утримання': stats.variation(df['Hold_Duration']),
        'Варіація інтервалів': stats.variation(df['Interval_Between_Keys'])
    }

    stats_output_path = os.path.join(output_dir, 'keyboard_biometrics_stats.xlsx')

    with pd.ExcelWriter(stats_output_path) as writer:
        stats_df.round(4).to_excel(writer, sheet_name='Статистика по клавішах', index=False)
        pd.DataFrame([metrics]).round(4).transpose().to_excel(writer, sheet_name='Загальні метрики')

    return stats_df, metrics 

def print_analysis_results(stats_df, metrics):
    print("\n\nСТАТИСТИКА ПО КЛАВІШАХ")
    print(tabulate(stats_df.round(4), headers='keys', tablefmt='pretty'))

    print("\nЗАГАЛЬНІ МЕТРИКИ")
    metrics_table = [[metric, f"{value:.4f}"] for metric, value in metrics.items()]
    print(tabulate(metrics_table, headers=["Метрика", "Значення"], tablefmt='pretty'))

def run_analysis(file_path):
    stats_df, metrics = analyze_keyboard_biometrics(file_path)
    print_analysis_results(stats_df, metrics) 

file_path = "/Users/mukha/Documents/Унік/3й курс/Сем 1/зпд/code/lab_13/result.csv"
collected_file = collect_keystroke_data(file_path) 
run_analysis(collected_file) 
