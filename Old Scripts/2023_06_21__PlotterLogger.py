# Log sequence recorded on 2023/06/21 12:51:26
import time
import zhinst.core

daq = zhinst.core.ziDAQServer('192.168.103.198', 8004, 6)
# Starting module impedanceModule on 2023/06/21 12:51:26
impedance = daq.impedanceModule()
#for i in dir(impedance):
#    print(f"{i}: {getattr(impedance, i)}")

impedance.set('device', 'dev6641')
impedance.set('mode', 5)
impedance.set('path', 'C:\\Users\\WaveWhisperer\\AppData\\Roaming\\Zurich Instruments\\LabOne\\WebServer\\setting')

impedance.subscribe('/dev6641/imps/0/sample')
impedance.execute()
time.sleep(3)
result = impedance.save("bob")
result = impedance.read()
impedance.finish()
impedance.unsubscribe("*")
time.sleep(1)

print(result)
