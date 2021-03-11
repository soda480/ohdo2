import sys
import json
import logging
from string import Template

logger = logging.getLogger(__name__)

SUMMARY = Template("""
    Code scanned:
        Total lines of code: ${loc}
        Total lines skipped (#nosec): ${nosec}
    Run metrics:
        Total issues (by severity):
            Undefined: ${severity_undefined}
            Low: ${severity_low}
            Medium: ${severity_medium}
            High: ${severity_high}
        Total issues (by confidence):
            Undefined: ${confidence_undefined}
            Low: ${confidence_low}
            Medium: ${confidence_medium}
            High: ${confidence_high}""")


def read_data(filename):
    """ return dictionary read from bandit json file
    """
    with open(filename) as infile:
        return json.load(infile)


def get_summary(data):
    """ return string summary from bandit data
    """
    metrics = data.get('metrics', {}).get('_totals', {})
    # sanitize metrics keys to be valid variables to enable string substitution
    metrics_vars = {}
    for key, value in metrics.items():
        metrics_vars[key.lower().replace('.', '_')] = value
    summary = SUMMARY.substitute(metrics_vars)
    # remove leading spaces from string generated from string template
    return '\n'.join([line[4:] for line in summary.split('\n')])


def log_summary(data):
    """ log metrics from bandit data
    """
    totals = data.get('metrics', {}).get('_totals', {})
    logger.debug('Code scanned:')
    logger.debug(f"    Total lines of code: {totals.get('loc')}")
    logger.debug(f"    Total lines skipped (#nosec): {totals.get('nosec')}")
    logger.debug('Run metrics:')
    logger.debug('    Total issues (by severity):')
    logger.debug(f"        Undefined: {totals.get('SEVERITY.UNDEFINED')}")
    logger.debug(f"        Low: {totals.get('SEVERITY.LOW')}")
    logger.debug(f"        Medium: {totals.get('SEVERITY.MEDIUM')}")
    logger.debug(f"        High: {totals.get('SEVERITY.HIGH')}")
    logger.debug('    Total issues (by confidence):')
    logger.debug(f"        Undefined: {totals.get('CONFIDENCE.UNDEFINED')}")
    logger.debug(f"        Low: {totals.get('CONFIDENCE.LOW')}")
    logger.debug(f"        Medium: {totals.get('CONFIDENCE.MEDIUM')}")
    logger.debug(f"        High: {totals.get('CONFIDENCE.HIGH')}")


def get_reports_directory(project):
    return project.expand_path(f'$dir_reports')


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

data = read_data('bandit.json')

log_summary(data)
logger.debug(get_summary(data))
