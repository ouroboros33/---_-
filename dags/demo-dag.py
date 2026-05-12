from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Параметры по умолчанию
default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Описание DAG
with DAG(
    'demo_diplom_dag',
    default_args=default_args,
    description='Демонстрационный DAG для диплома. Запускается раз в 7 дней',
    schedule_interval='@weekly',  # Каждые 7 дней (в воскресенье)
    catchup=False,
    tags=['diplom', 'demo'],
) as dag:

    # Задача 1: Начало
    start = EmptyOperator(task_id='start')

    # Задача 2: Имитация загрузки данных
    extract = EmptyOperator(task_id='extract_data')

    # Задача 3: Имитация обработки
    transform = EmptyOperator(task_id='transform_data')

    # Задача 4: Имитация загрузки в хранилище
    load = EmptyOperator(task_id='load_to_dwh')

    # Задача 5: Завершение
    end = EmptyOperator(task_id='end')

    # Порядок выполнения (зависимости)
    start >> extract >> transform >> load >> end