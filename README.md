
[![CircleCI](https://circleci.com/gh/prosehair/prose-pre-commit-hooks.svg?style=shield&circle-token=7effb344aa53d658f1cf4df1a907ffbd01a3c338)](https://circleci.com/gh/prosehair/prose-pre-commit-hooks)


prose-pre-commit-hooks
======================

Some hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit


## Using prose-pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/prosehair/prose-pre-commit-hooks
    rev: v0.0.1  # Use the ref you want to point at
    hooks:
    -   id: manage-airflow-dag-task-id
```

## Hooks available

#### `manage-airflow-dag-task-id`
Enforce the specification of version in dag filename and ensure the consistency between the dag file name, the dag_id and the task_id(s).

## As a standalone package

If you'd like to use these hooks, they're also available as a standalone package.

Simply `pip install prose-pre-commit-hooks`
