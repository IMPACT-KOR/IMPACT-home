def parse_investment_file(file_path):
    investments = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(',')
                if len(parts) == 3:  # 세 개의 부분이 제대로 있는지 확인
                    id_part, target_part, amount_part = parts

                    user_id = id_part.split(':')[1].strip()
                    target = target_part.split(':')[1].strip()
                    amount = int(amount_part.split(':')[1].strip())

                    if target not in investments:
                        investments[target] = []

                    investments[target].append({
                        'investor': user_id,
                        'amount': amount
                    })
                else:
                    print(f"잘못된 형식의 줄이 있습니다: {line}")
    return investments


def calculate_total_investments(investment_data):
    total_investments = {}
    
    for target, investments in investment_data.items():
        total_investment = sum(investment['amount'] for investment in investments)
        total_investments[target] = total_investment

    return total_investments

def assign_teams(investment_data, team_count):
    total_investments = calculate_total_investments(investment_data)
    
    # 모든 투자자를 집합으로 모아 중복 없이 인원수 계산
    all_investors = set(investor for inv_list in investment_data.values() for investor in [x['investor'] for x in inv_list])
    total_people = len(all_investors)
    
    # 팀의 최대 인원 계산
    max_team_size = total_people // team_count
    remainder = total_people % team_count
    
    # 투자 합계가 높은 순서대로 팀장 선정
    sorted_leaders = sorted(total_investments.keys(), key=lambda k: total_investments[k], reverse=True)
    
    # 입력받은 팀 수만큼 팀장 선출
    leaders = sorted_leaders[:team_count]
    teams = {leader: [] for leader in leaders}

    # 팀에 합류시키기
    for leader in leaders:
        # 해당 팀장에게 투자한 사람들 목록
        investments = sorted(investment_data[leader], key=lambda x: x['amount'], reverse=True)
        for investor_data in investments:
            investor = investor_data['investor']
            # 팀장을 팀원에서 제외하고, 이미 다른 팀에 소속되지 않았고, 팀 최대 인원 수를 넘지 않도록 확인
            if investor not in leaders and not any(investor in team for team in teams.values()) and len(teams[leader]) < max_team_size:
                teams[leader].append(investor)
    
    # 남은 인원 확인 및 배분
    assigned_investors = set(investor for team in teams.values() for investor in team)
    remaining = list(all_investors - assigned_investors - set(leaders))
    
    if remaining:
        # 나머지 인원 배분
        for investor in remaining:
            for leader in leaders:
                if len(teams[leader]) < max_team_size + (1 if remainder > 0 else 0):
                    teams[leader].append(investor)
                    remainder -= 1
                    break

    return teams

from collections import defaultdict

def calculate_investment_sums(investment_data):
    investment_sums = defaultdict(int)
    
    for person, investments in investment_data.items():
        for investment in investments:
            investment_sums[person] += investment['amount']
    
    sorted_investments = sorted(investment_sums.items(), key=lambda x: x[1], reverse=True)
    
    return {name: amount for name, amount in sorted_investments}

def balance_teams(teams):
    # 팀의 크기 계산
    team_sizes = {team: len(members) for team, members in teams.items()}
    max_team_size = max(team_sizes.values())
    min_team_size = min(team_sizes.values())
    
    # 팀 크기 차이가 1 이하가 될 때까지 반복
    while max_team_size - min_team_size > 1:
        # 가장 인원이 많은 팀과 적은 팀을 찾기
        largest_team = max(team_sizes, key=team_sizes.get)
        smallest_team = min(team_sizes, key=team_sizes.get)
        
        # 가장 인원이 많은 팀에서 가장 적게 투자한 사람을 찾기
        smallest_investor = None
        smallest_investment = float('inf')
        
        for member in teams[largest_team]:
            member_investment = next((inv['amount'] for inv in investment_data[largest_team] if inv['investor'] == member), 0)
            if member_investment < smallest_investment:
                smallest_investment = member_investment
                smallest_investor = member
        
        # 그 사람을 가장 인원이 적은 팀으로 이동
        if smallest_investor:
            teams[largest_team].remove(smallest_investor)
            teams[smallest_team].append(smallest_investor)
        
        # 팀 크기 다시 계산
        team_sizes = {team: len(members) for team, members in teams.items()}
        max_team_size = max(team_sizes.values())
        min_team_size = min(team_sizes.values())
    
    return teams


if __name__ == '__main__':
    # 텍스트 데이터 파일에서 읽어오기
    file_path = 'investment_log.txt'
    investment_data = parse_investment_file(file_path)

    # 팀 총 수를 입력받음
    team_count = int(input("팀 총 수를 입력하세요: "))

    # 팀 할당
    teams = assign_teams(investment_data, team_count)

    # 결과 출력
    print("\n팀 구성 결과:")
    for team, members in teams.items():
        print(f"{team} 팀: {', '.join(members)}")
        
    # 팀 구성 결과를 리밸런스
    balanced_teams = balance_teams(teams)

    # 결과 출력
    print("\n균형 잡힌 팀 구성 결과:")
    for team, members in balanced_teams.items():
        print(f"{team} 팀: {', '.join(members)}")