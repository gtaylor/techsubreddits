import datetime

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.appengine.api.app_identity import get_application_id

from techsubs import app


def get_metrics_client():
    """
    :return: A properly discovered and built Google Metrics client.
    """
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('monitoring', 'v3', credentials=credentials)


def format_rfc3339(datetime_instance=None):
    """
    Formats a datetime per RFC 3339.

    :param datetime_instance: Datetime instance to format, defaults to utcnow
    """
    return datetime_instance.isoformat("T") + "Z"


def get_now_rfc3339():
    """
    :rtype: str
    :return: The current time (in UTC) in RFC 3339 format.
    """
    return format_rfc3339(datetime.datetime.utcnow())


def parse_rfc3339(dt_str):
    """
    :param str dt_str: A properly formed RFC 3339 datetime string.
    :rtype: datetime.datetime
    :return: The corresponding native Python datetime.datetime instance.
    """
    return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")


class BaseMetric(object):
    """
    Base class for metrics. Sub-class this to create a new type of metric.
    IE: Gauge, Cumulative (Counter), Delta, etc.

    .. tip:: Use this class's children to define or report metrics.
    """
    # Override these in your metric type sub-classes.
    metric_kind = None
    metric_value_type = None

    # Override these in your metric sub-classes.
    metric_name = None
    display_name = None
    description = None

    # Included in all metrics.
    _standard_label_definitions = [
        {
            "key": "environment",
            "valueType": "STRING",
            "description": "One of 'production' or 'devel'"
        },
    ]
    # Override and add any extras.
    extra_labels = []

    @classmethod
    def _value_type_to_typed_value(cls):
        """
        See https://cloud.google.com/monitoring/api/ref_v3/rest/v3/TypedValue
        """
        value_type = cls.metric_value_type
        if value_type == 'INT64':
            return 'int64Value'
        else:
            raise ValueError('Un-implemented value type: %s' % value_type)

    @classmethod
    def _cast_value_according_to_type(cls, value):
        """
        Given an arbitrary value, cast it to the metric's type.

        :param value: The value to cast.
        :return: The casted value.
        """
        value_type = cls.metric_value_type
        if value_type == 'INT64':
            return int(value)
        else:
            raise ValueError('Un-implemented value type: %s' % value_type)

    @classmethod
    def _get_standard_label_values(cls):
        """
        These get automatically reported for any metric we send.
        """
        return {
            "environment": 'prod' if app.config['IS_PRODUCTION'] else 'dev'
        }

    @classmethod
    def _get_metric_vars(cls):
        project_id = get_application_id()
        md_type = "custom.googleapis.com/{}".format(cls.metric_name)
        md_name = "projects/{}/metricDescriptors/{}".format(
            project_id, md_type)
        project_resource = "projects/{0}".format(project_id)
        return md_name, md_type, project_resource

    @classmethod
    def create_metric(cls):
        """
        Sets the metric up in Google Metrics. You must do this before
        sending values in most cases.
        """
        labels = cls._standard_label_definitions + cls.extra_labels
        md_name, md_type, project_resource = cls._get_metric_vars()
        metrics_descriptor = {
            "name": md_name,
            "type": md_type,
            "labels": labels,
            "metricKind": cls.metric_kind,
            "valueType": cls.metric_value_type,
            "unit": "items",
            "displayName": cls.display_name,
            "description": cls.description,
        }

        client = get_metrics_client()
        return client.projects().metricDescriptors().create(
            name=project_resource, body=metrics_descriptor).execute()

    @classmethod
    def _write_value(cls, value, interval, labels=None):
        """
        Used by sub-classes to send metrics to Google Metrics.

        :param value: The value to report for the interval.
        :param tuple interval: A tuple comprised of datetimes for the
            interval start and end time.
        :param dict labels: Optionally, apply labels to the point.
        """
        # We have a standard set of labels that we apply to all metrics.
        all_labels = cls._get_standard_label_values()
        if labels:
            all_labels.update(labels)

        # Specify a new data point for the time series.
        md_name, md_type, project_resource = cls._get_metric_vars()
        timeseries_data = {
            "metric": {
                "type": md_type,
                "labels": all_labels,
            },
            "resource": {
                "type": 'global',
            },
            "metricKind": cls.metric_kind,
            "valueType": cls.metric_value_type,
            "points": [
                {
                    "interval": {
                        "startTime": interval[0],
                        "endTime": interval[1]
                    },
                    "value": {
                        cls._value_type_to_typed_value(): value,
                    }
                }
            ]
        }

        client = get_metrics_client()
        request = client.projects().timeSeries().create(
            name=project_resource, body={"timeSeries": [timeseries_data]})
        request.execute()


class GaugeMetric(BaseMetric):
    """
    Tracks a value over time.
    """
    metric_kind = 'GAUGE'

    @classmethod
    def _validate_labels(cls, labels):
        """
        Make sure the label values that were passed in are valid.

        :param dict labels: A dict of labels to validate.
        :raises: ValueError if something is wrong with the labels that
            were passed in.
        """
        labels = labels or {}
        # The metrics that were passed into write_gauge via `labels`.
        passed_label_keys = set(labels.keys())
        # These are the metrics that our definition said we are providing.
        defined_label_keys = set([l['key'] for l in cls.extra_labels])
        # If all required labels were specified, this should be empty.
        diff = defined_label_keys - passed_label_keys
        if diff:
            raise ValueError("Missing label value(s): %s" % diff)

    @classmethod
    def write_gauge(cls, value, labels=None, time_override=None):
        """
        Send a point value to Google Metrics.

        :param value: The value to send for the gauge.
        :param dict labels: An optional dict of labels to apply to the point.
        :param datetime.datetime time_override: If the point should fall
            outside of the current time, pass it in here. Remember, UTC!
        """
        cls._validate_labels(labels)
        if time_override:
            metric_time = format_rfc3339(time_override)
        else:
            metric_time = get_now_rfc3339()
        interval = (metric_time, metric_time)
        cls._write_value(value, interval, labels=labels)

    @classmethod
    def query_gauge(cls, start_time, end_time, environment='prod',
                    metric_label_filters=None, page_size=100):
        """
        Used for returning point values between a start and end time for
        the gauge.

        :param datetime.datetime start_time: Beginning of the interval to query.
        :param datetime.datetime end_time: End of the interval to query.
        :param str environment: One of 'prod' or 'dev'.
        :param dict metric_label_filters: Optionally, only return metrics
            that match these label key/vals.
        :param int page_size: Max number of points returned per page (this
            is handled transparently).
        :rtype: generator
        :return: A generator of metric point dicts.
        """
        client = get_metrics_client()
        md_name, md_type, project_resource = cls._get_metric_vars()
        filter_str = (
            'metric.type="{}" AND metric.label.environment="{}"'.format(
                md_type, environment))
        if metric_label_filters:
            for label_name, label_val in metric_label_filters.items():
                filter_str += ' AND metric.label.{}="{}"'.format(
                    label_name, label_val)

        next_page_token = None
        # Automatically paginate through the metric results.
        while True:
            request = client.projects().timeSeries().list(
                name=project_resource,
                filter=filter_str,
                pageSize=page_size,
                interval_startTime=format_rfc3339(start_time),
                interval_endTime=format_rfc3339(end_time),
                pageToken=next_page_token)

            response = request.execute()
            next_page_token = response.get('nextPageToken')
            num_timeseries = len(response['timeSeries'])
            assert num_timeseries == 1, "Metrics query returned %s time " \
                                        "series instead of 1. Check your " \
                                        "filters." % num_timeseries
            points = response['timeSeries'][0]['points']
            for point in points:
                value = point['value'][cls._value_type_to_typed_value()]
                # If we don't expand our return values much more, may be
                # better to do a tuple instead.
                yield {
                    'time': parse_rfc3339(point['interval']['startTime']),
                    'value': cls._cast_value_according_to_type(value),
                }

            if not next_page_token:
                break
