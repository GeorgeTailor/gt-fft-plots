import wave
import matplotlib.pyplot as plt
import numpy as np
import struct

def oneChannel(fname, chanIdx):
    ''' list with specified channel's data from multichannel wave with 16-bit data '''
    f = wave.open(fname, 'rb')
    chans = f.getnchannels()
    samps = f.getnframes()
    sampwidth = f.getsampwidth()
    print('number of channels ' + str(f.getnchannels()))
    print('sample width: ' + str(f.getsampwidth()))
    print('frame rate(sampling frequency): ' + str(f.getframerate()))
    print('number of frames: ' + str(f.getnframes()))
    assert sampwidth == 2
    s = f.readframes(samps) #read the all the samples from the file into a byte string
    f.close()
    unpstr = '<{0}h'.format(samps*chans) #little-endian 16-bit samples
    x = list(struct.unpack(unpstr, s)) #convert the byte string into a list of ints
    return x[chanIdx::chans] #return the desired channel

def main():
    firstChannel = oneChannel('gtr-jazz.wav', 0)
    
    plt.figure(1)
    plt.title('firstChannel wo hamming...')
    plt.plot(firstChannel)
    hammingWindow = np.hamming(len(firstChannel))
    firstChannel = hammingWindow * firstChannel
    plt.figure(2)
    plt.title('firstChannel w hamming...')
    plt.plot(firstChannel)
    
    A = np.fft.rfft(firstChannel, 80000)
    amplitudeSpectrum = np.abs(A)
    powerSpectrum = np.abs(A)**2
    phaseSpectrum = np.angle(A)

    plt.figure(3)
    plt.title('phaseSpectrum...')
    plt.plot(phaseSpectrum)
    plt.figure(4)
    plt.title('powerSpectrum...')
    plt.plot(powerSpectrum)
    
    plt.show()

main()