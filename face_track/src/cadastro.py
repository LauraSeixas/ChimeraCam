import cv2
import os


# Criar a pasta "imagens" se ela não existir
if not os.path.exists('../imagens_cadastro'):
    os.makedirs('../imagens_cadastro')

# Inicializa a captura de vídeo a partir da webcam
cap = cv2.VideoCapture(0)

# Verificar se a webcam foi aberta corretamente
if not cap.isOpened():
    raise IOError("Não foi possível abrir a webcam")

# Loop para captura de frames da webcam
while True:
    ret, frame = cap.read()

    # Salva o frame capturado em um arquivo
    cv2.imwrite('../imagens_cadastro/imagem_capturada.jpg', frame)

    # Mostrar o frame na janela
    cv2.imshow('Webcam', frame)

    # Aperte "q" quando quiser capturar um frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Finaliza a captura de vídeo
cap.release()
cv2.destroyAllWindows()
