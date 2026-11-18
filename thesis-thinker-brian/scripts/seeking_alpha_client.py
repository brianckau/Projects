#!/usr/bin/env python3
"""One bounded GET to the configured Seeking Alpha RapidAPI provider.

Read RAPIDAPI_KEY from the runtime environment. Pass only verified endpoint
paths and parameters. Never log headers or raw server error bodies.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

HOST = 'seeking-alpha-api.p.rapidapi.com'
MAX_BYTES = 2_000_000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def build_url(path, parameters):
    if not re.fullmatch(r'/[A-Za-z0-9_/-]+', path) or path.startswith('//'):
        raise ValueError('Use a verified relative endpoint path without a query or host')
    pairs = []
    for item in parameters:
        if '=' not in item:
            raise ValueError('Query parameters must use name=value')
        name, value = item.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_\[\]-]+', name):
            raise ValueError('Invalid query parameter name')
        if any(term in name.lower() for term in ('key', 'token', 'secret', 'authorization', 'host')):
            raise ValueError('Credentials and host configuration cannot be query parameters')
        pairs.append((name, value))
    query = urllib.parse.urlencode(pairs)
    return 'https://' + HOST + path + ('?' + query if query else '')


def error_result(kind, status=None):
    result = {'ok': False, 'error': kind}
    if status is not None:
        result['http_status'] = status
    return result


def request_once(path, parameters, check=False, opener=None, credential=None):
    url = build_url(path, parameters)
    secret = os.environ.get('RAPIDAPI_KEY', '') if credential is None else credential
    if not secret or not secret.strip():
        return error_result('missing_runtime_key')
    if '\n' in secret or '\r' in secret:
        return error_result('invalid_runtime_key')
    req = urllib.request.Request(url, headers={
        'X-RapidAPI-Key': secret,
        'X-RapidAPI-Host': HOST,
        'Accept': 'application/json',
    }, method='GET')
    transport = opener or urllib.request.build_opener(NoRedirect)
    try:
        with transport.open(req, timeout=20) as response:
            status = response.status
            body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            return error_result('response_too_large', status)
        if not 200 <= status < 300:
            return error_result('unexpected_http_status', status)
        # Treat a reflected credential as an unusable response, never output it.
        if secret.encode() in body:
            return error_result('response_contains_credential', status)
        try:
            data = json.loads(body)
        except (ValueError, UnicodeError):
            return error_result('invalid_json', status)
        if isinstance(data, dict) and (data.get('error') or data.get('success') is False or data.get('ok') is False):
            return error_result('api_error_envelope', status)
        if not isinstance(data, (dict, list)):
            return error_result('unexpected_json_type', status)
        result = {'ok': True, 'http_status': status, 'endpoint_path': path,
                  'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'response_bytes': len(body), 'json_type': type(data).__name__}
        if check:
            result['record_content_verified'] = False
        else:
            result['data'] = data
        return result
    except urllib.error.HTTPError as exc:
        kind = {401: 'authentication_or_access_denied', 402: 'subscription_or_payment_required',
                403: 'authentication_or_access_denied', 404: 'endpoint_or_symbol_not_found',
                429: 'quota_or_rate_limited'}.get(exc.code, 'http_error')
        if 300 <= exc.code < 400:
            kind = 'redirect_refused'
        elif exc.code >= 500:
            kind = 'provider_error'
        # Do not print the remote message; it may echo credentials.
        return error_result(kind, exc.code)
    except (urllib.error.URLError, TimeoutError, OSError):
        return error_result('network_error')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--endpoint-path', required=True, help='Exact GET path verified in provider docs')
    parser.add_argument('--param', action='append', default=[], help='Verified query parameter name=value; repeatable')
    parser.add_argument('--check', action='store_true', help='Print connection metadata only, no response data')
    args = parser.parse_args()
    try:
        result = request_once(args.endpoint_path, args.param, args.check)
    except ValueError:
        result = error_result('invalid_endpoint_or_parameters')
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result['ok'] else 2


if __name__ == '__main__':
    sys.exit(main())
