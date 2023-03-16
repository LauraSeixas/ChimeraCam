# ChimeraCam

> Uma aplicação de um carro inteligente que reconhece os passageiros e pode emitir diversos alertas e realizar 
> comportamentos de acordo com os passageiros detectados.

## pré-requisitos

### Reconhecimento e detecção facial

Antes de começar seguir os passos:

* git clone do opencv para detecção facial `git clone https://github.com/opencv/opencv.git`

* Na pasta models ter uma pasta `<age_detection>` com arquivos chamados `age_deploy.prototxt` e `age_net.caffemodel` para treinamento do modelo de detecção de idade (ver código).