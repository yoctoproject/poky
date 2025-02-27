"""
BitBake 'Fetch' GitHub release artifacts implementation

"""

# Copyright (C) 2025 Leonard Göhrs
#
# Based on bb.fetch2.wget:
# Copyright (C) 2003, 2004  Chris Larson
#
# SPDX-License-Identifier: GPL-2.0-only
#
# Based on functions from the base bb module, Copyright 2003 Holger Schurig

import json

from urllib.request import urlopen, Request

from bb.fetch2 import FetchError
from bb.fetch2.wget import Wget


class GitHubReleaseArtifact(Wget):
    API_HEADERS = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    DOWNLOAD_HEADERS = {
        "Accept": "application/octet-stream"
    }

    def supports(self, ud, d):
        return ud.type in ["ghra"]

    def _resolve_artifact_url(self, ud, d):
        """Resolve `ghra://` pseudo URLs to `https://` URLs and set auth header.

        This method resolved URLs like `ghra://github.com/rauc/rauc/v1.13/rauc-1.13.tar.xz`
        to a backing URL like `https://api.github.com/repos/rauc/rauc/releases/assets/222455085`
        while optionally setting the required authentication headers to download from
        private repositories.
        """

        try:
            user, repo, tag, asset_name = ud.path.strip("/").split("/")
        except ValueError as e:
            raise FetchError(
                f"Expected path like '/<user>/<repo>/<tag>/<asset_name>', got: '{ud.path}'"
            ) from e

        # The GitHub authentication token may be provided as URL parameter
        # (to enable using different tokens for different URLs in the same recipe)
        # or via a variable for cleaner URLs.
        token = ud.parm.get("token") or d.getVar("GH_TOKEN")

        meta_url = f"https://api.{ud.host}/repos/{user}/{repo}/releases/tags/{tag}"

        auth_headers = {}

        if token is not None:
            auth_headers["Authorization"] = f"Bearer {token}"

        try:
            req = Request(url=meta_url, headers=(auth_headers | self.API_HEADERS))
            with urlopen(req) as resp:
                result = json.load(resp)

        except Exception as e:
            raise FetchError(f"Error downloading artifact list: {e}") from e

        asset_urls = dict((asset["name"], asset["url"]) for asset in result["assets"])

        if asset_name not in asset_urls:
            asset_list = ", ".join(asset_urls.keys())
            raise FetchError(
                f"Did not find asset '{asset_name}' in release asset list: {asset_list}"
            )

        # Override the `url` and `headers` in the FetchData object,
        # enabling the Wget class to perform the actual downloading.
        ud.url = asset_urls[asset_name]
        ud.headers = auth_headers | self.DOWNLOAD_HEADERS

    def checkstatus(self, fetch, ud, d):
        self._resolve_artifact_url(ud, d)

        return super().checkstatus(fetch, ud, d)

    def download(self, ud, d):
        self._resolve_artifact_url(ud, d)

        return super().download(ud, d)
