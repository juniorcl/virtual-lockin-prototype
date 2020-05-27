############################# Helper #################################
##      This file was created to support the lock-in program        ##
######################################################################
## These functions can be imported using: import lockin-auxiliary as aux
## and put aux.<name of the function>
from scipy.signal import bessel, filtfilt, butter
import numpy as np
import wave

def lowPassAll(sinal, REFSIG, RATE, ORDER, ROLL):

    CUTOFF_100 = 100
    CUTOFF_200 = 200
    CUTOFF_300 = 300
    CUTOFF_400 = 400
    CUTOFF_500 = 500
    CUTOFF_600 = 600
    CUTOFF_700 = 700
    CUTOFF_800 = 800
    CUTOFF_900 = 900
    CUTOFF_1000 = 1000
    

    y_fft0, x_fft0 = freq0fftPSD(sinal, REFSIG, RATE, ROLL)
    y_bessel, x_bessel = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_100, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter, x_butter = lowButterPSD(sinal, REFSIG, RATE, CUTOFF_100, ORDER, ROLL)

    y_bessel_200, x_bessel_200 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_200, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_200, x_butter_200 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_200, ORDER, ROLL) #faz o psd com o filtro passa-baixo

    y_bessel_300, x_bessel_300 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_300, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_300, x_butter_300 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_300, ORDER, ROLL) #faz o psd com o filtro passa-baixo

    y_bessel_400, x_bessel_400 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_400, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_400, x_butter_400 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_400, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    
    y_bessel_500, x_bessel_500 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_500, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_500, x_butter_500 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_500, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    
    y_bessel_600, x_bessel_600 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_600, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_600, x_butter_600 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_600, ORDER, ROLL) #faz o psd com o filtro passa-baixo

    y_bessel_700, x_bessel_700 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_700, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_700, x_butter_700 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_700, ORDER, ROLL) #faz o psd com o filtro passa-baixo

    y_bessel_800, x_bessel_800 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_800, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_800, x_butter_800 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_800, ORDER, ROLL) #faz o psd com o filtro passa-baixo

    y_bessel_900, x_bessel_900 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_900, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_900, x_butter_900 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_900, ORDER, ROLL) #faz o psd com o filtro passa-baixo

    y_bessel_1000, x_bessel_1000 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_1000, ORDER, ROLL) #faz o psd com o filtro passa-baixo
    y_butter_1000, x_butter_1000 = lowBesselPSD(sinal, REFSIG, RATE, CUTOFF_1000, ORDER, ROLL) #faz o psd com o filtro passa-baixo

    return x_fft0, y_fft0, x_bessel, y_bessel, x_butter, y_butter, x_bessel_200, y_bessel_200, x_butter_200, y_butter_200, x_bessel_300, y_bessel_300, x_butter_300, y_butter_300, x_bessel_400, y_bessel_400, x_butter_400, y_butter_400, x_bessel_500, y_bessel_500, x_butter_500, y_butter_500, x_bessel_600, y_bessel_600, x_butter_600, y_butter_600, x_bessel_700, y_bessel_700, x_butter_700, y_butter_700, x_bessel_800, y_bessel_800, x_butter_800, y_butter_800, x_bessel_900, y_bessel_900, x_butter_900, y_butter_900, x_bessel_1000, y_bessel_1000, x_butter_1000, y_butter_1000

def refSignal(file, chunk):
    wf = wave.open(file, 'rb')
    sinalbit = np.frombuffer(wf.readframes(chunk), np.int16)
    return inVolt(sinalbit[::2])

def rmsFunction(signal):
    #Root-Mean-Square function
    f = lambda i: i**2/len(signal)
    soma = np.sum(list(map(f, signal)))
    return np.sqrt(soma)

def sigMultiply(signal, signal_ref, roll):
    #multiply the signal and referency signals
    sin_psd = np.multiply(signal, signal_ref)
    cos_psd = np.multiply(signal, np.roll(signal_ref, roll))
    return sin_psd, cos_psd

def lowButter(data, fs, cutoff, order):
    #this is a butter lowpass filter
    nyq = 0.5*fs
    normal_cutoff = cutoff/nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def lowBessel(data, fs, cutoff, order):
    #this is a bessel lowpass filter
    nyq = 0.5*fs
    normal_cutoff = cutoff/nyq
    b, a = bessel(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def inVolt(signal):
    #converts bits to volts
    slope = 1.4286015335045335e-4 #slope found with minor error: 7.672327425854542e-09
    intercept = 20.975684328898847e-4 #intercept is the same of slope
    f = lambda bit: round(slope*bit + intercept, 6)
    return list(map(f, signal)) #6 decimal places

def fftFunction(signal, rate):
    signal_len = len(signal)
    fft = np.abs(np.fft.rfft(signal))/signal_len
    freqs = np.fft.rfftfreq(signal_len)*rate
    return fft, freqs

def freq0fftPSD(signal, signal_ref, rate, roll):
    #get just the amplitude at freq = 0
    sin_psd, cos_psd = sigMultiply(signal, signal_ref, roll)
    sin_psd_fft, _ = fftFunction(sin_psd, rate)
    cos_psd_fft, _ = fftFunction(cos_psd, rate)
    return sin_psd_fft[0], cos_psd_fft[0]

def fftPSD(signal, signal_ref, freq, rate, roll):
    #get the amplitude at freq = 0 and 2 * freq
    sin_psd, cos_psd = sigMultiply(signal, signal_ref, roll)
    sin_psd_fft, sin_psd_freqs = fftFunction(sin_psd, rate)
    cos_psd_fft, cos_psd_freqs = fftFunction(cos_psd, rate)
    y = sin_psd_fft[0] + dict(zip(sin_psd_freqs, sin_psd_fft))[2*freq]
    x = cos_psd_fft[0] + dict(zip(cos_psd_freqs, cos_psd_fft))[2*freq]
    return y, x

def lowButterPSD(signal, signal_ref, rate, cutoff, order, roll):
    #PSD using the butter low pass filter
    sin_psd, cos_psd = sigMultiply(signal, signal_ref, roll)
    y = rmsFunction(lowButter(sin_psd, rate, cutoff, order))
    x = rmsFunction(lowButter(cos_psd, rate, cutoff, order))
    return y, x

def lowBesselPSD(signal, signal_ref, rate, cutoff, order, roll):
    #PSD using the bessel low pass filter
    sin_psd, cos_psd = sigMultiply(signal, signal_ref, roll)
    y = rmsFunction(lowBessel(sin_psd, rate, cutoff, order))
    x = rmsFunction(lowBessel(cos_psd, rate, cutoff, order))
    return y, x
