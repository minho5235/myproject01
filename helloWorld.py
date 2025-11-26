import random
import time

class Player:
    def __init__(self, job):
        self.job = job
        self.level = 1
        self.exp = 0
        self.max_exp = 100
        self.gold = 0
        self.potions = 5  # 포션 5개로 시작 (지원금)
        self.revive = True # 부활권 1회
        
        if job == '전사':
            self.max_hp = 180   # 체력 상향
            self.max_mp = 40
            self.atk = 18       # 공격력 상향
            self.name = "🛡️ 전사"
            self.skills = {"강타(MP8)": 8, "철벽(MP0)": 0}
        elif job == '마법사':
            self.max_hp = 110   # 체력 상향
            self.max_mp = 150
            self.atk = 10
            self.name = "🔮 마법사"
            self.skills = {"파이어볼(MP15)": 15, "힐(MP25)": 25}
        
        self.hp = self.max_hp
        self.mp = self.max_mp

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.max_exp = int(self.max_exp * 1.3)
        self.max_hp += 20
        self.max_mp += 10
        self.atk += 3
        self.hp = self.max_hp
        self.mp = self.max_mp
        print(f"\n🌟🌟 [LEVEL UP!] {self.level}레벨 달성! (전체 회복) 🌟🌟")

def get_monster(floor):
    # 일반 몬스터 스케일링
    scale = 1 + (floor * 0.1) 
    
    kinds = [
        {"name": "슬라임", "hp": 50, "atk": 8, "gold": 10},
        {"name": "늑대", "hp": 70, "atk": 11, "gold": 15},
        {"name": "오크", "hp": 90, "atk": 13, "gold": 20},
        {"name": "병사", "hp": 110, "atk": 16, "gold": 25}
    ]
    
    # 보스전 (스케일링 버그 수정: 고정 수치 + 층수 비례)
    if floor % 5 == 0:
        boss_hp = 250 + (floor * 20)  # 예: 5층 350, 10층 450
        boss_atk = 15 + (floor * 1.5) # 예: 5층 22, 10층 30
        m = {"name": f"🐲 {floor}층 보스", "hp": int(boss_hp), "atk": int(boss_atk), "gold": 200}
        m['max_hp'] = m['hp']
        return m # 보스는 scale 적용 안 함 (이미 계산됨)
    else:
        m = random.choice(kinds).copy()
        
    m['hp'] = int(m['hp'] * scale)
    m['max_hp'] = m['hp']
    m['atk'] = int(m['atk'] * scale)
    m['gold'] = int(m['gold'] * scale)
    return m

def shop(player):
    print("\n" + "="*40)
    print("               🏚️  상  점  🏚️")
    print("="*40)
    while True:
        print(f"\n💰 골드: {player.gold}G | ⚔️ 공격력: {player.atk}")
        print("1. 🧪 포션 구매 (50G)")
        print("2. ⚔️ 무기 강화 (200G)")
        print("3. 🚪 나가기")
        try:
            choice = int(input("선택 >> "))
            if choice == 1:
                if player.gold >= 50:
                    player.gold -= 50
                    player.potions += 1
                    print(">> 포션 획득!")
                else: print(">> 돈 부족")
            elif choice == 2:
                if player.gold >= 200:
                    player.gold -= 200
                    player.atk += 5
                    print(f">> 강화 성공! 공격력+5")
                else: print(">> 돈 부족")
            elif choice == 3: break
        except: pass

def game_start():
    print("=== 🏰 무한의 탑 (Ver 4.0 난이도 하향) ===")
    print("1.전사  2.마법사")
    while True:
        try:
            c = int(input("직업 선택 >> "))
            if c in [1, 2]: break
        except: pass
        
    player = Player('전사' if c == 1 else '마법사')
    floor = 1
    
    while True:
        monster = get_monster(floor)
        m_hp = monster['hp']
        m_max = monster['max_hp']
        
        print(f"\n\n🔶🔶 [ {floor}층 ] {monster['name']} (HP:{m_max}) 🔶🔶")
        time.sleep(0.5)
        
        while m_hp > 0:
            print(f"\n{'='*12} 🆚 {'='*12}")
            print(f"👾 {monster['name']} : ♥ {m_hp}/{m_max} (공격력:{monster['atk']})")
            print(f"😎 {player.name} : ♥ {int(player.hp)}/{player.max_hp} | 💧 {player.mp}/{player.max_mp}")
            print(f"💰 {player.gold}G | 🧪 포션:{player.potions}")
            print(f"{'-'*30}")
            
            atk_msg = "평타(MP+5)" if player.job == '마법사' else "공격"
            print(f"1.{atk_msg}  2.스킬({list(player.skills.keys())[0]})  3.특수({list(player.skills.keys())[1]})  4.포션")
            
            try:
                act = int(input("행동 >> "))
            except: continue
                
            dmg = 0
            guard = False
            
            # 플레이어 행동
            if act == 1:
                dmg = random.randint(player.atk, player.atk + 4)
                if player.job == '마법사':
                    player.mp = min(player.max_mp, player.mp + 5)
                    print(f"🗡️ 마력 흡수! {dmg} 데미지")
                else:
                    print(f"🗡️ 공격! {dmg} 데미지")

            elif act == 2:
                cost = list(player.skills.values())[0]
                if player.mp >= cost:
                    player.mp -= cost
                    multiplier = 3.5 if player.job == '마법사' else 2.0
                    dmg = int(player.atk * multiplier)
                    txt = "🔥 파이어볼!" if player.job == '마법사' else "💥 강타!"
                    print(f"{txt} {dmg} 데미지!!")
                else:
                    print("💧 MP 부족! 평타 나갑니다.")
                    dmg = int(player.atk * 0.5)

            elif act == 3:
                cost = list(player.skills.values())[1]
                if player.mp >= cost:
                    player.mp -= cost
                    if player.job == '전사':
                        guard = True
                        print("🛡️ 방어! 데미지 1/3 감소")
                    else:
                        heal = int(player.max_hp * 0.5)
                        player.hp = min(player.max_hp, player.hp + heal)
                        print(f"✨ 힐링! 체력 {heal} 회복")
                else:
                    print("💧 MP 부족...")

            elif act == 4:
                if player.potions > 0:
                    player.potions -= 1
                    player.hp = min(player.max_hp, player.hp + 120)
                    print("🧪 포션 사용! (HP +120)")
                else: print("⚠️ 포션 없음")

            m_hp -= dmg
            
            # 몬스터 처치 시
            if m_hp <= 0:
                print(f"\n🎉 승리! (+{monster['gold']}G)")
                player.gold += monster['gold']
                player.exp += 30 + (floor * 3)
                
                # 보스 처치 보너스
                if floor % 5 == 0:
                    print("🎁 [보스 보상] 공격력이 10 증가했습니다!")
                    player.atk += 10
                    
                if player.exp >= player.max_exp: player.level_up()
                break
            
            # 몬스터 반격
            m_dmg = monster['atk'] + random.randint(-2, 2)
            if guard: m_dmg //= 3
            player.hp -= m_dmg
            print(f"💥 피격! {m_dmg} 피해")
            
            # 사망 처리 (부활 로직 추가)
            if player.hp <= 0:
                if player.revive:
                    print("\n👼 [부활 발동] 교수님이 칠판을 보는 사이 몰래 살아났습니다!")
                    player.hp = int(player.max_hp * 0.5)
                    player.revive = False
                    print(f"👼 체력 50% 회복! (부활권 소멸)")
                else:
                    print(f"\n💀 사망했습니다... 최종 기록: {floor}층")
                    return

        if floor % 3 == 0: shop(player)
        else:
            player.hp = min(player.max_hp, player.hp + 30)
            player.mp = min(player.max_mp, player.mp + 15)
            print("\n⛺ 휴식 (HP/MP 소량 회복)")
            
        floor += 1

game_start()