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

# Bloco e código para gerar o Gráfico 1 que é a Distância relativa 𝑑 entre o robô e a bola como função do tempo 𝑡
# np.range, sendo usado para criar uma sequencia de tempo
# O tempo é calculado de 0 até o comprimento da trajetória do robô multiplicado pelo intervalo de amostragem dt, com intervalo de tempo dt. o 0 passado como argumento é o ponto inicial da sequencia, o argumento seguinte é o ponto final (dt intervalo de tempo entre cada amostra de espaço percorrido, multiplicado pelo número de amostras de espaço percorrido pelo robô) e o dt é o espaçamento entre cada ponto.
tempo = np.arange(0, len(trajetoria_robo) * dt, dt)

#calculo da distância relativa entre o robô e a bola em cada ponto do tempo.
#np.linalg.norm para calcula a norma euclidiana entre as coordenadas do robô e da bola.
# Para isso, subtraí as coordenadas da trajetória do robô das coordenadas da trajetória da bola.
# [:len(trajetoria_robo), 1:3] é utilizado para garantir que ambas as trajetórias tenham o mesmo comprimento.
distancia_relativa = np.linalg.norm(
    trajetoria_robo - trajetoria_bola[:len(trajetoria_robo), 1:3], axis=1)

fig, ax = plt.subplots(figsize=(10, 6)) #essa linha cria uma figura em um conjunto de eixos e especifica o seu tamanho
ax.plot(tempo, distancia_relativa, label="Distância Relativa", color="red") #Essa plota a distância relativa em função do tempo, e define a cor da linha e legenda
ax.set_title("Distância Relativa entre o Robô e a Bola em Função do Tempo") #titulo do gráfico
ax.set_xlabel("Tempo (s)") #rótulo do eixo
ax.set_ylabel("Distância (m)") #rótulo do outro eixo

# Esse bloco de código inteiro Adiciona uma equação no gráfico
equacao1 = r'$d = \sqrt{(x_{\mathrm{robo}} - x_{\mathrm{bola}})^2 + (y_{\mathrm{robo}} - y_{\mathrm{bola}})^2}$' #Essa linha cria uma variável de equação1 e atribui a ela uma equação matemática que calcula a distância d entre robô e bola, distância entre 2 pontos em um plano bidimensional, essa fórmula é a distância euclidiana entre dois pontos. que é a raiz quadrada da soma dos quadrados da diferença entre x do robô e x da bola e y do rôbo e y da bola. e formatá o jeito que ela tem que ser visualizada.
#essa parte toda adiciona uma anotação, onde a equação ficará no gráfico, e define sua posição e outras configurações
ax.annotate(equacao1, (0.30, 0.92), 
            xycoords='axes fraction',
            fontsize=10,
            color='black')

#esse bloco inteiro adiciona ao gráfico o valor final da distância
valor_final_distancia = distancia_relativa[-1] #essa linha atribui a uma variável o ultimo elemento da array distancia_relativa, que é a distância relativa entre bola e robô ao longo do tempo.
#toda essa parte em seguida adiciona um texto no gráfica, contendo os elementos de tempo, o valor da variável atribuida anteriormente e as configurações de posição e cor.
ax.text(tempo[-1],
        valor_final_distancia,
        f'{valor_final_distancia:.2f} m',
        ha='right',
        va='bottom')
            


            color='black')

ax.legend() #adiciona uma legenda ao gráfico
plt.show() #exibe o gráfico na tela


# Bloco e código para gerar o Gráfico 2 que é a Trajetórias da bola e do robô em um plano 𝑥𝑦, até o ponto de interceptação
fig, ax = plt.subplots(figsize=(10, 6))  #essa linha cria uma figura em um conjunto de eixos e especifica o seu tamanho
# Essa parte plota a trajetória da bola no plano XY, pega as duas matrizes que correspondem as posições x e y da bola, e adicionauma legenda e suas configurações.
ax.plot(trajetoria_bola[:, 1],
        trajetoria_bola[:, 2],
        label="Trajetória da Bola",
        color="blue",
        linewidth=2)
# Essa parte plota a trajetória do robô no plano XY, pega as duas matrizes que correspondem as posições x e y do robô, e adiciona uma legenda e suas configurações.
ax.plot(trajetoria_robo[:, 0],
        trajetoria_robo[:, 1],
        label="Trajetória do Robô",
        linestyle="--",
        color="orange",
        linewidth=2)
# essa parte define o titulo do gráfico e as medidas nos eixos em metros
ax.set_title("Trajetórias da Bola e do Robô no Plano XY até a Interceptação")
ax.set_xlabel("Posição X (m)")
ax.set_ylabel("Posição Y (m)")

# Todo esse bloco de código adiciona texto aos gráficos para ajudar a visualizar no gráfico onde bola e robô começam e terminam suas trajetórias, os textos indica posição inicial e final da bola e do robô.
ax.text(trajetoria_bola[0, 1], #coordenadas X inicial da bola
        trajetoria_bola[0, 2], #coordenadas Y inicial da bola
        'Inicial Bola', # texto que será exibido no gráfico
        ha='right',
        va='bottom')
ax.text(trajetoria_robo[0, 0], #coordenadas X inicial do robô
        trajetoria_robo[0, 1], #coordenadas X inicial do robô
        'Inicial Robô', # texto que será exibido no gráfico
        ha='right',
        va='bottom')

ax.text(trajetoria_bola[-1, 1], #coordenadas X final da bola
        trajetoria_bola[-1, 2], #coordenadas Y final da bola
        'Final Bola', # texto que será exibido no gráfico
        ha='right',
        va='bottom')
ax.text(trajetoria_robo[-1, 0], #coordenadas X final do robô
        trajetoria_robo[-1, 1], #coordenadas Y final da robô
        'Final Robô', #texto que será exibido no gráfico
        ha='right',
        va='bottom')

ax.legend() #adiciona uma legenda ao gráfico
plt.show() #exibe o gráfico na tela





