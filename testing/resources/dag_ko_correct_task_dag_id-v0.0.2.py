import datetime
from functools import partial

from airflow import models
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from prose_airflow_plugin.callback_functions import task_fail_slack_alert

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)
SLACK_CONN_ID = "slack_prose_etl"

_task_fail_slack_alert = partial(task_fail_slack_alert, slack_conn_id=SLACK_CONN_ID)


default_args = {
    "owner": "airflow",
    "retries": 0,
    "on_failure_callback": task_fail_slack_alert,
}

with models.DAG(
    dag_id="dag_ko_correct_task_dag_id-v0.0.1",
    schedule_interval=datetime.timedelta(days=1),
    start_date=YESTERDAY,
    default_args=default_args,
) as dag:

    task_that_always_fails = BashOperator(
        task_id="task_that_always_fails-v0.0.1",
        bash_command="exit 1",
        dag=dag,
        on_failure_callback=_task_fail_slack_alert,
    )

    task_that_always_fails = BashOperator(
        task_id="task_that_always_fails2",
        bash_command="exit 1",
        dag=dag,
        on_failure_callback=_task_fail_slack_alert,
    )

    t_end = DummyOperator(task_id='prose_data_end-v0.0.2-beta5')
