import json
from requests import Session

from lib.base import SaltAction


class SaltLocal(SaltAction):
    __explicit__ = [
        "cmdmod",
        "event",
        "file",
        "grains",
        "pillar",
        "pkg",
        "saltcloudmod",
        "schedule",
        "service",
        "state",
        "status",
    ]

    def run(self, module, target, tgt_type, args, **kwargs):
        """
        CLI Examples:

            st2 run salt.local module=test.ping matches='web*'
            st2 run salt.local module=test.ping tgt_type=grain target='os:Ubuntu'
        """

        # ChatOps alias and newer St2 versions set default args=[] which
        # breaks test.ping & test.version
        if args == [] and module in ["test.ping", "test.version"]:
            args = None

        self.generate_package(
            "local", cmd=module, target=target, tgt_type=tgt_type, args=args, data=kwargs
        )

        request = self.generate_request()
        request.prepare_body(json.dumps(self.data), None)
        resp = Session().send(request, verify=self.verify_tls)
        try:
            retval = resp.json()
        except Exception as exc:
            retval = (False, f"Failed to decode json! {str(exc)}")
        return retval
