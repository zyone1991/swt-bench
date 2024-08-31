"""
Method vs coverage
main
"""

import fire

from figures.util import *
from tabulate import tabulate
from datasets import load_dataset


def main(instance_log_path: str = "./run_instance_swt_logs", dataset_name: str = "princeton-nlp/SWE-bench_Lite", split: str = "test"):
    dataset = load_dataset(dataset_name)
    all_instances = {instance["instance_id"] for instance in dataset[split]}

    instance_log_path = Path(instance_log_path)
    if not instance_log_path.exists():
        raise FileNotFoundError(f"Instance log directory not found at {instance_log_path}")
    methods = [
        ("gold", f"validate-gold-{i}")
        for i in range(1, 6)
    ]
    resolved_instances = all_instances.copy()
    for model, run_id in methods:
        reports = collect_reports(model, run_id, instance_log_path, filter_cases=False)
        resolved_instances &= {instance_id for instance_id, report in reports.items() if report["resolved"]}
    print(f"Resolved by all: {len(resolved_instances)}")
    for instance in all_instances - resolved_instances:
        print(instance)

if __name__ == "__main__":
    fire.Fire(main)