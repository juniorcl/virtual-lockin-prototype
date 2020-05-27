from time import sleep, strftime
import matplotlib.pyplot as plt
from drawnow import drawnow
import auxiliary as aux
import numpy as np
import pyaudio
import visa


#function to get the signal
def linSignal():
    sinal = np.float32(np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), np.int16))
    return aux.inVolt(sinal[1::2]), aux.inVolt(sinal[::2]) #pego os índices ímpares (plug branco) e os pares (plug vermelho)


#funtion where the signals are calculated
def makeFig():
    sinal, _ = linSignal() 
    x, y = list(map(np.float, inst.query('SNAP?1,2').split(','))) #pega os valores reais de x e y

    pot = np.float(inst.query('OAUX?3'))
    temp = round(float(inst.query('OAUX?1')), 3) #valor da temperatura

    x_fft0, y_fft0, x_bessel, y_bessel, x_butter, y_butter = aux.lowPassFilter(sinal, REFSIG, RATE, ORDER_1, ROLL)
    
    file.writelines("%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,\n" % (x, y, x_fft0, y_fft0, x_bessel, y_bessel, x_butter, y_butter, temp, pot))

    R_psd.append(np.sqrt(np.power(x_butter_900, 2) + np.power(y_butter_900, 2)))
    R.append(np.sqrt(np.power(x, 2) + np.power(y, 2)))

    plt.subplot(2,1,1)
    plt.plot(R)
    plt.grid()

    plt.subplot(2,1,2)
    plt.plot(R_psd)
    plt.grid()



## Vetores utilizados
R = [] #vetor do R do lockin real
R_psd = [] #vetor do R da função psd virtual


## Informações para funcionamento do lock-in
inst = visa.ResourceManager().open_resource(visa.ResourceManager().list_resources()[2]) #instrumento lockin real
TEMP = round(float(inst.query("OAUX?1")), 3) #valor da temperatura
TEMPFIM = 15*0.1 #seta a temperatura final. (temperatura de 15C)


## Informações para captação do sinal
FREQ = 3802 #np.int(inst.query("FREQ?")) #frequencia utilizada
PP = 20 #num de pontos por períodos
NP = 200 #número de pontos por período
FORMAT = pyaudio.paInt16 #formato
CHANNELS = 2 #canais
RATE = FREQ*PP #taxa de amostragem
CHUNK = PP*NP #num de pontos
INDEX_LIN = 1 #index da entrada de linha

ROLL = round(PP/1.33333333) #apróxima para a melhor transformação de cosseno
ORDER = 1 #ordem do filtro utilizado


ref_name = "Ref_N2O_ch=2_t=30min_mod=0.460V_freq=3802_PP=20_NP=200.wav" #nome do arquivo para sinal de referência
t = np.linspace(0, NP*(1/FREQ), PP*NP)
REFSIG = 0.48*np.sin(2*np.pi*FREQ*t) #aux.refSignal(ref_name, CHUNK) #pega o valor do sinal de referência em volts


## Arquivos onde serao gravados os valores
aquisicao = "x,y,x-fft0,y-fft0,x-bessel,y-bessel,x-butter,y-butter,temperatura,potencia\n"

file_name = "N2O_freq=%i_PP=%i_NP=%i_Conc=0ppmv_Temp=-15a%.1f_roll=%i_order=%i_data=%s.dat" % (FREQ, PP, NP, TEMPFIM*10, ROLL, ORDER, strftime("%a_%d-%m-%Y_%Hh%Mmin%Ss"))
file = open(file_name, 'w')
file.writelines(aquisicao)


## Criação de streams e iniciação da stream
pa = pyaudio.PyAudio()
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=INDEX_LIN) #stream da entrada de linha
stream.start_stream() #inicia o stream de linha


## Coração do programa
if (TEMP - 0.005) <= TEMP < (TEMP + 0.005): #range aceitável de temperatura
    
    for T in np.arange(TEMP*10, TEMPFIM, 0.01): #esta etapa sera executada ate chegar a uma determinada temperatura
        drawnow(makeFig) #entra na função de drawnow
        inst.write("AUXV1,%.2f" % (T)) #setar o valor que a cada 0.1 V e equivalente a 1 C
        sleep(2) #espera 2s, pois é preciso esperar um pouco até a temp estabilizar


## Fecha arquivos
file.close() #fecha o arquivo

## Para e Fecha os streams
stream.stop_stream()
stream.close()
pa.terminate()
