from machine import Pin,ADC
import time

adc = ADC(Pin(36))

adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

while True:
    print (adc.read())
    time.sleep(0.05)