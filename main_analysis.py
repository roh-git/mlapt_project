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
        print(f"[{name}] 데이터 로드 완료 (원본): {dfs[name].shape}")
        
    return dfs

def drop_unnecessary_columns(dfs):
    """사용자 요청에 따라 불필요한 칼럼을 삭제합니다."""
    cols_to_drop = {
        '관리비': [
            '차량유지비', '지능형네트워크유지비', '재해예방비', '가스사용료(공용)', '가스사용료(전용)', 
            '기타', '제세공과금', '교육훈련비', '시설유지비', '안전점검비', '위탁관리수수료', 
            '급탕비(공용)', '수도료(공용)', 'TV수신료', '정화조오물수수료', '선관위운영비'
        ],
        '기본정보': ['시공사', '주택관리업자'],
        '시설정보': [
            '건물구조', '전기-수전용량', '전기-세대전기계약방식', '승강기관리-관리방식', 
            'CCTV대수', '부대복리시설', '홈네트워크'
        ],
        '운영정보': [
            '경비관리-계약업체', '청소관리-계약업체', '음식물 처리방법', '소독관리-계약업체', 
            '일반관리-관리방식', '경비관리-관리방식', '청소관리-관리방식', '소독관리-관리방식'
        ],
        '장기수선': ['입주자기여수익', '공동기여수익']
    }
    
    print("\n[진행] 불필요한 칼럼 삭제 시작...")
    for table_name, columns in cols_to_drop.items():
        if table_name in dfs:
            # errors='ignore'를 사용하여 이미 없는 칼럼이 있어도 안전하게 넘어갑니다
            dfs[table_name] = dfs[table_name].drop(columns=columns, errors='ignore')
            print(f"[{table_name}] 지정된 칼럼 삭제 완료 -> 남은 컬럼 수: {dfs[table_name].shape[1]}")
            
    return dfs

def merge_data(dfs):
    """불러온 DataFrame들을 하나의 Master DataFrame으로 병합합니다."""
    
    # [중요] 면적정보 테이블은 평형(세부면적)별로 여러 행이 존재하여 조인 시 데이터가 N배로 뻥튀기됨.
    # 단지 레벨의 분석을 위해 '관리비부과면적', '주거전용면적(단지합계)'만 가져오도록 중복 제거.
    if '면적정보' in dfs:
        dfs['면적정보'] = dfs['면적정보'].drop_duplicates(subset=['단지코드']).drop(columns=['주거전용면적(세부)', '세대수'], errors='ignore')

    print("\n[진행] 정적 테이블(단지코드 기준) 병합 시작...")
    
    # 1. 정적(Static) 테이블 병합 (기본, 면적, 시설, 운영, 위치)
    static_df = dfs['기본정보']
    static_tables = ['면적정보', '시설정보', '운영정보', '위치정보']
    
    for table_name in static_tables:
        df_to_merge = dfs[table_name]
        # 단지코드를 제외한 중복 칼럼(예: 동수, 시도) 방지
        cols_to_use = [col for col in df_to_merge.columns if col not in static_df.columns or col == '단지코드']
        static_df = pd.merge(static_df, df_to_merge[cols_to_use], on='단지코드', how='left')
    
    print(f"정적 데이터 병합 완료: {static_df.shape}")

    print("\n[진행] 시계열 테이블(단지코드, 발생년월 기준) 병합 시작...")
    
    # 2. 시계열(Time-Series) 테이블 병합 (관리비, 장기수선)
    ts_df = dfs['관리비']
    repair_df = dfs['장기수선']
    
    join_keys = ['단지코드', '발생년월(YYYYMM)']
    
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
    
    dfs = load_data()
    dfs = drop_unnecessary_columns(dfs)
    final_df = merge_data(dfs)
    
    print("\n=== Data Preview (최상위 5행) ===")
    # 콘솔 출력 시 인코딩 안깨지게 텍스트 변환
    print(final_df.head().to_string(index=False))
    
    print("\n=== 남은 최종 컬럼 리스트 ===")
    print(list(final_df.columns))
    
    return final_df

if __name__ == "__main__":
    df = main()
