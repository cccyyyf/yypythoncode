import sys
import subprocess

needToInstallList = ["selenium", "airtest-selenium", "airtest", "pytest", "pytest-html", "pytest-rerunfailures",
                     "unittest2", "PyMySQL", "pywin32", "pyyaml", "configparser", "pytest-assume", "pytest-xdist",
                     "pandas","numpy", "pocoui", "pocounit","allure-pytest","requests","redis"]


def cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return (output, err, p_status)


if __name__ == '__main__':
    if sys.version_info.major == 2:
        raise Exception("请使用python3")
    elif sys.version_info.major == 3:
        (alread_installed_output, alread_installed_err, alread_installed_p_status) = cmd("pip list")
        alread_installed_list = alread_installed_output.decode(encoding="gbk")
        for list in needToInstallList:
            if list not in alread_installed_list:
                (install_output, install_err, install_p_status) = cmd(
                    "python -m pip install " + list + " -i https://pypi.tuna.tsinghua.edu.cn/simple")
                print("=" * 40)
                print("install " + list)
                print(install_output.decode(encoding="gbk"))
                print(install_err)
                print(install_p_status)
