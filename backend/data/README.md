# Dataset Directory

This directory contains the datasets used by the **Cloud Policy, Cost and Security Simulator**. The platform uses publicly available datasets to support cloud resource simulation, FinOps analysis, infrastructure monitoring, and AI assisted threat detection.

To keep the repository lightweight and easy to download, only processed or sample datasets are included. Large public datasets should be downloaded separately and preprocessed before use.

---

## Directory Structure

```text
backend/
└── data/
    ├── finops/
    │   ├── *.csv
    │   ├── *.tsv
    │   ├── *.json
    │   └── *.jsonl
    ├── cicids_subset.csv
    ├── dataset-3k-final.csv
    └── README.md
```

---

## Datasets

### Cloud Resource & FinOps

The simulator uses cloud workload and utilization datasets for generating realistic infrastructure metrics, including:

- CPU utilization
- Memory utilization
- Resource allocation
- Cost analysis
- Capacity planning
- Infrastructure monitoring

**Recommended Dataset**

- Alibaba Cluster Trace v2018

---

### Security & Threat Detection

The AI assisted Threat Detection module uses network traffic datasets to simulate cyber attacks and classify malicious activity.

The repository includes a lightweight subset of the **CICIDS2017** dataset for demonstration and testing purposes.

**Recommended Dataset**

- CICIDS2017 (Canadian Institute for Cybersecurity Intrusion Detection Dataset)

---

## Expected Data Schema

### FinOps / Resource Monitoring

Processed datasets should contain the following fields whenever available:

| Column |
|---------|
| date |
| total_cost |
| cpu_utilization_avg |
| memory_utilization_avg |
| provisioned_resources |
| idle_resources |

---

### Security / Threat Detection

Processed datasets should contain the following fields whenever available:

| Column |
|---------|
| label |
| requests_per_minute |
| avg_latency_ms |
| error_rate |
| bytes_in |
| bytes_out |
| active_connections |
| cpu_utilization |
| memory_utilization |
| disk_read_iops |
| disk_write_iops |
| network_in_mbps |
| network_out_mbps |
| auth_failures |

---

## Preparing Datasets

If downloading the original public datasets, preprocess them before using the simulator.

To regenerate the lightweight CICIDS subset included in this repository, run:

```bash
python backend/scripts/reduce_cicids.py
```

---

## Notes

- Only publicly available datasets are used.
- Sample datasets are included to simplify project setup.
- Large datasets are intentionally excluded from the repository because of GitHub storage limitations.
- Additional datasets can be added as long as they follow the expected schema described above.

---

## Disclaimer

This project is intended for **educational and research purposes only**. The included datasets are publicly available and are used solely to simulate cloud operations, infrastructure behavior, and cybersecurity scenarios within the Cloud Policy, Cost and Security Simulator.