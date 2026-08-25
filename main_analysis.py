import pandas as pd
import os

# 데이터가 저장된 디렉토리 경로 설정
DATA_DIR = 'data'

def load_data():
    """7개의 CSV 파일을 각각 DataFrame으로 불러옵니다."""
    files = {
        '기본정보': '기본정보.csv',
        '면적정보': '면적정보.csv',
        '시설정보': '시설정보.csv',
        '운영정보': '운영정보.csv',
        '위치정보': '위치정보.csv',
        '장기수선': '장기수선.csv',
        '관리비': '관리비.csv'
    }
    
    dfs = {}
    for name, filename in files.items():
        path = os.path.join(DATA_DIR, filename)
        # 인코딩 문제 방지를 위해 utf-8 시도 후 cp949 적용
        try:
            dfs[name] = pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            dfs[name] = pd.read_csv(path, encoding='cp949')
        print(f"[{name}] 데이터 로드 완료: {dfs[name].shape}")
        
    return dfs

def merge_data(dfs):
    """불러온 DataFrame들을 하나의 Master DataFrame으로 병합합니다."""
    print("\n[진행] 정적 테이블(단지코드 기준) 병합 시작...")
    
    # 1. 정적(Static) 테이블 병합 (기본, 면적, 시설, 운영, 위치)
    static_df = dfs['기본정보']
    static_tables = ['면적정보', '시설정보', '운영정보', '위치정보']
    
    for table_name in static_tables:
        df_to_merge = dfs[table_name]
        # 단지코드를 제외한 중복 칼럼(예: 동수, 세대수) 방지
        cols_to_use = [col for col in df_to_merge.columns if col not in static_df.columns or col == '단지코드']
        static_df = pd.merge(static_df, df_to_merge[cols_to_use], on='단지코드', how='left')
    
    print(f"정적 데이터 병합 완료: {static_df.shape}")

    print("\n[진행] 시계열 테이블(단지코드, 발생년월 기준) 병합 시작...")
    
    # 2. 시계열(Time-Series) 테이블 병합 (관리비, 장기수선)
    ts_df = dfs['관리비']
    repair_df = dfs['장기수선']
    
    # 시계열 조인 키: 단지코드 + 발생년월
    join_keys = ['단지코드', '발생년월(YYYYMM)']
    
    # 중복 칼럼 방지
    cols_to_use = [col for col in repair_df.columns if col not in ts_df.columns or col in join_keys]
    ts_df = pd.merge(ts_df, repair_df[cols_to_use], on=join_keys, how='left')
    
    print(f"시계열 데이터 병합 완료: {ts_df.shape}")

    print("\n[진행] 최종 전체 병합 (시계열 데이터 + 정적 데이터) 시작...")
    
    # 3. 최종 병합 (시계열 데이터 원본 유지 기준 Left Join)
    final_df = pd.merge(ts_df, static_df, on='단지코드', how='left')
    print(f"최종 Master 데이터 병합 완료: {final_df.shape}")
    
    return final_df

def main():
    print("=== 데이터 분석 파이프라인 시작 ===")
    
    # 1. 데이터 로드
    dfs = load_data()
    
    # 2. 데이터 병합
    final_df = merge_data(dfs)
    
    # 3. 결과 저장 (선택 사항)
    # output_path = os.path.join(DATA_DIR, 'merged_master_data.csv')
    # final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    # print(f"\n최종 데이터셋 저장 완료: {output_path}")
    
    print("\n=== Data Preview ===")
    print(final_df.head())
    print("\n=== Columns List ===")
    print(list(final_df.columns))
    
    return final_df

if __name__ == "__main__":
    df = main()
    # 이후 df를 활용하여 EDA 및 가설 검증, 모델링 코드를 이어나가면 됩니다.
