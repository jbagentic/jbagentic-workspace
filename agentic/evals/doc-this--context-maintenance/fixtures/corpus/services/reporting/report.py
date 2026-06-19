# Reporting service — builds usage and revenue reports.


def build_report(period):
    """Build a usage report for the given billing period."""
    raise NotImplementedError


def summarize(rows):
    """Aggregate raw rows into report totals."""
    raise NotImplementedError
