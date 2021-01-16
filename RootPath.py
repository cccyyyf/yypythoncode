import os

class RootPath:
    @classmethod
    def getRootPath(cls):
        return os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def getWebIniPath(cls):
        return os.path.join(RootPath.getRootPath(),"resources/webpage/baidu/baidu.ini")

    @classmethod
    def getInterfaceIniPath(cls):
        return os.path.join(RootPath.getRootPath(),"resources/interface/ZHDD/")

    @classmethod
    def getDevicePlatPath(cls):
        """
        获取设备平台资源地址
        """
        return os.path.join(RootPath.getRootPath(), "resources/interface/DevicePlat/")

    @classmethod
    def getErGongPath(cls):
        """
        获取二供资源地址
        """
        return os.path.join(RootPath.getRootPath(), "resources/interface/ErGong/")

    @classmethod
    def getPath(cls, par_dir):
        """
        parDir: 类似"resources/interface/OutWork/"
        """
        return os.path.join(RootPath.getRootPath(), par_dir)

    @classmethod
    def getOutWorkPath(cls):
        return os.path.join(RootPath.getRootPath(), "resources/interface/OutWork/")

    @classmethod
    def getErGongPath(cls):
        """
        获取二供资源地址
        """
        return os.path.join(RootPath.getRootPath(), "resources/interface/ErGong/")


if __name__ == '__main__':
    res = RootPath.getInterfaceIniPath()
    print(res)