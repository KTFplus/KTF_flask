# 최종 백엔드 서버
## 음성 파일 업로드 및 전사 API(필수)

```yaml
POST /upload-audio
```

- **요청 형식**: multipart/form-data(형식, 필드명 동일해야함)
    - `audio`: 음성 파일 (필수)
    - `userId`: 사용자 ID(`string`일단 ‘test-users’로 처리)
- **처리**:
    - 오디오 파일을 ASR 서버(Colab/로컬)로 전송하여 인식 및 화자 분리 결과 수신
    - 결과(스크립트, 화자별 대사)를 DB에 저장 및 프론트엔드로 반환

--- 
### 발음 평가 API(필수)

```yaml
POST /pronunciation-evaluate
```
- **요청 형식(참고)**: multipart/form-data(필드명,형식 동일해야함)
    - `audio`: 발음 녹음 파일 (필수)
    - `sentenceId`: 평가할 문장 ID (필수)-위에서부터 1,2,3,…
    - `userId`: 사용자 ID(일단 ‘test-users’로 처리)
- **처리**:
    - 프론트로부터 입력받은 음성파일을 발음평가 모듈로 전송
    - 결과(평가 결과 및 점수) 수신 후 프론트엔드로 반환
