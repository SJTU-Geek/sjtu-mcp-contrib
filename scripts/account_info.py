
METADATA = {
    "name": "account_info",
    "version": "1.0.0",
    "author": "Teruteru",
    "description": "获取当前用户的个人信息",
    "category": "basic",
    "require_auth": True,
    "tools": [
        {
            "name": "account_info",
            "description": "Obtain the current user's personal information.",
            "entryPoint": "tool_account_info",
            "schema": {
                "title": "account_info",
                "description": "Obtain the current user's personal information.",
                "type": "object",
                "properties": {
                }
            }
	    }
    ]
}

from dataclasses import dataclass
from typing import Any, List, Optional, Dict
from scripts.base.data_utils import from_str, from_none, from_bool, from_dict, from_int, from_list, from_union, to_class
from scripts.base.mcp_context import get_http_session

@dataclass
class Birthday:
    birth_day: str
    birth_month: str
    birth_year: str

    @staticmethod
    def from_dict(obj: Any) -> 'Birthday':
        assert isinstance(obj, dict)
        birth_day = from_str(obj.get("birthDay"))
        birth_month = from_str(obj.get("birthMonth"))
        birth_year = from_str(obj.get("birthYear"))
        return Birthday(birth_day, birth_month, birth_year)

    def to_dict(self) -> dict:
        result: dict = {}
        result["birthDay"] = from_str(self.birth_day)
        result["birthMonth"] = from_str(self.birth_month)
        result["birthYear"] = from_str(self.birth_year)
        return result


@dataclass
class Major:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Major':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return Major(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class MgtOrganize:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'MgtOrganize':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return MgtOrganize(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class IdentityOrganize:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'IdentityOrganize':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return IdentityOrganize(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class TopMgtOrganize:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'TopMgtOrganize':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return TopMgtOrganize(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class PurpleTopOrganize:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleTopOrganize':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return PurpleTopOrganize(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class TopOrganizeElement:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'TopOrganizeElement':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return TopOrganizeElement(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class Identity:
    create_date: int
    default_optional: bool
    expire_date: str
    is_default: bool
    kind: str
    status: str
    update_date: int
    user_type: str
    user_type_name: str
    admission_date: Optional[str] = None
    class_no: Optional[str] = None
    code: Optional[str] = None
    gjm: Optional[str] = None
    graduate_date: Optional[str] = None
    major: Optional[Major] = None
    mgt_organize: Optional[MgtOrganize] = None
    organize: Optional[IdentityOrganize] = None
    photo_url: Optional[str] = None
    top_mgt_organize: Optional[TopMgtOrganize] = None
    top_organize: Optional[PurpleTopOrganize] = None
    top_organizes: Optional[List[TopOrganizeElement]] = None
    train_level: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Identity':
        assert isinstance(obj, dict)
        create_date = from_int(obj.get("createDate"))
        default_optional = from_bool(obj.get("defaultOptional"))
        expire_date = from_str(obj.get("expireDate"))
        is_default = from_bool(obj.get("isDefault"))
        kind = from_str(obj.get("kind"))
        status = from_str(obj.get("status"))
        update_date = from_int(obj.get("updateDate"))
        user_type = from_str(obj.get("userType"))
        user_type_name = from_str(obj.get("userTypeName"))
        admission_date = from_union([from_str, from_none], obj.get("admissionDate"))
        class_no = from_union([from_str, from_none], obj.get("classNo"))
        code = from_union([from_str, from_none], obj.get("code"))
        gjm = from_union([from_str, from_none], obj.get("gjm"))
        graduate_date = from_union([from_str, from_none], obj.get("graduateDate"))
        major = from_union([Major.from_dict, from_none], obj.get("major"))
        mgt_organize = from_union([MgtOrganize.from_dict, from_none], obj.get("mgtOrganize"))
        organize = from_union([IdentityOrganize.from_dict, from_none], obj.get("organize"))
        photo_url = from_union([from_str, from_none], obj.get("photoUrl"))
        top_mgt_organize = from_union([TopMgtOrganize.from_dict, from_none], obj.get("topMgtOrganize"))
        top_organize = from_union([PurpleTopOrganize.from_dict, from_none], obj.get("topOrganize"))
        top_organizes = from_union([lambda x: from_list(TopOrganizeElement.from_dict, x), from_none], obj.get("topOrganizes"))
        train_level = from_union([from_str, from_none], obj.get("trainLevel"))
        return Identity(create_date, default_optional, expire_date, is_default, kind, status, update_date, user_type, user_type_name, admission_date, class_no, code, gjm, graduate_date, major, mgt_organize, organize, photo_url, top_mgt_organize, top_organize, top_organizes, train_level)

    def to_dict(self) -> dict:
        result: dict = {}
        result["createDate"] = from_int(self.create_date)
        result["defaultOptional"] = from_bool(self.default_optional)
        result["expireDate"] = from_str(self.expire_date)
        result["isDefault"] = from_bool(self.is_default)
        result["kind"] = from_str(self.kind)
        result["status"] = from_str(self.status)
        result["updateDate"] = from_int(self.update_date)
        result["userType"] = from_str(self.user_type)
        result["userTypeName"] = from_str(self.user_type_name)
        result["admissionDate"] = from_union([from_str, from_none], self.admission_date)
        result["classNo"] = from_union([from_str, from_none], self.class_no)
        result["code"] = from_union([from_str, from_none], self.code)
        result["gjm"] = from_union([from_str, from_none], self.gjm)
        result["graduateDate"] = from_union([from_str, from_none], self.graduate_date)
        result["major"] = from_union([lambda x: to_class(Major, x), from_none], self.major)
        result["mgtOrganize"] = from_union([lambda x: to_class(MgtOrganize, x), from_none], self.mgt_organize)
        result["organize"] = from_union([lambda x: to_class(IdentityOrganize, x), from_none], self.organize)
        result["photoUrl"] = from_union([from_str, from_none], self.photo_url)
        result["topMgtOrganize"] = from_union([lambda x: to_class(TopMgtOrganize, x), from_none], self.top_mgt_organize)
        result["topOrganize"] = from_union([lambda x: to_class(PurpleTopOrganize, x), from_none], self.top_organize)
        result["topOrganizes"] = from_union([lambda x: from_list(lambda x: to_class(TopOrganizeElement, x), x), from_none], self.top_organizes)
        result["trainLevel"] = from_union([from_str, from_none], self.train_level)
        return result


@dataclass
class EntityOrganize:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'EntityOrganize':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return EntityOrganize(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class EntityTopOrganize:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'EntityTopOrganize':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return EntityTopOrganize(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class Entity:
    account: str
    account_photo_url: str
    avatars: Dict[str, Any]
    birthday: Birthday
    card_no: str
    card_type: str
    class_no: str
    code: str
    email: str
    mobile: str
    gender: str
    id: str
    identities: List[Identity]
    kind: str
    name: str
    organize: EntityOrganize
    time_zone: int
    top_organize: EntityTopOrganize
    union_id: str
    user_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Entity':
        assert isinstance(obj, dict)
        account = from_str(obj.get("account"))
        account_photo_url = from_str(obj.get("accountPhotoUrl"))
        avatars = from_dict(lambda x: x, obj.get("avatars"))
        birthday = Birthday.from_dict(obj.get("birthday"))
        card_no = from_str(obj.get("cardNo"))
        card_type = from_str(obj.get("cardType"))
        class_no = from_str(obj.get("classNo"))
        code = from_str(obj.get("code"))
        email = from_str(obj.get("email"))
        mobile = from_str(obj.get("mobile"))
        gender = from_str(obj.get("gender"))
        id = from_str(obj.get("id"))
        identities = from_list(Identity.from_dict, obj.get("identities"))
        kind = from_str(obj.get("kind"))
        name = from_str(obj.get("name"))
        organize = EntityOrganize.from_dict(obj.get("organize"))
        time_zone = from_int(obj.get("timeZone"))
        top_organize = EntityTopOrganize.from_dict(obj.get("topOrganize"))
        union_id = from_str(obj.get("unionId"))
        user_type = from_str(obj.get("userType"))
        return Entity(account, account_photo_url, avatars, birthday, card_no, card_type, class_no, code, email, mobile, gender, id, identities, kind, name, organize, time_zone, top_organize, union_id, user_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["account"] = from_str(self.account)
        result["accountPhotoUrl"] = from_str(self.account_photo_url)
        result["avatars"] = from_dict(lambda x: x, self.avatars)
        result["birthday"] = to_class(Birthday, self.birthday)
        result["cardNo"] = from_str(self.card_no)
        result["cardType"] = from_str(self.card_type)
        result["classNo"] = from_str(self.class_no)
        result["code"] = from_str(self.code)
        result["email"] = from_str(self.email)
        result["mobile"] = from_str(self.mobile)
        result["gender"] = from_str(self.gender)
        result["id"] = from_str(self.id)
        result["identities"] = from_list(lambda x: to_class(Identity, x), self.identities)
        result["kind"] = from_str(self.kind)
        result["name"] = from_str(self.name)
        result["organize"] = to_class(EntityOrganize, self.organize)
        result["timeZone"] = from_int(self.time_zone)
        result["topOrganize"] = to_class(EntityTopOrganize, self.top_organize)
        result["unionId"] = from_str(self.union_id)
        result["userType"] = from_str(self.user_type)
        return result


@dataclass
class AccountInfo:
    """ApifoxModel"""
    entities: List[Entity]
    errno: int
    error: str
    total: int

    @staticmethod
    def from_dict(obj: Any) -> 'AccountInfo':
        assert isinstance(obj, dict)
        entities = from_list(Entity.from_dict, obj.get("entities"))
        errno = from_int(obj.get("errno"))
        error = from_str(obj.get("error"))
        total = from_int(obj.get("total"))
        return AccountInfo(entities, errno, error, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["entities"] = from_list(lambda x: to_class(Entity, x), self.entities)
        result["errno"] = from_int(self.errno)
        result["error"] = from_str(self.error)
        result["total"] = from_int(self.total)
        return result

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
}

def get_account_info() -> AccountInfo:
    sess = get_http_session()
    resp = sess.get("https://my.sjtu.edu.cn/api/account", headers=HEADERS)
    if (not resp.url.startswith("https://my.sjtu.edu.cn/")):
        raise Exception("认证失败")
    result = AccountInfo.from_dict(resp.json())
    if (result.errno != 0):
        raise Exception(result.error)
    return result

def tool_account_info() -> str:
    result = get_account_info()
    from types_linq import Enumerable
    info = Enumerable(result.entities) \
        .first()
    identity = Enumerable(info.identities) \
        .first(lambda x: x.is_default)
    res = \
        f"姓名：{info.name}" + "\n" + \
        f"性别：{info.gender}" + "\n" + \
        f"学号：{info.code}" + "\n" + \
        f"邮箱：{info.email}" + "\n" + \
        f"班号：{info.class_no}" + "\n" + \
        f"jAccount 账号：{info.account}" + "\n" + \
        f"手机号：{info.mobile}" + "\n" + \
        f"专业：{identity.major.name}" + "\n" + \
        f"学院：{identity.organize.name}" + "\n" + \
        f"身份证号：{info.card_no}" + "\n"
    return res