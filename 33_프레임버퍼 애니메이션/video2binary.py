import imageio
from PIL import Image
import array

filename = 'cat_meme.mp4'
reader = imageio.get_reader(filename, 'ffmpeg')
# 총 프레임 수 = 재생시간 * 프레임레이트
duration = reader.get_meta_data()['duration']
fps = reader.get_meta_data()['fps']
frames = duration * fps
print(frames)


# 64개의 이미지 x 가로 128 x 세로 128 x 24비트 컬러
# ROM 크기 = 64 x (7비트 + 7비트 = 총 주소:14비트 (한 프레임당) x 24bit
size = 256 # 저장할 이미지 수
width = 64 # 저장할 이미지 가로 크기
height = 64 # 저장할 이미지 세로 크기
colordepth = 3 # R, G, B 3개
gap = int(frames / size)  #저장할 프레임 간격
# 바이너리 파일 이름
binaryName = 'CATDATA.BIN'
# 저장할 바이너리 파일을 이진쓰기 모드로 열기
fp = open(binaryName, 'wb') 
# 어떤 변수가 가리키는 메모리를 위 파일에 쓸거냐 (1차원 배열)
image = array.array('B', [0, 0, 0] * width * height * size)

# 현재 프레임 번호
curr_num = 0
z = 0
 # 프레임을 한장씩 가져온다
for im in reader:
    # 만약 가져온 현재 프레임이 지정된 간격일때 저장
    if curr_num % gap == 0:
        imageio.imwrite('temp.jpg', im)
        im2 = Image.open('temp.jpg')
        # 가로 세로 이미지 사이즈 변경
        im2 = im2.resize((width, height))
        # 이미지의 전체 (x,y) 픽셀 값을 가져온다 
        pix = im2.load()
        for y in range(height):
            for x in range(width):
                #image 배열 인덱스 계산
                idx = z * ( width * height * colordepth ) + (y * width + x) * colordepth
                image[idx + 0] = pix[x,y][0] #RED 채널 값
                image[idx + 1] = pix[x,y][1] #GREEN 채널 값
                image[idx + 2] = pix[x,y][2] #BLUE 채널 값
        print(curr_num, z)
        # 저장된 프레임 번호 증가
        z += 1
        if z > size - 1:
            break
    # 현재 프레임 번호 증가
    curr_num += 1


image.tofile(fp)
fp.close()



