def expressions(num):
    answer = 1 # 모든 숫자는 최소 1가지 방법이 존재
    sum = 0
    start = 0
    while start != (num // 2 + 1): # 시작점은 절반(num//2)이면 충분하다.
        if sum < num:
            for i in range(start+1, num // 2 + 1 + 1):
                sum += i 
                if sum == num: 	# num과 같으면
                    answer += 1 # 경우의 수를 하나 찾았으므로 1 증가
                    start += 1 # 시작점 1 증가
                    sum = 0  # sum을 0으로 초기화
                    break

                elif sum > num: # num을 초과하면
                    start += 1  # 시작점 1 증가
                    sum = 0  # sum을 0으로 초기화
                    break
    return answer

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(expressions(15));
