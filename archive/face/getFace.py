import cv2, os
from api.face.detect_anime_face import getFaceRect
from api.utils.createPath import createPath

# 画像のロード
def loadImage(imagePath): 
    return cv2.imread(imagePath)

# 画像のリサイズ
def resizeImage(image, maxResolution: int = 2000):
    height, width = image.shape[:2]
    while width > maxResolution or height > maxResolution:
        width = int(width * 3 / 4)
        height = int(height * 3 / 4)
    return cv2.resize(image, (width, height))

# 顔検出
def detectFace(image, modelPath):
    # モデルのロード
    FACE_MODEL = cv2.CascadeClassifier(modelPath)
    # 画像のグレースケール変換
    GRAY_IMAGE = cv2.cvtColor(resizeImage(image, 1500), cv2.COLOR_BGR2GRAY)
    # 顔検出
    return FACE_MODEL.detectMultiScale(GRAY_IMAGE, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# 顔検出部分の拡張
def extendFaceRect(
    x, y, x2, y2, 
    image, 
    initExtension_neg: int = 20,
    initExtension_pos: int = 20,
    decrement: int = 20
):
    max_x, max_y = image.shape[1], image.shape[0]
    min_x, min_y = 0, 0
    extension_neg = initExtension_neg
    extension_pos = initExtension_pos

    while True: 
        nx = max(min_x, x - extension_neg)
        ny = max(min_y, y - extension_neg)
        nx2 = min(max_x, x2 + extension_pos)
        ny2 = min(max_y, y2 + extension_pos)

        # 画像の端に顔がある場合は拡張しない 
        if (nx == min_x or ny == min_y or nx2 == max_x or ny2 == max_y) and (extension_neg > 0 or extension_pos > 0):
            extension_neg -= decrement
            extension_pos -= decrement
        else:
            break
        
    return (nx, ny, nx2, ny2)
    
# 顔検出部分を切り抜き保存
def cropFace(faces, image, resizeResolution, extension):
    resizedFaces = []
    for i, (x, y, x2, y2) in enumerate(faces):
        x, y, x2, y2 = extendFaceRect(x, y, x2, y2, image)

        h = y2 - y
        w = x2 - x
        face = image[y:y+h, x:x+w]
        resizedFace = cv2.resize(face, resizeResolution)
        result, encodedFace = cv2.imencode(extension, resizedFace)
        if result:
            resizedFaces.append(encodedFace)
        else:
            print(f"failed to encode image: {resizedFace}")
    return resizedFaces

# 画像の表示
def displayFace(faces, image):
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('Detected Faces', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 元画像から顔を抜き出し保存        
def cropImageToFace(
    image, 
    resizeResolution = (224, 224), 
    extension = '.jpg',
    usingOldModel = False,
    oldModelPath = createPath('face', 'lbpcascade_animeface.xml')
):
    resizedImage = resizeImage(image, 1500)
    faces = getFaceRect(resizedImage) if not usingOldModel else detectFace(resizedImage, oldModelPath)
    if len(faces) == 0:
        print(f"no faces detected")
    elif len(faces) > 1:
        print(f"detected {len(faces)} faces")
    return cropFace(faces, resizedImage, resizeResolution, extension)

