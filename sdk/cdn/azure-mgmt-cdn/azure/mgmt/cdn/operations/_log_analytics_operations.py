# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import datetime
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models as _models
from .._serialization import Serializer
from .._vendor import MixinABC, _convert_request, _format_url_section

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


def build_get_log_analytics_metrics_request(
    resource_group_name: str,
    profile_name: str,
    subscription_id: str,
    *,
    metrics: List[Union[str, _models.LogMetric]],
    date_time_begin: datetime.datetime,
    date_time_end: datetime.datetime,
    granularity: Union[str, _models.LogMetricsGranularity],
    custom_domains: List[str],
    protocols: List[str],
    group_by: Optional[List[Union[str, _models.LogMetricsGroupBy]]] = None,
    continents: Optional[List[str]] = None,
    country_or_regions: Optional[List[str]] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version = kwargs.pop("api_version", _params.pop("api-version", "2021-06-01"))  # type: str
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsMetrics",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._\(\)]+$"
        ),
        "profileName": _SERIALIZER.url("profile_name", profile_name, "str"),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")
    _params["metrics"] = [_SERIALIZER.query("metrics", q, "str") if q is not None else "" for q in metrics]
    _params["dateTimeBegin"] = _SERIALIZER.query("date_time_begin", date_time_begin, "iso-8601")
    _params["dateTimeEnd"] = _SERIALIZER.query("date_time_end", date_time_end, "iso-8601")
    _params["granularity"] = _SERIALIZER.query("granularity", granularity, "str")
    if group_by is not None:
        _params["groupBy"] = [_SERIALIZER.query("group_by", q, "str") if q is not None else "" for q in group_by]
    if continents is not None:
        _params["continents"] = [_SERIALIZER.query("continents", q, "str") if q is not None else "" for q in continents]
    if country_or_regions is not None:
        _params["countryOrRegions"] = [
            _SERIALIZER.query("country_or_regions", q, "str") if q is not None else "" for q in country_or_regions
        ]
    _params["customDomains"] = [
        _SERIALIZER.query("custom_domains", q, "str") if q is not None else "" for q in custom_domains
    ]
    _params["protocols"] = [_SERIALIZER.query("protocols", q, "str") if q is not None else "" for q in protocols]

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_log_analytics_rankings_request(
    resource_group_name: str,
    profile_name: str,
    subscription_id: str,
    *,
    rankings: List[Union[str, _models.LogRanking]],
    metrics: List[Union[str, _models.LogRankingMetric]],
    max_ranking: int,
    date_time_begin: datetime.datetime,
    date_time_end: datetime.datetime,
    custom_domains: Optional[List[str]] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version = kwargs.pop("api_version", _params.pop("api-version", "2021-06-01"))  # type: str
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsRankings",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._\(\)]+$"
        ),
        "profileName": _SERIALIZER.url("profile_name", profile_name, "str"),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")
    _params["rankings"] = [_SERIALIZER.query("rankings", q, "str") if q is not None else "" for q in rankings]
    _params["metrics"] = [_SERIALIZER.query("metrics", q, "str") if q is not None else "" for q in metrics]
    _params["maxRanking"] = _SERIALIZER.query("max_ranking", max_ranking, "int")
    _params["dateTimeBegin"] = _SERIALIZER.query("date_time_begin", date_time_begin, "iso-8601")
    _params["dateTimeEnd"] = _SERIALIZER.query("date_time_end", date_time_end, "iso-8601")
    if custom_domains is not None:
        _params["customDomains"] = [
            _SERIALIZER.query("custom_domains", q, "str") if q is not None else "" for q in custom_domains
        ]

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_log_analytics_locations_request(
    resource_group_name: str, profile_name: str, subscription_id: str, **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version = kwargs.pop("api_version", _params.pop("api-version", "2021-06-01"))  # type: str
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsLocations",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._\(\)]+$"
        ),
        "profileName": _SERIALIZER.url("profile_name", profile_name, "str"),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_log_analytics_resources_request(
    resource_group_name: str, profile_name: str, subscription_id: str, **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version = kwargs.pop("api_version", _params.pop("api-version", "2021-06-01"))  # type: str
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsResources",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._\(\)]+$"
        ),
        "profileName": _SERIALIZER.url("profile_name", profile_name, "str"),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_waf_log_analytics_metrics_request(
    resource_group_name: str,
    profile_name: str,
    subscription_id: str,
    *,
    metrics: List[Union[str, _models.WafMetric]],
    date_time_begin: datetime.datetime,
    date_time_end: datetime.datetime,
    granularity: Union[str, _models.WafGranularity],
    actions: Optional[List[Union[str, _models.WafAction]]] = None,
    group_by: Optional[List[Union[str, _models.WafRankingGroupBy]]] = None,
    rule_types: Optional[List[Union[str, _models.WafRuleType]]] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version = kwargs.pop("api_version", _params.pop("api-version", "2021-06-01"))  # type: str
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getWafLogAnalyticsMetrics",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._\(\)]+$"
        ),
        "profileName": _SERIALIZER.url("profile_name", profile_name, "str"),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")
    _params["metrics"] = [_SERIALIZER.query("metrics", q, "str") if q is not None else "" for q in metrics]
    _params["dateTimeBegin"] = _SERIALIZER.query("date_time_begin", date_time_begin, "iso-8601")
    _params["dateTimeEnd"] = _SERIALIZER.query("date_time_end", date_time_end, "iso-8601")
    _params["granularity"] = _SERIALIZER.query("granularity", granularity, "str")
    if actions is not None:
        _params["actions"] = [_SERIALIZER.query("actions", q, "str") if q is not None else "" for q in actions]
    if group_by is not None:
        _params["groupBy"] = [_SERIALIZER.query("group_by", q, "str") if q is not None else "" for q in group_by]
    if rule_types is not None:
        _params["ruleTypes"] = [_SERIALIZER.query("rule_types", q, "str") if q is not None else "" for q in rule_types]

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_waf_log_analytics_rankings_request(
    resource_group_name: str,
    profile_name: str,
    subscription_id: str,
    *,
    metrics: List[Union[str, _models.WafMetric]],
    date_time_begin: datetime.datetime,
    date_time_end: datetime.datetime,
    max_ranking: int,
    rankings: List[Union[str, _models.WafRankingType]],
    actions: Optional[List[Union[str, _models.WafAction]]] = None,
    rule_types: Optional[List[Union[str, _models.WafRuleType]]] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version = kwargs.pop("api_version", _params.pop("api-version", "2021-06-01"))  # type: str
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getWafLogAnalyticsRankings",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._\(\)]+$"
        ),
        "profileName": _SERIALIZER.url("profile_name", profile_name, "str"),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")
    _params["metrics"] = [_SERIALIZER.query("metrics", q, "str") if q is not None else "" for q in metrics]
    _params["dateTimeBegin"] = _SERIALIZER.query("date_time_begin", date_time_begin, "iso-8601")
    _params["dateTimeEnd"] = _SERIALIZER.query("date_time_end", date_time_end, "iso-8601")
    _params["maxRanking"] = _SERIALIZER.query("max_ranking", max_ranking, "int")
    _params["rankings"] = [_SERIALIZER.query("rankings", q, "str") if q is not None else "" for q in rankings]
    if actions is not None:
        _params["actions"] = [_SERIALIZER.query("actions", q, "str") if q is not None else "" for q in actions]
    if rule_types is not None:
        _params["ruleTypes"] = [_SERIALIZER.query("rule_types", q, "str") if q is not None else "" for q in rule_types]

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


class LogAnalyticsOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.cdn.CdnManagementClient`'s
        :attr:`log_analytics` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs):
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def get_log_analytics_metrics(
        self,
        resource_group_name: str,
        profile_name: str,
        metrics: List[Union[str, _models.LogMetric]],
        date_time_begin: datetime.datetime,
        date_time_end: datetime.datetime,
        granularity: Union[str, _models.LogMetricsGranularity],
        custom_domains: List[str],
        protocols: List[str],
        group_by: Optional[List[Union[str, _models.LogMetricsGroupBy]]] = None,
        continents: Optional[List[str]] = None,
        country_or_regions: Optional[List[str]] = None,
        **kwargs: Any
    ) -> _models.MetricsResponse:
        """Get log report for AFD profile.

        :param resource_group_name: Name of the Resource group within the Azure subscription. Required.
        :type resource_group_name: str
        :param profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile
         which is unique within the resource group. which is unique within the resource group. Required.
        :type profile_name: str
        :param metrics: Required.
        :type metrics: list[str or ~azure.mgmt.cdn.models.LogMetric]
        :param date_time_begin: Required.
        :type date_time_begin: ~datetime.datetime
        :param date_time_end: Required.
        :type date_time_end: ~datetime.datetime
        :param granularity: Known values are: "PT5M", "PT1H", and "P1D". Required.
        :type granularity: str or ~azure.mgmt.cdn.models.LogMetricsGranularity
        :param custom_domains: Required.
        :type custom_domains: list[str]
        :param protocols: Required.
        :type protocols: list[str]
        :param group_by: Default value is None.
        :type group_by: list[str or ~azure.mgmt.cdn.models.LogMetricsGroupBy]
        :param continents: Default value is None.
        :type continents: list[str]
        :param country_or_regions: Default value is None.
        :type country_or_regions: list[str]
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MetricsResponse or the result of cls(response)
        :rtype: ~azure.mgmt.cdn.models.MetricsResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.MetricsResponse]

        request = build_get_log_analytics_metrics_request(
            resource_group_name=resource_group_name,
            profile_name=profile_name,
            subscription_id=self._config.subscription_id,
            metrics=metrics,
            date_time_begin=date_time_begin,
            date_time_end=date_time_end,
            granularity=granularity,
            custom_domains=custom_domains,
            protocols=protocols,
            group_by=group_by,
            continents=continents,
            country_or_regions=country_or_regions,
            api_version=api_version,
            template_url=self.get_log_analytics_metrics.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.AfdErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("MetricsResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_log_analytics_metrics.metadata = {"url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsMetrics"}  # type: ignore

    @distributed_trace
    def get_log_analytics_rankings(
        self,
        resource_group_name: str,
        profile_name: str,
        rankings: List[Union[str, _models.LogRanking]],
        metrics: List[Union[str, _models.LogRankingMetric]],
        max_ranking: int,
        date_time_begin: datetime.datetime,
        date_time_end: datetime.datetime,
        custom_domains: Optional[List[str]] = None,
        **kwargs: Any
    ) -> _models.RankingsResponse:
        """Get log analytics ranking report for AFD profile.

        :param resource_group_name: Name of the Resource group within the Azure subscription. Required.
        :type resource_group_name: str
        :param profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile
         which is unique within the resource group. which is unique within the resource group. Required.
        :type profile_name: str
        :param rankings: Required.
        :type rankings: list[str or ~azure.mgmt.cdn.models.LogRanking]
        :param metrics: Required.
        :type metrics: list[str or ~azure.mgmt.cdn.models.LogRankingMetric]
        :param max_ranking: Required.
        :type max_ranking: int
        :param date_time_begin: Required.
        :type date_time_begin: ~datetime.datetime
        :param date_time_end: Required.
        :type date_time_end: ~datetime.datetime
        :param custom_domains: Default value is None.
        :type custom_domains: list[str]
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: RankingsResponse or the result of cls(response)
        :rtype: ~azure.mgmt.cdn.models.RankingsResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.RankingsResponse]

        request = build_get_log_analytics_rankings_request(
            resource_group_name=resource_group_name,
            profile_name=profile_name,
            subscription_id=self._config.subscription_id,
            rankings=rankings,
            metrics=metrics,
            max_ranking=max_ranking,
            date_time_begin=date_time_begin,
            date_time_end=date_time_end,
            custom_domains=custom_domains,
            api_version=api_version,
            template_url=self.get_log_analytics_rankings.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.AfdErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("RankingsResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_log_analytics_rankings.metadata = {"url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsRankings"}  # type: ignore

    @distributed_trace
    def get_log_analytics_locations(
        self, resource_group_name: str, profile_name: str, **kwargs: Any
    ) -> _models.ContinentsResponse:
        """Get all available location names for AFD log analytics report.

        :param resource_group_name: Name of the Resource group within the Azure subscription. Required.
        :type resource_group_name: str
        :param profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile
         which is unique within the resource group. which is unique within the resource group. Required.
        :type profile_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ContinentsResponse or the result of cls(response)
        :rtype: ~azure.mgmt.cdn.models.ContinentsResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.ContinentsResponse]

        request = build_get_log_analytics_locations_request(
            resource_group_name=resource_group_name,
            profile_name=profile_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get_log_analytics_locations.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.AfdErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ContinentsResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_log_analytics_locations.metadata = {"url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsLocations"}  # type: ignore

    @distributed_trace
    def get_log_analytics_resources(
        self, resource_group_name: str, profile_name: str, **kwargs: Any
    ) -> _models.ResourcesResponse:
        """Get all endpoints and custom domains available for AFD log report.

        :param resource_group_name: Name of the Resource group within the Azure subscription. Required.
        :type resource_group_name: str
        :param profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile
         which is unique within the resource group. which is unique within the resource group. Required.
        :type profile_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ResourcesResponse or the result of cls(response)
        :rtype: ~azure.mgmt.cdn.models.ResourcesResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.ResourcesResponse]

        request = build_get_log_analytics_resources_request(
            resource_group_name=resource_group_name,
            profile_name=profile_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get_log_analytics_resources.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.AfdErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ResourcesResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_log_analytics_resources.metadata = {"url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getLogAnalyticsResources"}  # type: ignore

    @distributed_trace
    def get_waf_log_analytics_metrics(
        self,
        resource_group_name: str,
        profile_name: str,
        metrics: List[Union[str, _models.WafMetric]],
        date_time_begin: datetime.datetime,
        date_time_end: datetime.datetime,
        granularity: Union[str, _models.WafGranularity],
        actions: Optional[List[Union[str, _models.WafAction]]] = None,
        group_by: Optional[List[Union[str, _models.WafRankingGroupBy]]] = None,
        rule_types: Optional[List[Union[str, _models.WafRuleType]]] = None,
        **kwargs: Any
    ) -> _models.WafMetricsResponse:
        """Get Waf related log analytics report for AFD profile.

        :param resource_group_name: Name of the Resource group within the Azure subscription. Required.
        :type resource_group_name: str
        :param profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile
         which is unique within the resource group. which is unique within the resource group. Required.
        :type profile_name: str
        :param metrics: Required.
        :type metrics: list[str or ~azure.mgmt.cdn.models.WafMetric]
        :param date_time_begin: Required.
        :type date_time_begin: ~datetime.datetime
        :param date_time_end: Required.
        :type date_time_end: ~datetime.datetime
        :param granularity: Known values are: "PT5M", "PT1H", and "P1D". Required.
        :type granularity: str or ~azure.mgmt.cdn.models.WafGranularity
        :param actions: Default value is None.
        :type actions: list[str or ~azure.mgmt.cdn.models.WafAction]
        :param group_by: Default value is None.
        :type group_by: list[str or ~azure.mgmt.cdn.models.WafRankingGroupBy]
        :param rule_types: Default value is None.
        :type rule_types: list[str or ~azure.mgmt.cdn.models.WafRuleType]
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: WafMetricsResponse or the result of cls(response)
        :rtype: ~azure.mgmt.cdn.models.WafMetricsResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.WafMetricsResponse]

        request = build_get_waf_log_analytics_metrics_request(
            resource_group_name=resource_group_name,
            profile_name=profile_name,
            subscription_id=self._config.subscription_id,
            metrics=metrics,
            date_time_begin=date_time_begin,
            date_time_end=date_time_end,
            granularity=granularity,
            actions=actions,
            group_by=group_by,
            rule_types=rule_types,
            api_version=api_version,
            template_url=self.get_waf_log_analytics_metrics.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.AfdErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("WafMetricsResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_waf_log_analytics_metrics.metadata = {"url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getWafLogAnalyticsMetrics"}  # type: ignore

    @distributed_trace
    def get_waf_log_analytics_rankings(
        self,
        resource_group_name: str,
        profile_name: str,
        metrics: List[Union[str, _models.WafMetric]],
        date_time_begin: datetime.datetime,
        date_time_end: datetime.datetime,
        max_ranking: int,
        rankings: List[Union[str, _models.WafRankingType]],
        actions: Optional[List[Union[str, _models.WafAction]]] = None,
        rule_types: Optional[List[Union[str, _models.WafRuleType]]] = None,
        **kwargs: Any
    ) -> _models.WafRankingsResponse:
        """Get WAF log analytics charts for AFD profile.

        :param resource_group_name: Name of the Resource group within the Azure subscription. Required.
        :type resource_group_name: str
        :param profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile
         which is unique within the resource group. which is unique within the resource group. Required.
        :type profile_name: str
        :param metrics: Required.
        :type metrics: list[str or ~azure.mgmt.cdn.models.WafMetric]
        :param date_time_begin: Required.
        :type date_time_begin: ~datetime.datetime
        :param date_time_end: Required.
        :type date_time_end: ~datetime.datetime
        :param max_ranking: Required.
        :type max_ranking: int
        :param rankings: Required.
        :type rankings: list[str or ~azure.mgmt.cdn.models.WafRankingType]
        :param actions: Default value is None.
        :type actions: list[str or ~azure.mgmt.cdn.models.WafAction]
        :param rule_types: Default value is None.
        :type rule_types: list[str or ~azure.mgmt.cdn.models.WafRuleType]
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: WafRankingsResponse or the result of cls(response)
        :rtype: ~azure.mgmt.cdn.models.WafRankingsResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.WafRankingsResponse]

        request = build_get_waf_log_analytics_rankings_request(
            resource_group_name=resource_group_name,
            profile_name=profile_name,
            subscription_id=self._config.subscription_id,
            metrics=metrics,
            date_time_begin=date_time_begin,
            date_time_end=date_time_end,
            max_ranking=max_ranking,
            rankings=rankings,
            actions=actions,
            rule_types=rule_types,
            api_version=api_version,
            template_url=self.get_waf_log_analytics_rankings.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.AfdErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("WafRankingsResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_waf_log_analytics_rankings.metadata = {"url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{profileName}/getWafLogAnalyticsRankings"}  # type: ignore
