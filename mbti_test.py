questions = [
    {
        "question": "주말에 당신은 보통:",
        "options": {
            "a": "다양한 친구들과 어울리며 시간을 보낸다.",
            "b": "집에서 조용히 혼자만의 시간을 즐긴다."
        },
        "type": "EI"
    },
    {
        "question": "새로운 일을 시작할 때 당신은:",
        "options": {
            "a": "먼저 전체적인 계획을 세우고 시작한다.",
            "b": "일단 부딪혀보면서 해결해나가는 편이다."
        },
        "type": "SN"
    },
    {
        "question": "결정을 내릴 때 당신은:",
        "options": {
            "a": "객관적인 사실과 논리를 바탕으로 판단한다.",
            "b": "주변 사람들의 감정과 상황을 더 중요하게 생각한다."
        },
        "type": "TF"
    },
    {
        "question": "여행을 계획할 때 당신은:",
        "options": {
            "a": "숙소, 교통, 일정을 미리 다 정해놓는다.",
            "b": "특별한 계획 없이 자유롭게 돌아다니는 것을 선호한다."
        },
        "type": "JP"
    }
]

def run_mbti_test():
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    print("간단한 MBTI 검사를 시작합니다. 각 질문에 a 또는 b로 답해주세요.")
    print("-" * 30)

    for q in questions:
        print(q["question"])
        for key, value in q["options"].items():
            print(f"{key}) {value}")

        while True:
            answer = input("당신의 선택은? (a/b): ").lower()
            if answer in ["a", "b"]:
                break
            else:
                print("잘못된 입력입니다. a 또는 b를 입력해주세요.")

        if q["type"] == "EI":
            if answer == "a":
                scores["E"] += 1
            else:
                scores["I"] += 1
        elif q["type"] == "SN":
            if answer == "a":
                scores["S"] += 1
            else:
                scores["N"] += 1
        elif q["type"] == "TF":
            if answer == "a":
                scores["T"] += 1
            else:
                scores["F"] += 1
        elif q["type"] == "JP":
            if answer == "a":
                scores["J"] += 1
            else:
                scores["P"] += 1
        print("-" * 30)

    mbti_type = ""
    mbti_type += "E" if scores["E"] >= scores["I"] else "I"
    mbti_type += "S" if scores["S"] >= scores["N"] else "N"
    mbti_type += "T" if scores["T"] >= scores["F"] else "F"
    mbti_type += "J" if scores["J"] >= scores["P"] else "P"

    print(f"검사가 완료되었습니다!")
    print(f"당신의 MBTI 유형은 {mbti_type} 입니다!")

if __name__ == "__main__":
    run_mbti_test()
