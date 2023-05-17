# Pending Queue Service

## Deprecated

moved to https://github.com/hatiolab/operato-foundation-service.git

## API Document

로컬 설치의 경우 다음 URL을 통해서 제공되는 API들을 확인하실 수 있습니다.

**http://127.0.0.1:9903/docs**


## 설치 및 실행

### 파이썬 버전

- python 3.9 or later


### 필수 모듈 설치

```bash
pip install -r src/requirements.txt
```

### 설치 시 오류 대처
##### 맥에서 psycopg2 설치 시 에러가 날 경우.

```bash
# please 
brew install postgresql
```


### ***config.yaml*** 준비

***config/config.yaml***을  ***src/*** 디렉토리에 복사하고 필요 시 일부 모듈을 수정합니다.


### API 서버 실행

```bash
cd src
python3 main.py
```

### 유닛 테스트 코드 실행

```bash
cd src
python3 -m unittest discover -s test -p "*_test.py"
```



## Additional Things

### 도커 이미지 생성 및 배포

```bash
# build a docker image
./build.sh

# push the docker image
./push.sh
```


### 쿠버네티스 배포

k8s/* 파일들을 참조하여 배포합니다.

```bash
kubectl apply -f k8s/statefulset-readwriteonce.yaml
kubectl apply -f k8s/service.yaml

```

### 코드 포맷터

Black(https://github.com/psf/black)

```bash
pip install black
```
