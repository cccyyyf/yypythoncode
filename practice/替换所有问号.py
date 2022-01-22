"""
@Author  ：Margot
@Date    ：2022/1/5 21:00 
@Question：
给你一个仅包含小写英文字母和 '?' 字符的字符串 s，请你将所有的 '?' 转换为若干小写字母，使最终的字符串不包含任何 连续重复 的字符。
注意：你 不能 修改非 '?' 字符。
题目测试用例保证 除 '?' 字符 之外，不存在连续重复的字符。
"""


class Solution(object):
    def modifyString(s):
        res = list(s)
        l = len(s)
        for i in range(l):
            if res[i] == "?":
                for ch in "abc":
                    if not (
                        i > 0 and res[i - 1] == ch or i < l - 1 and res[i + 1] == ch
                    ):
                        res[i] = ch
        return "".join(res)


if __name__ == "__main__":
    s = input("请输入仅包含小写英文字母和?字符的字符串：")
    print(Solution().modifyString(s))
