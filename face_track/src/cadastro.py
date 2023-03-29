import cv2
import os
import numpy as np

# Pergunta o nome da pessoa
# nome = input("Digite o seu nome: ")



# Inicializa a captura de vídeo a partir da webcam



# Define um valor inicial para a variável frame
# ret, frame = cap.read()

# Criar uma imagem branca com o mesmo tamanho do frame
# white_img = np.zeros(frame.shape, dtype=np.uint8)
# white_img.fill(255)

# Exibe mensagem para mudar a posição do rosto e pressionar "q"
# mensagem = 'Mova o seu rosto a cada 2s.'
# mensagem_dois = 'Pressione "q" para iniciar a captura.'
# cv2.putText(white_img, mensagem, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
# cv2.putText(white_img, mensagem_dois, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
# cv2.imshow('Webcam', white_img)

# Loop para aguardar pressionar a tecla "q" para iniciar a captura de frames
# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


def registration(name):
    # Criar a pasta "imagens com o nome da pessoa que está se cadastrando" se ela não existir
    if not os.path.exists(f'../imagens_cadastro/{name}'):
        os.makedirs(f'../imagens_cadastro/{name}')
    cap = cv2.VideoCapture(0)

    # Verificar se a webcam foi aberta corretamente
    if not cap.isOpened():
        raise IOError("Não foi possível abrir a webcam")

    # Inicializa o contador de imagens capturadas
    count = 0
    intervalo = 2  # segundos
    fps = 30
    count_cadastro = 1
    # Loop para captura de frames da webcam
    while True:
        ret, frame = cap.read()

        # Mostrar o frame na janela
        cv2.imshow('Webcam', frame)

        # Verificar se o tempo de intervalo passou para capturar uma nova imagem
        if count > 5 and (count % (intervalo * fps) == 0 and count_cadastro <= 5):
            # Captura a imagem e salva em um arquivo
            cv2.imwrite('../imagens_cadastro/{}/{}.jpg'.format(name, count_cadastro), frame)
            print('Imagem {} capturada'.format(count_cadastro))
            count_cadastro += 1
        elif count_cadastro > 5:
            break
        # Incrementa o contador de imagens capturadas
        count += 1

        # Espera por uma tecla (1 milissegundo), aperte "q" quando quiser parar a captura 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Encerra o loop quando 5 imagens foram capturadas
        if count_cadastro > 5:
            break


    #Finaliza a captura de vídeo
    cap.release()
    cv2.destroyAllWindows()

registration('luan')