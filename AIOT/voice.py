from machine import Pin,ADC        #打開, 關閉
import time
from keras_lite import Model   
import ulab as np  

#增加神經網路的參數
mean=135.50511111111112  #平均值
std=356.3339495262662   #標準差
model = Model('voice_model1.json')   # 建立模型物件
label_name = ['on','off','others']  # label名稱

led=Pin(32,Pin.OUT,value=0)    # LED燈腳位

adc = ADC(Pin(36))       # 設定36為ADC腳位
adc.width(ADC.WIDTH_12BIT) 
adc.atten(ADC.ATTN_11DB) # 設定最大電壓為3.6V
while True:
    sound=adc.read()  # 接收聲音
    if(sound>100):     # 有聲音時
        print('')
        no_sound=0     # 重置沒聲音次數
        data=[sound]   # 重置data
        
        # 沒聲音次數少於150或超過資料儲存量時
        while(no_sound<150 and len(data)<550): 
            sound=adc.read()  # 接收聲音
            data.append(sound)
            if(sound==0):     # 沒聲音時
                no_sound+=1   # 沒聲音次數+1
            else:             # 有聲音時
                no_sound=0    # 重置聲音次數
            time.sleep_us(500)                    
        data=data[:-150]      # 將0的部分刪除
        
        if(len(data)<150):  # 如果資料長度小於150, 認為是噪音
            print('noise, try again')
            continue

        while(len(data)<400): # 如果資料長度不夠
            data.append(0)     # 補充數字0
            
        data = np.array([data])    # 將data轉換為numpy格式
        data = data-mean           # data減掉平均數
        data = data/std            # data除以標準差
        status_label = model.predict_classes(data)   # 得出狀態(0或1或2)
        print(label_name[status_label[0]])
        
        if(label_name[status_label[0]]=='on'):     # 判斷為on
            led.value(1)                           # 開燈
        elif(label_name[status_label[0]]=='off'):  # 判斷為off
            led.value(0)                           # 關燈    
    time.sleep_us(500)                             # sleep_us=1微秒=0.000001秒

