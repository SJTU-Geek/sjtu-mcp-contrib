METADATA = {
    "name": "sjtu_study_rooms",
    "version": "1.0.0",
    "author": "",
    "description": "获取自习室教室",
    "category": "info_portal",
    "require_auth": False,
    "tools": [
        {
            "name": "sjtu_study_rooms",
            "description": "Fetch self-study classroom information.",
            "entrypoint": "tool_sjtu_study_rooms",
            "schema": {
                "title": "sjtu_study_rooms",
                "description": "Fetch self-study classroom information.",
                "type": "object",
                "properties": {},
            },
        }
    ],
}

from typing import Any, Dict, List, Tuple
from json import loads, dumps
import requests
from scripts.base.mcp_context import NETWORK_DEBUG


def getSjtuStudyRooms() -> Tuple[bool, List[Dict[str, Any]]]:
    """获取自习室教室信息"""
    pageUrl = "https://ids.sjtu.edu.cn/classRoom/getByFreeClassroomInfo"
    req = requests.post(
        pageUrl,
        data="roomCode=LGXQ",
        headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8"},
        verify=not NETWORK_DEBUG,
    )
    if req.status_code != requests.codes.ok:
        return False, [{"error": "获取信息失败，请检查网络连接"}]

    result = list(
        map(
            lambda e: {
                "room": e["name"],
                "building": e["buildName"],
                "seats": int(e["kwNum"]),
                "occupied_seats": e["realTimeNum"],
            },
            loads(req.json()["data"]["freeClassRoomList"]),
        )
    )

    return True, result


def tool_sjtu_study_rooms():
    success, result = getSjtuStudyRooms()
    if not success:
        return result
    else:
        return dumps(result)


if __name__ == "__main__":
    print(tool_sjtu_study_rooms())
