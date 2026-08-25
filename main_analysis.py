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
        try:
            dfs[name] = pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            dfs[name] = pd.read_csv(path, encoding='cp949')
        print(f"[{name}] 데이터 로드 완료: {dfs[name].shape}")
        
    return dfs

def merge_raw_data(dfs):
    """불러온 원본 DataFrame들을 하나의 기반 Master DataFrame으로 우선 병합합니다."""
    
    # 면적정보 중복 방지 (단지 레벨 분석용)
    if '면적정보' in dfs:
        dfs['면적정보'] = dfs['면적정보'].drop_duplicates(subset=['단지코드']).drop(columns=['주거전용면적(세부)', '세대수'], errors='ignore')

    print("\n[진행] 정적 테이블(단지코드 기준) 병합 시작...")
    static_df = dfs['기본정보']
    static_tables = ['면적정보', '시설정보', '운영정보', '위치정보']
    
    for table_name in static_tables:
        df_to_merge = dfs[table_name]
        cols_to_use = [col for col in df_to_merge.columns if col not in static_df.columns or col == '단지코드']
        static_df = pd.merge(static_df, df_to_merge[cols_to_use], on='단지코드', how='left')
    
    print("\n[진행] 시계열 테이블(단지코드, 발생년월 기준) 병합 시작...")
    ts_df = dfs['관리비']
    repair_df = dfs['장기수선']
    join_keys = ['단지코드', '발생년월(YYYYMM)']
    
    cols_to_use = [col for col in repair_df.columns if col not in ts_df.columns or col in join_keys]
    ts_df = pd.merge(ts_df, repair_df[cols_to_use], on=join_keys, how='left')
    
    print("\n[진행] 최종 전체 원본 병합 (시계열 + 정적) 시작...")
    raw_master_df = pd.merge(ts_df, static_df, on='단지코드', how='left')
    print(f"기반이 되는 원본 Master 데이터 병합 완료: {raw_master_df.shape}")
    
    return raw_master_df

def drop_unnecessary_columns(df):
    """병합 완료된 Master DataFrame에서 불필요한 칼럼들을 일괄 삭제(전처리)합니다."""
    cols_to_drop = [
        # 관리비
        '차량유지비', '지능형네트워크유지비', '재해예방비', '가스사용료(공용)', '가스사용료(전용)', 
        '기타', '제세공과금', '교육훈련비', '시설유지비', '안전점검비', '위탁관리수수료', 
        '급탕비(공용)', '수도료(공용)', 'TV수신료', '정화조오물수수료', '선관위운영비',
        # 기본정보
        '시공사', '주택관리업자',
        # 시설정보
        '건물구조', '전기-수전용량', '전기-세대전기계약방식', '승강기관리-관리방식', 
        'CCTV대수', '부대복리시설', '홈네트워크',
        # 운영정보
        '경비관리-계약업체', '청소관리-계약업체', '음식물 처리방법', '소독관리-계약업체', 
        '일반관리-관리방식', '경비관리-관리방식', '청소관리-관리방식', '소독관리-관리방식',
        # 장기수선
        '입주자기여수익', '공동기여수익'
    ]
    
    print("\n[진행] 병합된 데이터에서 불필요한 칼럼 일괄 삭제 전처리 시작...")
    existing_cols = [col for col in cols_to_drop if col in df.columns]
    df_cleaned = df.drop(columns=existing_cols)
    print(f"삭제된 칼럼 수: {len(existing_cols)}개")
    print(f"전처리 완료 후 최종 남은 데이터 크기: {df_cleaned.shape}")
    
    return df_cleaned

def main():
    print("=== 데이터 분석 파이프라인 시작 ===")
    
    # 1. 데이터 로드
    dfs = load_data()
    
    # 2. 기반 데이터프레임 병합 (원본 유지)
    raw_master_df = merge_raw_data(dfs)
    
    # 3. 전처리: 병합된 프레임에서 칼럼 삭제
    final_df = drop_unnecessary_columns(raw_master_df)
    
    print("\n=== Data Preview (최상위 5행) ===")
    print(final_df.head().to_string(index=False))
    
    print("\n=== 남은 최종 컬럼 리스트 ===")
    print(list(final_df.columns))
    
    return final_df

if __name__ == "__main__":
    df = main()
