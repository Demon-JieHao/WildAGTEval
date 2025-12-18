#!/bin/bash

# 환경별 파일들 배치 변환 스크립트

# 파라미터 검증
if [ $# -eq 0 ]; then
    echo "❌ 환경 이름을 지정해주세요."
    echo ""
    echo "사용법: $0 <환경이름>"
    echo ""
    echo "예시:"
    echo "  $0 TransactionEnv"
    echo "  $0 MediaControlEnv"
    echo "  $0 SmartHomeEnv"
    echo "  $0 CommunicationController"
    echo "  $0 CulinaryControlEnv"
    echo "  $0 InformationControlEnv"
    echo "  $0 TimeNotificationEnv"
    exit 1
fi

# 환경 이름 파라미터 받기
ENV_NAME="$1"

echo "🔄 $ENV_NAME 파일 배치 변환 시작..."

# 입력 및 출력 디렉토리 설정
INPUT_DIR="atomic_conversation_units/success_conversations/$ENV_NAME"
OUTPUT_DIR="atomic_conversation_units/success_conversations/${ENV_NAME}_transformed"

# 입력 디렉토리 존재 확인
if [ ! -d "$INPUT_DIR" ]; then
    echo "❌ 입력 디렉토리를 찾을 수 없습니다: $INPUT_DIR"
    echo "💡 사용 가능한 환경들을 확인해보세요:"
    ls -d atomic_conversation_units/success_conversations/*/ 2>/dev/null | grep -v "_transformed" | sed 's|.*/||' | sed 's|/$||' || echo "   (디렉토리를 찾을 수 없습니다)"
    exit 1
fi

# 출력 디렉토리 생성
mkdir -p "$OUTPUT_DIR"

# 변환 통계
total_files=0
success_files=0
failed_files=0

echo "📂 입력 디렉토리: $INPUT_DIR"
echo "📁 출력 디렉토리: $OUTPUT_DIR"
echo ""

# *exec.py 파일들을 찾아서 변환
for input_file in "$INPUT_DIR"/*exec.py; do
    # 파일이 존재하는지 확인
    if [ ! -f "$input_file" ]; then
        echo "❌ 파일을 찾을 수 없습니다: $input_file"
        continue
    fi
    
    # 파일명 추출 (경로 제거)
    filename=$(basename "$input_file")
    base_name="${filename%.*}"  # 확장자 제거
    
    # 출력 파일 경로 생성 (transformed 접미사 추가)
    output_file="$OUTPUT_DIR/${base_name}.py"
    
    echo "🔄 변환 중: $filename"
    echo "   입력: $input_file"
    echo "   출력: $output_file"
    
    # 변환 실행
    if python3 common/transform_scenario_script.py --input "$input_file" --output "$output_file"; then
        echo "✅ 변환 성공: $filename"
        ((success_files++))
    else
        echo "❌ 변환 실패: $filename"
        ((failed_files++))
    fi
    
    ((total_files++))
    echo ""
done

# 최종 통계 출력
echo "================================"
echo "📊 배치 변환 완료 요약"
echo "================================"
echo "총 파일 수: $total_files"
echo "성공한 파일: $success_files"
echo "실패한 파일: $failed_files"

if [ $total_files -gt 0 ]; then
    success_rate=$(( success_files * 100 / total_files ))
    echo "성공률: ${success_rate}%"
fi

echo ""
if [ $success_files -gt 0 ]; then
    echo "✅ 변환된 파일들은 $OUTPUT_DIR 디렉토리에 저장되었습니다."
fi

if [ $failed_files -gt 0 ]; then
    echo "❌ $failed_files 개의 파일 변환에 실패했습니다."
    exit 1
else
    echo "🎉 모든 파일이 성공적으로 변환되었습니다!"
    exit 0
fi
