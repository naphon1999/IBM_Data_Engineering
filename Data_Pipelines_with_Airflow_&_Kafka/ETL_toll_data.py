from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Define the DAG arguments
dag_args = {
    'owner': 'dummy_owner',  # Replace with your dummy name
    'start_date': datetime.today(),
    'email': 'dummyemail@example.com',  # Replace with your dummy email
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'ETL_toll_data',  # DAG ID
    default_args=dag_args,
    description='Apache Airflow Final Assignment',  # Description of the DAG
    schedule_interval='@daily',  # Schedule to run daily once
)

# Task 1: unzip_data - Unzips the data
unzip_task = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzvf /path/to/your/data.tar.gz -C /path/to/destination/directory/',  # Replace with actual paths
    dag=dag,
)

# Task 2: extract_data_from_csv - Extracts data from CSV file
extract_data_from_csv_task = BashOperator(
    task_id='extract_data_from_csv',
    bash_command=(
        'awk -F, \'NR > 1 {print $1 "," $2 "," $3 "," $4}\' /path/to/vehicle-data.csv > /path/to/csv_data.csv'  # Replace paths
    ),
    dag=dag,
)

# Task 3: extract_data_from_tsv - Extracts data from TSV file
extract_data_from_tsv_task = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command=(
        'awk -F"\t" \'NR > 1 {print $1 "," $2 "," $3}\' /path/to/tollplaza-data.tsv > /path/to/tsv_data.csv'  # Replace paths
    ),
    dag=dag,
)

# Task 4: extract_data_from_fixed_width - Extracts data from Fixed Width file
extract_data_from_fixed_width_task = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command=(
        'awk \'{print substr($0, 1, 5) "," substr($0, 6, 10)}\' /path/to/payment-data.txt > /path/to/fixed_width_data.csv'  # Replace paths
    ),
    dag=dag,
)

# Task 5: consolidate_data - Consolidates data from all previous extractions
consolidate_data_task = BashOperator(
    task_id='consolidate_data',
    bash_command=(
        'paste -d, /path/to/csv_data.csv /path/to/tsv_data.csv /path/to/fixed_width_data.csv > /path/to/extracted_data.csv'
    ),  # Replace paths with the actual file paths
    dag=dag,
)

# Task 6: transform_data - Transforms vehicle type to uppercase
transform_data_task = BashOperator(
    task_id='transform_data',
    bash_command=(
        'awk -F, \'BEGIN {OFS=","} { $4 = toupper($4); print $0 }\' /path/to/extracted_data.csv > /path/to/staging/transformed_data.csv'
    ),  # Replace paths as necessary
    dag=dag,
)

# Set task dependencies (define task pipeline order)
unzip_task >> extract_data_from_csv_task >> extract_data_from_tsv_task >> extract_data_from_fixed_width_task >> consolidate_data_task >> transform_data_task
