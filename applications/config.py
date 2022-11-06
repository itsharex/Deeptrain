import json
import os.path
from typing import *
from DjangoWebsite.settings import APPLICATIONS_CONFIG_FILE, CODING


class RepositoryAddress(object):  # NamedTuple: AttributeError: attribute '__dict__' of 'type' objects is not writable
    """
    Repository - address
    e.g.

    >>> from applications.config import *
    In[1]
    >>> repo = RepositoryAddress(github="1", gitee="2", gitcode="  ")
    >>> print(repo)

    Out[1]
    > Repository Address:
    >    github: 1
    >    gitee: 2
    >

    In[2]
    >>> repo = RepositoryAddress()
    >>> print(repo)

    Out[2]
    > Empty Repository Address
    >

    """
    support = (
        "github",
        "gitee",
        "gitcode"
    )
    github: str = ""
    gitee: str = ""
    gitcode: str = ""

    # gitlab_address: str = "" 2022 年 7 月 31 日后，本 GitLab 实例已停止向中科大校外用户服务。校外用户数据将于 2022 年 12 月 31 日后删除

    def __init__(self, *_, **kwargs):
        for addr, res in kwargs.items():
            if addr in self.support and isinstance(res, str):
                setattr(self, addr, res.strip(" "))

    def get_dict(self) -> dict:  # __dict__: RecursionError
        return {addr: getattr(self, addr) for addr in self.support if getattr(self, addr)}

    def __iter__(self) -> Iterable[Tuple[str, str]]:
        return iter(self.get_dict().items())

    def __str__(self):
        return "Repository Address: {}".format('\n\t'.join([''] + list(map(lambda addrs: f"{addrs[0]}: {addrs[1]}",
                                                                           list(iter(self)))))) if self.get_dict() \
            else "Empty Repository Address"


# class _BaseConfig(NamedTuple):
#     repository_address: Union[RepositoryAddress, dict] = {}
#
#     name: str = ""
#     author: str = ""
#     profile: str = """..."""
#     image: str = ""
#
#     application_location: str = ""
#     UrlRoute: bool = True
#
#
# class Config(_BaseConfig):
#     @classmethod
#     def __init__(cls, *args, **kwargs):
#         # 不调用 super(Config, cls).__init__(*args, **kwargs),
#         # 因为 Config <- _BaseConfig <- typing.NamedTuple <- NamedTupleMeta <- type
#         # 并且 若执行 super 调用, 将会抛出 classmethod-TypeError: descriptor '__init__' of 'object' object needs an argument
#         if isinstance(cls.repository_address, dict):
#             cls.repository_address = RepositoryAddress(**cls.repository_address)
#         if not cls.repository_address:
#             cls.repository_address = RepositoryAddress()
#         print(cls.repository_address)
#
#     def write(self, fp: "IO[str]"):
#         json.dump({
#             "repository_address": self.repository_address.get_dict(),
#             "author": self.author,
#             "profile": self.profile,
#             "image": self.image,
#             "application_location": self.application_location,
#             "UrlRoute": self.UrlRoute,
#         }, fp)
#
#     def get_repository_info(self) -> dict:
#         return self.repository_address.get_dict()


class _BaseConfig(object):
    repository_address: Union[RepositoryAddress, dict] = {}

    name: str = ""
    author: str = ""
    profile: str = """..."""
    image: str = ""
    info_urls: str = ""

    UrlRoute: bool = True

    def __init__(self, *_, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if isinstance(self.repository_address, dict):
            self.repository_address = RepositoryAddress(**self.repository_address)

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "repository_address": self.get_repository_info(),
            "author": self.author,
            "profile": self.profile,
            "image": self.image,
            "info_urls": self.info_urls,
            "UrlRoute": self.UrlRoute,
        }

    def get_repository_info(self) -> dict:
        return self.repository_address.get_dict()

    def __str__(self) -> str:
        return \
            f"{self.__class__.__name__}({', '.join(map(lambda kv: f'{kv[0]}={repr(kv[1])}', self.get_dict().items()))})"


class JSONConfig(_BaseConfig):
    def __init__(self, fp: Union["IO[str]", str]):
        if isinstance(fp, str):
            fp = open(fp, "r")
        super().__init__(**json.load(fp))
        self.io_file = fp.name
        fp.close()

    @staticmethod
    def ConfigDump(cls: _BaseConfig, fp: "IO[str]"):
        json.dump(cls.get_dict(), fp, indent=4)
        fp.close()

    def dump(self, fp: Union["IO[str]", None] = None):
        self.ConfigDump(self, fp or open(self.io_file, "w", encoding=CODING))

    def dumps(self) -> str:
        return json.dumps(self.get_dict(), indent=4)

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)


def json_parser(path: str) -> Union[JSONConfig, None]:
    path = os.path.join(path, APPLICATIONS_CONFIG_FILE)
    if os.path.isfile(path):
        try:
            return JSONConfig(path)
        except Exception:
            pass
    return


def json_writer(repository_address: dict = None,
                name: str = "",
                author: str = "",
                profile: str = "",
                image: str = "",
                info_urls: list = None,
                UrlRoute: bool = True,
                path: str = "") -> _BaseConfig:
    path = os.path.join(path, APPLICATIONS_CONFIG_FILE)
    _conf = _BaseConfig(
        repository_address=repository_address,
        name=name,
        author=author,
        profile=profile,
        image=image,
        info_urls=info_urls,
        UrlRoute=UrlRoute,
    )
    # _conf = _BaseConfig(**locals())
    JSONConfig.ConfigDump(
        _conf,
        open(path, "w", encoding=CODING),
    )
    return _conf


if __name__ == '__main__':
    js = json_parser("Snake")
    print(js)
    js.dump()
