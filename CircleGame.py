# @Time: 2021/12/7 22:32
# @Auth: Margot

'''
一个回合制游戏，每个角色都有hp和power，hp代表血量，power代表攻击力，hp初始值为1000，power初始值为200.
定义一个fight方法：
 final_hp = hp-enemy_power
 enemy_final_hp = enemy_hp-power
 两个hp进行对比，血量剩余多的人获胜
-------------------------------
第二个角色，叫后裔，继承了角色的hp和power，并多了护甲属性：houyi_hp = hp+defense-enemy_power
-------------------------------
加入异常的改造：平局的时候抛出异常
'''

class Game():
    def __init__(self, hp, power):
        self.hp = hp
        self.power = power
    def fight(self, enemy_hp, enemy_power):
        final_hp = self.hp - enemy_power
        enemy_final_hp = enemy_hp - self.power
        if final_hp>enemy_final_hp:
            print("我赢了")
        elif final_hp<enemy_final_hp:
            print("你赢了")
        else:
            print("平局")

class HouYi(Game):
   def __init__(self, defense):
    #如果在子类中重新定义了_init_，那么父类的_init_将会被覆盖
        super().__init__(1000,200)
        self.defense = defense
   def houyi_fight(self, enemy_hp, enemy_power):
        while True:
            hp = self.hp+self.defense - enemy_power
            enemy_hp = enemy_hp - self.power
            print("我的hp是{}".format(hp))
            print(f"敌人的hp是{enemy_hp}")
            if hp <=0:
                print("敌人赢了")
                break
            elif enemy_hp <=0:
                print("我赢了")
                break

defense = 300
h = HouYi(defense)
a = int(input("请输入enemy_hp\n"))
b = int(input("请输入enemy_power\n"))
h.houyi_fight(a,b)

# hp = 1000
# power = 200
# g = Game(hp ,power)
# a = int(input("请输入hp"))
# b = int(input("请输入power"))
# g.fight(a,b)