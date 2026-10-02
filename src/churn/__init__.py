"""churn -- the MLSecOps course telecom churn prediction project.

Stages are runnable as modules so that dvc.yaml can call them:
    python -m src.churn.prepare | python -m churn.train | python -m churn.evaluate
"""

__version__ = "0.3.0"
