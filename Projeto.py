import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy


h_area = 1.0
D_penalti = 2.0
larguraCampo = 9.0
h_campo = 6.0
LarguraArea = 0.5
Intervalo_20ms = 0.02  
aceleracaoMaxima = 2.8  
velocidadeMaxima = 2.8  

velocidades_robo = []
aceleracoes_robo = []


with open("trajetoria_bola.dat", "r") as file:
  # Ignora a primeira linha (cabeçalho)
  next(file)

  b_trajetoria = numpy.array(
    # transforma todos os valores em Float trocando a virgula por ponto
    # Separa pelo caracter delimitador ( " espaço ")
      [[float(value.replace(",", ".")) for value in line.split("\t")]
       for line in file])


robo_pos_inicial = numpy.array([
    float(input("Inicio em X: ")),
    float(input(" Inicio em Y: "))
])


rb_pos_atual = robo_pos_inicial
rb_velo = numpy.array([0.0 , 0.0])
rb_aceleracao = numpy.array([0.0 , 0.0])

#Criando o array base ( vazio ) de aceleracao da bola
b_aceleracao_x = numpy.zeros_like(b_trajetoria[:, 0])
b_aceleracao_y = numpy.zeros_like(b_trajetoria[:, 0])

for i in range(1, len(b_trajetoria)):
  # Usa a formula de Ponto inicio - ponto final / tempo inicio - tempo final ( 0.02)
   b_aceleracao_y[i] = (b_trajetoria[i, 2] -
                          b_trajetoria[i - 1, 2]) / Intervalo_20ms
  
   b_aceleracao_x[i] = (b_trajetoria[i, 1] -
                          b_trajetoria[i - 1, 1]) / Intervalo_20ms
 

trajetoria_robo = []

# Interceptação
for i in range(len(b_trajetoria)):
  # usamos a funcao linalg.norm para pegar as posições 1 e 2 do vetor
  # Ela tambem calcula o modulo ( Distancia ) dessas posições, A Raiz Quadrada dos quadrados das duas posições
  d = numpy.linalg.norm(rb_pos_atual - b_trajetoria[i, 1:3])
                                        # X e Y do array de trajetoria ( Começa em 0)

  # Armazena a posição atual do robô na trajetória
  trajetoria_robo.append(numpy.copy(rb_pos_atual))

  # Velocidade Robo
  velocidades_robo.append(numpy.copy(rb_velo))

  # Aceleracao Robo
  aceleracoes_robo.append(numpy.copy(rb_aceleracao))

  # Calculo de direção Usando a formula de  ArcTangente( Py/Px) 
  direcao_aceleracao = numpy.arctan2(b_trajetoria[i, 2] - rb_pos_atual[1], b_trajetoria[i, 1] - rb_pos_atual[0])

  # Velocidade = Deslocamento / Diferença de Tempo
  # Calcula a velocidade da bola ( Ele pega o deslocamento de cada eixo X e Y e divide pelo 0.02)

  velocidade_bola = numpy.array(   
        [
        # Eixo X
        (b_trajetoria[i, 1] - b_trajetoria[i - 1, 1]) / Intervalo_20ms if i > 0 else 0.0,
        # Eixo Y
        (b_trajetoria[i, 2] - b_trajetoria[i - 1, 2]) / Intervalo_20ms  if i > 0 else 0.0
        ]
    )


  # Tempo para interceptar os dois = Calcula o Módulo ( Distancia) dos pontos ( x , y ) da bola e robo /  Velocidade maxima 
  tempo_para_interceptar = numpy.linalg.norm(b_trajetoria[i, 1:3] - rb_pos_atual) / velocidadeMaxima
  # Consegue o ponto futuro ( Posição atual + velocidade atual + tempo_para_interceptar) 
  ponto_intersecao = b_trajetoria[i, 1:3] + velocidade_bola * tempo_para_interceptar

  # Calcula a direção para o ponto de interseção
  direcao_intersecao = ponto_intersecao - rb_pos_atual
  # Conseguindo um vetor unitario
  direcao_intersecao /= numpy.linalg.norm(direcao_intersecao)


  # Ajustando a velocidade pela quantidade de vetor unitario
  velocidade_desejada = direcao_intersecao * velocidadeMaxima
  # Ajusta o valor da aceleração
  robo_aceleracao = (velocidade_desejada - robo_velocidade) / Intervalo_20ms

  # Limita os valores de aceleração maxima e minima
  robo_aceleracao = numpy.clip(robo_aceleracao, -aceleracaoMaxima, aceleracaoMaxima)

  # Ajustando velocidade do robo
  robo_velocidade +=  robo_aceleracao * Intervalo_20ms

  # Limita os valores de velocidade maxima e minima
  robo_velocidade = numpy.clip(robo_velocidade, -velocidadeMaxima, velocidadeMaxima)

  # Atualiza a posição do robô
  rb_pos_atual += robo_velocidade * Intervalo_20ms


  # Verifica se o robô ( raio ) interceptou a bola < 8.0
  if numpy.linalg.norm(rb_pos_atual - ponto_intersecao) < 8.0:
    break

# Função para adicionar a equação no gráfico, essa função será chamada, em outras partes receberá arguementos e gerará equações ao gráfico a partir dos arguementos que forem passados.
def add_equation(ax, equation, x, y):
  # Adiciona uma equação ao gráfico nas coordenadas (x, y)
  ax.annotate(equation, (x, y),  
              # Define a posição do texto da equação em relação às coordenadas especificadas
              xytext=(10, -20),   
              # Indica que as coordenadas do texto são medidas em pontos
              textcoords='offset points',  
              # Define as propriedades da seta que aponta para a equação
              arrowprops=dict(arrowstyle="->", color='black'))  

# função para gerar o Gráfico 1 que é a Distância relativa 𝑑 entre o robô e a bola como função do tempo 𝑡
# np.range, sendo usado para criar uma sequencia de tempo
# O tempo é calculado de 0 até o comprimento da trajetória do robô multiplicado pelo intervalo de amostragem dt, com intervalo de tempo dt. o 0 passado como argumento é o ponto inicial da sequencia, o argumento seguinte é o ponto final (dt intervalo de tempo entre cada amostra de espaço percorrido, multiplicado pelo número de amostras de espaço percorrido pelo robô) e o dt é o espaçamento entre cada ponto.
tempo = np.arange(0, len(trajetoria_robo) * dt, dt)

#calculo da distância relativa entre o robô e a bola em cada ponto do tempo.
#np.linalg.norm para calcula a norma euclidiana entre as coordenadas do robô e da bola.
# Para isso, subtraí as coordenadas da trajetória do robô das coordenadas da trajetória da bola.
# [:len(trajetoria_robo), 1:3] é utilizado para garantir que ambas as trajetórias tenham o mesmo comprimento.
distancia_relativa = np.linalg.norm(
    trajetoria_robo - trajetoria_bola[:len(trajetoria_robo), 1:3], axis=1)





