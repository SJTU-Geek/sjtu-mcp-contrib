
METADATA = {
    "name": "sjtu_jw",
    "version": "1.0.0",
    "author": "Teruteru",
    "description": "获取教务网的相关信息",
    "category": "academic",
    "require_auth": True,
    "tools": [
        {
            "name": "personal_course_table",
            "description": "Get class schedules for a given semester.",
            "entrypoint": "tool_personal_course_table",
            "schema": {
                "title": "personal_course_table",
                "description": "Get class schedules for a given semester.",
                "type": "object",
                "properties": {
                    "semester": {
                        "description": "The specified semester, defaults to the current semester if left blank.",
                        "type": "string"
                    },
                },
                "required": [
                ]
            }
	    },
        {
            "name": "personal_course_score",
            "description": "Get course scores for a given semester.",
            "entrypoint": "tool_course_score_list",
            "schema": {
                "title": "personal_course_score",
                "description": "Get course scores for a given semester.",
                "type": "object",
                "properties": {
                    "semester": {
                        "description": "The specified semester, defaults to the current semester if left blank.",
                        "type": "string"
                    },
                },
                "required": [
                ]
            }
	    },
    ]
}

import requests
import datetime
import re
from scripts.base.mcp_context import get_http_session, NETWORK_DEBUG
from scripts.base.data_utils import from_str, from_none, from_bool, from_dict, from_int, from_list, from_union, to_class
from dataclasses import dataclass
from typing import List, Any, Optional, TypeVar, Callable, Type, cast

@dataclass
class QueryModel:
    current_page: int
    current_result: int
    entity_or_field: bool
    limit: int
    offset: int
    page_no: int
    page_size: int
    show_count: int
    sorts: List[str]
    total_count: int
    total_page: int
    total_result: int

    @staticmethod
    def from_dict(obj: Any) -> 'QueryModel':
        assert isinstance(obj, dict)
        current_page = from_int(obj.get("currentPage"))
        current_result = from_int(obj.get("currentResult"))
        entity_or_field = from_bool(obj.get("entityOrField"))
        limit = from_int(obj.get("limit"))
        offset = from_int(obj.get("offset"))
        page_no = from_int(obj.get("pageNo"))
        page_size = from_int(obj.get("pageSize"))
        show_count = from_int(obj.get("showCount"))
        sorts = from_list(from_str, obj.get("sorts"))
        total_count = from_int(obj.get("totalCount"))
        total_page = from_int(obj.get("totalPage"))
        total_result = from_int(obj.get("totalResult"))
        return QueryModel(current_page, current_result, entity_or_field, limit, offset, page_no, page_size, show_count, sorts, total_count, total_page, total_result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currentPage"] = from_int(self.current_page)
        result["currentResult"] = from_int(self.current_result)
        result["entityOrField"] = from_bool(self.entity_or_field)
        result["limit"] = from_int(self.limit)
        result["offset"] = from_int(self.offset)
        result["pageNo"] = from_int(self.page_no)
        result["pageSize"] = from_int(self.page_size)
        result["showCount"] = from_int(self.show_count)
        result["sorts"] = from_list(from_str, self.sorts)
        result["totalCount"] = from_int(self.total_count)
        result["totalPage"] = from_int(self.total_page)
        result["totalResult"] = from_int(self.total_result)
        return result


@dataclass
class UserModel:
    monitor: bool
    role_count: int
    role_keys: str
    role_values: str
    status: int
    usable: bool

    @staticmethod
    def from_dict(obj: Any) -> 'UserModel':
        assert isinstance(obj, dict)
        monitor = from_bool(obj.get("monitor"))
        role_count = from_int(obj.get("roleCount"))
        role_keys = from_str(obj.get("roleKeys"))
        role_values = from_str(obj.get("roleValues"))
        status = from_int(obj.get("status"))
        usable = from_bool(obj.get("usable"))
        return UserModel(monitor, role_count, role_keys, role_values, status, usable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["monitor"] = from_bool(self.monitor)
        result["roleCount"] = from_int(self.role_count)
        result["roleKeys"] = from_str(self.role_keys)
        result["roleValues"] = from_str(self.role_values)
        result["status"] = from_int(self.status)
        result["usable"] = from_bool(self.usable)
        return result


@dataclass
class KBList:
    cdmc: str
    jc: str
    jxb_id: str
    jxbmc: str
    jxbzc: str
    kcbj: str
    kch: str
    kch_id: str
    kcmc: str
    kcxszc: str
    kcxz: str
    kczxs: str
    xkbz: str
    xm: str
    xnm: str
    xqdm: str
    xqh_id: str
    xqj: str
    xqjmc: str
    xqm: str
    xqmc: str
    xsdm: str
    zcd: str
    zxs: str
    bklxdjmc: Optional[str] = None
    cd_id: Optional[str] = None
    cdbh: Optional[str] = None
    cdlbmc: Optional[str] = None
    cxbj: Optional[str] = None
    cxbjmc: Optional[str] = None
    date: Optional[str] = None
    date_digit: Optional[str] = None
    date_digit_separator: Optional[str] = None
    day: Optional[str] = None
    jcor: Optional[str] = None
    jcs: Optional[str] = None
    jgh_id: Optional[str] = None
    jgpxzd: Optional[str] = None
    kclb: Optional[str] = None
    khfsmc: Optional[str] = None
    kkzt: Optional[str] = None
    lh: Optional[str] = None
    listnav: Optional[str] = None
    locale_key: Optional[str] = None
    month: Optional[str] = None
    oldjc: Optional[str] = None
    oldzc: Optional[str] = None
    pageable: Optional[bool] = None
    page_total: Optional[int] = None
    pkbj: Optional[str] = None
    px: Optional[str] = None
    qqqh: Optional[str] = None
    query_model: Optional[QueryModel] = None
    rangeable: Optional[bool] = None
    rk: Optional[str] = None
    rsdzjs: Optional[int] = None
    sfjf: Optional[str] = None
    sfkckkb: Optional[bool] = None
    skfsmc: Optional[str] = None
    sxbj: Optional[str] = None
    total_result: Optional[str] = None
    user_model: Optional[UserModel] = None
    xf: Optional[str] = None
    xqh1: Optional[str] = None
    xslxbj: Optional[str] = None
    year: Optional[str] = None
    zcmc: Optional[str] = None
    zfjmc: Optional[str] = None
    zhxs: Optional[str] = None
    zxxx: Optional[str] = None
    zyfxmc: Optional[str] = None
    zyhxkcbj: Optional[str] = None
    zzrl: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'KBList':
        assert isinstance(obj, dict)
        cdmc = from_str(obj.get("cdmc"))
        jc = from_str(obj.get("jc"))
        jxb_id = from_str(obj.get("jxb_id"))
        jxbmc = from_str(obj.get("jxbmc"))
        jxbzc = from_str(obj.get("jxbzc"))
        kcbj = from_str(obj.get("kcbj"))
        kch = from_str(obj.get("kch"))
        kch_id = from_str(obj.get("kch_id"))
        kcmc = from_str(obj.get("kcmc"))
        kcxszc = from_str(obj.get("kcxszc"))
        kcxz = from_str(obj.get("kcxz"))
        kczxs = from_str(obj.get("kczxs"))
        xkbz = from_str(obj.get("xkbz"))
        xm = from_str(obj.get("xm"))
        xnm = from_str(obj.get("xnm"))
        xqdm = from_str(obj.get("xqdm"))
        xqh_id = from_str(obj.get("xqh_id"))
        xqj = from_str(obj.get("xqj"))
        xqjmc = from_str(obj.get("xqjmc"))
        xqm = from_str(obj.get("xqm"))
        xqmc = from_str(obj.get("xqmc"))
        xsdm = from_str(obj.get("xsdm"))
        zcd = from_str(obj.get("zcd"))
        zxs = from_str(obj.get("zxs"))
        bklxdjmc = from_union([from_str, from_none], obj.get("bklxdjmc"))
        cd_id = from_union([from_str, from_none], obj.get("cd_id"))
        cdbh = from_union([from_str, from_none], obj.get("cdbh"))
        cdlbmc = from_union([from_str, from_none], obj.get("cdlbmc"))
        cxbj = from_union([from_str, from_none], obj.get("cxbj"))
        cxbjmc = from_union([from_str, from_none], obj.get("cxbjmc"))
        date = from_union([from_str, from_none], obj.get("date"))
        date_digit = from_union([from_str, from_none], obj.get("dateDigit"))
        date_digit_separator = from_union([from_str, from_none], obj.get("dateDigitSeparator"))
        day = from_union([from_str, from_none], obj.get("day"))
        jcor = from_union([from_str, from_none], obj.get("jcor"))
        jcs = from_union([from_str, from_none], obj.get("jcs"))
        jgh_id = from_union([from_str, from_none], obj.get("jgh_id"))
        jgpxzd = from_union([from_str, from_none], obj.get("jgpxzd"))
        kclb = from_union([from_str, from_none], obj.get("kclb"))
        khfsmc = from_union([from_str, from_none], obj.get("khfsmc"))
        kkzt = from_union([from_str, from_none], obj.get("kkzt"))
        lh = from_union([from_str, from_none], obj.get("lh"))
        listnav = from_union([from_str, from_none], obj.get("listnav"))
        locale_key = from_union([from_str, from_none], obj.get("localeKey"))
        month = from_union([from_str, from_none], obj.get("month"))
        oldjc = from_union([from_str, from_none], obj.get("oldjc"))
        oldzc = from_union([from_str, from_none], obj.get("oldzc"))
        pageable = from_union([from_bool, from_none], obj.get("pageable"))
        page_total = from_union([from_int, from_none], obj.get("pageTotal"))
        pkbj = from_union([from_str, from_none], obj.get("pkbj"))
        px = from_union([from_str, from_none], obj.get("px"))
        qqqh = from_union([from_str, from_none], obj.get("qqqh"))
        query_model = from_union([QueryModel.from_dict, from_none], obj.get("queryModel"))
        rangeable = from_union([from_bool, from_none], obj.get("rangeable"))
        rk = from_union([from_str, from_none], obj.get("rk"))
        rsdzjs = from_union([from_int, from_none], obj.get("rsdzjs"))
        sfjf = from_union([from_str, from_none], obj.get("sfjf"))
        sfkckkb = from_union([from_bool, from_none], obj.get("sfkckkb"))
        skfsmc = from_union([from_str, from_none], obj.get("skfsmc"))
        sxbj = from_union([from_str, from_none], obj.get("sxbj"))
        total_result = from_union([from_str, from_none], obj.get("totalResult"))
        user_model = from_union([UserModel.from_dict, from_none], obj.get("userModel"))
        xf = from_union([from_str, from_none], obj.get("xf"))
        xqh1 = from_union([from_str, from_none], obj.get("xqh1"))
        xslxbj = from_union([from_str, from_none], obj.get("xslxbj"))
        year = from_union([from_str, from_none], obj.get("year"))
        zcmc = from_union([from_str, from_none], obj.get("zcmc"))
        zfjmc = from_union([from_str, from_none], obj.get("zfjmc"))
        zhxs = from_union([from_str, from_none], obj.get("zhxs"))
        zxxx = from_union([from_str, from_none], obj.get("zxxx"))
        zyfxmc = from_union([from_str, from_none], obj.get("zyfxmc"))
        zyhxkcbj = from_union([from_str, from_none], obj.get("zyhxkcbj"))
        zzrl = from_union([from_str, from_none], obj.get("zzrl"))
        return KBList(cdmc, jc, jxb_id, jxbmc, jxbzc, kcbj, kch, kch_id, kcmc, kcxszc, kcxz, kczxs, xkbz, xm, xnm, xqdm, xqh_id, xqj, xqjmc, xqm, xqmc, xsdm, zcd, zxs, bklxdjmc, cd_id, cdbh, cdlbmc, cxbj, cxbjmc, date, date_digit, date_digit_separator, day, jcor, jcs, jgh_id, jgpxzd, kclb, khfsmc, kkzt, lh, listnav, locale_key, month, oldjc, oldzc, pageable, page_total, pkbj, px, qqqh, query_model, rangeable, rk, rsdzjs, sfjf, sfkckkb, skfsmc, sxbj, total_result, user_model, xf, xqh1, xslxbj, year, zcmc, zfjmc, zhxs, zxxx, zyfxmc, zyhxkcbj, zzrl)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cdmc"] = from_str(self.cdmc)
        result["jc"] = from_str(self.jc)
        result["jxb_id"] = from_str(self.jxb_id)
        result["jxbmc"] = from_str(self.jxbmc)
        result["jxbzc"] = from_str(self.jxbzc)
        result["kcbj"] = from_str(self.kcbj)
        result["kch"] = from_str(self.kch)
        result["kch_id"] = from_str(self.kch_id)
        result["kcmc"] = from_str(self.kcmc)
        result["kcxszc"] = from_str(self.kcxszc)
        result["kcxz"] = from_str(self.kcxz)
        result["kczxs"] = from_str(self.kczxs)
        result["xkbz"] = from_str(self.xkbz)
        result["xm"] = from_str(self.xm)
        result["xnm"] = from_str(self.xnm)
        result["xqdm"] = from_str(self.xqdm)
        result["xqh_id"] = from_str(self.xqh_id)
        result["xqj"] = from_str(self.xqj)
        result["xqjmc"] = from_str(self.xqjmc)
        result["xqm"] = from_str(self.xqm)
        result["xqmc"] = from_str(self.xqmc)
        result["xsdm"] = from_str(self.xsdm)
        result["zcd"] = from_str(self.zcd)
        result["zxs"] = from_str(self.zxs)
        if self.bklxdjmc is not None:
            result["bklxdjmc"] = from_union([from_str, from_none], self.bklxdjmc)
        if self.cd_id is not None:
            result["cd_id"] = from_union([from_str, from_none], self.cd_id)
        if self.cdbh is not None:
            result["cdbh"] = from_union([from_str, from_none], self.cdbh)
        if self.cdlbmc is not None:
            result["cdlbmc"] = from_union([from_str, from_none], self.cdlbmc)
        if self.cxbj is not None:
            result["cxbj"] = from_union([from_str, from_none], self.cxbj)
        if self.cxbjmc is not None:
            result["cxbjmc"] = from_union([from_str, from_none], self.cxbjmc)
        if self.date is not None:
            result["date"] = from_union([from_str, from_none], self.date)
        if self.date_digit is not None:
            result["dateDigit"] = from_union([from_str, from_none], self.date_digit)
        if self.date_digit_separator is not None:
            result["dateDigitSeparator"] = from_union([from_str, from_none], self.date_digit_separator)
        if self.day is not None:
            result["day"] = from_union([from_str, from_none], self.day)
        if self.jcor is not None:
            result["jcor"] = from_union([from_str, from_none], self.jcor)
        if self.jcs is not None:
            result["jcs"] = from_union([from_str, from_none], self.jcs)
        if self.jgh_id is not None:
            result["jgh_id"] = from_union([from_str, from_none], self.jgh_id)
        if self.jgpxzd is not None:
            result["jgpxzd"] = from_union([from_str, from_none], self.jgpxzd)
        if self.kclb is not None:
            result["kclb"] = from_union([from_str, from_none], self.kclb)
        if self.khfsmc is not None:
            result["khfsmc"] = from_union([from_str, from_none], self.khfsmc)
        if self.kkzt is not None:
            result["kkzt"] = from_union([from_str, from_none], self.kkzt)
        if self.lh is not None:
            result["lh"] = from_union([from_str, from_none], self.lh)
        if self.listnav is not None:
            result["listnav"] = from_union([from_str, from_none], self.listnav)
        if self.locale_key is not None:
            result["localeKey"] = from_union([from_str, from_none], self.locale_key)
        if self.month is not None:
            result["month"] = from_union([from_str, from_none], self.month)
        if self.oldjc is not None:
            result["oldjc"] = from_union([from_str, from_none], self.oldjc)
        if self.oldzc is not None:
            result["oldzc"] = from_union([from_str, from_none], self.oldzc)
        if self.pageable is not None:
            result["pageable"] = from_union([from_bool, from_none], self.pageable)
        if self.page_total is not None:
            result["pageTotal"] = from_union([from_int, from_none], self.page_total)
        if self.pkbj is not None:
            result["pkbj"] = from_union([from_str, from_none], self.pkbj)
        if self.px is not None:
            result["px"] = from_union([from_str, from_none], self.px)
        if self.qqqh is not None:
            result["qqqh"] = from_union([from_str, from_none], self.qqqh)
        if self.query_model is not None:
            result["queryModel"] = from_union([lambda x: to_class(QueryModel, x), from_none], self.query_model)
        if self.rangeable is not None:
            result["rangeable"] = from_union([from_bool, from_none], self.rangeable)
        if self.rk is not None:
            result["rk"] = from_union([from_str, from_none], self.rk)
        if self.rsdzjs is not None:
            result["rsdzjs"] = from_union([from_int, from_none], self.rsdzjs)
        if self.sfjf is not None:
            result["sfjf"] = from_union([from_str, from_none], self.sfjf)
        if self.sfkckkb is not None:
            result["sfkckkb"] = from_union([from_bool, from_none], self.sfkckkb)
        if self.skfsmc is not None:
            result["skfsmc"] = from_union([from_str, from_none], self.skfsmc)
        if self.sxbj is not None:
            result["sxbj"] = from_union([from_str, from_none], self.sxbj)
        if self.total_result is not None:
            result["totalResult"] = from_union([from_str, from_none], self.total_result)
        if self.user_model is not None:
            result["userModel"] = from_union([lambda x: to_class(UserModel, x), from_none], self.user_model)
        if self.xf is not None:
            result["xf"] = from_union([from_str, from_none], self.xf)
        if self.xqh1 is not None:
            result["xqh1"] = from_union([from_str, from_none], self.xqh1)
        if self.xslxbj is not None:
            result["xslxbj"] = from_union([from_str, from_none], self.xslxbj)
        if self.year is not None:
            result["year"] = from_union([from_str, from_none], self.year)
        if self.zcmc is not None:
            result["zcmc"] = from_union([from_str, from_none], self.zcmc)
        if self.zfjmc is not None:
            result["zfjmc"] = from_union([from_str, from_none], self.zfjmc)
        if self.zhxs is not None:
            result["zhxs"] = from_union([from_str, from_none], self.zhxs)
        if self.zxxx is not None:
            result["zxxx"] = from_union([from_str, from_none], self.zxxx)
        if self.zyfxmc is not None:
            result["zyfxmc"] = from_union([from_str, from_none], self.zyfxmc)
        if self.zyhxkcbj is not None:
            result["zyhxkcbj"] = from_union([from_str, from_none], self.zyhxkcbj)
        if self.zzrl is not None:
            result["zzrl"] = from_union([from_str, from_none], self.zzrl)
        return result


@dataclass
class XqjmcMap:
    the_1: str
    the_2: str
    the_3: str
    the_4: str
    the_5: str
    the_6: str
    the_7: str

    @staticmethod
    def from_dict(obj: Any) -> 'XqjmcMap':
        assert isinstance(obj, dict)
        the_1 = from_str(obj.get("1"))
        the_2 = from_str(obj.get("2"))
        the_3 = from_str(obj.get("3"))
        the_4 = from_str(obj.get("4"))
        the_5 = from_str(obj.get("5"))
        the_6 = from_str(obj.get("6"))
        the_7 = from_str(obj.get("7"))
        return XqjmcMap(the_1, the_2, the_3, the_4, the_5, the_6, the_7)

    def to_dict(self) -> dict:
        result: dict = {}
        result["1"] = from_str(self.the_1)
        result["2"] = from_str(self.the_2)
        result["3"] = from_str(self.the_3)
        result["4"] = from_str(self.the_4)
        result["5"] = from_str(self.the_5)
        result["6"] = from_str(self.the_6)
        result["7"] = from_str(self.the_7)
        return result


@dataclass
class XsbjList:
    xsdm: str
    xsmc: str
    xslxbj: Optional[str] = None
    ywxsmc: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'XsbjList':
        assert isinstance(obj, dict)
        xsdm = from_str(obj.get("xsdm"))
        xsmc = from_str(obj.get("xsmc"))
        xslxbj = from_union([from_str, from_none], obj.get("xslxbj"))
        ywxsmc = from_union([from_str, from_none], obj.get("ywxsmc"))
        return XsbjList(xsdm, xsmc, xslxbj, ywxsmc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["xsdm"] = from_str(self.xsdm)
        result["xsmc"] = from_str(self.xsmc)
        if self.xslxbj is not None:
            result["xslxbj"] = from_union([from_str, from_none], self.xslxbj)
        if self.ywxsmc is not None:
            result["ywxsmc"] = from_union([from_str, from_none], self.ywxsmc)
        return result


@dataclass
class Xsxx:
    bjmc: str
    jfzt: int
    kcms: int
    kxkxxq: str
    njdm_id: str
    xh: str
    xh_id: str
    xkkg: str
    xkkgxq: str
    xm: str
    xnm: str
    xnmc: str
    xqm: str
    xqmmc: str
    ywxm: str
    zyh_id: str
    zymc: str

    @staticmethod
    def from_dict(obj: Any) -> 'Xsxx':
        assert isinstance(obj, dict)
        bjmc = from_str(obj.get("BJMC"))
        jfzt = from_int(obj.get("JFZT"))
        kcms = from_int(obj.get("KCMS"))
        kxkxxq = from_str(obj.get("KXKXXQ"))
        njdm_id = from_str(obj.get("NJDM_ID"))
        xh = from_str(obj.get("XH"))
        xh_id = from_str(obj.get("XH_ID"))
        xkkg = from_str(obj.get("XKKG"))
        xkkgxq = from_str(obj.get("XKKGXQ"))
        xm = from_str(obj.get("XM"))
        xnm = from_str(obj.get("XNM"))
        xnmc = from_str(obj.get("XNMC"))
        xqm = from_str(obj.get("XQM"))
        xqmmc = from_str(obj.get("XQMMC"))
        ywxm = from_str(obj.get("YWXM"))
        zyh_id = from_str(obj.get("ZYH_ID"))
        zymc = from_str(obj.get("ZYMC"))
        return Xsxx(bjmc, jfzt, kcms, kxkxxq, njdm_id, xh, xh_id, xkkg, xkkgxq, xm, xnm, xnmc, xqm, xqmmc, ywxm, zyh_id, zymc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["BJMC"] = from_str(self.bjmc)
        result["JFZT"] = from_int(self.jfzt)
        result["KCMS"] = from_int(self.kcms)
        result["KXKXXQ"] = from_str(self.kxkxxq)
        result["NJDM_ID"] = from_str(self.njdm_id)
        result["XH"] = from_str(self.xh)
        result["XH_ID"] = from_str(self.xh_id)
        result["XKKG"] = from_str(self.xkkg)
        result["XKKGXQ"] = from_str(self.xkkgxq)
        result["XM"] = from_str(self.xm)
        result["XNM"] = from_str(self.xnm)
        result["XNMC"] = from_str(self.xnmc)
        result["XQM"] = from_str(self.xqm)
        result["XQMMC"] = from_str(self.xqmmc)
        result["YWXM"] = from_str(self.ywxm)
        result["ZYH_ID"] = from_str(self.zyh_id)
        result["ZYMC"] = from_str(self.zymc)
        return result


@dataclass
class JwPersonalCourseList:
    """ApifoxModel"""
    kb_list: List[KBList]
    djdz_list: Optional[List[str]] = None
    jfckbkg: Optional[bool] = None
    jxhjkc_list: Optional[List[str]] = None
    kblx: Optional[int] = None
    qsxqj: Optional[str] = None
    rqazc_list: Optional[List[str]] = None
    sfxsd: Optional[str] = None
    sjfwkg: Optional[bool] = None
    sjk_list: Optional[List[str]] = None
    xkkg: Optional[bool] = None
    xnxqsfkz: Optional[str] = None
    xqbzxxsz_list: Optional[List[str]] = None
    xqjmc_map: Optional[XqjmcMap] = None
    xsbj_list: Optional[List[XsbjList]] = None
    xskbsfxstkzt: Optional[str] = None
    xsxx: Optional[Xsxx] = None
    zckbsfxssj: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'JwPersonalCourseList':
        assert isinstance(obj, dict)
        kb_list = from_list(KBList.from_dict, obj.get("kbList"))
        djdz_list = from_union([lambda x: from_list(from_str, x), from_none], obj.get("djdzList"))
        jfckbkg = from_union([from_bool, from_none], obj.get("jfckbkg"))
        jxhjkc_list = from_union([lambda x: from_list(from_str, x), from_none], obj.get("jxhjkcList"))
        kblx = from_union([from_int, from_none], obj.get("kblx"))
        qsxqj = from_union([from_str, from_none], obj.get("qsxqj"))
        rqazc_list = from_union([lambda x: from_list(from_str, x), from_none], obj.get("rqazcList"))
        sfxsd = from_union([from_str, from_none], obj.get("sfxsd"))
        sjfwkg = from_union([from_bool, from_none], obj.get("sjfwkg"))
        sjk_list = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sjkList"))
        xkkg = from_union([from_bool, from_none], obj.get("xkkg"))
        xnxqsfkz = from_union([from_str, from_none], obj.get("xnxqsfkz"))
        xqbzxxsz_list = from_union([lambda x: from_list(from_str, x), from_none], obj.get("xqbzxxszList"))
        xqjmc_map = from_union([XqjmcMap.from_dict, from_none], obj.get("xqjmcMap"))
        xsbj_list = from_union([lambda x: from_list(XsbjList.from_dict, x), from_none], obj.get("xsbjList"))
        xskbsfxstkzt = from_union([from_str, from_none], obj.get("xskbsfxstkzt"))
        xsxx = from_union([Xsxx.from_dict, from_none], obj.get("xsxx"))
        zckbsfxssj = from_union([from_str, from_none], obj.get("zckbsfxssj"))
        return JwPersonalCourseList(kb_list, djdz_list, jfckbkg, jxhjkc_list, kblx, qsxqj, rqazc_list, sfxsd, sjfwkg, sjk_list, xkkg, xnxqsfkz, xqbzxxsz_list, xqjmc_map, xsbj_list, xskbsfxstkzt, xsxx, zckbsfxssj)

    def to_dict(self) -> dict:
        result: dict = {}
        result["kbList"] = from_list(lambda x: to_class(KBList, x), self.kb_list)
        if self.djdz_list is not None:
            result["djdzList"] = from_union([lambda x: from_list(from_str, x), from_none], self.djdz_list)
        if self.jfckbkg is not None:
            result["jfckbkg"] = from_union([from_bool, from_none], self.jfckbkg)
        if self.jxhjkc_list is not None:
            result["jxhjkcList"] = from_union([lambda x: from_list(from_str, x), from_none], self.jxhjkc_list)
        if self.kblx is not None:
            result["kblx"] = from_union([from_int, from_none], self.kblx)
        if self.qsxqj is not None:
            result["qsxqj"] = from_union([from_str, from_none], self.qsxqj)
        if self.rqazc_list is not None:
            result["rqazcList"] = from_union([lambda x: from_list(from_str, x), from_none], self.rqazc_list)
        if self.sfxsd is not None:
            result["sfxsd"] = from_union([from_str, from_none], self.sfxsd)
        if self.sjfwkg is not None:
            result["sjfwkg"] = from_union([from_bool, from_none], self.sjfwkg)
        if self.sjk_list is not None:
            result["sjkList"] = from_union([lambda x: from_list(from_str, x), from_none], self.sjk_list)
        if self.xkkg is not None:
            result["xkkg"] = from_union([from_bool, from_none], self.xkkg)
        if self.xnxqsfkz is not None:
            result["xnxqsfkz"] = from_union([from_str, from_none], self.xnxqsfkz)
        if self.xqbzxxsz_list is not None:
            result["xqbzxxszList"] = from_union([lambda x: from_list(from_str, x), from_none], self.xqbzxxsz_list)
        if self.xqjmc_map is not None:
            result["xqjmcMap"] = from_union([lambda x: to_class(XqjmcMap, x), from_none], self.xqjmc_map)
        if self.xsbj_list is not None:
            result["xsbjList"] = from_union([lambda x: from_list(lambda x: to_class(XsbjList, x), x), from_none], self.xsbj_list)
        if self.xskbsfxstkzt is not None:
            result["xskbsfxstkzt"] = from_union([from_str, from_none], self.xskbsfxstkzt)
        if self.xsxx is not None:
            result["xsxx"] = from_union([lambda x: to_class(Xsxx, x), from_none], self.xsxx)
        if self.zckbsfxssj is not None:
            result["zckbsfxssj"] = from_union([from_str, from_none], self.zckbsfxssj)
        return result
    
@dataclass
class JwCourseScoreItem:
    date: str
    date_digit: str
    date_digit_separator: str
    day: str
    jgpxzd: str
    jxb_id: str
    jxbmc: str
    kch: str
    kch_id: str
    kcmc: str
    kkbm_id: str
    kkbmmc: str
    listnav: str
    locale_key: str
    month: str
    pageable: bool
    page_total: int
    query_model: QueryModel
    rangeable: bool
    row_id: str
    total_result: str
    user_model: UserModel
    xf: str
    xh_id: str
    xmblmc: str
    xmcj: str
    xnm: str
    xnmmc: str
    xqm: str
    xqmmc: str
    year: str

    @staticmethod
    def from_dict(obj: Any) -> 'JwCourseScoreItem':
        assert isinstance(obj, dict)
        date = from_str(obj.get("date"))
        date_digit = from_str(obj.get("dateDigit"))
        date_digit_separator = from_str(obj.get("dateDigitSeparator"))
        day = from_str(obj.get("day"))
        jgpxzd = from_str(obj.get("jgpxzd"))
        jxb_id = from_str(obj.get("jxb_id"))
        jxbmc = from_str(obj.get("jxbmc"))
        kch = from_str(obj.get("kch"))
        kch_id = from_str(obj.get("kch_id"))
        kcmc = from_str(obj.get("kcmc"))
        kkbm_id = from_str(obj.get("kkbm_id"))
        kkbmmc = from_str(obj.get("kkbmmc"))
        listnav = from_str(obj.get("listnav"))
        locale_key = from_str(obj.get("localeKey"))
        month = from_str(obj.get("month"))
        pageable = from_bool(obj.get("pageable"))
        page_total = from_int(obj.get("pageTotal"))
        query_model = QueryModel.from_dict(obj.get("queryModel"))
        rangeable = from_bool(obj.get("rangeable"))
        row_id = from_str(obj.get("row_id"))
        total_result = from_str(obj.get("totalResult"))
        user_model = UserModel.from_dict(obj.get("userModel"))
        xf = from_str(obj.get("xf"))
        xh_id = from_str(obj.get("xh_id"))
        xmblmc = from_str(obj.get("xmblmc"))
        xmcj = from_str(obj.get("xmcj"))
        xnm = from_str(obj.get("xnm"))
        xnmmc = from_str(obj.get("xnmmc"))
        xqm = from_str(obj.get("xqm"))
        xqmmc = from_str(obj.get("xqmmc"))
        year = from_str(obj.get("year"))
        return JwCourseScoreItem(date, date_digit, date_digit_separator, day, jgpxzd, jxb_id, jxbmc, kch, kch_id, kcmc, kkbm_id, kkbmmc, listnav, locale_key, month, pageable, page_total, query_model, rangeable, row_id, total_result, user_model, xf, xh_id, xmblmc, xmcj, xnm, xnmmc, xqm, xqmmc, year)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_str(self.date)
        result["dateDigit"] = from_str(self.date_digit)
        result["dateDigitSeparator"] = from_str(self.date_digit_separator)
        result["day"] = from_str(self.day)
        result["jgpxzd"] = from_str(self.jgpxzd)
        result["jxb_id"] = from_str(self.jxb_id)
        result["jxbmc"] = from_str(self.jxbmc)
        result["kch"] = from_str(self.kch)
        result["kch_id"] = from_str(self.kch_id)
        result["kcmc"] = from_str(self.kcmc)
        result["kkbm_id"] = from_str(self.kkbm_id)
        result["kkbmmc"] = from_str(self.kkbmmc)
        result["listnav"] = from_str(self.listnav)
        result["localeKey"] = from_str(self.locale_key)
        result["month"] = from_str(self.month)
        result["pageable"] = from_bool(self.pageable)
        result["pageTotal"] = from_int(self.page_total)
        result["queryModel"] = to_class(QueryModel, self.query_model)
        result["rangeable"] = from_bool(self.rangeable)
        result["row_id"] = from_str(self.row_id)
        result["totalResult"] = from_str(self.total_result)
        result["userModel"] = to_class(UserModel, self.user_model)
        result["xf"] = from_str(self.xf)
        result["xh_id"] = from_str(self.xh_id)
        result["xmblmc"] = from_str(self.xmblmc)
        result["xmcj"] = from_str(self.xmcj)
        result["xnm"] = from_str(self.xnm)
        result["xnmmc"] = from_str(self.xnmmc)
        result["xqm"] = from_str(self.xqm)
        result["xqmmc"] = from_str(self.xqmmc)
        result["year"] = from_str(self.year)
        return result


@dataclass
class JwCourseScoreList:
    """ApifoxModel"""
    current_page: int
    current_result: int
    entity_or_field: bool
    items: List[JwCourseScoreItem]
    limit: int
    offset: int
    page_no: int
    page_size: int
    show_count: int
    sort_name: str
    sort_order: str
    sorts: List[str]
    total_count: int
    total_page: int
    total_result: int

    @staticmethod
    def from_dict(obj: Any) -> 'JwCourseScoreList':
        assert isinstance(obj, dict)
        current_page = from_int(obj.get("currentPage"))
        current_result = from_int(obj.get("currentResult"))
        entity_or_field = from_bool(obj.get("entityOrField"))
        items = from_list(JwCourseScoreItem.from_dict, obj.get("items"))
        limit = from_int(obj.get("limit"))
        offset = from_int(obj.get("offset"))
        page_no = from_int(obj.get("pageNo"))
        page_size = from_int(obj.get("pageSize"))
        show_count = from_int(obj.get("showCount"))
        sort_name = from_str(obj.get("sortName"))
        sort_order = from_str(obj.get("sortOrder"))
        sorts = from_list(from_str, obj.get("sorts"))
        total_count = from_int(obj.get("totalCount"))
        total_page = from_int(obj.get("totalPage"))
        total_result = from_int(obj.get("totalResult"))
        return JwCourseScoreList(current_page, current_result, entity_or_field, items, limit, offset, page_no, page_size, show_count, sort_name, sort_order, sorts, total_count, total_page, total_result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currentPage"] = from_int(self.current_page)
        result["currentResult"] = from_int(self.current_result)
        result["entityOrField"] = from_bool(self.entity_or_field)
        result["items"] = from_list(lambda x: to_class(JwCourseScoreItem, x), self.items)
        result["limit"] = from_int(self.limit)
        result["offset"] = from_int(self.offset)
        result["pageNo"] = from_int(self.page_no)
        result["pageSize"] = from_int(self.page_size)
        result["showCount"] = from_int(self.show_count)
        result["sortName"] = from_str(self.sort_name)
        result["sortOrder"] = from_str(self.sort_order)
        result["sorts"] = from_list(from_str, self.sorts)
        result["totalCount"] = from_int(self.total_count)
        result["totalPage"] = from_int(self.total_page)
        result["totalResult"] = from_int(self.total_result)
        return result

def getCurrentXnXq():
    now = datetime.datetime.now()
    mm = now.month
    yy = now.year
    xq = xn = 0
    if (mm >= 9 or mm <= 2):
        xq = "3" #第一学期
        xn = str(yy) if mm >= 9 else str(yy - 1)
    elif (mm >= 3 and mm <= 7):
        xq = "12" #第二学期
        xn = str(yy - 1)
    else :
        xq = "16" #第三学期
        xn = str(yy - 1)
    return (xn, xq)

def parseXnXq(semester: str):
    integers = re.findall(r"\d+", semester)
    if (len(integers) == 0):
        raise Exception("学期学年格式错误！请使用类似“2024-2025学年第一学期”的格式")
    xn = int(integers[0])
    if (xn < 2000):
        raise Exception("学期学年格式错误！请使用类似“2024-2025学年第一学期”的格式")
    parse_chinese = False
    xq = 0
    if (len(integers) >= 2):
        t = int(integers[1])
        if (t > 2000):
            if (len(integers) >= 3):
                xq = int(integers[2])
            else:
                parse_chinese = True #数字数量不足
        else:
            xq = t
    else:
        parse_chinese = True
    if (parse_chinese):
        if ('一' in semester):
            xq = 1
        elif ('二' in semester):
            xq = 2
        elif ('三' in semester):
            xq = 3
    if (xq < 1 or xq > 3):
        raise Exception("学期学年格式错误！请使用类似“2024-2025学年第一学期”的格式")
    xq = ([3, 12, 16])[xq - 1]
    return (str(xn), str(xq))

def login(sess: requests.Session):
    resp = sess.get(
        "https://i.sjtu.edu.cn/jaccountlogin",
        verify=not NETWORK_DEBUG
    )
    resp.raise_for_status()
    if (not resp.url.startswith("https://i.sjtu.edu.cn/")):
        raise Exception("认证失败")
    
    return True

def getPersonalCourseTable(sess: requests.Session, semester: str = None):
    if (semester):
        xnxq = parseXnXq(semester)
    else:
        xnxq = getCurrentXnXq()
    resp = sess.post(
        "https://i.sjtu.edu.cn/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151",
        data={
            "xnm": xnxq[0],
            "xqm": xnxq[1],
            "kzlx": "ck",
            "xsdm": "",
        },
        verify=not NETWORK_DEBUG
    )
    return JwPersonalCourseList.from_dict(resp.json())

def getCourseScoreList(sess: requests.Session, semester: str = None):
    if (semester):
        xnxq = parseXnXq(semester)
    else:
        xnxq = getCurrentXnXq()
    resp = sess.post(
        "https://i.sjtu.edu.cn/cjcx/cjcx_cxXsKccjList.html?gnmkdm=N305007",
        data={
            "xnm": xnxq[0],
            "xqm": xnxq[1],
            "_search": "false",
            "queryModel.showCount": "200",
            "queryModel.currentPage": "1",
            "queryModel.sortName": "",
            "queryModel.sortOrder": "asc",
            "time": "3",
        },
        verify=not NETWORK_DEBUG
    )
    return JwCourseScoreList.from_dict(resp.json())

def renderPersonalCourse(c: KBList):
    res = \
    f"- {c.kcmc}（{c.kch}）" + "\n" + \
    f"  周数：{c.zcd}" + "\n" + \
    f"  校区：{c.xqmc}" + "\n" + \
    f"  上课时间：{c.xqjmc} {c.jc}" + "\n" + \
    f"  上课地点：{c.cdmc}" + "\n" + \
    f"  教师：{c.xm}" + "\n" + \
    f"  教学班：{c.jxbmc}" + "\n" + \
    f"  选课备注：{c.xkbz if c.xkbz.strip() else '无'}" + "\n" + \
    f"  学分：{c.xf}" + "\n" + \
    f"  课程标记：{c.kcbj}" + "\n" + \
    f"  是否专业核心课程：{c.zyhxkcbj}" + "\n" + \
    ""
    return res

def renderPersonalCourseTable(list: JwPersonalCourseList):
    return '\n'.join([renderPersonalCourse(c) for c in list.kb_list])

def renderSingleCourseScore(c: List[JwCourseScoreItem]):
    res = \
    f"- {c[0].kcmc}（课程号：{c[0].kch}；学分：{c[0].xf}）" + "\n" + \
    '\n'.join([
        f"  - {r.xmblmc}：{r.xmcj}" for r in c
    ])
    return res

def renderCourseScoreList(list: JwCourseScoreList):
    from types_linq import Enumerable
    groups = Enumerable(list.items).group_by(lambda x: x.kch, lambda y: y)
    return '\n'.join(groups.select(lambda c: renderSingleCourseScore(c.to_list())))

def tool_personal_course_table(semester: str = None):
    sess = get_http_session()
    login(sess)
    courses = getPersonalCourseTable(sess, semester)
    if (len(courses.kb_list) == 0):
        return True, "指定的学期没有课程！"
    res = renderPersonalCourseTable(courses)
    return res

def tool_course_score_list(semester: str = None):
    sess = get_http_session()
    login(sess)
    scores = getCourseScoreList(sess, semester)
    if (scores.total_count == 0):
        return True, "找不到数据，可能是成绩还没有出哦~"
    res = renderCourseScoreList(scores)
    return res