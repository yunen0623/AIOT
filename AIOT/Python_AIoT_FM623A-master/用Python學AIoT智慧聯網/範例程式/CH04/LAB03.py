from machine import Pin,ADC

f=open('test.txt','w')

adc_pin=Pin(36)     
adc = ADC(adc_pin)  
adc.width(ADC.WIDTH_9BIT)  
adc.atten(ADC.ATTN_11DB)
tem=input('請輸入現在溫度:')

f.write(str(adc.read())+' '+tem)
f.close()