from pathlib import Path
import pandas as pd

#############################
############################
def 정제(df):
	정제_df = df.copy()

	# 점수가 비어 있는 행을 삭제한다.
	정제_df = 정제_df.dropna(subset=["점수"])
	print("점수 결측 행 삭제 후:", len(정제_df))

	# 모든 열의 값이 완전히 같은 중복 행을 삭제한다.
	정제_df = 정제_df.drop_duplicates()
	print("중복 행 삭제 후:", len(정제_df))

	# 반과 과목 값의 앞뒤 공백을 제거한다.
	정제_df["반"] = 정제_df["반"].str.strip()
	정제_df["과목"] = 정제_df["과목"].str.strip()
	print("공백 제거 후:", len(정제_df))

	# 점수가 0 이상 100 이하인 행만 남긴다.
	정제_df = 정제_df[정제_df["점수"].between(0, 100)]
	정제_df["점수"] = 정제_df["점수"].astype(int)
	print("점수 범위 적용 후:", len(정제_df))

	return 정제_df

import pandas as pd
csv_path = Path(__file__).with_name("scores_2026.csv")
df = pd.read_csv(csv_path)
df = 정제(df)
정제_df = df.copy()
print(sorted(df["반"].unique()))      # ['1반', '2반']       ← 세 개에서 두 개로
print(sorted(df["과목"].unique()))    # ['수학','영어','프로그래밍'] ← 네 개에서 세 개로

# 시작        114
# 빈 칸 제거  108      ← 114 - 108 = 6    진단표의 「빈 칸」과 같은가?
# 중복 제거   104      ← 108 - 104 = 4    진단표의 「중복」과 같은가?
# 범위 밖 제거 100     ← 104 - 100 = 4    999 세 개 + 음수 하나


csv_path = Path(__file__).with_name("scores_2026.csv")
원본_df = pd.read_csv(csv_path)

print(원본_df.shape)                      # (114, 5)
print(원본_df["점수"].isna().sum())        # 6  <- 빈 칸이 몇 개인가
print(원본_df.duplicated().sum())         # 4  <- 완전히 같은 행이 몇 개인가
print(원본_df["반"].unique())             # ['2반' '1반' '1반 ']  <- 세 개?
print(원본_df["과목"].unique())           # ['수학' '프로그래밍' '영어' '프로그래밍 ']
print(원본_df["점수"].describe())         # max 999.0 min -5.0  <- 점수인데?

# 정제된 데이터에서 수학 과목의 행만 남긴다.
df = df[df["과목"] == "수학"]
print("수학 과목 행 수:", len(df))

# 정제된 전체 데이터에서 반별 점수 평균을 계산한다.
반별_평균 = 정제_df.groupby("반")["점수"].mean()
print("반별 점수 평균:")
print(반별_평균)

# 정제된 전체 데이터를 과목과 반으로 묶어 점수 평균을 계산한다.
과목_반별_평균 = 정제_df.groupby(["과목", "반"])["점수"].mean()
print("과목·반별 점수 평균:")
print(과목_반별_평균)

# 정제된 전체 데이터에서 반별 개수, 평균, 중앙값, 최댓값을 계산한다.
반별_요약 = 정제_df.groupby("반").agg(
	개수=("점수", "count"),
	평균=("점수", "mean"),
	중앙값=("점수", "median"),
	최댓값=("점수", "max"),
).round(2)
print("반별 점수 요약:")
print(반별_요약)

